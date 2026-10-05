# Project: Kilomenos Backend Lifecycle Ecosystem

## Architecture
Kilomenos Backend is a high-performance, type-safe backend platform and multi-agent lifecycle governance ecosystem supporting the KmSafe mobility application. Built on **Node.js 20+, TypeScript, and Hono**, it integrates tightly with **Supabase (PostgreSQL with Row Level Security)**, **Supabase Edge Functions (Deno)**, **Google Play Billing (RTDN)**, **Firebase Cloud Messaging (FCM HTTP v1)**, and **Atlassian Jira Cloud**.

### Core Components
1. **Agent Roles and Contract Handoffs (`AGENTS.md`, `templates/`, `schemas/`)**:
   - Primary lifecycle roles: Product Owner, Backend Software Architect, Senior Backend Developer, QA/Testing Engineer, DevOps & Supabase Deployment Specialist.
   - Standardized document templates (PRD, ADR, Component Spec, QA Report).
   - Strict Draft-07 JSON Schemas governing machine-readable transition payloads between roles, eliminating informal unstructured chatter.
2. **Backend API & Edge Runtime (`src/`, `supabase/functions/api/`)**:
   - Ultra-fast REST APIs in Hono with Zod input validation, JWT auth middleware, and entitlement protection guards (FREE vs PREMIUM/TRIAL).
   - Serverless Edge Functions in Deno (`supabase/functions/api/index.ts`) for distributed cloud execution.
3. **Database & Row Level Security (`supabase/migrations/`)**:
   - PostgreSQL relational schemas with strict Row Level Security (RLS) guaranteeing tenant isolation (`auth.uid() = user_id`).
   - Transactional database migrations (`BEGIN ... COMMIT`) maintaining backward compatibility.
4. **Cloud Integrations (FCM & Google Play RTDN)**:
   - Modern FCM HTTP v1 notification dispatcher with OAuth2 token caching and automatic dead-token pruning.
   - Google Play RTDN Pub/Sub webhook for subscription lifecycle synchronization.
5. **Supabase Automated Deployment Engine (`scripts/supabase_deployer.py`)**:
   - Automated multi-environment deployment (development `pfbdokxsmmrhrltfsnox` vs production `rezviycyzlhxlmhlhdfr`).
   - Automated migration audit (`supabase db push`), Edge Function deployment, remote smoke testing, and Jira issue transition to "Listo".
6. **Self-Contained Verification Suite (`scripts/verify_ecosystem.py`, `tests/`)**:
   - Zero-external-dependency Draft-07 schema validator and automated test suites verifying contracts, skills, and backend services.

## Feature Inventory
| # | Feature | Description | Status |
|---|---------|-------------|--------|
| 1 | Role Definitions | Comprehensive AGENTS.md for PO, Architect, Backend Dev, QA, DevOps | ACTIVE |
| 2 | PRD Template | Standardized backend PRD template with ACs and NFRs | ACTIVE |
| 3 | ADR Template | Architecture Decision Record template with backend & cloud specifics | ACTIVE |
| 4 | Component Spec Template | Route, DTOs, SQL schemas, RLS policies, and service contracts | ACTIVE |
| 5 | QA Report Template | API verification matrix, RLS tests, HTTP status codes, tsc clean | ACTIVE |
| 6 | PO->Architect Schema | JSON Schema enforcing strict typing for PO handoffs | ACTIVE |
| 7 | Architect->Dev Schema | JSON Schema enforcing backend architectural contracts and DTOs | ACTIVE |
| 8 | Dev->QA Schema | JSON Schema enforcing compilation, unit/service tests, and manifests | ACTIVE |
| 9 | QA Verdict Schema | JSON Schema enforcing quality gate verdicts and defect routing | ACTIVE |
| 10 | Deployment Schema | JSON Schema enforcing DevOps deployment handoff payloads | ACTIVE |
| 11 | Automated Deployer | CLI deployer for Supabase DB push, functions, smoke tests, Jira close | ACTIVE |
| 12 | Jira Cloud Integration | Bidirectional Atlassian bridge for tickets, status, and comments | ACTIVE |
| 13 | FCM HTTP v1 Service | Push dispatcher with token pruning and remote notification recording | ACTIVE |
| 14 | Notification API (FEAT-009) | Local-First sync, pagination, unread counters, and RLS security | COMPLETE |
| 15 | Subscriptions & RTDN | Google Play RTDN webhook, trial management, and entitlement guards | ACTIVE |

## Interface Contracts
### Product Owner ↔ Software Architect
- Input: Feature request, business problem statement
- Output: `docs/prd/PRD-<id>.md` (PRD template), `handoffs/po_to_architect_<id>.json`
- Schema: `schemas/po_to_architect_handoff.schema.json`

### Software Architect ↔ Senior Backend Developer
- Input: `docs/prd/PRD-<id>.md`, `handoffs/po_to_architect_<id>.json`
- Output: `docs/adr/ADR-<id>.md`, `docs/specs/COMP-SPEC-<id>.md`, `handoffs/architect_to_dev_<id>.json`
- Schema: `schemas/architect_to_dev_handoff.schema.json`

### Senior Backend Developer ↔ QA / Testing Engineer
- Input: `docs/adr/ADR-<id>.md`, `docs/specs/COMP-SPEC-<id>.md`, `handoffs/architect_to_dev_<id>.json`
- Output: TypeScript source, SQL migrations, test files, `handoffs/dev_to_qa_<id>.json`
- Schema: `schemas/dev_to_qa_handoff.schema.json`

### QA / Testing Engineer ↔ DevOps Specialist / PO
- Input: Production code, migration scripts, test suites, `handoffs/dev_to_qa_<id>.json`
- Output: Integration tests, `docs/qa/QA-REPORT-<id>.md`, `handoffs/qa_verdict_<id>.json`
- Schema: `schemas/qa_verdict_handoff.schema.json`

### DevOps Deployment Specialist ↔ Jira Release Delivery
- Input: `handoffs/qa_verdict_<id>.json` (PASS), `supabase/migrations/*.sql`, Edge Functions
- Output: Database push, function deploy, smoke test, `handoffs/deployment_<id>.json`, Jira "Listo"
- Schema: `schemas/deployment_handoff.schema.json`

## Code Layout
```
kilomenos-backend/
├── AGENTS.md                                 # Primary lifecycle role definitions & protocols
├── PROJECT.md                                # Master project architecture & feature inventory
├── README.md                                 # Backend architecture, setup & API catalog
├── package.json                              # Node.js dependencies (Hono, Supabase, TypeScript)
├── tsconfig.json                             # TypeScript compiler configuration
├── src/                                      # Backend production application source
│   ├── index.ts                              # Hono REST API router & middleware
│   ├── middleware/auth.ts                    # Supabase JWT authentication middleware
│   └── services/                             # Core backend domain services
│       ├── fcmService.ts                     # Firebase Cloud Messaging HTTP v1 dispatcher
│       ├── notificationService.ts            # User notifications CRUD & Local-First sync
│       └── subscriptionService.ts            # Entitlements & Google Play RTDN handling
├── supabase/                                 # Supabase infrastructure as code
│   ├── config.toml                           # Supabase CLI project configuration
│   ├── migrations/                           # Transactional PostgreSQL migrations with RLS
│   └── functions/api/index.ts                # Serverless Edge Function router (Deno runtime)
├── templates/                                # Standardized markdown document templates
│   ├── prd-template.md                       # Product Requirements Document template
│   ├── adr-template.md                       # Architecture Decision Record template
│   ├── component-spec-template.md            # Component & API Specification template
│   ├── qa-report-template.md                 # QA Quality Gate Report template
│   └── contract-escalation-template.md       # Pre-QA Technical Escalation template
├── schemas/                                  # Machine-readable Draft-07 JSON Schema contracts
│   ├── po_to_architect_handoff.schema.json   # PO -> Architect transition contract
│   ├── architect_to_dev_handoff.schema.json  # Architect -> Dev transition contract
│   ├── dev_to_qa_handoff.schema.json         # Dev -> QA transition contract
│   ├── qa_verdict_handoff.schema.json        # QA -> DevOps/PO transition contract
│   ├── dev_to_architect_escalation.schema.json # Pre-QA Escalation contract
│   └── deployment_handoff.schema.json        # DevOps Deployment transition contract
├── scripts/                                  # Automation CLI tools & deployment engines
│   ├── atlassian_bridge.py                   # Jira Cloud & Confluence bidirectional bridge
│   ├── supabase_deployer.py                  # Supabase automated migration & deploy engine
│   ├── schema_validator.py                   # Self-contained zero-dependency JSON Schema validator
│   ├── openspec_cli.py                       # Spec-Driven Development CLI orchestrator
│   └── verify_ecosystem.py                   # Master ecosystem verification runner
├── openspec/                                 # Living specifications & active changesets
│   ├── changes/                              # Active and archived feature changesets
│   └── specs/                                # Canonical system and contract specifications
└── tests/                                    # Automated test suites
    ├── test_notifications.ts                 # Notifications API integration tests
    ├── test_fcm_service.ts                   # FCM dispatcher tests
    ├── test_contracts.py                     # Draft-07 schema validation test suite
    ├── test_skills.py                        # Antigravity skill structure & frontmatter tests
    └── test_scripts.py                       # Python CLI automation tests
```
