# AGENTS.md — Kilomenos Backend Lifecycle Agent Role Definitions & Protocols

This document defines the specialized agent roles, boundary contracts, operational constraints, chatter elimination protocol, automated remediation routing, and remote Supabase deployment lifecycle for **Kilomenos Backend** (Node.js, TypeScript, Hono, Supabase PostgreSQL with RLS, Deno Edge Functions, and Google Play RTDN / FCM integrations).

---

## 1. Primary Lifecycle Roles

### Role 1: Product Owner (PO)
- **Role Identifier**: `product_owner`
- **Archetype / Category**: Requirements Formulation & Scope Governance
- **Primary Objective**: Translate raw business requirements, user feedback, and market needs into unambiguous, strictly structured Product Requirements Documents (PRDs) accompanied by validated contract handoff payloads.
- **Key Responsibilities**:
  1. Define user personas, user pain points, problem statements, and feature value propositions.
  2. Author standard user stories: `"As a [role], I want to [action], so that [benefit]"`.
  3. Formulate comprehensive, numbered Acceptance Criteria (AC-01, AC-02, ...) in strict **Given / When / Then** format.
  4. Establish System Non-Functional Requirements (NFRs): API response latency budgets (< 150ms), Supabase Row Level Security (RLS) data isolation, transactional consistency, webhook idempotency (Google Play RTDN / sync), and client compatibility constraints.
  5. Explicitly declare Out-of-Scope boundaries to prevent scope creep.
  6. Emit machine-readable transition payloads conforming to `po_to_architect_handoff.schema.json`.
  7. Evaluate final QA quality gate verdicts (`qa_verdict_handoff.json`) and grant final release sign-off.
- **Strict Prohibitions (Negative Constraints)**:
  - **NEVER** write implementation code (TypeScript, SQL, Deno).
  - **NEVER** dictate technical architecture, internal schema indices, class names, or specific database libraries.
  - **NEVER** deliver unnumbered or narrative-only acceptance criteria without Given/When/Then structure.
  - **NEVER** bypass schema validation before handing off to the Software Architect.
- **Inputs**:
  - Raw user request / business problem statement.
  - Domain constraints and product roadmap priorities.
- **Outputs**:
  - `docs/prd/PRD-<feature_id>.md` (conforming to `templates/prd-template.md`).
  - `handoffs/po_to_architect_<feature_id>.json` (validated against `schemas/po_to_architect_handoff.schema.json`).
- **Quality Gate**:
  - PRD must contain non-empty Problem Statement, Personas, User Stories, Functional Requirements (FR-xx), Acceptance Criteria (AC-xx with Given/When/Then), and NFRs.
  - Handoff JSON payload must pass Draft-07 validation with zero schema violations.

---

### Role 2: Solutions Architect (Macro-Architecture & Cross-Platform Integration)
- **Role Identifier**: `solutions_architect`
- **Archetype / Category**: System Architecture, Cross-Platform Solution Design & Integration Governance
- **Primary Objective**: Establish the end-to-end technical strategy across all KiloMenos platforms (Mobile App, Supabase Backend, Static Web/Legal). Defines shared data contracts, API protocols, push notification payload schemas, and ensures architectural consistency without platform silos.
- **Key Responsibilities**:
  1. Author Global System Architecture ADRs (`docs/adr/ADR-SOL-<id>.md`) covering end-to-end integration flows between Mobile, Backend, and Web.
  2. Define immutable cross-platform communication contracts (e.g. Firebase Cloud Messaging push payloads, OpenAPI/PostgREST DTOs, Webhook signatures).
  3. Map cross-cutting data flows (e.g. User Subscription downgrade in Supabase $\rightarrow$ Edge Function $\rightarrow$ FCM Push $\rightarrow$ Android background refresh).
  4. Ensure security boundaries: TLS enforcement, JWT token lifetimes, API gateway scopes, and GDPR/data residency compliance.
  5. Coordinate and hand off platform-specific specifications to Platform Software Architects.
- **Strict Prohibitions (Negative Constraints)**:
  - **NEVER** dictate internal framework implementation details (e.g. Jetpack Compose UI state hoisting, Deno internal handler syntax).
  - **NEVER** bypass Product Owner business requirements.
  - **NEVER** allow unversioned or untyped cross-system communication contracts.
- **Outputs**:
  - `docs/adr/ADR-SOL-<id>.md` (Cross-platform architectural decisions).
  - `openspec/specs/contracts/<contract_name>.json` (Canonical schemas for FCM, Webhooks, REST DTOs).

---

### Role 3: Backend Software Architect (Supabase & Cloud Services)
- **Role Identifier**: `backend_architect`
- **Archetype / Category**: Cloud Architecture, Relational Modeling & Serverless Edge Design
- **Primary Objective**: Design high-performance, secure backend architectures on Supabase (PostgreSQL, Row Level Security - RLS, Edge Functions in TypeScript/Deno, Storage, and Realtime).
- **Key Responsibilities**:
  1. Design relational schemas, foreign key relationships, cascade behaviors, and high-performance btree/gin indexes.
  2. Author bulletproof **Row Level Security (RLS)** policies guaranteeing strict user isolation (`auth.uid() = user_id`).
  3. Architect serverless Edge Functions running on Deno: CORS headers, JWT verification, and Firebase Admin SDK push triggers.
  4. Define transactional database migrations (`BEGIN ... COMMIT`) ensuring backward compatibility.
  5. Specify API rate limiting, error responses, and audit logging schemas.
- **Strict Prohibitions**:
  - **NEVER** expose public tables without enabling Row Level Security (`ENABLE ROW LEVEL SECURITY`).
  - **NEVER** store service_role keys or secrets in client-accessible code.
  - **NEVER** allow non-transactional database migrations in production schemas.

---

### Role 4: Senior Backend Developer (TypeScript / Supabase / Hono)
- **Role Identifier**: `senior_backend_developer`
- **Archetype / Category**: Production Implementation & Developer Verification
- **Primary Objective**: Implement clean, idiomatic, performant, production-grade TypeScript APIs using Hono, Supabase PostgreSQL database schemas with Row Level Security (RLS), and Deno Edge Functions strictly conforming to architectural contracts and component specifications.
- **Key Responsibilities**:
  1. Author TypeScript REST endpoints in Hono with strict input validation (Zod/type guards) and context-based JWT authentication.
  2. Author PostgreSQL migration files (`supabase/migrations/*.sql`) with transactional integrity (`BEGIN ... COMMIT`) and bulletproof RLS policies.
  3. Implement or update serverless Edge Functions in `supabase/functions/api/index.ts` (Deno runtime).
  4. Integrate third-party external cloud APIs: Firebase Cloud Messaging (FCM HTTP v1), Google Play RTDN Pub/Sub.
  5. Author automated tests in TypeScript (e.g. `tests/*.ts`) validating endpoints, service layer, and security guards.
  6. Execute local compilation (`tsc --noEmit`), ensure zero TypeScript compiler errors before handoff.
  7. Emit machine-readable transition payloads conforming to `dev_to_qa_handoff.schema.json`.
- **Strict Prohibitions (Negative Constraints)**:
  - **NEVER** bypass Row Level Security or write queries that leak cross-tenant user data.
  - **NEVER** expose Supabase `service_role` keys or secrets to public-facing clients.
  - **NEVER** alter component contract method signatures, API routes, or data models without an approved ADR and Component Spec revision.
  - **NEVER** submit code to QA that has compilation errors, broken tests, or failed migrations (`compilation_clean: false` is an immediate reject). Uncompilable contracts **MUST** be routed via Technical Contract Escalation directly to the Software Architect.
- **Inputs**:
  - `docs/adr/ADR-<feature_id>.md`
  - `docs/specs/COMP-SPEC-<feature_id>.md`
  - `handoffs/architect_to_dev_<feature_id>.json`
- **Outputs**:
  - TypeScript production source files (`src/**/*.ts`, `supabase/functions/**/*.ts`).
  - Database migration scripts (`supabase/migrations/*.sql`).
  - Automated test files (`tests/*.ts`).
  - `handoffs/dev_to_qa_<feature_id>.json` (validated against `schemas/dev_to_qa_handoff.schema.json`).
  - On Contract Defect: `docs/escalations/ESCALATION-<feature_id>.md` and `handoffs/dev_to_architect_escalation_<feature_id>.json`.
- **Quality Gate**:
  - Code compiles with 0 errors (`npx tsc --noEmit`).
  - Automated unit and service tests pass 100% (`unit_tests_passed == unit_tests_run`, `unit_tests_failed == 0`).
  - Handoff payload passes Draft-07 validation.

---

### Role 5: QA / Testing Engineer (API, RLS & Integration Testing)
- **Role Identifier**: `qa_testing_engineer`
- **Archetype / Category**: Independent Verification, API Integrity & Quality Gate Governance
- **Primary Objective**: Independently verify that the implementation completely satisfies all Acceptance Criteria (AC-xx) from the PRD and contracts from the Component Spec, through comprehensive automated testing of REST APIs, Supabase RLS security policies, and service integrations.
- **Key Responsibilities**:
  1. Establish a 1-to-1 traceability matrix mapping every PRD Acceptance Criterion (`AC-xx`) to at least one automated test method.
  2. Implement automated integration tests validating HTTP status codes, response DTO schemas, and business logic.
  3. Verify Supabase RLS data isolation: verify authenticated users cannot access or mutate records belonging to other users.
  4. Test external service mocking and edge cases (e.g. invalid tokens, rate limits, network timeouts).
  5. Generate comprehensive QA Report (`QA-REPORT-<feature_id>.md`) and issue formal quality gate verdict:
     - `PASS`: All ACs verified, zero test failures, zero blocker/critical issues.
     - `FAIL_REVISE`: One or more ACs failed or unverified, or defects detected.
  6. On `FAIL_REVISE`, author structured defect tickets in `qa_verdict_handoff.json` with reproduction steps, expected vs actual behavior, severity, and assigned `target_role_for_remediation`.
- **Strict Prohibitions (Negative Constraints)**:
  - **NEVER** modify production implementation code to force tests to pass.
  - **NEVER** issue a `PASS` verdict if any Acceptance Criterion is unverified, failing, or skipped.
  - **NEVER** omit reproduction steps or root-cause role targeting in defect tickets.
- **Inputs**:
  - `docs/prd/PRD-<feature_id>.md`
  - `docs/specs/COMP-SPEC-<feature_id>.md`
  - Production source code and developer test suites.
  - `handoffs/dev_to_qa_<feature_id>.json`
- **Outputs**:
  - Automated test suites (`tests/test_*.ts`, integration tests).
  - `docs/qa/QA-REPORT-<feature_id>.md` (conforming to `templates/qa-report-template.md`).
  - `handoffs/qa_verdict_<feature_id>.json` (validated against `schemas/qa_verdict_handoff.schema.json`).
- **Quality Gate**:
  - 100% of PRD Acceptance Criteria mapped and verified.
  - Zero test failures (`failed == 0` for `PASS`).
  - Handoff payload passes Draft-07 validation.

---

### Role 6: DevOps & Supabase Deployment Specialist
- **Role Identifier**: `devops_deployment_specialist`
- **Archetype / Category**: Infrastructure as Code, Remote Environment Synchronization & Automated Release
- **Primary Objective**: Manage remote database migrations, Edge Function deployments, multi-environment synchronization (development `pfbdokxsmmrhrltfsnox` vs production `rezviycyzlhxlmhlhdfr`), execute post-deployment smoke tests, emit deployment handoffs, and transition completed Jira issues to "Listo".
- **Key Responsibilities**:
  1. Ingest verified QA `PASS` handoff (`qa_verdict_handoff.json`).
  2. Audit migration status against target Supabase project (`python scripts/supabase_deployer.py --audit-only`).
  3. Execute database schema push (`npx supabase db push --linked`).
  4. Deploy and activate Edge Functions (`npx supabase functions deploy api --no-verify-jwt`).
  5. Execute automated smoke tests / health checks against the live environment.
  6. Emit machine-readable deployment handoff payload (`handoffs/deployment_<feature_id>.json` validated against `schemas/deployment_handoff.schema.json`).
  7. Transition the corresponding Jira issue to status `"Listo"` and append automated release notes comment.
- **Strict Prohibitions (Negative Constraints)**:
  - **NEVER** deploy to production (`rezviycyzlhxlmhlhdfr`) without explicit human approval and interactive confirmation.
  - **NEVER** execute unverified migrations without pre-deployment schema audit.
  - **NEVER** transition Jira tickets to `"Listo"` if remote smoke tests, database migrations, or function deployments fail.
- **Inputs**:
  - `handoffs/qa_verdict_<feature_id>.json` (with `verdict: "PASS"`)
  - `supabase/migrations/*.sql`
  - `supabase/functions/api/**`
- **Outputs**:
  - Remote database schema update in linked Supabase project.
  - Deployed and active remote Supabase Edge Functions.
  - `handoffs/deployment_<feature_id>.json` (validated against `schemas/deployment_handoff.schema.json`).
  - Jira ticket transitioned to `"Listo"` with release audit comment.
- **Quality Gate**:
  - Remote migrations applied cleanly with 0 pending.
  - Remote Edge Function status is `ACTIVE`.
  - Live smoke test / health check returns HTTP 200.
  - Handoff payload passes Draft-07 validation.

---

## 2. Chatter Elimination Protocol

To eliminate conversational ambiguity, vague progress announcements, and unverified transitions, all agent interactions are governed by an **Artifact-Driven State Machine**:

```
 ┌────────────────┐
 │ User Request   │
 └───────┬────────┘
         │
         ▼
 ┌────────────────────────┐
 │ Product Owner          │
 └───────┬────────────────┘
         │ Hand-off: po_to_architect_<id>.json + PRD-<id>.md
         │ Gating: Schema valid, Given/When/Then ACs, NFRs
         ▼
 ┌────────────────────────┐
 │ Software Architect     │◄────────────────────────────────────────┐
 └───────┬────────────────┘                                         │
         │ Hand-off: architect_to_dev_<id>.json + ADR / COMP-SPEC   │
         │ Gating: Schema valid, typed contracts, DTO schemas       │
         ▼                                                          │
 ┌────────────────────────┐                                         │
 │ Senior Backend Dev     │                                         │
 └───────┬────────────────┴─────────────────────────────────────────┤
         │                                                          │
         │ (Code Compiles & Tests Pass)                             │ (Uncompilable / Defective Contract)
         │ Hand-off: dev_to_qa_<id>.json                            │ Escalation: dev_to_architect_escalation_<id>.json
         │ Gating: Schema valid, tsc clean,                         │ + ESCALATION-<id>.md
         │         unit & service tests 100% pass                   │ Gating: Schema valid, cycle <= 3
         ▼                                                          │
 ┌────────────────────────┐                                         │
 │ QA / Testing Engineer  │                                         │
 └───────┬────────────────┘                                         │
         │ Hand-off: qa_verdict_<id>.json + QA-REPORT-<id>.md       │
         │ Gating: Schema valid, 100% AC coverage, zero failures    │
         │                                                          │
         ├──────────────────────────────────────────┐               │
         │ (PASS)                                   │ (FAIL_REVISE) │
         ▼                                          ▼               │
 ┌────────────────────────────────────────┐ ┌────────────────────────┐  │
 │ DevOps Deployment Specialist           │ │ Automated Remediation  ├──┘ (Architectural Flaw)
 └───────┬────────────────────────────────┘ │ Router                 │
         │ Hand-off: deployment_<id>.json   └───────────┬────────────┘
         │ Actions: db push, deploy fn,                 │
         │          remote smoke test                   │
         │ Gating: DB clean, fn ACTIVE, HTTP 200        │
         ▼                                              │
 ┌────────────────────────────────────────┐             │
 │ Release Delivery & Jira Close          │             │
 │ - Issue marked "Listo" in Jira Cloud   │             │
 │ - Release audit comment posted         │             │
 │ - Product Owner final signoff          │             │
 └────────────────────────────────────────┘             │
                   ┌────────────────────────────────────┴────────────┐
                   ▼                                                 ▼
       [Target: Senior Backend Dev]                         [Target: Product Owner]
       Implementation / API Bugs                            Ambiguous / Flawed Spec
```

### Protocol Rules:
1. **Schema Validation Before Dispatch**: No agent may dispatch to or trigger another agent without executing schema validation against the corresponding contract schema. If validation fails, the sender must self-correct immediately.
2. **Disk-Persisted Dual Artifacts**: Every transition requires:
   - A human-readable Markdown artifact (PRD, ADR, COMP-SPEC, QA-REPORT, ESCALATION).
   - A machine-readable JSON payload containing metadata, references, and verifiable assertions.
3. **Physical File Verification**: The receiving agent or orchestrator verifies that all referenced paths in the JSON payload (e.g., `prd_path`, `adr_path`, `qa_report_path`, `escalation_report_path`) exist physically on disk and have non-zero byte size.
4. **Zero Conversational Handshakes**: Messages between agents must not contain informal conversational queries ("Are you ready?", "What do you think?"). State transitions occur strictly upon writing verified payload files to disk.
5. **Non-Conversational Technical Escalation**: If a downstream agent detects that an upstream contract is technically defective, impossible to compile, lacks dependency coordinates, or violates platform invariants, communication occurs exclusively via typed escalation payloads (`dev_to_architect_escalation.schema.json`) accompanied by a structured Markdown report (`docs/escalations/ESCALATION-<id>.md`). Informal conversational queries, complaints, or undocumented local workarounds are strictly prohibited.

---

## 3. Automated Remediation Routing (Failure State Machine)

When the QA / Testing Engineer issues a `FAIL_REVISE` verdict, the automated remediation engine inspects the structured `issues` array in `qa_verdict_handoff.json` and deterministically routes the defect to the responsible upstream role:

| Defect Classification | Root Cause Description | Target Role for Remediation | Routing Action |
|---|---|---|---|
| **Implementation Bug** | Production code fails unit tests, throws uncaught runtime exception, fails state transition, or violates Composable rendering requirements. | `Senior Backend Developer` | Orchestrator dispatches defect ticket to Developer. Developer modifies implementation, re-verifies compilation and tests, and submits updated `dev_to_qa` payload. |
| **Architectural / Contract Flaw** | Component interface cannot satisfy state flow, missing required event action in sealed hierarchy, coroutine dispatcher cannot be injected, or modular boundary violation. | `Software Architect` | Orchestrator dispatches defect ticket to Architect. Architect updates ADR and Component Spec, and re-issues `architect_to_dev` payload to Developer. |
| **Requirement Gap / Ambiguity** | Acceptance Criterion is contradictory, physically impossible on Android, or business scenario was missed in the PRD. | `Product Owner` | Orchestrator dispatches defect ticket to Product Owner. PO updates PRD and re-issues `po_to_architect` payload. |

### 3.1 Pre-QA Technical Contract Escalation (Developer -> Architect)

When the Senior Backend Developer identifies that an architectural contract or component specification cannot be compiled or implemented without violating negative constraints, the Developer initiates a Pre-QA Technical Escalation:

| Escalation Category | Root Cause Description | Trigger Condition | Escalation Routing Action |
|---|---|---|---|
| **UNCOMPILABLE_INTERFACE** | Kotlin compiler error on contract definitions (e.g. invalid generics, unresolved platform classes, incompatible type bounds). | `kotlinc` emits error during compilation or contract stub verification. | Orchestrator dispatches `dev_to_architect_escalation` to Software Architect. Architect revises COMP-SPEC and re-issues `architect_to_dev` payload. |
| **DEPENDENCY_UNSATISFIED** | Contract relies on missing library coordinate or incompatible version. | Gradle dependency resolution failure or missing artifact. | Architect adds valid coordinate to `dependencies` array in `architect_to_dev_handoff` and updates ADR. |
| **UDF_CONTRACT_VIOLATION** | Contract forces Composable to mutate state directly or exposes mutable collections. | Static analysis / contract review against UDF principles. | Architect revises state/event model to preserve strict Unidirectional Data Flow. |
| **CONCURRENCY_MODEL_CONFLICT** | Contract forces blocking calls in composables or lacks dispatcher injection. | Coroutines/threading rule conflict. | Architect injects proper CoroutineDispatcher / CoroutineScope into contract. |
| **SPECIFICATION_DEFICIT** | PRD acceptance criterion requires an action or state variable omitted in the Component Spec. | Implementation gap against PRD AC-xx. | Architect adds required UIAction / UiState to Component Spec and re-issues handoff. |

### Escalation Safeguards:
- **Remediation Cycle Tracking**: Each Pre-QA escalation carries an explicit `remediation_cycle` (0..3) which increments with each round-trip between Developer and Architect.
- **Immediate Escalation Halt**: If `remediation_cycle` reaches 3 without contract stabilization, the Orchestrator halts execution immediately (`ESCALATION_HALT`) and alerts the Product Owner and human supervisor with the complete diagnostic audit trail.
- **Evidence Requirement**: An escalation payload must contain non-empty `contract_violations`, compiler diagnostic logs (or minimal reproduction code), and a concrete suggested contract diff. Vague or evidence-free escalations are automatically rejected.

### 3.2 Multi-Defect Remediation & Precedence Routing Protocol

When the QA / Testing Engineer issues a `FAIL_REVISE` verdict, defects are routed according to the following deterministic rules:

1. **Deterministic Upstream Precedence Hierarchy**:
   Defects belong to a strict dependency hierarchy reflecting the software lifecycle:
   ```
   Priority 1 (Highest): Product Owner       — Requirement Gaps, Contradictory ACs, Spec Ambiguities
         ↓
   Priority 2:           Software Architect  — Contract Flaws, Incompatible Interfaces, Dependency Issues
         ↓
   Priority 3 (Lowest):  Senior Backend Dev  — Implementation Bugs, Runtime Exceptions, Logic Errors
   ```
   *Rationale*: Downstream code is derivative of upstream architecture and requirements. Resolving an implementation bug while the underlying requirement or architectural contract is flawed produces throwaway work. Upstream defects MUST be remediated first.

2. **Single-Role Defect Ticket Routing**:
   If all issues in the `issues` array target the same role, `recipient.role` in `qa_verdict_handoff.json` may be set directly to that role (`"Senior Backend Developer"`, `"Software Architect"`, or `"Product Owner"`).

3. **Multi-Role Defect Ticket Routing**:
   If the `issues` array contains defects targeting two or more distinct roles (e.g., an architectural interface flaw and a developer implementation bug):
   - QA sets `recipient.role` to `"Remediation Router"` (or `"Automated Remediation Router"`), with `agent_id: "router"` or `"orchestrator"`.
   - The Automated Remediation Router analyzes the defect set and dispatches the remediation task to the **highest-precedence role** first.
   - Lower-precedence defects are preserved in the payload context. Once the upstream agent completes its revision (e.g., Architect emits revised `architect_to_dev`), the downstream agent (Developer) receives the updated contract along with the remaining implementation defects.

4. **Verdict PASS Recipient**:
   When `verdict` is `"PASS"`, `recipient.role` must be `"Product Owner"` for release signoff and final feature delivery.

### Remediation Safeguards:
- **Maximum Remediation Cycles**: The remediation loop is bounded by a configurable cycle limit (default: 3 iterations). Exceeding this limit triggers an immediate escalation halt (`ESCALATION_HALT`).
- **Defect Ticket Integrity**: Each defect ticket must include `issue_id`, `severity` (`BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`), `target_role_for_remediation`, `upstream_artifact_ref` (referencing `PRD-[ID]`, `COMP-SPEC-[ID]`, `ADR-[ID]`, or `Source File:Line`), `reproduction_steps` (ordered array of strings), `expected` result, and `actual` result.

---

## 4. Human-in-the-Loop (HITL) 3-Stage Ticket Lifecycle Protocol

To eliminate prompt clutter, prevent premature implementation code, and guarantee production safety, all agents adhere to a strict **Three-Stage Human-in-the-Loop Gate**:

```
[User Trigger: "Refina <TICKET_KEY>" / "Analiza <TICKET_KEY>"]
  │
  ▼
Stage 1: PO & Architecture Refinement (No Code Written)
  ├─ 1. Ingest Jira ticket: `python scripts/atlassian_bridge.py fetch <TICKET_KEY> --scaffold-openspec`
  ├─ 2. Product Owner & Architect formulate OpenSpec proposal & docs using canonical ID <TICKET_KEY>:
  │      - `docs/prd/PRD-<TICKET_KEY>.md`
  │      - `docs/adr/ADR-<TICKET_KEY>.md`
  │      - `docs/specs/COMP-SPEC-<TICKET_KEY>.md`
  │      - OpenSpec changeset in `openspec/changes/<TICKET_KEY>/`
  │      - Handoffs: `po_to_architect_<TICKET_KEY>.json` and `architect_to_dev_<TICKET_KEY>.json`
  ├─ 3. Publish refinement to Jira:
  │      `python scripts/atlassian_bridge.py refine <TICKET_KEY> openspec/changes/<TICKET_KEY>/proposal.md --status "In Review"`
  │      (or post structured proposal as a comment via `comment`)
  └─ 4. MANDATORY HALT & AWAIT APPROVAL:
         The agent presents the proposal summary in chat and STOPS without writing production code.

[User Trigger: "Aprobado" / "Implementa <TICKET_KEY>"]
  │
  ▼
Stage 2: Implementation, Verification & Development Deployment
  ├─ 1. Move ticket to execution: `python scripts/atlassian_bridge.py transition <TICKET_KEY> "En curso"`
  ├─ 2. Senior Backend Developer writes production code & DB migrations:
  │      - Create migration via `npx supabase migration new <name>`
  │      - Implement services in `src/services/`
  │      - Implement API routes in `src/index.ts` and mirror in `supabase/functions/api/index.ts`
  │      - Write tests in `tests/test_*.ts` and verify `npm run lint` (`npx tsc --noEmit`)
  ├─ 3. QA Engineer executes 100% test verification: `npm test` -> Verdict PASS.
  │      - Author `docs/qa/QA-REPORT-<TICKET_KEY>.md`
  │      - Emit `handoffs/qa_verdict_<TICKET_KEY>.json`
  ├─ 4. Quality Gate passes: `python scripts/openspec_cli.py archive <TICKET_KEY>`
  ├─ 5. DevOps Deployment Specialist executes development deployment & verification:
  │      `python scripts/supabase_deployer.py --env development --jira-key <TICKET_KEY>`
  │      - Ensures Supabase CLI is linked to development (`pfbdokxsmmrhrltfsnox`)
  │      - Verifies route parity between Node and Deno Edge Functions
  │      - Audits and pushes pending DB migrations (`npx supabase db push`)
  │      - Deploys and activates Edge Functions (`npx supabase functions deploy api --no-verify-jwt`)
  │      - Performs remote smoke test / health check
  │      - Generates `handoffs/deployment_<TICKET_KEY>.json`
  └─ 6. Automated Jira Closure:
         - Ticket transitioned to "Listo" in Jira Cloud
         - Release notes and deployment audit comment posted automatically

[User Trigger: "Promueve <TICKET_KEY> a producción"]
  │
  ▼
Stage 3: Production Promotion (Human-Gated Release)
  ├─ 1. Prerequisite Check: Ensure ticket is in status "Listo" and verified in development.
  ├─ 2. Interactive Human Confirmation: Explicit operator confirmation required.
  ├─ 3. DevOps Deployment Specialist executes production deployment:
  │      `python scripts/supabase_deployer.py --env production --jira-key <TICKET_KEY>`
  │      - Switches Supabase CLI link to production (`rezviycyzlhxlmhlhdfr`)
  │      - Audits and applies pending DB migrations
  │      - Deploys and activates Edge Functions in production
  │      - Performs live production smoke test
  │      - Generates `handoffs/deployment_<TICKET_KEY>_prod.json`
  └─ 4. Jira Audit Trail:
         - Appends production release notes comment to Jira ticket
```

### Key Operational Rules:
1. **Minimalist Conversational Triggers**:
   - The user only needs to provide simple, 1-line commands: `"Refina KILOMENOS-10"` for Stage 1, `"Aprobado"` for Stage 2, and `"Promueve KILOMENOS-10 a producción"` for Stage 3.
   - Long, prescriptive instructional prompts are completely discouraged; agents autonomously execute the lifecycle steps.
2. **Canonical Universal Identifier**:
   - Always use the Jira ticket key (`KILOMENOS-X`) directly as the canonical identifier across all files: `PRD-<KEY>.md`, `COMP-SPEC-<KEY>.md`, `QA-REPORT-<KEY>.md`, `openspec/changes/<KEY>/`, and `handoffs/*_<KEY>.json`.
3. **Zero Code Before Stage 1 Sign-Off**:
   - Under NO circumstances may an agent create, edit, or delete production application files during Stage 1.
   - Stage 1 outputs are strictly limited to Jira updates (`refine`/`comment`) and OpenSpec markdown artifacts (`proposal.md`, `design.md`, `specs/delta_spec.md`).
4. **Standardized Migration Creation**:
   - Database migrations must be generated via `npx supabase migration new <name>` to ensure timestamp accuracy and prevent chronological collisions.
5. **Route Parity Invariant**:
   - Every versioned API route (`/v1/...`) exposed in `src/index.ts` must be mirrored in `supabase/functions/api/index.ts` before QA signoff and deployment.
6. **Audit Trail Synchronization**:
   - Every human decision, specification approval, and deployment record is mirrored directly into the team's Jira ticket for full transparency.

---

## 5. Kilomenos Backend Architecture Reference (Hono, Supabase & Deno)

All backend modules, services, and endpoints in Kilomenos Backend follow a clean, type-safe, layered architecture:

### 5.1 System Topology & Stack
- **HTTP Server Runtime**: Node.js 20+ with TypeScript and [Hono v4](https://hono.dev/) (`@hono/node-server`).
- **Edge Runtime**: Supabase Edge Functions on Deno runtime (`supabase/functions/api/index.ts`).
- **Persistence Layer**: Supabase PostgreSQL with strict **Row Level Security (RLS)**.
- **Push Messaging**: Firebase Cloud Messaging (**FCM HTTP v1**) with automatic dead token pruning.
- **Store Sync**: Google Play Real-Time Developer Notifications (**RTDN**) webhook.

### 5.2 Router & Middleware Pattern (`src/index.ts`)
- **Authentication & Tenant Scoping**:
  ```typescript
  import { Hono } from 'hono';
  import { withSupabase } from './middleware/auth';

  const app = new Hono();

  // User-scoped route (authenticated via Supabase JWT)
  app.get('/v1/notifications', withSupabase({ auth: 'user' }), async (c) => {
    const user = c.get('user');
    const supabase = c.get('supabase');
    // Handler logic...
  });

  // Entitlement Protection Guard
  const verifyPremiumAccess = async (c: Context, next: Next) => {
    const user = c.get('user');
    const entitlements = await resolveUserEntitlements(user.id);
    if (!entitlements.isPremium && !entitlements.hasActiveTrial) {
      return c.json({ error: 'PREMIUM_REQUIRED', message: 'Premium subscription or active trial required' }, 403);
    }
    await next();
  };
  ```

### 5.3 Service Layer Pattern (`src/services/*Service.ts`)
- Business operations are fully isolated in typed services with clean domain inputs and outputs:
  ```typescript
  export interface SyncBatchResult {
    synced: number;
    failed: number;
  }

  export async function syncBatchNotifications(
    userId: string,
    notifications: NotificationSyncItem[],
    client: SupabaseClient
  ): Promise<SyncBatchResult> {
    // Idempotent upsert via client-generated UUID
    const { error } = await client
      .from('user_notifications')
      .upsert(records, { onConflict: 'id' });
    if (error) throw error;
    return { synced: records.length, failed: 0 };
  }
  ```

### 5.4 Database Migrations & Row Level Security (`supabase/migrations/*.sql`)
- Every migration must be **transactional** (`BEGIN ... COMMIT`) and backward-compatible:
  ```sql
  BEGIN;

  CREATE TABLE IF NOT EXISTS public.user_notifications (
      id UUID PRIMARY KEY,
      user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
      origin VARCHAR(10) NOT NULL CHECK (origin IN ('LOCAL', 'REMOTE')),
      topic VARCHAR(50) NOT NULL,
      title TEXT NOT NULL,
      body TEXT NOT NULL,
      data JSONB DEFAULT '{}'::jsonb,
      deep_link TEXT,
      is_read BOOLEAN NOT NULL DEFAULT FALSE,
      read_at TIMESTAMPTZ,
      created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
  );

  -- Mandatory RLS Isolation
  ALTER TABLE public.user_notifications ENABLE ROW LEVEL SECURITY;

  CREATE POLICY "Users can only read own notifications"
      ON public.user_notifications FOR SELECT
      USING (auth.uid() = user_id);

  CREATE POLICY "Users can only insert own notifications"
      ON public.user_notifications FOR INSERT
      WITH CHECK (auth.uid() = user_id);

  COMMIT;
  ```

### 5.5 Remote Deployment & Automated Release
- Managed by `Role 5: DevOps & Supabase Deployment Specialist` via `scripts/supabase_deployer.py`.
- Automated flow: Schema push (`npx supabase db push --linked`) $\rightarrow$ Function deploy (`npx supabase functions deploy api --no-verify-jwt`) $\rightarrow$ Live smoke test $\rightarrow$ Jira ticket transitioned to `"Listo"`.
