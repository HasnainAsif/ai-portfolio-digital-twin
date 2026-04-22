"""
Session management module for handling conversation history and session state.
Manages session persistence using Redis (Upstash) with TTL and IP conversation limits.
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
RESTRICT_CONVERSATIONS_PER_IP = os.getenv("RESTRICT_CONVERSATIONS_PER_IP", "true").lower() == "true"
MAX_CONVERSATIONS_PER_IP = int(os.getenv("MAX_CONVERSATIONS_PER_IP", "20"))

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
IP_CONV_TTL = 86400  # 24 hours - IP conversation counter resets after 24 hours
SESSION_KEY_PREFIX = "twin:session:"
IP_CONV_KEY_PREFIX = "twin:ip_conv:"
MAX_CONVERSATION_LENGTH = 16  # Max 16 messages (8 exchanges) kept in history

# In-memory fallback store used when Redis is disabled or unavailable
_memory_store: dict = {}
_ip_conv_store: dict = {}  # tracks conversation count per IP when Redis is unavailable


def load_conversation(session_id: str) -> List:
    if not USE_UPSTASH_REDIS or not redis_client:
        messages = _memory_store.get(session_id, [])
        return list(messages[-MAX_CONVERSATION_LENGTH:]) if len(messages) > MAX_CONVERSATION_LENGTH else list(messages)

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


# Disabled: replaced by IP conversation limit (is_ip_blocked).
# Re-enable if you want to cap messages per session (depth limit) in addition to the IP breadth limit.
# Requires Redis — fails open (always allows) without it.
# Example: MAX_CONVERSATIONS_PER_IP(20 conversations) × DAILY_LIMIT(50 messages/conversation) = 1000 max messages per IP/day.
def check_session_limit(session_id: str) -> dict:
    if not redis_client:
        return {"allowed": True, "remaining_messages": 50, "daily_limit": 50}

    try:
        key = f"twin:limit:{session_id}"
        current_count = redis_client.incr(key)
        if current_count == 1:
            redis_client.expire(key, 86400)
        within_limit = current_count <= 50
        return {
            "allowed": within_limit,
            "remaining_messages": max(0, 50 - current_count),
            "daily_limit": 50,
        }
    except Exception as e:
        print(f"Error checking session limit for {session_id}: {e}", file=sys.stderr)
        return {"allowed": True, "remaining_messages": 50, "daily_limit": 50}


def is_ip_blocked(ip: str) -> bool:
    """Return True if this IP has reached MAX_CONVERSATIONS and should be hard-blocked."""
    if not RESTRICT_CONVERSATIONS_PER_IP:
        return False
    
    if not USE_UPSTASH_REDIS or not redis_client:
        print(f"IP conversation counts (in-memory): {_ip_conv_store}")
        return _ip_conv_store.get(ip, 0) >= MAX_CONVERSATIONS_PER_IP

    try:
        key = f"{IP_CONV_KEY_PREFIX}{ip}"
        count = redis_client.get(key)
        return int(count or 0) >= MAX_CONVERSATIONS_PER_IP
    except Exception as e:
        print(f"Error checking IP block for {ip}: {e}", file=sys.stderr)
        return False


def increment_ip_conversation(ip: str) -> None:
    """Increment the conversation counter for an IP when a new conversation starts."""
    if not RESTRICT_CONVERSATIONS_PER_IP:
        return

    if not USE_UPSTASH_REDIS or not redis_client:
        _ip_conv_store[ip] = _ip_conv_store.get(ip, 0) + 1
        return

    try:
        key = f"{IP_CONV_KEY_PREFIX}{ip}"
        count = redis_client.incr(key)
        if count == 1:
            redis_client.expire(key, IP_CONV_TTL)
    except Exception as e:
        print(f"Error incrementing IP conversation count for {ip}: {e}", file=sys.stderr)


def generate_session_id() -> str:
    return str(uuid.uuid4())
