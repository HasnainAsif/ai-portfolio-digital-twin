# Projects

## 1. Support Copilot RAG System [FEATURED]

**Result:** 41% reduction in repetitive support tickets in 6 weeks

A production RAG system that grounds support answers in internal standard operating procedures, dramatically reducing volume of repetitive tickets and freeing support team for complex issues.

**What I Built:**
- RAG pipeline that ingests and chunks internal SOPs into vector embeddings
- Intelligent retrieval system with metadata routing by product area and user tier
- Hybrid retrieve-rerank architecture for high-precision answer matching
- Confidence scoring with automatic fallback escalation to human support
- Answer grounding with source citations so users see where answers come from

**Technical Decisions:**
- Used Pinecone for vector storage with structured metadata for intelligent filtering
- Implemented confidence thresholds to catch edge cases before they reach users
- Built fallback escalation logic—low-confidence queries automatically route to human support team
- Added comprehensive logging for continuous pipeline improvement

**Stack:** Next.js, FastAPI, LangChain, Pinecone, OpenAI GPT-4

---

## 2. RevOps Multi-Agent Workflow

**Result:** Saved 18 hours/week for sales operations team

A multi-agent AI system that automates lead qualification, CRM updates, and personalized follow-up sequences—orchestrating a complex workflow with guardrails and human oversight.

**What I Built:**
- Planner-executor-reviewer agent loop that breaks complex RevOps tasks into structured steps
- Tool calling system for lead qualification, CRM data updates, and email generation
- Confidence scoring guards that flag uncertain decisions for human review
- Mandatory approval gates for high-value actions (contracts, VIP accounts)
- Event logging and replay tracing for debugging and auditing workflows

**Technical Decisions:**
- Architected as planner (decompose tasks) → executor (run subtasks) → reviewer (validate) loop
- Implemented structured tool calling with schema validation for deterministic behavior
- Added confidence scoring on every decision point with configurable approval thresholds
- Built comprehensive audit trails so any workflow can be replayed and debugged

**Stack:** Node.js, LangGraph, OpenAI, HubSpot API

---

## 3. Contract Intelligence Assistant

**Result:** Reduced first-pass review time from 2.5 hours to 35 minutes per contract

A document intelligence system that extracts risk clauses, highlights problematic terms, and generates negotiation-ready summaries for legal teams.

**What I Built:**
- Private document ingestion pipeline with end-to-end encryption
- Role-based access control (lawyers see all clauses, non-legal stakeholders see summaries)
- Risk clause extraction with confidence scoring and explanation of why clauses matter
- Side-by-side source citations so reviewers see extracted text next to original document
- Negotiation summary generation with recommended action items and red flags

**Technical Decisions:**
- Implemented private document storage with encrypted vectors (private embeddings never leave organization)
- Built role-based views—contract leadership sees risk summary, legal team sees full clause analysis
- Added confidence scoring on every extraction so borderline clauses are flagged for manual review
- Designed citation system to build lawyer trust (they verify reasoning against source text)

**Stack:** React, Express, MongoDB, Azure OpenAI

---

## 4. Commerce Admin Suite

A full-stack MERN dashboard for managing inventory, orders, returns, and analytics across an e-commerce operation.

**Stack:** React, Node.js, Express, MongoDB, Redux

---

## 5. Real-time Collaboration Board

A Kanban-style workspace enabling teams to collaborate with real-time presence awareness, threaded comments, and activity timelines.

**Stack:** Next.js, Socket.IO, Node.js, PostgreSQL

---

## 6. Hiring Pipeline Tracker

A recruitment workflow application managing candidate progression through stages with interview scorecards, feedback collection, and hiring analytics.

**Stack:** React, Express, MongoDB, JWT, Tailwind CSS
