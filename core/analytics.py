"""
Analytics and logging module for tracking interactions and system metrics.
Records conversation data, user interactions, and generates analytics reports.
"""
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

USE_SUPABASE_POSTGRES = os.getenv("USE_SUPABASE_POSTGRES", "false").lower() == "true"

# Create Supabase client only when flag is enabled
supabase_client = None
if USE_SUPABASE_POSTGRES:
    try:
        from supabase import create_client

        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")

        if SUPABASE_URL and SUPABASE_KEY:
            supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        else:
            print("Warning: SUPABASE_URL or SUPABASE_KEY not configured", file=sys.stderr)
    except ImportError:
        print("Warning: supabase library not installed", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Failed to initialize Supabase client: {e}", file=sys.stderr)

_LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "conversations.jsonl"


def _write_local_log(entry: dict) -> None:
    try:
        _LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with _LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Error writing local log: {e}", file=sys.stderr)


async def log_conversation(
    session_id: str,
    visitor_ip: str,
    intent: str,
    user_message: str,
    ai_response: str,
    model: str = "",
    input_tokens: int = 0,
    output_tokens: int = 0,
    total_tokens: int = 0,
    cached_input_tokens: int = 0,
    response_time_ms: int = 0,
) -> None:
    """
    Log a conversation turn to Supabase (production) or a local JSONL file (testing).

    Never raises exceptions; errors are logged to stderr.
    """
    if not USE_SUPABASE_POSTGRES:
        _write_local_log({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "visitor_ip": visitor_ip,
            "intent": intent,
            "response_time_ms": response_time_ms,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cached_input_tokens": cached_input_tokens,
            "user_message": user_message,
            "ai_response": ai_response,
        })
        return

    if supabase_client is None:
        print("Warning: Supabase client not available, cannot log conversation", file=sys.stderr)
        return

    try:
        data = {
            "session_id": session_id,
            "visitor_ip": visitor_ip,
            "intent": intent,
            "user_message": user_message,
            "ai_response": ai_response,
        }
        supabase_client.table("twin_logs").insert(data).execute()
    except Exception as e:
        print(f"Error logging conversation to Supabase: {e}", file=sys.stderr)
