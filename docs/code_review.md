# Code Review: Portfolio Digital Twin API

**Date:** 2026-04-25  
**Reviewer:** Claude Code (automated)  
**Scope:** Full repository review  
**Branch:** `main`

---

## Executive Summary

The codebase is well-architected with a clean separation of concerns, solid security controls, and production-ready async patterns. The request pipeline in `server.py` is logically structured and easy to follow. The main actionable issues are: one confirmed bug in the prompt-building logic (missing `f` prefix), missing error handling for startup file loads, unpinned dependencies, and no test coverage.

---

## Repository Structure

```
portfolio-digital-twin-api/
├── server.py               # FastAPI app — main request pipeline
├── requirements.txt        # Dependencies (unpinned)
├── Procfile                # Railway deployment config
├── core/
│   ├── __init__.py         # Package exports
│   ├── analytics.py        # Supabase / local JSONL logging
│   ├── context.py          # System prompt assembly
│   ├── intent.py           # Keyword-based intent classifier
│   ├── resources.py        # Startup file loader
│   ├── security.py         # Rate limiting, injection detection, output filter
│   └── session.py          # Redis session + IP conversation tracking
├── data/                   # Markdown/JSON/text content files
├── migrations/             # Supabase SQL migrations
└── architecture/           # Design docs
```

---

## Findings by File

### `server.py`

| Severity | Finding |
|----------|---------|
| Medium | **Duplicate step label** — `# Step 3` appears twice (lines ~231 and ~247). Minor but confusing during debugging. |
| Medium | **IP block returns HTTP 200** — When an IP is blocked, the endpoint returns a `ChatResponse` with status 200 instead of 429. This breaks REST conventions and makes it harder for clients to distinguish a real response from a rate-limit message. |
| Low | **Redis client re-created on every `/health` call** — A new `Redis(...)` object is instantiated inside the health check handler on every request instead of reusing the module-level `redis_client`. |
| Low | **Large commented-out blocks** — Multiple code paths are commented out (session depth limiting, concise retry, old identity prompt). These should either be deleted or documented in an ADR. |
| Low | **`asyncio.create_task` in fire-and-forget** — Safe pattern, but if the event loop closes before the task completes (e.g., during rapid shutdown), log entries can be silently lost. Consider a background task queue or shutdown hook. |
| Info | The 8-step pipeline structure is clear and well-commented. The retry logic for `RateLimitError` and `APIError` is a good defensive pattern. |

**Action:** Fix step numbering. Change IP-block response to HTTP 429. Reuse `redis_client` in `/health`. Delete dead comment blocks.

---

### `core/context.py`

| Severity | Finding |
|----------|---------|
| **Bug** | **`scope_section` is not an f-string** — Line 124 uses `"""..."""` (not `f"""..."""`), so all `{name}` placeholders inside are emitted literally into the system prompt. The AI receives `"{name}'s skills and experience"` verbatim. |
| Low | `rules_section` (line 133) is correctly an f-string, so `{name}` is substituted there. |
| Low | **Commented-out alternative identity/context sections** (lines 82–110) — large dead block should be removed. |
| Low | **`CERTIFICATIONS`, `SUMMARY`, `SERVICES`, `STYLE` loaded at startup but not injected into the live prompt** — only `resume` is used in `context_section`. The other variables are exported from `__init__.py` but go unused in prompt construction. This is either a regression or leftover from a refactor. |
| Info | Intent-aware style hints (`INTENT_TECHNICAL`, etc.) are a clean pattern. |

**Action:** Add `f` prefix to `scope_section`. Remove commented blocks. Audit which data variables are still needed in the prompt.

---

### `core/resources.py`

| Severity | Finding |
|----------|---------|
| High | **No error handling for required files** — `summary.txt`, `style.txt`, and `facts.json` are opened with bare `open()` calls (lines 20–27). If any file is missing or corrupt the entire server crashes at startup with an unhandled exception. |
| Medium | **`linkedin` variable loaded but never exported or used** — `PdfReader` runs on every startup to parse `linkedin.pdf`, but the result is not used anywhere. |
| Low | **Duplicate `facts.json` loading** — `facts` is loaded here and again inside `context.py::_load_facts()`. The module-level `facts` from `resources.py` is what `server.py` imports; `context.py` loads its own separate copy `FACTS`. Two copies of the same data in memory. |

**Action:** Wrap bare `open()` calls in try/except with a descriptive error and `sys.exit(1)`. Remove or export `linkedin`. Consolidate to a single `facts.json` load.

---

### `core/security.py`

| Severity | Finding |
|----------|---------|
| Medium | **Rate limiter uses in-memory storage** (`storage_uri="memory://"`). This is fine for a single-instance deployment but resets on every restart and does not work across multiple instances. Document this limitation explicitly. |
| Low | **Phone number regex is US-only** — `PHONE_PATTERN` matches `+1-XXX-XXX-XXXX` but not international formats (e.g., `+44 20 7946 0958`). |
| Low | **Injection pattern list is allow-list style** — A sufficiently creative rephrasing can bypass keyword-based detection. This is an accepted limitation for a first layer of defence, but it should not be the only layer. |
| Info | Compiled regex patterns, output filtering, and abuse logging are all solid. |

**Action:** Document single-instance limitation in `.env.example` / README. Consider `phonenumbers` library for international number detection.

---

### `core/intent.py`

| Severity | Finding |
|----------|---------|
| Low | **Keyword overlap causes classification bias** — `"built"` appears in both `TECHNICAL_KEYWORDS` and `PROJECT_KEYWORDS`. Because `TECHNICAL` is checked first, "tell me about a project you built" always resolves as `INTENT_TECHNICAL`. |
| Low | **Simple substring matching** — `"available"` in `RECRUITER_KEYWORDS` will match `"unavailable"`, producing false positives. |
| Info | Using `frozenset` instead of `set` for keyword containers would signal immutability to readers. No runtime impact. |

**Action:** Remove duplicate keywords across sets. Add word-boundary checks for ambiguous keywords.

---

### `core/session.py`

| Severity | Finding |
|----------|---------|
| Medium | **Non-atomic incr + expire** — In `increment_ip_conversation`, `redis_client.incr(key)` and `redis_client.expire(key, IP_CONV_TTL)` are two separate calls (lines ~120–122). Under concurrent requests a key could be incremented and then expire before the `expire` call runs, or the `expire` could race with a second `incr`. Use a Lua script or `SET key 1 EX ttl NX` pattern for atomicity. |
| Medium | **In-memory fallback stores are unbounded** — `_memory_store` and `_ip_conv_store` grow indefinitely for long-running processes. Every unique session ID and IP address accumulates. Add a periodic cleanup or use `functools.lru_cache` / a TTL dict. |
| Low | **`MAX_CONVERSATION_LENGTH` slicing duplicated** — The slice `messages[-MAX_CONVERSATION_LENGTH:]` is repeated in both `load_conversation` and `save_conversation`. Extract to a helper. |

**Action:** Make Redis incr+expire atomic. Add LRU/TTL eviction to in-memory fallback. Deduplicate slicing logic.

---

### `core/analytics.py`

| Severity | Finding |
|----------|---------|
| Low | **Duplicate log entry dict construction** — The `data` dict is built twice: once for local JSONL (lines ~67–80) and once for Supabase (lines ~88–99), with identical keys. Build it once, then branch on the destination. |
| Info | The never-raise contract (`Never raises exceptions`) is well-documented and correctly implemented. |

**Action:** Extract shared dict construction before the `if not USE_SUPABASE_POSTGRES` branch.

---

### `requirements.txt`

| Severity | Finding |
|----------|---------|
| High | **No version pinning** — All 10 dependencies are unpinned. A new release of `openai`, `fastapi`, or `supabase` can introduce breaking changes silently on the next deploy. |

**Action:** Pin all dependencies. Run `pip freeze > requirements.txt` against the current working virtualenv, then clean up dev-only packages.

---

### `migrations/001_create_twin_logs.sql`

| Severity | Finding |
|----------|---------|
| Low | **No composite index on `(session_id, created_at)`** — Common query pattern is likely `WHERE session_id = ? ORDER BY created_at`. The existing separate indexes on each column are less efficient than a composite. |
| Info | RLS policy correctly restricts inserts to `service_role`. Schema is clean. |

**Action:** Add `CREATE INDEX idx_twin_logs_session_created ON twin_logs(session_id, created_at);`

---

### `data/facts.json`

| Severity | Finding |
|----------|---------|
| Low | **Typo: `"calendaly"`** — The key is spelled `calendaly` but the correct field name should be `calendly`. This causes `facts.get("calendaly", "")` in `context.py` rules to return an empty string, so the Calendly link is silently omitted from the system prompt. |

**Action:** Rename key to `"calendly"` in `facts.json` and update all `facts.get("calendaly", ...)` calls.

---

## Security Summary

| Control | Status | Notes |
|---------|--------|-------|
| Prompt injection detection | ✓ Active | Regex-based; bypassable with creative phrasing |
| Output filtering (PII) | ✓ Active | Email + phone + system-prompt keyword checks |
| Rate limiting (per IP) | ✓ Active | 10 req/min via slowapi; in-memory — resets on restart |
| IP conversation limit | ✓ Active | 20 conversations/24h per IP |
| CORS | ✓ Active | Single origin only; credentials disabled |
| Supabase RLS | ✓ Active | Insert-only for service role |
| Session TTL | ✓ Active | 2h inactivity expiry |
| CSRF protection | ✗ Missing | POST `/chat` has no origin verification beyond CORS |
| Request authentication | ✗ Missing | No API key or token required to call `/chat` |
| Secrets management | ✓ Good | `.env` via `python-dotenv`; `.gitignore` covers `.env` |

---

## Performance Summary

| Area | Status | Notes |
|------|--------|-------|
| Async I/O | ✓ Good | `AsyncOpenAI`, `asyncio.create_task` for logging |
| Intent classification | ✓ Fast | Pure keyword matching, no AI call |
| Prompt caching | ✗ Missing | System prompt rebuilt on every request; no OpenAI prompt caching headers |
| Regex compilation | ✓ Good | Patterns compiled once at module load |
| Redis reuse | ✗ Partially | `redis_client` is a module-level singleton in `session.py` but re-created in `/health` |
| OpenAI retry backoff | ✗ Fixed delay | Uses fixed 2s / 1s delays; exponential backoff would be more resilient |
| In-memory leak risk | ✗ Medium | Unbounded `_memory_store` / `_ip_conv_store` in session.py |

---

## Prioritised Action List

### P1 — Fix Before Next Deploy

1. **`core/context.py` line 124** — Add `f` prefix to `scope_section` string literal so `{name}` placeholders are substituted.
2. **`core/resources.py` lines 20–27** — Wrap bare `open()` calls with `try/except FileNotFoundError` and exit gracefully with an informative message.
3. **`requirements.txt`** — Pin all dependency versions to avoid silent breaking upgrades.
4. **`data/facts.json`** — Fix `"calendaly"` typo to `"calendly"` and update all `facts.get("calendaly", ...)` calls in `context.py`.

### P2 — Short-term Improvements

5. **`core/session.py`** — Make `incr` + `expire` atomic using a Lua script or `SET ... EX ... NX`.
6. **`server.py`** — Return HTTP 429 for IP-blocked responses instead of HTTP 200.
7. **`core/session.py`** — Add TTL-based eviction to `_memory_store` and `_ip_conv_store` to prevent unbounded growth.
8. **`core/analytics.py`** — Deduplicate log entry dict construction.
9. **`core/intent.py`** — Remove `"built"` from `TECHNICAL_KEYWORDS` (already in `PROJECT_KEYWORDS`) to remove classification bias.
10. **Dead code** — Remove large commented-out blocks in `server.py` and `context.py`.

### P3 — Long-term Improvements

11. Add unit tests for `validate_input`, `classify_intent`, `filter_output`, and `build_prompt`.
12. Cache the built system prompt per intent (`functools.lru_cache`) to avoid rebuilding on every request.
13. Add exponential backoff to the OpenAI retry loop.
14. Add composite index `(session_id, created_at)` to `twin_logs` migration.
15. Audit which data variables (`SUMMARY`, `CERTIFICATIONS`, `SERVICES`, `STYLE`) are still needed in the system prompt — several are loaded but not injected.
16. Consider adding an API key requirement to `/chat` to prevent unauthenticated scraping.
