# AGENTS.md — Multi-Agent Lifecycle Role Definitions & Protocols

Index and state machine charter for the Agentic Ecosystem across platforms. Platform-specific roles reside in `packs/<pack>/roles/*.md`.

---

## 1. Primary Lifecycle Roles

| Role Identifier | Title | Platform | Specification Reference |
|---|---|---|---|
| `product_owner` | Product Owner (PO) | Universal | See §1.1 below |
| `solutions_architect` | Solutions Architect | Universal / Cross-Platform | See §1.2 below |
| `ecosystem_optimizer` | Ecosystem Optimizer & AgentOps | Universal | See §1.3 below |
| `software_architect` | Mobile Software Architect | Android | [packs/android/roles/software_architect.md](packs/android/roles/software_architect.md) |
| `senior_android_developer` | Senior Android Developer | Android | [packs/android/roles/senior_android_developer.md](packs/android/roles/senior_android_developer.md) |
| `qa_testing_engineer` | Android QA / Testing Engineer | Android | [packs/android/roles/qa_testing_engineer.md](packs/android/roles/qa_testing_engineer.md) |
| `backend_architect` | Backend Software Architect | Backend | [packs/backend/roles/backend_architect.md](packs/backend/roles/backend_architect.md) |
| `web_architect` | Web Software Architect | Web | [packs/web/roles/web_architect.md](packs/web/roles/web_architect.md) |

### 1.1 Product Owner (PO)
- **Role Identifier**: `product_owner`
- **Objective**: Translate business requirements into unambiguous PRDs and valid handoff payloads.
- **Key Responsibilities**:
  1. Author numbered Acceptance Criteria (AC-01, AC-02, ...) in strict **Given / When / Then** format.
  2. Define Functional Requirements (`FR-xx`) and Non-Functional Requirements (NFRs).
  3. Declare Out-of-Scope boundaries.
  4. Emit handoff payload conforming to `core/schemas/po_to_architect_handoff.schema.json`.
- **Negative Constraints**: NEVER write implementation code. NEVER dictate internal technical architecture or class names.

### 1.2 Solutions Architect (Macro-Architecture & Cross-Platform Integration)
- **Role Identifier**: `solutions_architect`
- **Objective**: Define cross-platform technical strategy, shared contracts, and end-to-end integration flows across Mobile, Backend, and Web.
- **Key Responsibilities**:
  1. Author Global System Architecture ADRs (`docs/adr/ADR-SOL-<id>.md`).
  2. Define immutable cross-platform communication contracts (`core/contracts/`).
  3. Ensure security boundaries (TLS, JWT lifetimes, API scopes).
- **Negative Constraints**: NEVER dictate internal framework syntax (Compose UI hoisting, Deno internal handler syntax).

### 1.3 Ecosystem Optimizer & AgentOps Specialist
- **Role Identifier**: `ecosystem_optimizer`
- **Objective**: Maintain ecosystem health, token budgets, domain purity, and schema integrity.
- **Key Responsibilities**:
  1. Audit context budgets via `audit_context_budget.py` (`python scripts/workflow.py audit`).
  2. Enforce platform domain purity via `lint_platform_leakage.py`.
  3. Validate Draft-07 schemas and hub-spoke sync (`.agentic.lock`).
- **Negative Constraints**: NEVER introduce conversational prose that inflates prompt tokens. Keep platform rules strictly isolated.

---

## 2. Chatter Elimination Protocol

All agent transitions are governed by an **Artifact-Driven State Machine**:

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
         │ Gate: Draft-07 schema valid, ACs Given/When/Then
         ▼
 ┌────────────────────────┐
 │ Software Architect     │◄────────────────────────────────────────┐
 └───────┬────────────────┘                                         │
         │ Hand-off: architect_to_dev_<id>.json + ADR / COMP-SPEC   │
         │ Gate: Draft-07 schema valid, immutable state, UDF        │
         ▼                                                          │
 ┌────────────────────────┐                                         │
 │ Senior Developer       │                                         │
 └───────┬────────────────┴─────────────────────────────────────────┤
         │                                                          │
         │ (Code Compiles & Tests Pass)                             │ (Uncompilable / Defective Contract)
         │ Hand-off: dev_to_qa_<id>.json                            │ Escalation: dev_to_architect_escalation_<id>.json
         │ Gate: compilation_clean == true, unit tests 100%         │ Gate: Draft-07 schema valid, cycle <= 3
         ▼                                                          │
 ┌────────────────────────┐                                         │
 │ QA / Testing Engineer  │                                         │
 └───────┬────────────────┘                                         │
         │ Hand-off: qa_verdict_<id>.json + QA-REPORT-<id>.md       │
         │ Gate: 100% AC coverage verified, 0 test failures         │
         │                                                          │
         ├──────────────────────────────────────────┐               │
         │ (PASS)                                   │ (FAIL_REVISE) │
         ▼                                          ▼               │
 ┌────────────────────────┐             ┌────────────────────────┐  │
 │ Release Delivery       │             │ Automated Remediation  ├──┘ (Architectural Flaw)
 │ (Product Owner Signoff)│             │ Router                 │
 └────────────────────────┘             └───────────┬────────────┘
                                                    │
                   ┌────────────────────────────────┴────────────────┐
                   ▼                                                 ▼
       [Target: Senior Developer]                           [Target: Product Owner]
       Implementation Bugs                                  Ambiguous / Flawed Spec
```

### Protocol Rules:
1. **Schema Validation Before Dispatch**: No agent dispatches without passing Draft-07 schema validation against the contract.
2. **Dual Artifacts**: Every transition requires a human-readable Markdown artifact and a machine-readable JSON payload.
3. **Physical File Verification**: All referenced artifact paths in JSON payloads must physically exist on disk with non-zero bytes.
4. **Zero Conversational Handshakes**: Transitions occur strictly through persisted disk payloads, never through chat questions.
5. **Non-Conversational Technical Escalation**: Downstream agents blocked by uncompilable contracts emit `dev_to_architect_escalation.schema.json` directly to the Architect.

---

## 3. Automated Remediation Routing (Failure State Machine)

On `FAIL_REVISE`, defects in `qa_verdict_handoff.json` are routed deterministically:

| Defect Classification | Root Cause Description | Target Role | Routing Action |
|---|---|---|---|
| **Implementation Bug** | Production code fails unit tests, throws runtime exception, fails state transition. | `Senior Android Developer` | Developer modifies implementation, verifies tests, re-submits `dev_to_qa`. |
| **Architectural / Contract Flaw** | Component interface cannot satisfy state flow, missing action, concurrency conflict. | `Software Architect` | Architect updates ADR/COMP-SPEC, re-issues `architect_to_dev`. |
| **Requirement Gap / Ambiguity** | Acceptance Criterion contradictory, impossible, or scenario missed in PRD. | `Product Owner` | PO updates PRD, re-issues `po_to_architect`. |

### Precedence Hierarchy:
```
Priority 1 (Highest): Product Owner       — Requirement Gaps, Contradictory ACs
      ↓
Priority 2:           Software Architect  — Contract Flaws, Incompatible Interfaces
      ↓
Priority 3 (Lowest):  Senior Developer    — Implementation Bugs, Logic Errors
```
Upstream defects are remediated first. Multi-role defects route to `"Remediation Router"`, which dispatches to highest priority first. Maximum remediation loop limit is 3 cycles.

---

## 4. Human-in-the-Loop (HITL) 2-Stage Lifecycle

```
[User: "Refina <KEY>"]  ──► Stage 1 (PO & Arch): Ingest Jira, formulate OpenSpec, HALT & AWAIT APPROVAL
[User: "Aprobado"]      ──► Stage 2 (Dev & QA): Implement code, 100% tests, archive spec, finalize Jira
```
- **Zero Ghost Code**: Never write unrequested code.
- **Zero Implementation Before Stage 1 Sign-Off**: No production code files created or modified during Stage 1.
