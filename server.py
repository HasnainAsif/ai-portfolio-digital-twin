import asyncio
from contextlib import asynccontextmanager
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI, RateLimitError, APIError
from pydantic import BaseModel

from analytics import log_conversation
from context import build_prompt
from intent import classify_intent, INTENT_OFFTOPIC, OFFTOPIC_RESPONSE
from security import limiter, validate_input, filter_output, log_abuse
from session import (
    load_conversation,
    save_conversation,
    check_session_limit,
    generate_session_id,
)

# Load environment variables
load_dotenv()


# Lifespan event handler
@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize on startup, cleanup on shutdown"""
    print("Digital Twin API starting...")
    print(f"Loaded OpenAI model: {openai_model}")
    print("Context files loaded")

    # Attempt Upstash Redis connection ping
    try:
        from upstash_redis import Redis
        r = Redis.from_env()
        r.ping()
        print("Upstash Redis connected")
    except Exception as e:
        print(f"Warning: Upstash Redis connection failed - {str(e)}")

    yield


# Initialize FastAPI app
app = FastAPI(title="Hasnain Digital Twin API", lifespan=lifespan)

# Add SlowAPI rate limiting middleware
app.state.limiter = limiter

# Configure CORS
cors_origin = os.getenv("CORS_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[cors_origin],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")
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
    """Health check endpoint"""
    return {
        "status": "ok",
        "model": openai_model,
    }


@app.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(request: Request, chat_request: ChatRequest):
    """Chat endpoint with rate limiting and security checks"""

    client_ip = request.client.host
    session_id = chat_request.session_id

    # Step 1: SECURITY CHECK
    validation_result = validate_input(chat_request.message)
    if not validation_result["valid"]:
        reason = validation_result.get("reason", "unknown")

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
        session_id = generate_session_id()

    session_check = check_session_limit(session_id)
    if not session_check["allowed"]:
        return ChatResponse(
            response=(
                "You have reached the daily message limit for this session. "
                "Please reach out directly at hasnainsaf52@gmail.com"
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

    while retry_count <= max_retries:
        try:
            openai_response = await openai_client.chat.completions.create(
                model=openai_model,
                messages=messages,
                max_tokens=600,
                temperature=0.6,
            )
            break
        except RateLimitError:
            if retry_count < max_retries:
                await asyncio.sleep(2)
                retry_count += 1
            else:
                return ChatResponse(
                    response=(
                        "I'm having a brief technical issue. Please try again in a "
                        "moment or reach out at hasnainsaf52@gmail.com"
                    ),
                    session_id=session_id,
                )
        except APIError:
            if retry_count < max_retries:
                await asyncio.sleep(1)
                retry_count += 1
            else:
                return ChatResponse(
                    response=(
                        "I'm having a brief technical issue. Please try again in a "
                        "moment or reach out at hasnainsaf52@gmail.com"
                    ),
                    session_id=session_id,
                )

    if not openai_response:
        return ChatResponse(
            response=(
                "I'm having a brief technical issue. Please try again in a "
                "moment or reach out at hasnainsaf52@gmail.com"
            ),
            session_id=session_id,
        )

    # Step 6: OUTPUT FILTER
    response_text = openai_response.choices[0].message.content
    filtered_response = filter_output(response_text, "hasnainsaf52@gmail.com")

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
        )
    )

    return ChatResponse(response=filtered_response, session_id=session_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
