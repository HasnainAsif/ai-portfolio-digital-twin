import asyncio
from contextlib import asynccontextmanager
import os
import time
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI, RateLimitError, APIError
from pydantic import BaseModel

from core.analytics import log_conversation
from core.context import build_prompt
from core.intent import classify_intent, INTENT_OFFTOPIC, OFFTOPIC_RESPONSE
from core.security import limiter, validate_input, filter_output, log_abuse
from core.session import (
    UPSTASH_REDIS_URL,
    UPSTASH_REDIS_TOKEN,
    USE_UPSTASH_REDIS,
    load_conversation,
    save_conversation,
    check_session_limit,
    check_ip_conversation_limit,
    generate_session_id,
)
from core.analytics import USE_SUPABASE_POSTGRES
from core.resources import facts

# Load environment variables
load_dotenv()


# Environment validation function
def validate_environment():
    """
    Validate required and optional environment variables at startup.
    - Required vars: server will not accept requests if missing (but will still start)
    - Optional vars: server logs warnings if missing
    """
    required_vars = ["OPENAI_API_KEY", "CORS_ORIGIN"]
    optional_vars = {}

    if USE_UPSTASH_REDIS:
        required_vars.append("UPSTASH_REDIS_URL")
        optional_vars["UPSTASH_REDIS_TOKEN"] = "Advanced Redis features unavailable"

    if USE_SUPABASE_POSTGRES:
        optional_vars["SUPABASE_URL"] = "Analytics disabled"
        optional_vars["SUPABASE_KEY"] = "Analytics disabled"

    missing_required = []
    missing_optional = []

    # Check required variables
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)

    # Check optional variables
    for var, warning_msg in optional_vars.items():
        if not os.getenv(var):
            missing_optional.append((var, warning_msg))

    # Print results
    if missing_required:
        print(f"⚠️  MISSING REQUIRED ENVIRONMENT VARIABLES:")
        for var in missing_required:
            print(f"   - {var}")
        print("   Server will continue but may not function properly.")

    if missing_optional:
        print(f"⚠️  OPTIONAL FEATURES DISABLED:")
        for var, warning_msg in missing_optional:
            print(f"   - {var}: {warning_msg}")

    if not missing_required and not missing_optional:
        print("✓ Environment OK")


# Lifespan event handler
@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Initialize on startup, cleanup on shutdown.
    The lifespan pattern ensures resources are properly initialized before the app
    starts accepting requests, and properly cleaned up when the app shuts down.
    """
    print("Digital Twin API starting...")
    print(f"Loaded OpenAI model: {openai_model}")
    print("Context files loaded")

    # Validate environment variables
    validate_environment()

    # Attempt Upstash Redis connection ping
    if USE_UPSTASH_REDIS:
        try:
            from upstash_redis import Redis
            redis_client = Redis(url=UPSTASH_REDIS_URL, token=UPSTASH_REDIS_TOKEN)
            redis_client.ping()
            print("Upstash Redis connected")
        except Exception as e:
            print(f"Warning: Upstash Redis connection failed - {str(e)}")
    else:
        print("Upstash Redis disabled (USE_UPSTASH_REDIS=false)")

    yield # Server is now running and accepting requests
    ### Add cleanup code here if needed (e.g., redis_client.close())
    # db.close()
    # cache.disconnect()
    # logger.info("App shutdown complete")


# Initialize FastAPI app
app = FastAPI(title="Hasnain Digital Twin API", lifespan=lifespan)

# Add SlowAPI rate limiting middleware
app.state.limiter = limiter

contact_email = facts.get("email", "hasnainasif52@gmail.com")

# Configure CORS
cors_origin = os.getenv("CORS_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[cors_origin],
    allow_credentials=False, # Set to False for better security since we don't need cookies
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
openai_client = AsyncOpenAI(api_key=openai_api_key) # Use the new AsyncOpenAI client for async calls


# Pydantic models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Hasnain Digital Twin API",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with service status"""
    if USE_UPSTASH_REDIS:
        redis_status = "unavailable"
        try:
            from upstash_redis import Redis
            redis_client = Redis(url=UPSTASH_REDIS_URL, token=UPSTASH_REDIS_TOKEN)
            redis_client.ping()
            redis_status = "connected"
        except Exception:
            redis_status = "unavailable"
    else:
        redis_status = "disabled"

    analytics_status = "enabled" if USE_SUPABASE_POSTGRES else "disabled"

    return {
        "status": "ok",
        "model": openai_model,
        "redis": redis_status,
        "analytics": analytics_status,
    }


@app.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute") # 10 requests per minute per IP are allowed to prevent abuse
async def chat(request: Request, chat_request: ChatRequest):
    """Chat endpoint with rate limiting and security checks"""

    client_ip = request.client.host
    session_id = chat_request.session_id

    # Step 1: SECURITY CHECK
    is_valid, reason = validate_input(chat_request.message)
    if not is_valid:
        if reason == "injection_attempt":
            await log_abuse(
                client_ip,
                session_id or "none",
                reason,
                chat_request.message,
            )
            return ChatResponse(
                response=(
                    "I'm only able to discuss Hasnain's professional experience. "
                    "Please ask me about his background, projects, or services."
                ),
                session_id=session_id or "unknown",
            )
        elif reason == "too_long":
            return ChatResponse(
                response=(
                    "Could you keep your message under 500 characters? "
                    "Happy to help with a shorter question."
                ),
                session_id=session_id or "unknown",
            )

    # Step 2: SESSION SETUP
    if not session_id:
        ip_check = check_ip_conversation_limit(client_ip)
        if not ip_check["allowed"]:
            return ChatResponse(
                response=(
                    "You've reached the maximum number of conversations allowed from your network. "
                    f"Please reach out directly at {contact_email}"
                ),
                session_id="",
            )
        session_id = generate_session_id()

    session_check = check_session_limit(session_id)
    if not session_check["allowed"]:
        return ChatResponse(
            response=(
                "You have reached the daily message limit for this session. "
                f"Please reach out directly at {contact_email}"
            ),
            session_id=session_id,
        )

    conversation = load_conversation(session_id)

    # Step 3: INTENT CLASSIFICATION
    intent = classify_intent(chat_request.message)
    if intent == INTENT_OFFTOPIC:
        return ChatResponse(
            response=OFFTOPIC_RESPONSE,
            session_id=session_id,
        )

    # Step 4: CONTEXT ASSEMBLY
    system_prompt = build_prompt(intent)

    # Step 5: OPENAI CALL
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation)
    messages.append({"role": "user", "content": chat_request.message})

    openai_response = None
    retry_count = 0
    max_retries = 1
    openai_response_time_ms = 0

    # create separate function for OpenAI response
    while retry_count <= max_retries:
        try:
            _t0 = time.monotonic()
            openai_response = await openai_client.chat.completions.create(
                model=openai_model,
                messages=messages,
                max_completion_tokens=1500,
                # temperature=0.6,
            )
            openai_response_time_ms = int((time.monotonic() - _t0) * 1000)
            break
        except RateLimitError:
            # Handle OpenAI rate limit errors (quota exceeded for this minute)
            if retry_count < max_retries:
                # Retry is available: wait longer (2s) to allow OpenAI quota to reset
                print("OpenAI rate limit exceeded. Attempting retry after delay...")
                await asyncio.sleep(2)
                retry_count += 1
            else:
                # No more retries: inform user to try again in a moment
                print("OpenAI rate limit exceeded. Informing user to try again later.")
                return ChatResponse(
                    response=(
                        "I'm having a brief technical issue. Please try again in a "
                        f"moment or reach out at {contact_email}"
                    ),
                    session_id=session_id,
                )
        except APIError as e:
            # Handle transient OpenAI API errors (timeouts, 5xx errors, etc.)
            if retry_count < max_retries:
                print(f"OpenAI API error occurred (attempt {retry_count + 1}): {e}")
                await asyncio.sleep(1)
                retry_count += 1
            else:
                print(f"OpenAI API error persisted after retry: {e}")
                return ChatResponse(
                    response=(
                        "I'm having a brief technical issue. Please try again in a "
                        f"moment or reach out at {contact_email}"
                    ),
                    session_id=session_id,
                )

    if not openai_response:
        print("Failed to get response from OpenAI after retries. Informing user to try again later.")
        failure_response = (
            "I'm having a brief technical issue. Please try again in a "
            f"moment or reach out at {contact_email}"
        )
        return ChatResponse(response=failure_response, session_id=session_id)

    # Step 6: OUTPUT FILTER
    response_text = openai_response.choices[0].message.content
    if not response_text:
        print(f"[warning] Empty response from OpenAI — finish_reason={openai_response.choices[0].finish_reason} usage={openai_response.usage}")
        failure_response = (
            "I'm having a brief technical issue. Please try again in a "
            f"moment or reach out at {contact_email}"
        )
        _usage = openai_response.usage
        _cached = getattr(getattr(_usage, "prompt_tokens_details", None), "cached_tokens", 0) or 0
        asyncio.create_task(
            log_conversation(
                session_id,
                client_ip,
                intent,
                chat_request.message,
                failure_response,
                model=openai_model or os.getenv("OPENAI_MODEL", "unknown"),
                input_tokens=_usage.prompt_tokens,
                output_tokens=_usage.completion_tokens,
                total_tokens=_usage.total_tokens,
                cached_input_tokens=_cached,
                response_time_ms=openai_response_time_ms,
            )
        )
        return ChatResponse(response=failure_response, session_id=session_id)
    filtered_response = filter_output(response_text, contact_email)

    usage = openai_response.usage
    cached_input_tokens = getattr(getattr(usage, "prompt_tokens_details", None), "cached_tokens", 0) or 0
    print(f"[model]: {openai_model}; [tokens] session={session_id} input={usage.prompt_tokens} output={usage.completion_tokens} total={usage.total_tokens} cached={cached_input_tokens}")

    # Step 7: SAVE AND RESPOND
    conversation.append({"role": "user", "content": chat_request.message})
    conversation.append({"role": "assistant", "content": filtered_response})

    save_conversation(session_id, conversation)

    # Fire and forget logging
    asyncio.create_task(
        log_conversation(
            session_id,
            client_ip,
            intent,
            chat_request.message,
            filtered_response,
            model=openai_model,
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            cached_input_tokens=cached_input_tokens,
            response_time_ms=openai_response_time_ms,
        )
    )

    return ChatResponse(response=filtered_response, session_id=session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
