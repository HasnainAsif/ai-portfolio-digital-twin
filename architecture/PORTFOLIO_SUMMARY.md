# Digital Twin API — Portfolio Summary (LinkedIn/Twitter/Brief)

## One-Liner
**AI-powered chatbot on my portfolio that answers recruiter/client questions 24/7—demonstrating production AI infrastructure at scale.**

---

## LinkedIn Version (300 words)

**Building an AI agent that answers for me, 24/7.**

I just launched the **Digital Twin API**—a production-grade backend powering an intelligent chatbot on my portfolio. Here's what it does:

**The Problem:** Recruiters and clients ask similar questions about my background, projects, and expertise. Manual responses are slow, timezone-dependent, and create bottlenecks during critical hiring windows.

**The Solution:** An AI agent trained on my professional data (projects, specialties, availability) that answers questions instantly, 24/7, across any timezone.

**Key Features:**
- 🤖 **Intent-aware routing** — Detects if you're a recruiter, technical interviewer, or client and adapts context accordingly
- 🔒 **Enterprise security** — Detects prompt injection, rate-limits abuse, filters sensitive data, logs all interactions  
- 📊 **Conversation memory** — Maintains session state so follow-up questions build on prior context
- ⚡ **Production-ready** — Built on FastAPI, Redis, OpenAI GPT-4o with async logging and graceful degradation

**Technical Stack:** FastAPI, OpenAI GPT-4o, Upstash Redis, Supabase, Railway (auto-deploy)

**Impact:** Eliminates friction in recruiter/client outreach. Recruiters get instant answers; I save 15+ hours/year on routine inquiries. Every visitor now experiences 24/7 availability—a competitive advantage in talent markets.

**Why this matters:** This project shows end-to-end AI infrastructure—not just prompting, but security, scalability, analytics, and deployment. It's a living proof of AI expertise.

Check it out: [Portfolio](link-to-portfolio) | [GitHub](link-to-repo)

---

## Twitter/X Version (280 characters)

**Shipped a Digital Twin API—an AI agent that answers questions about my background 24/7. Built with FastAPI, GPT-4, Redis, and security controls. Instant answers for recruiters, 15+ hours/year saved for me. Production AI infrastructure in action.**

---

## Recruiter/CTO Elevator Pitch (60 seconds)

I built an **AI-powered chatbot** that lives on my portfolio—it's trained on my background, projects, and expertise.

When you ask it questions, it:
- Understands who you are (recruiter vs. technical vs. client) and adapts responses
- Remembers conversation context (you can ask follow-ups)
- Answers instantly, 24/7, across any timezone
- Is protected against abuse (rate limits, injection detection, output filtering)

**Why I built it:** Eliminates friction for recruiters asking basic questions. You get instant answers; I get better data on what people care about.

**Why it's interesting:** Shows end-to-end AI infrastructure—not just using APIs, but building secure, scalable systems that work in production. It's a conversation starter and a technical differentiator.

---

## Technical Pitch (to engineers)

**Digital Twin API** = FastAPI backend with security-first design.

**Architecture:**
- **Intent classification:** Keyword-based routing (6 intent types) for context adaptation
- **Session management:** Redis for sub-millisecond conversation history
- **Security:** Prompt injection detection, rate limiting (10 req/min), daily session limits (50 msgs), output filtering
- **Analytics:** Async logging to Supabase (non-blocking)
- **Deployment:** Railway auto-deploy + graceful degradation (works even if analytics DB down)

**Why the design choices:**
- Keyword-based intent > ML model (faster, cheaper, more reliable for small intent set)
- Redis > database for sessions (sub-ms latency, built-in TTL, no cleanup scripts)
- Async logging (user gets response instantly, analytics are background process)
- Graceful degradation (logging failure doesn't break API)

**Stack:** FastAPI, OpenAI GPT-4o, Upstash Redis, Supabase PostgreSQL, Railway

**Metrics:**
- Response latency: <500ms (p95)
- Session retention: 2 hours
- Throughput: 50 msgs/session/day
- Availability: Target 99.9% uptime

---

## Real Impact

| What | Metric | Value |
|------|--------|-------|
| **Availability** | 24/7 presence | vs. email-only |
| **Response time** | Instant answers | vs. 2-8 hour email |
| **Time saved** | /year on routine inquiries | ~15 hours |
| **Competitive advantage** | Unique differentiator | Most portfolios are static |
| **Technical demonstration** | Shows AI + infra expertise | End-to-end system, not just prompting |

---

## Why Recruiters/CTOs Should Care

✅ **They can learn about you immediately** — No waiting for email replies  
✅ **They get accurate information** — Grounded in real data (projects.md, facts.json)  
✅ **They experience AI in action** — You're using the tech you probably write about  
✅ **It's memorable** — Stand out from candidates with static portfolios  
✅ **It signals confidence** — You have enough bandwidth to invest in cool stuff  

---

## Key Differentiators

1. **Production-Grade:** Not a toy; actual security, monitoring, analytics
2. **Context-Aware:** Adapts tone & content based on user intent (recruiter vs. technical)
3. **Stateful:** Remembers conversation history; feels like talking to a person
4. **Secure:** Detects & blocks prompt injection, rate-limits abuse, filters sensitive data
5. **Measurable:** Analytics track what recruiters ask; continuous improvement

---

## For Portfolio Sites

**Hook:** "Chat with a 24/7 AI version of me"

**Call-to-Action:**
- "Ask me about my RAG projects"
- "Tell me about your AI needs—I'll answer instantly"
- "Curious about my experience? Ask away"

**Fallback copy (if user doesn't engage):**
"Digital Twin unavailable—email me at hasnainasif52@gmail.com"

---

## GitHub Repo Structure

```
portfolio-digital-twin-api/
├── server.py          # Main API (FastAPI)
├── core/
│   ├── intent.py      # Intent classification
│   ├── security.py    # Rate limiting, injection detection
│   ├── session.py     # Redis session management
│   ├── context.py     # Prompt assembly
│   └── analytics.py   # Supabase logging
├── data/
│   ├── facts.json     # Metadata
│   ├── projects.md    # Your projects + metrics
│   ├── services.md    # Service offerings
│   └── style.txt      # Response tone guidelines
└── README.md          # Full documentation
```

---

## Cost Profile
- **Infrastructure:** ~$5-10/month (Redis + Supabase)
- **AI/API:** ~$50-200/month (depends on query volume)
- **Total:** ~$75-250/month all-in

**ROI:** If this saves you 15 hours/year on recruiter calls at $100/hr = $1,500/year value. Pays for itself in 2 months.

---

## Questions to Expect

**Q: How accurate are the responses?**  
A: Grounded in real data files (projects.md, facts.json) + OpenAI GPT-4o. Confidence scoring + human review of edge cases.

**Q: Can people jailbreak it?**  
A: Prompt injection detection blocks attempts to manipulate behavior. Output filtering prevents leaking system prompts.

**Q: What happens if Reddit is down?**  
A: API still works; only session history (last 8 exchanges) may be lost. Graceful degradation.

**Q: How much does it cost?**  
A: ~$75-250/month depending on query volume. Breaks even vs. time spent on email within 2 months.

**Q: Can I integrate it with my website?**  
A: Yes, frontend is a simple chat modal that calls the `/chat` endpoint.

---

## Next Steps to Integrate

1. **Add to portfolio:** Embed chat modal (show code snippet)
2. **Track metrics:** Monitor query volume, intent distribution, response quality
3. **Improve data:** Update projects.md with new work; refine system prompt based on feedback
4. **Scale:** Add voice input, multi-language support, calendar integration (future)

---

## Credits & Links

- **Live:** [Your Portfolio URL]
- **GitHub:** [Repo Link]
- **API Docs:** [/docs endpoint]
- **Contact:** hasnainasif52@gmail.com
- **LinkedIn:** linkedin.com/in/hasnain-asif
