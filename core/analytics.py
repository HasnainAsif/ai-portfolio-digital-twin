"""
Analytics and logging module for tracking interactions and system metrics.
Records conversation data, user interactions, and generates analytics reports.
"""
import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
try:
    from supabase import create_client

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if SUPABASE_URL and SUPABASE_KEY:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    else:
        print("Warning: SUPABASE_URL or SUPABASE_KEY not configured", file=sys.stderr)
        supabase_client = None
except ImportError:
    print("Warning: supabase library not installed", file=sys.stderr)
    supabase_client = None
except Exception as e:
    print(f"Warning: Failed to initialize Supabase client: {e}", file=sys.stderr)
    supabase_client = None


async def log_conversation(
    session_id: str,
    visitor_ip: str,
    intent: str,
    user_message: str,
    ai_response: str,
) -> None:
    """
    Log a conversation turn to Supabase permanently and asynchronously.

    Args:
        session_id: Unique identifier for the conversation session
        visitor_ip: IP address of the visitor
        intent: Classified intent of the user message
        user_message: The user's message text
        ai_response: The AI's response text

    Returns:
        None. Never raises exceptions; errors are logged to stderr.
    """
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
