# ADR-[ID]: [Short Title of Architectural Decision]

**Feature ID**: [FEAT-XXX]  
**Status**: PROPOSED | ACCEPTED | REJECTED | DEPRECATED | SUPERSEDED  
**Deciders**: Software Architect  
**Date**: YYYY-MM-DD  
**Technical Stakeholders**: Senior Android Developer, QA/Testing Engineer  

---

## 1. Context and Problem Statement
[Describe the technical context, business drivers, and the specific architectural challenge being solved. Reference PRD-[ID] and relevant functional requirements.]

## 2. Decision Drivers
- [Driver 1: e.g., Low latency (< 150ms) and type safety via TypeScript / Hono]
- [Driver 2: e.g., Strict tenant isolation and GDPR compliance via PostgreSQL Row Level Security]
- [Driver 3: e.g., Local-First mobile sync support with client-generated UUID idempotency]
- [Driver 4: e.g., Automated deployment reproducibility across Supabase environments]

## 3. Considered Architectural Options
1. **Option 1**: [Description — e.g., Monolithic ORM (Prisma / TypeORM) with Express]
   - *Pros*: Familiar abstraction, automatic schema migration generation.
   - *Cons*: High memory footprint, cold-start latency, bypasses Supabase native RLS policies.
2. **Option 2**: [Description — e.g., Hono REST Router + Supabase Client + Native SQL RLS]
   - *Pros*: Lightweight edge-ready performance, native PostgreSQL RLS multi-tenant security, typed Hono context, zero cold-start bloat.
   - *Cons*: Requires maintaining SQL migration files and typed DTO interfaces manually.
3. **Option 3**: [Description — e.g., Pure Supabase PostgREST direct client calls (No custom backend)]
   - *Pros*: Zero server code required for simple CRUD.
   - *Cons*: Cannot handle third-party webhooks (Google Play RTDN), OAuth2 token caching (FCM HTTP v1), or server-side entitlement validation.

## 4. Decision Outcome
- **Chosen Option**: Option 2 — Hono REST Router + Supabase PostgreSQL RLS + Typed Services
- **Architecture Pattern**: `HONO_SUPABASE_LAYERED` | `EDGE_FUNCTION_SERVERLESS`
- **Justification**: [Explain why the chosen option best balances security, low latency, idempotency, and long-term maintainability for Kilomenos.]

## 5. System Topology & Module Structure
- **Target Layers & Packaging**:
  - `src/index.ts` — Hono router, auth middleware, request validation, and error boundaries.
  - `src/services/[service]Service.ts` — Isolated business logic, third-party integrations, and idempotent database mutations.
  - `supabase/migrations/` — Transactional PostgreSQL tables, indices, and Row Level Security policies.
  - `supabase/functions/api/` — Serverless Edge Functions mirror for cloud distribution on Deno.
- **Security & Multi-Tenancy**:
  - Authentication: Supabase Auth JWT parsed in middleware.
  - Authorization: Row Level Security guarantees data isolation (`auth.uid() = user_id`).
  - Entitlements: Guard middleware (`verifyPremiumAccess`) enforces subscription level before handler execution.
- **External Cloud Integrations**:
  - FCM HTTP v1: Dispatcher with in-memory token cache and dead token pruning.
  - Google Play RTDN: Webhook endpoint processing Pub/Sub push events.

## 6. Consequences & Tradeoffs
- **Positive Consequences**:
  - Ultra-low latency and minimal resource overhead.
  - Bulletproof security: data cannot leak between tenants even if application code has logic flaws.
  - 100% testable via isolated TypeScript integration suites without mock emulators.
- **Negative Consequences**:
  - Database migrations must be explicitly crafted in SQL with transactional blocks.
  - Synchronizing routes between local Node server and Deno Edge Functions requires discipline or shared modules.
- **Neutral Consequences**:
  - Requires strict convention compliance regarding DTO validation and error serialization.

## 7. Guardrails & Compliance Rules
1. **Mandatory Row Level Security (RLS)**: Every public table must enable RLS and have explicit tenant isolation policies (`auth.uid() = user_id`).
2. **Atomic Migrations**: All database schema changes must be wrapped in transactional `BEGIN ... COMMIT` blocks with idempotent guards (`IF NOT EXISTS`).
3. **Never Expose Service Role Key**: Client-facing endpoints and edge functions must never return or leak `SUPABASE_SERVICE_ROLE_KEY`.
4. **Defensive Schema Validation**: All external payload inputs must be validated with runtime schema parsing before reaching domain or database services.

