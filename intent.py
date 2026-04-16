"""
Intent recognition and routing module for analyzing user messages.
Determines user intent from input text using keyword and pattern matching only.
No AI calls in this module.
"""

# Intent category constants
INTENT_TECHNICAL = "technical"
INTENT_RECRUITER = "recruiter"
INTENT_PROJECT = "project"
INTENT_SERVICES = "services"
INTENT_GENERAL = "general"
INTENT_OFFTOPIC = "off_topic"

# Keyword maps for intent classification
TECHNICAL_KEYWORDS = {
    "stack", "architecture", "built", "how did you", "langchain", "pinecone",
    "fastapi", "react", "node", "mongodb", "postgresql", "docker", "api", "rag",
    "vector", "embedding", "agent", "llm", "openai", "typescript", "redis", "websocket"
}

RECRUITER_KEYWORDS = {
    "available", "availability", "hire", "hiring", "full-time", "full time",
    "salary", "rate", "remote", "relocate", "open to", "looking for",
    "contract", "freelance", "opportunity", "role", "position", "job"
}

PROJECT_KEYWORDS = {
    "project", "built", "demo", "github", "portfolio", "show me", "example",
    "case study", "result", "metric", "worked on", "shipped"
}

SERVICES_KEYWORDS = {
    "service", "offer", "help me", "work together", "cost", "price", "budget",
    "quote", "timeline", "deliverable", "engagement", "scope", "build for me",
    "how to hire", "contact"
}

OFFTOPIC_KEYWORDS = {
    "homework", "recipe", "weather", "sports", "politics", "movie", "music",
    "write me a poem", "tell me a joke", "what is the capital",
    "stock price", "news today", "celebrity"
}

# Off-topic response for users
OFFTOPIC_RESPONSE = (
    "I'm set up to talk about Hasnain's professional experience, projects, "
    "and services. Is there something about his background or how he can "
    "help you that I can answer?"
)


def classify_intent(message: str) -> str:
    """
    Classify incoming message into intent categories using keyword matching.

    Checks keywords in order: technical, recruiter, project, services.
    Returns off-topic if message matches off-topic signals.
    Returns general as default fallback.

    Args:
        message: The incoming message to classify

    Returns:
        One of the INTENT_ constants: technical, recruiter, project, services,
        general, or off_topic
    """
    message_lower = message.lower()

    # Check technical keywords
    if any(keyword in message_lower for keyword in TECHNICAL_KEYWORDS):
        return INTENT_TECHNICAL

    # Check recruiter keywords
    if any(keyword in message_lower for keyword in RECRUITER_KEYWORDS):
        return INTENT_RECRUITER

    # Check project keywords
    if any(keyword in message_lower for keyword in PROJECT_KEYWORDS):
        return INTENT_PROJECT

    # Check services keywords
    if any(keyword in message_lower for keyword in SERVICES_KEYWORDS):
        return INTENT_SERVICES

    # Check off-topic keywords
    if any(keyword in message_lower for keyword in OFFTOPIC_KEYWORDS):
        return INTENT_OFFTOPIC

    # Default to general for anything professional-sounding
    return INTENT_GENERAL


__all__ = [
    "classify_intent",
    "INTENT_TECHNICAL",
    "INTENT_RECRUITER",
    "INTENT_PROJECT",
    "INTENT_SERVICES",
    "INTENT_GENERAL",
    "INTENT_OFFTOPIC",
    "OFFTOPIC_RESPONSE",
]
