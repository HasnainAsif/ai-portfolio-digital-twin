"""
Session management module for handling conversation history and session state.
Manages session persistence using Redis (Upstash) with TTL and daily message limits.
"""

import os
import json
import uuid
import sys
from typing import List
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

UPSTASH_REDIS_URL = os.getenv("UPSTASH_REDIS_URL")
UPSTASH_REDIS_TOKEN = os.getenv("UPSTASH_REDIS_TOKEN")
USE_UPSTASH_REDIS = os.getenv("USE_UPSTASH_REDIS", "false").lower() == "true"

# Create Upstash Redis client only when flag is enabled
redis_client = None
if USE_UPSTASH_REDIS:
    try:
        from upstash_redis import Redis
        redis_client = Redis(url=UPSTASH_REDIS_URL, token=UPSTASH_REDIS_TOKEN)
    except Exception as e:
        print(f"Error initializing Upstash Redis client: {e}", file=sys.stderr)

# Constants
SESSION_TTL = 7200  # 2 hours - session expires after 2 hours of inactivity
DAILY_LIMIT = 50 # Max 50 messages per session per day
DAILY_LIMIT_TTL = 86400  # 24 hours - daily limit resets after 24 hours
SESSION_KEY_PREFIX = "twin:session:"
LIMIT_KEY_PREFIX = "twin:limit:"
MAX_CONVERSATION_LENGTH = 16 # Max 16 messages (8 exchanges) in conversation history to keep in Redis

# In-memory fallback store used when Redis is disabled or unavailable
_memory_store: dict = {}


def load_conversation(session_id: str) -> List:
    if not USE_UPSTASH_REDIS or not redis_client:
        return list(_memory_store.get(session_id, []))

    try:
        key = f"{SESSION_KEY_PREFIX}{session_id}"
        data = redis_client.get(key)

        if data is None:
            return []

        messages = json.loads(data)
        return messages[-MAX_CONVERSATION_LENGTH:] if len(messages) > MAX_CONVERSATION_LENGTH else messages

    except Exception as e:
        print(f"Error loading conversation for session {session_id}: {e}", file=sys.stderr)
        return []


def save_conversation(session_id: str, messages: List) -> None:
    if not USE_UPSTASH_REDIS or not redis_client:
        _memory_store[session_id] = messages[-MAX_CONVERSATION_LENGTH:]
        return

    try:
        key = f"{SESSION_KEY_PREFIX}{session_id}"
        data = json.dumps(messages)
        redis_client.setex(key, SESSION_TTL, data)

    except Exception as e:
        print(f"Error saving conversation for session {session_id}: {e}", file=sys.stderr)


def check_session_limit(session_id: str) -> dict:
    """
    Check if session is within daily message limit (50 messages per day).
    Increments the counter on each call.

    Args:
        session_id: The session identifier

    Returns:
        Dictionary with:
            - allowed (bool): True if session is within limit, False if limit exceeded
            - remaining_messages (int): Number of messages remaining in daily quota
            - daily_limit (int): Total daily message limit
    """
    if not redis_client:
        # Fail open - allow through if Redis is unreachable
        return {
            "allowed": True,
            "remaining_messages": DAILY_LIMIT,
            "daily_limit": DAILY_LIMIT
        }

    try:
        key = f"{LIMIT_KEY_PREFIX}{session_id}"

        # Increment the counter
        current_count = redis_client.incr(key)

        # Set TTL on first message of the day
        if current_count == 1:
            redis_client.expire(key, DAILY_LIMIT_TTL)  # Set TTL to 24 hours on first increment

        within_limit = current_count <= DAILY_LIMIT # Check if within limit
        remaining = max(0, DAILY_LIMIT - current_count)

        return {
            "allowed": within_limit,
            "remaining_messages": remaining,
            "daily_limit": DAILY_LIMIT,
            # "reset_time": "2026-04-17T00:00:00Z",
            # "reason": "daily_limit_exceeded",
        }

    except Exception as e:
        print(f"Error checking session limit for {session_id}: {e}", file=sys.stderr)
        # Fail open - allow through if error occurs
        return {
            "allowed": True,
            "remaining_messages": DAILY_LIMIT,
            "daily_limit": DAILY_LIMIT
        }


def generate_session_id() -> str:
    """
    Generate a new session ID using UUID4.

    Returns:
        A new UUID4 string
    """
    return str(uuid.uuid4())
