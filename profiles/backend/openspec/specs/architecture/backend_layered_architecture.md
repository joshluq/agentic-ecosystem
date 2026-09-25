# Architecture Specification: Backend Layered Architecture (Hono & Supabase)

## 1. Purpose & Scope
This specification defines the architectural invariants, layer boundaries, and state management rules for all backend API routes, services, and database migrations in Kilomenos Backend.

## 2. Core Architectural Layers

```
Client Requests (Mobile / Webhooks)
        ↓
[Layer 1: Routing & Middleware (`src/index.ts`)]
  - Supabase Auth JWT Verification (`withSupabase`)
  - Entitlement Guards (`verifyPremiumAccess`)
  - Input Validation & Parameter Sanitization
        ↓
[Layer 2: Service Layer (`src/services/`)]
  - Isolated Business Logic & Calculations
  - Cloud Service Adapters (FCM HTTP v1, Google Play RTDN)
  - Idempotent Transactional Operations
        ↓
[Layer 3: Persistence & Security (`supabase/`)]
  - PostgreSQL Tables & Relational Constraints
  - Bulletproof Row Level Security (RLS) Policies
  - Transactional Migrations (`BEGIN ... COMMIT`)
```

### 2.1 Layer Invariants:
- **Routing Layer (`src/index.ts`)**:
  - Responsible strictly for HTTP protocol orchestration, status codes, and error formatting.
  - Must never contain raw SQL queries or complex business logic.
- **Service Layer (`src/services/*Service.ts`)**:
  - Independent, unit-testable TypeScript functions.
  - Must enforce idempotency on write operations (upserts with client UUIDs).
- **Persistence Layer (`supabase/migrations/`)**:
  - Must enable Row Level Security on every table (`ENABLE ROW LEVEL SECURITY`).
  - Policies must enforce tenant boundaries (`auth.uid() = user_id`).
  - Privilege escalation is strictly prohibited outside authorized background jobs.

## 3. Serverless Edge Compatibility
- All backend routes implemented in `src/index.ts` must maintain compatibility with Deno Edge Functions in `supabase/functions/api/index.ts`.
- Environment variables must be resolved through standardized config helpers supporting both Node `process.env` and Deno `Deno.env`.
