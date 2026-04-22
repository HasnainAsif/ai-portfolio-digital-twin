# Hasnain Digital Twin API

A production-grade FastAPI backend that powers an AI-powered digital twin of Hasnain Asif. The API uses intent classification, prompt injection detection, rate limiting, and conversation state management to deliver contextual responses about his professional experience, projects, and services.

This system demonstrates enterprise-grade AI infrastructure with security controls, session management, analytics, and graceful degradation when external services are unavailable.

## Local Setup

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (fast Python package installer)

### 1. Install uv (if not already installed)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (with PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or use pip
pip install uv
```

### 2. Install Dependencies

**Check which configuration file exists, then use the appropriate command:**

**If `pyproject.toml` exists:**
```bash
uv sync
```
Creates a virtual environment and installs all dependencies from `pyproject.toml`.

**If only `requirements.txt` exists:**
```bash
uv pip install -r requirements.txt
```
Installs all dependencies directly from `requirements.txt`.

**For this project** (uses `requirements.txt`):
```bash
uv pip install -r requirements.txt
```

### 3. Activate Virtual Environment (optional)
```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

Or run commands directly with `uv run`:
```bash
uv run python server.py
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory with the following variables:

```env
# Required
OPENAI_API_KEY=sk-...
UPSTASH_REDIS_URL=https://...redis.upstash.io
CORS_ORIGIN=http://localhost:3000

# Optional (for analytics)
SUPABASE_URL=https://...supabase.co
SUPABASE_KEY=eyJ...
UPSTASH_REDIS_TOKEN=...
```

### 5. Run the Server
```bash
uv run python server.py
```

Or if virtual environment is activated:
```bash
python server.py
```

The server starts at `http://localhost:8000`. View API docs at `http://localhost:8000/docs`.

---

## Project Structure

```
portfolio-digital-twin-api/
├── server.py                 # Main FastAPI application
├── core/                     # Core modules package
│   ├── __init__.py          # Package exports
│   ├── analytics.py         # Supabase logging and analytics
│   ├── context.py           # System prompt building and context assembly
│   ├── intent.py            # Intent classification (keyword-based routing)
│   ├── security.py          # Input validation, rate limiting, output filtering
│   ├── session.py           # Redis session management and conversation history
│   └── resources.py         # Data file loading (facts, projects, etc.)
├── data/                     # Data files (loaded by resources.py)
│   ├── facts.json           # Core metadata and configuration
│   ├── summary.txt          # Professional summary
│   ├── projects.md          # Project descriptions
│   ├── certifications.md    # Education and credentials
│   ├── services.md          # Service offerings
│   ├── style.txt            # Response style guidelines
│   └── linkedin.pdf         # LinkedIn profile data
├── migrations/              # Database migrations
│   ├── README.md            # Migration setup instructions
│   └── 001_create_twin_logs.sql
├── .env                     # Environment variables (not in git)
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Module Organization

**`core/` Package** - All helper modules grouped for maintainability:
- **analytics.py** - Supabase client and conversation logging
- **context.py** - Loads data files and builds AI system prompts
- **intent.py** - Classifies user intent from messages (no AI calls)
- **security.py** - Rate limiting, injection detection, output filtering
- **session.py** - Redis-based conversation history and daily limits
- **resources.py** - Loads and exposes facts.json and other data files

**`server.py`** - Main application:
- FastAPI application setup and middleware configuration
- Route definitions (/, /health, /chat)
- Request/response handling
- Integration of all core modules

---

## API Endpoints

### 1. Root Endpoint
```
GET /
```
**Description:** Returns API metadata and version information.

**Response:**
```json
{
  "name": "Hasnain Digital Twin API",
  "version": "1.0.0"
}
```

---

### 2. Health Check
```
GET /health
```
**Description:** Returns system status including service connectivity and feature availability.

**Response:**
```json
{
  "status": "ok",
  "model": "gpt-4o",
  "redis": "connected",
  "analytics": "enabled"
}
```

**Status Values:**
- `redis`: "connected" | "unavailable" (session storage)
- `analytics`: "enabled" | "disabled" (Supabase logging)

---

### 3. Chat / Ask Digital Twin
```
POST /chat
```
**Description:** Send a message to the digital twin. Returns contextual responses based on intent classification, conversation history, and security validation.

**Rate Limit:** 10 requests per minute per IP address

**Request Body:**
```json
{
  "message": "Tell me about your RAG projects",
  "session_id": "uuid-string-optional"
}
```

**Response:**
```json
{
  "response": "I've built several RAG systems...",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Features:**
- **Intent Classification:** Automatically routes to technical, recruiter, project, or services-focused context
- **Security Validation:** Detects and blocks prompt injection attempts and oversized messages
- **Conversation History:** Maintains session state (2-hour TTL) with last 8 exchanges
- **Daily Limits:** 50 messages per session per 24 hours
- **Output Filtering:** Prevents leaking sensitive information (system prompts, unauthorized emails, phone numbers)
- **Async Logging:** Conversation data logged to Supabase (non-blocking)

---

## Data Files

All data files are in the `data/` directory. The system loads them on startup:

| File | Type | Purpose | Update Method |
|------|------|---------|----------------|
| **facts.json** | JSON | Core metadata (name, email, location, specialties, years_experience, etc.) | Edit JSON directly |
| **summary.txt** | Text | Professional summary and value proposition (3-4 paragraphs) | Edit in plain text |
| **projects.md** | Markdown | Detailed project descriptions with metrics and technologies used | Edit Markdown, supports code blocks |
| **certifications.md** | Markdown | Education, certifications, courses, and relevant credentials | Edit Markdown with dates |
| **services.md** | Markdown | Service offerings, pricing, engagement models, and typical timelines | Edit Markdown with structured sections |
| **style.txt** | Text | Response style guidelines (tone, voice, formatting preferences) | Edit in plain text |
| **linkedin.pdf** | PDF | LinkedIn profile export for additional context (optional) | Replace with updated PDF export |

### Updating Data

1. **During Development:** Edit files directly and restart the server
2. **In Production:** 
   - Update files in the repo
   - Redeploy the backend (Railway will auto-reload)
   - Changes take effect on next server startup

The system automatically reloads all data files when the server restarts.

---

## Deployment

### Railway Setup

#### 1. Add a `Procfile`

Create a `Procfile` in the project root so Railway knows how to start the server:

```
web: uvicorn server:app --host 0.0.0.0 --port $PORT
```

> Do **not** hardcode the port — Railway injects `$PORT` automatically.

#### 2. Pin your Python version

Create a `runtime.txt` in the project root:

```
python-3.12
```

Match this to the version in your `.python-version` file.

#### 3. Connect Repository

- Go to [Railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
- Connect your GitHub account and select this repository
- Railway auto-detects Python and installs dependencies from `requirements.txt`

#### 4. Set Environment Variables

In Railway dashboard → your service → **Variables**, add:

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `OPENAI_MODEL` | e.g. `gpt-4o` |
| `CORS_ORIGIN` | Your frontend URL (e.g. `https://yoursite.com`) |
| `USE_UPSTASH_REDIS` | `true` |
| `USE_SUPABASE_POSTGRES` | `true` |
| `UPSTASH_REDIS_URL` | Your Upstash Redis URL |
| `UPSTASH_REDIS_TOKEN` | Your Upstash token |
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Your Supabase service role key |
| `RESTRICT_CONVERSATIONS_PER_IP` | `true` |
| `MAX_CONVERSATIONS_PER_IP` | `15` |

#### 5. Generate a Public Domain

Railway dashboard → your service → **Settings** → **Networking** → **Generate Domain**

Update `CORS_ORIGIN` in your frontend to point to this domain.

#### 6. Deploy

- Push to your connected branch to trigger auto-deploy
- Monitor build and runtime logs in the Railway **Deployments** tab

### Required Services (Third-Party)

Before deploying, ensure these services are set up:

#### Upstash Redis
- **Purpose:** Session storage and rate limiting
- **Setup:** Create account at [upstash.com](https://upstash.com), create Redis database
- **Variables Needed:** `UPSTASH_REDIS_URL`, `UPSTASH_REDIS_TOKEN`
- **Status:** Check in `/health` endpoint

#### Supabase (Optional but Recommended)
- **Purpose:** Persistent analytics logging (conversation data)
- **Setup:** Create project at [supabase.com](https://supabase.com)
- **Variables Needed:** `SUPABASE_URL`, `SUPABASE_KEY`
- **Important:** Must create `twin_logs` table before first deployment (see below)

#### OpenAI API
- **Purpose:** AI response generation
- **Setup:** Get API key from [platform.openai.com](https://platform.openai.com)
- **Variable Needed:** `OPENAI_API_KEY`
- **Model:** `gpt-4o` (configurable via `OPENAI_MODEL` env var)

---

## Database: Supabase Setup

### Create the `twin_logs` Table

**IMPORTANT:** You must create this table in Supabase before deploying to production.

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Click **New Query**
4. Copy the SQL from `migrations/001_create_twin_logs.sql`
5. Click **Run**

The migration creates:
- `twin_logs` table with columns: `id`, `session_id`, `visitor_ip`, `intent`, `user_message`, `ai_response`, `created_at`
- Indexes on `session_id`, `created_at`, and `intent` for optimal query performance
- Row-level security policies restricting inserts to the service role

**Without this table, analytics logging will fail gracefully (logged to stderr) but the API will continue operating.**

For detailed setup instructions, see [migrations/README.md](../migrations/README.md).

---

## Architecture Overview

### Request Flow

```
Client Request
    ↓
Rate Limiting (slowapi) → Blocks if >10/min per IP
    ↓
Input Validation → Detects injection attempts & length violations
    ↓
Session Management → Load or create session from Redis
    ↓
Intent Classification → Keyword-based routing (no AI calls)
    ↓
Prompt Building → Assemble system prompt with context data
    ↓
OpenAI API Call → Generate response with conversation history
    ↓
Output Filtering → Remove sensitive data (emails, phones, system prompts)
    ↓
Session Save → Persist conversation to Redis (2-hour TTL)
    ↓
Async Logging → Fire-and-forget log to Supabase
    ↓
Response to Client
```

### Key Components

- **security.py:** Rate limiting, input validation (injection detection), output filtering, abuse logging
- **intent.py:** Keyword-based intent classification (technical, recruiter, project, services, general, off_topic)
- **context.py:** Data file loading and system prompt building with intent-aware style hints
- **session.py:** Redis-based conversation history and daily message limit tracking
- **analytics.py:** Supabase integration for persistent interaction logging
- **resources.py:** Loads facts.json and other data files for use across modules

### Security Features

✓ Prompt injection detection (ignores instructions, system prompts, jailbreaks)  
✓ Message length validation (max 500 chars)  
✓ Output filtering (prevents leaking emails, phones, system prompts)  
✓ Rate limiting (10 req/min per IP)  
✓ Daily message limits (50 per session)  
✓ Session TTL (2 hours inactivity)  
✓ Abuse logging (all flagged attempts recorded)  
✓ CORS configured (frontend origin whitelisting)  

---

## Monitoring & Debugging

### Check System Status
```bash
curl http://localhost:8000/health
```

### View Abuse Logs
```bash
cat logs/abuse.log
```

### Monitor Redis Connection
The `/health` endpoint will show `"redis": "unavailable"` if connection fails.

### Supabase Analytics
Query conversation data:
```sql
SELECT COUNT(*), intent 
FROM twin_logs 
WHERE created_at > NOW() - INTERVAL '24 hours'
GROUP BY intent
ORDER BY count DESC;
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Redis connection failed on startup | `UPSTASH_REDIS_URL` or token missing/invalid | Check `.env` file, regenerate tokens in Upstash dashboard |
| 429 Too Many Requests | Rate limit exceeded (10/min per IP) | Wait 60 seconds, requests are counted per IP address |
| Analytics not logging | Supabase table doesn't exist or credentials invalid | Run migration SQL (see Supabase Setup) |
| Response says "session limit exceeded" | Daily 50-message limit hit | Limit resets after 24 hours |
| Prompt injection detected | Message contains keywords like "ignore instructions" | Submit a legitimate question instead |

---

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Environment Variables for Testing
```env
OPENAI_API_KEY=test-key
UPSTASH_REDIS_URL=
UPSTASH_REDIS_TOKEN=
CORS_ORIGIN=http://localhost:3000
```

### Code Quality
- **Type Hints:** All functions use type annotations
- **Docstrings:** Every module, function, and complex logic documented
- **Comments:** Inline comments explain non-obvious decisions
- **Error Handling:** Graceful degradation (fails open) when optional services unavailable

---

## Support & Contact

For questions about the digital twin setup or API:
- Email: hasnainasif52@gmail.com
- LinkedIn: linkedin.com/in/hasnain-asif
- GitHub: github.com/HasnainAsif

---

## License

This project is for Hasnain Asif's professional portfolio. Unauthorized use or distribution is not permitted.
