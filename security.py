"""
Security module for AI Digital Twin FastAPI backend.

Handles:
- Rate limiting (slowapi)
- Input validation and prompt injection detection
- Output filtering for sensitive information
- Abuse logging
"""

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple

from slowapi import Limiter
from slowapi.util import get_remote_address

# ============================================================================
# RATE LIMITING
# ============================================================================

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10/minute"],  # 10 requests per minute per IP address
    storage_uri="memory://"  # Use in-memory storage for rate limit state
)

# ============================================================================
# INPUT VALIDATION
# ============================================================================

# Injection patterns (case-insensitive)
INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|your)\s+instructions",
    r"ignore\s+your",
    r"system\s+prompt",
    r"you\s+are\s+now",
    r"pretend\s+(you\s+are|to\s+be)",
    r"act\s+as\s+(if|though)",
    r"forget\s+(everything|your)",
    r"developer\s+mode",
    r"jailbreak",
    r"DAN",
    r"override\s+your",
    r"new\s+instructions",
    r"disregard",
]

# Compile patterns for efficiency
COMPILED_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in INJECTION_PATTERNS]


def validate_input(message: str) -> Tuple[bool, str]:
    """
    Validate user input for security issues.

    Args:
        message: The input message to validate

    Returns:
        Tuple of (is_valid, reason). If valid, returns (True, "").
        If invalid, returns (False, reason) where reason is one of:
        - "injection_attempt": Detected prompt injection attempt
        - "too_long": Message exceeds 500 characters
    """
    # Check if empty
    if not message or not message.strip():
        return False, "empty_message"

    # Check length
    if len(message) > 500:
        return False, "too_long"

    # Check for injection patterns
    for pattern in COMPILED_PATTERNS:
        if pattern.search(message):
            return False, "injection_attempt"

    return True, ""


# ============================================================================
# OUTPUT FILTERING
# ============================================================================

# Email pattern
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

# Phone number pattern - matches various phone number formats
PHONE_PATTERN = re.compile(
    r"(?:\+?1[-.\s]?)?\(?(?:\d{3})\)?[-.\s]?(?:\d{3})[-.\s]?(?:\d{4})\b"
)


def filter_output(response: str, context_email: str) -> str:
    """
    Filter output to prevent leaking sensitive information.

    Checks for:
    - System prompt/instruction references
    - Email addresses that don't match the context email
    - Phone number patterns

    Args:
        response: The AI response to filter
        context_email: The expected email for validation (usually hasnainasif52@gmail.com)

    Returns:
        The filtered response if clean, or a safe fallback if sensitive info detected
    """
    safe_fallback = (
        "I'm here to answer questions about Hasnain's professional experience and services. "
        "Could you ask me something about his background, projects, or how he can help you?"
    )

    # Check for system prompt or instruction mentions
    if re.search(r"system\s+prompt|my\s+instructions", response, re.IGNORECASE):
        return safe_fallback

    # Check for email addresses that don't match context_email
    emails_found = EMAIL_PATTERN.findall(response)
    if emails_found:
        for email in emails_found:
            if email.lower() != context_email.lower():
                return safe_fallback

    # Check for phone numbers
    if PHONE_PATTERN.search(response):
        return safe_fallback

    return response


# ============================================================================
# ABUSE LOGGING
# ============================================================================

def log_abuse(ip: str, session_id: str, reason: str, message: str) -> None:
    """
    Log abuse attempts to a file.

    Creates logs/abuse.log if it doesn't exist.
    Never raises exceptions - all errors are logged to stderr.

    Args:
        ip: IP address of the requester
        session_id: Session ID
        reason: Reason for the abuse flag (e.g., "injection_attempt", "too_long")
        message: The suspicious message (will be truncated to 100 chars)
    """
    try:
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        # Format the log entry
        timestamp = datetime.utcnow().isoformat()
        truncated_message = message[:100] if message else ""
        # Escape pipe characters in message to avoid breaking the log format
        truncated_message = truncated_message.replace("|", "\\|")
        log_entry = f"{timestamp} | {ip} | {session_id} | {reason} | {truncated_message}\n"

        # Append to abuse log
        log_file = log_dir / "abuse.log"
        with open(log_file, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error logging abuse: {e}", file=sys.stderr)
