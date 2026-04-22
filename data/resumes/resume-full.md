# Hasnain Asif

### Full Stack AI Engineer

hasnainasif52@gmail.com &nbsp;·&nbsp; [LinkedIn](#) &nbsp;·&nbsp; [GitHub](#) &nbsp;·&nbsp; [Portfolio](#)
Pakistan &nbsp;·&nbsp; Open to Remote — US / UK / EU

---

## Professional Summary

Full Stack AI Engineer with [X] years building production AI systems and enterprise-grade web platforms. Specializes in multi-agent orchestration, RAG pipelines, and LLM-powered backends using LangGraph and LangChain. Delivered systems at scale — 11,000+ users, 170+ franchises, 4 countries. Equally fluent across AI infrastructure and full-stack engineering, from LLM pipelines to React frontends and distributed backends.

---

## Technical Skills

| Category           | Technologies                                                                                                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AI & LLM**       | LangChain · LangGraph · LlamaIndex · CrewAI · OpenAI Agents SDK · RAG · Prompt Engineering · Vector Databases · Embeddings · Tool Calling · Multi-Agent Systems · FastAPI |
| **Cloud & DevOps** | AWS (Lambda · SQS · EventBridge · API Gateway · Bedrock · S3 · ECR · SageMaker) · Terraform · GitHub Actions · CI/CD · Docker                                             |
| **Full Stack**     | React · Next.js · Node.js · Express.js · TypeScript · PostgreSQL · MongoDB · Redux · REST APIs · GraphQL · WebSockets                                                     |
| **Databases**      | ChromaDB · FAISS · Pinecone · PostgreSQL · MongoDB · Redis                                                                                                                |

---

## Professional Experience

### AI Engineer — Agentic AI & Production Systems &nbsp;·&nbsp; Self-Employed &nbsp;·&nbsp; Oct 2025 – Present

Disclaimer: This experience is based on my personal projects and courses.

_Designing and building production agentic AI systems — multi-agent pipelines, RAG architectures, and LLM integrations deployed on AWS._

- Built an agentic RAG pipeline with a retrieval evaluator agent that filters documents by relevance before generation — improving answer quality in document-heavy use cases
- Deployed a distributed multi-agent system on AWS: five Lambda functions (one per agent), S3-backed vector storage, SageMaker embeddings, API Gateway orchestration, and CloudFront + S3 for a Next.js frontend
- Implemented IaC pipelines using Terraform and GitHub Actions for automated deployment across AWS Bedrock, Lambda, ECR, S3, and CloudFront

---

### Senior Software Engineer &nbsp;·&nbsp; Tkxel &nbsp;·&nbsp; Oct 2023 – Present &nbsp;·&nbsp; Lahore, Pakistan

_Product engineering consultancy delivering enterprise software for US-based clients_

- Built core scheduling, shift assignment, and timezone systems for an enterprise workforce platform serving 11,000+ users across 170+ franchises in 4 countries — invalid assignments blocked at the UI level to prevent payroll errors
- Engineered a location-anchored DST timezone engine adopted across 50+ components — eliminated production-level shift scheduling errors across the US, Canada, UK, and Australia
- Led a 5-engineer team to revive a 2-year abandoned multi-tenant social platform with no documentation — owned task breakdown, PR reviews, and all technical decisions
- Reverse-engineered OpenFGA authorization schema from legacy deployments — restored full role-based permission hierarchy across all admin levels
- Built and shipped multi-currency Stripe subscriptions (PKR, USD, GBP) on a platform designed for 1M+ audience members across 1,000–5,000 brand Hubs

---

### Software Engineer &nbsp;·&nbsp; Tkxel &nbsp;·&nbsp; May 2022 – Oct 2023 &nbsp;·&nbsp; Lahore, Pakistan

_Built full-stack features for enterprise tools and internal platforms_

- Built and shipped enterprise helpdesk features for Tikit, an MS Teams-integrated ticketing platform for high-volume IT, HR, and Finance workflows
- Fixed drag-and-drop issues in a Jira-style kanban board managing ticket lifecycle status transitions
- Built a Custom Views system for an MS Teams-integrated enterprise helpdesk — enabled persistent multi-filter configurations across thousands of concurrent tickets

---

### Software Engineer &nbsp;·&nbsp; Invozone &nbsp;·&nbsp; Oct 2021 – Jan 2022 &nbsp;·&nbsp; Lahore, Pakistan

_Built and shipped a production multi-chain decentralized exchange enabling token swaps across Ethereum, Binance Smart Chain, Polygon, and Avalanche_

- Led frontend delivery end-to-end — owned architecture decisions and directed the backend and frontend developers
- Integrated MetaMask and Coinbase wallet connections with live on-chain function calls via Web3.js

---

### Software Engineer &nbsp;·&nbsp; OptimusFox &nbsp;·&nbsp; Aug 2020 – Oct 2021 &nbsp;·&nbsp; Lahore, Pakistan

_Built full-stack blockchain-based platforms across fintech and civic tech — led delivery on multiple products_

- Served as tech lead on a token offering (ITO) platform — designed ERD, owned full-stack architecture, and routed tasks across a 4-engineer team
- Built a blockchain-based tamper-resistant e-voting system with three role-based panels — admin, candidate, and voter — with on-chain ballot execution via Web3.js
- Developed a full-stack ICO platform with crypto and fiat investment flows, token calculator, and Solidity smart contract integration via Web3.js
- Owned full-stack delivery across all projects — React + Redux frontends, Node.js/Express backends, PostgreSQL and MongoDB databases

---

## AI Projects

### DocInsight — Verified Document Q&A

`LangGraph · LangChain · RAG · ChromaDB · OpenAI · Pydantic`

Multi-agent RAG system that eliminates manual document review — three specialized agents gate relevance, generate grounded answers, and verify factual support before any response reaches the user. Targets the 1.8 hours/day knowledge workers lose to unverified information retrieval.

- Orchestrated a 3-agent LangGraph pipeline: Relevance Checker classifies queries as `CAN_ANSWER / PARTIAL / NO_MATCH` and exits early on irrelevant inputs; Research Agent generates answers strictly from retrieved context; Verification Agent checks factual support across 5 structured fields before surfacing results
- Implemented hybrid retrieval combining BM25 keyword search (40% weight) and ChromaDB vector search (60% weight) via EnsembleRetriever — dual-strategy approach improves recall on exact-match queries that pure semantic search consistently misses
- Built conditional re-research routing in LangGraph so answers failing verification automatically regenerate with structured feedback — unverified answers never surface to the user
- Applied SHA-256 hash-based document caching (7-day TTL) and session-level retriever caching, eliminating redundant reprocessing and API calls on repeated uploads or re-queries

---

### Sidekick — Autonomous AI Work Agent

`LangGraph · OpenAI · Playwright · Serper API · Python REPL · Pydantic`

Two-model agentic system that executes multi-step tasks across browser, code, files, and search without human supervision — a structurally independent evaluator verifies success criteria are met before any result is returned. Addresses the 62% of workday spent on tasks that could run unattended and the 9.5 minutes of focus lost each time a worker checks in on a running task.

- Designed a two-model LangGraph pipeline separating execution from evaluation: worker operates with Playwright browser automation, Python REPL, sandboxed file I/O, and web search; evaluator runs with no tool access and no task-completion pressure, eliminating self-evaluation bias
- Implemented a typed feedback loop using Pydantic structured output — evaluator rejections inject a machine-parseable feedback string directly into the worker's system prompt on retry, so the worker reads exactly why it failed before reattempting
- Added a third evaluator signal (`user_input_needed`) distinct from `success_criteria_met` — detects genuine stuck states and surfaces blockers to the user instead of looping silently on repeated failures
- Scoped all file operations to a sandboxed directory and configured Playwright in visible mode, enabling real-time user monitoring of browser actions for trust and debuggability

---

### AI-Powered Digital Twin API

`FastAPI · OpenAI · Redis · Supabase · Next.js · Railway`

Production AI backend that functions as a 24/7 intelligent digital twin — answers recruiter and client inquiries instantly with intent-aware responses, full conversation memory, and enterprise-grade security. Delivers sub-500ms response latency with a 5-layer security pipeline.

- Designed an 8-step request pipeline covering rate limiting (10 req/min per IP), prompt injection detection, Redis session retrieval, intent routing, prompt assembly, LLM generation, output filtering, and async logging to Supabase
- Built keyword-based intent classification that routes recruiter, client, and technical inquiries to context-matched response templates — no ML inference overhead, deterministic and auditable
- Deployed Redis-backed session management persisting last 8 exchanges per user with a 2-hour TTL, enabling natural multi-turn conversations across timezones without state loss
- Architected async fire-and-forget analytics logging so Supabase downtime never degrades API availability — graceful degradation by design

---

## Full-Stack Projects

### Enterprise Workforce Platform &nbsp;·&nbsp; Tkxel

`React · Node.js · MongoDB · Ruby on Rails · PostgreSQL · Azure`

Built a franchise-based security workforce management platform serving 11,000+ users across 170+ franchises in the US, Canada, UK, and Australia. Consolidated 5+ disconnected operational systems — scheduling, payroll, contracts, attendance, and invoicing — into a single unified platform.

- Engineered the scheduling and shift assignment system — supervisors split contract hours, manage shift states, and assign officers within contract bounds; invalid assignments blocked at the UI level to prevent payroll and billing errors on live contracts
- Designed and implemented a location-based DST-aware timezone engine adopted across 50+ frontend components — shift times anchor to franchise location regardless of browser timezone or DST changes, eliminating production drift where officers were appearing hours or a full day off
- Designed multi-tenant franchise isolation architecture so franchise users operate independently within their own data scope while platform owners retain global visibility across all 170+ franchises

---

### Multi-Tenant Social Platform &nbsp;·&nbsp; Tkxel

`React · Node.js · GraphQL · MongoDB · OpenFGA · Stripe · AWS (S3, Lambda)`

Led a 5-engineer team for 4 months to revive an abandoned multi-tenant social platform inactive for 2 years — restored a fully non-functional system with no documentation, no infrastructure visibility, and no prior ownership handoff.

- Reverse-engineered OpenFGA authorization schema and tuple relationships from legacy production data over 1 month — restored Super Admin, Organization Admin, and sub-admin permission hierarchies with zero documentation or handoff
- Diagnosed and recovered broken AWS infrastructure (S3, Lambda) with no prior system knowledge or architecture documentation
- Built and shipped multi-currency Stripe subscriptions — admins configure circle-level pricing in PKR, USD, and GBP; users subscribe in their preferred currency
- Restored core platform workflows including organization, hub, and circle management, content publishing, and audience engagement features — on a codebase no one had touched in 2 years

---

### Tikit — Enterprise Helpdesk on MS Teams &nbsp;·&nbsp; Tkxel

`React · TypeScript · FluentUI · Tailwind CSS · .NET · Azure`

MS Teams-integrated helpdesk platform for enterprise ticket management — supports high-volume workflows across IT, HR, and Finance. Enables users to raise tickets, analysts to triage, and admins to manage thousands of active requests within a unified Teams interface.

- Built Custom Views for ticket listing — admins save multi-filter configurations across high-volume queues (IT, HR, Finance), eliminating repetitive filtering across sessions
- Restored drag-and-drop status transitions across the ticket lifecycle (In Progress → In Review → Resolved) — stabilized core triage workflow for analysts managing high-volume queues
- Implemented pagination and search to support scalable handling of thousands of concurrent active tickets
- Built role-separated panels for users, analysts, and admins within MS Teams — each surface scoped to the actions and data relevant to that role

---

### Dexi Finance — Multi-Chain DEX

`React · Redux · Web3.js · MetaMask · Coinbase Wallet · Django · Bootstrap`

Multi-chain decentralized exchange supporting token swaps across Ethereum, Binance Smart Chain, Polygon, and Avalanche. Integrated MetaMask and Coinbase Wallet connections with real-time on-chain calls via Web3.js — users swap any supported token without a centralized intermediary.

- Led frontend delivery as sole frontend engineer — owned architecture decisions and directed the backend developer
- Built token swap flows across Ethereum, Binance Smart Chain, Polygon, and Avalanche with real-time on-chain function calls via Web3.js
- Integrated MetaMask and Coinbase Wallet connections handling live blockchain transactions across 4 networks

---

### Dinisium — Initial Token Offering Platform

`React · Redux · Node.js · Express.js · PostgreSQL · Web3.js · Solidity`

Blockchain-based investment platform giving retail investors access to tokenized assets aligned with their risk profile and ethical values. Built three separate panels — super admin, admin, and investor — with role-based access across the full stack.

- Served as tech lead on a 3-engineer team — designed the ERD, owned backend architecture, and routed tasks across the team
- Built three role-based panels (super admin, admin, investor) with full-stack delivery across React frontend and Node.js/PostgreSQL backend
- Delivered a production platform enabling retail investors to invest in tokenized assets aligned with their risk profile and ethical values — integrated smart contracts via Web3.js and Solidity

---

### Taswit — Blockchain E-Voting System

`React · Redux · Node.js · Express.js · PostgreSQL · Web3.js`

Tamper-resistant voting platform with three role-based panels — admin, candidate, and voter. Admins create elections and manage candidates; voters cast ballots on-chain. All panels include dashboards with ongoing, upcoming, and completed election views.

- Owned full-stack delivery — designed database schema, built React + Redux frontend across all three panels, Node.js/Express backend, and PostgreSQL database
- Built three role-based panels (admin, candidate, voter) with dashboards showing ongoing, upcoming, and completed elections
- Integrated on-chain ballot execution via Web3.js in collaboration with the blockchain developer

---

### Initial Coin Offering Platform

`React · Redux · Node.js · Express.js · MongoDB · Web3.js · Solidity`

Investment platform where investors review business ideas and fund them via crypto or fiat, receiving utility tokens in return. Separate admin and investor portals with full investment lifecycle management.

- Built full-stack — React + Redux frontend, Node.js/Express backend, and MongoDB database with smart contract integration via Web3.js and Solidity
- Developed separate admin and investor portals with full investment lifecycle management across both surfaces
- Built a token calculator allowing investors to preview token allocation before committing funds

---

### NFT Marketplace

`React · Redux · Node.js · Express.js · PostgreSQL · Web3.js`

Full-featured NFT marketplace where users create collections, list NFTs, and place bids — similar to OpenSea in scope and functionality.

- Built full-stack — React + Redux frontend, Node.js/Express backend, PostgreSQL database
- Integrated MetaMask and mobile wallet connections with live on-chain function calls via Web3.js in collaboration with the blockchain developer
- Built collection management, NFT listing, and bidding flows end to end across both frontend and backend

---

### Fantasy Sport — Decentralized NFT Marketplace _(Freelance)_

`React · Next.js · Redux · Web3.js · Styled Components`

Decentralized NFT marketplace where admins create and manage collections — separate admin panel (React) and client panel (Next.js) with shared Redux state management.

- Built a decentralized NFT marketplace with separate admin panel (React) and client panel (Next.js) sharing Redux state management
- Integrated MetaMask and mobile wallet connections across both panels with live on-chain function calls via Web3.js in collaboration with the blockchain developer
- Owned full frontend delivery as sole frontend engineer across both admin and client surfaces

---

## Education

### BS Software Engineering &nbsp;·&nbsp; University of Engineering and Technology, Taxila &nbsp;·&nbsp; Rawalpindi, Pakistan ·&nbsp; 2016 - 2020

---

## Certifications

| Credential                                                  | Issuer                | Platform      |
| ----------------------------------------------------------- | --------------------- | ------------- |
| **RAG and Agentic AI Specialization** _(Specialization)_    | IBM                   | Coursera      |
| AI Engineer Production Track: Deploy LLMs & Agents at Scale | Ed Donner             | Udemy         |
| AI Engineer Agentic Track: The Complete Agent & MCP Course  | Ed Donner             | Udemy         |
| Serverless Framework Bootcamp: Node.js, AWS & Microservices | Ariel Weinberger      | Udemy         |
| Data Science Internship Certificate                         | Gufhtugu Publications | Skilled Score |

---

_All placeholder lines marked [DUMMY] or [brackets] are to be replaced with real content._
