# Getting Started with AI Digital Twin API

This guide will help you set up and run the AI Digital Twin API application.

## Prerequisites

- Python 3.13 or higher
- `uv` package manager

## Setup Instructions

### 1. Clone/Navigate to the Project

Ensure you're in the project directory:

```bash
cd /path/to/portfolio-digital-twin-api
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit the `.env` file and configure the following variables:

```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
CORS_ORIGINS=http://localhost:3000
MEMORY_DIR=./memory
```

**Available environment variables:**

- `OPENAI_API_KEY` - Your OpenAI API key (required for API calls)
- `CORS_ORIGINS` - Comma-separated list of allowed origins (default: `http://localhost:3000`)
- `MEMORY_DIR` - Local directory for storing conversation memory (default: `./memory`)

### 3. Install Dependencies

#### Option A: If `pyproject.toml` exists

Use `uv sync` to sync and install all dependencies:

```bash
uv sync
```

#### Option B: If using `requirements.txt` only

Use `uv pip install` to install from requirements:

```bash
uv pip install -r requirements.txt
```

This will install:

- FastAPI
- Uvicorn (ASGI server)
- python-dotenv
- python-multipart
- pypdf
- And other required dependencies

### 4. Run the Server

Start the development server:

```bash
uv run python server.py
```

You should see output like:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 5. Verify the Server is Running

Open a new terminal and check the health endpoint:

```bash
curl http://localhost:8000/health
```

You should receive a success response.

## API Endpoints

### Root Endpoint

```http
GET /
```

Returns basic API information and storage type.

### Health Check

```http
GET /health
```

Returns the health status of the API.

### Chat Endpoint

```http
POST /chat
Content-Type: application/json

{
  "message": "Your message here",
  "session_id": "optional-session-id"
}
```

**Response:**

```json
{
  "response": "AI response here",
  "session_id": "session-id"
}
```

### Get Conversation History

```http
GET /conversation/{session_id}
```

Returns all messages in the conversation for the given session.

## Development

### Project Structure

```
.
├── server.py              # Main FastAPI application
├── context.py             # System prompt and context
├── resources.py           # Helper functions
├── requirements.txt       # Project dependencies
├── .env.example           # Environment variables template
├── .env                   # Environment variables (local, not in git)
├── data/                  # Data files (PDF, text, JSON)
└── .venv/                 # Virtual environment directory
```

### Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Install dependencies using one of these commands:
- `uv sync` (if pyproject.toml exists)
- `uv pip install -r requirements.txt` (if using requirements.txt)

### Issue: `OPENAI_API_KEY not found` or API calls fail

**Solution:** Make sure you've created a `.env` file and added your OpenAI API key:

```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### Issue: Port 8000 already in use

**Solution:** Change the port in `server.py` line 177:

```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use a different port
```

### Issue: CORS errors when calling from frontend

**Solution:** Update `CORS_ORIGINS` in `.env` to include your frontend URL:

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Next Steps

1. Test the API using tools like:
   - `curl` for command-line testing
   - Postman for GUI testing
   - The built-in OpenAPI docs at `http://localhost:8000/docs`

2. Integrate the API with your frontend application

3. Deploy to production (Docker, Heroku, Railway, etc.)

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [uv Package Manager](https://docs.astral.sh/uv/)
