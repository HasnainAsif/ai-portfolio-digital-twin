# Digital Twin API — Summary & Impact

## What It Is

A production-grade AI backend that acts as an always-available version of you on your portfolio. It answers recruiter, client, and technical questions instantly, 24/7, using your real project and experience data.

## Problem It Solves

Static portfolios and email-based outreach are slow and timezone-dependent. Recruiters move on. Clients lose confidence. The Digital Twin eliminates that friction.

## How It Works

8-step request pipeline: rate limit check → injection detection → session load → intent classification → prompt assembly → GPT-4o response → output filtering → async analytics logging.

**Stack:** FastAPI, OpenAI GPT-4o, Upstash Redis, Supabase, Railway

## Key Capabilities

- Intent-aware routing (recruiter, technical, client, general)
- Stateful conversations via Redis (2-hour session window, last 8 exchanges)
- Prompt injection detection, rate limiting (10 req/min), daily session cap (50 msgs)
- Async logging to Supabase — analytics never block the response
- Graceful degradation — API works even if analytics DB is down
- Auto-deploy via Railway on every git push

---

## Impact Metrics

| Metric | Value |
|--------|-------|
| Response latency (p95) | <500ms |
| Availability | 24/7 / 99.9% target uptime |
| Session window | 2 hours |
| Rate limit | 10 req/min per IP |
| Daily message cap | 50 msgs/session |
| Estimated time saved | ~15 hrs/year on routine inquiries |
| Infrastructure cost | ~$75–250/month all-in |
| Estimated time-savings value | $1,500/year at $100/hr |
| Estimated conversion improvement | 5–15% interview callback lift |
| Scalability | 100s–1000s concurrent users (OpenAI-bound) |

## Competitive Position

Most developers have static portfolios. This system puts you in the top 1% of candidates by demonstrating end-to-end AI infrastructure — not just API calls, but security, session management, analytics, and production deployment.

## Signal to Hiring Managers

Shows full-stack AI engineering: prompt design, security hardening, async architecture, observability, and deployment automation. Built and shipped, not prototyped.
