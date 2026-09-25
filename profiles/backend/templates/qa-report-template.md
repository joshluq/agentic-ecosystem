# QA Quality Gate Report: [FEATURE_NAME]

**Feature ID**: [FEAT-XXX]  
**Evaluation Date**: YYYY-MM-DDTHH:MM:SSZ  
**QA Lead**: QA / Testing Engineer  
**Upstream Dev Handoff Ref**: HANDOFF-DEV-QA-[ID]  
**Final Quality Gate Verdict**: [PASS | FAIL_REVISE]  

---

## 1. Test Execution Summary & Quality Metrics

| Quality Metric | Measured Value | Threshold / Target | Status |
|---|---|---|---|
| Total Automated Tests Executed | [Count] | >= 1 | PASS / FAIL |
| Automated Tests Passed | [Count] | 100% of Executed | PASS / FAIL |
| Automated Tests Failed | [0] | 0 | PASS / FAIL |
| Tests Skipped | [0] | 0 | PASS / FAIL |
| ViewModel & Domain Line Coverage | [XX.X%] | >= 80.0% | PASS / FAIL |
| Branch Coverage | [XX.X%] | >= 75.0% | PASS / FAIL |
| Compilation & Static Analysis Clean | [true / false] | true (zero errors) | PASS / FAIL |

---

## 2. Acceptance Criteria (AC) 1-to-1 Traceability Matrix

Every Acceptance Criterion defined in the upstream PRD (`AC-xx`) must map directly to at least one passing automated test case.

| PRD AC ID | Scenario Title & Requirement | Verifying Test Method / File | Verification Mechanism | Status | Notes |
|---|---|---|---|---|---|
| **AC-01** | [Scenario Title from PRD] | `tests/test_[feature].ts:test_AC01` | HTTP POST & DB assertion | PASS / FAIL | Record persisted cleanly |
| **AC-02** | [Scenario Title from PRD] | `tests/test_[feature].ts:test_AC02` | Guard assertion (403 Forbidden) | PASS / FAIL | Unauthorized user blocked |
| **AC-03** | [Scenario Title from PRD] | `tests/test_[feature].ts:test_AC03` | RLS cross-tenant query assertion | PASS / FAIL | Multi-tenant isolation verified |

---

## 3. API Contracts, RLS & Multi-Tenant Security Inspection

Automated verification of REST endpoints and Supabase PostgreSQL security guidelines:

- **Row Level Security (RLS) Tenant Isolation**:
  - Authenticated user A cannot read or mutate records of user B: `PASS`
  - Unauthenticated requests rejected with HTTP 401: `PASS`
  - `service_role` operations scoped to privileged background routines only: `PASS`
- **Entitlement & Subscription Guards**:
  - FREE tier users blocked from premium endpoints with HTTP 403 `PREMIUM_REQUIRED`: `PASS`
  - Active trial and active subscription access permitted: `PASS`
- **Idempotency & Concurrency**:
  - Re-sending batch sync with identical UUIDs updates existing records without duplicate primary key error: `PASS`
- **TypeScript Static Verification**:
  - Zero TypeScript compiler diagnostics (`npx tsc --noEmit`): `PASS`

---

## 4. Structured Defect Tickets (Required for FAIL_REVISE)

If the quality gate verdict is `FAIL_REVISE`, each failure must be formulated as a structured remediation ticket below:

### Defect 1: [Short Descriptive Title of Issue]
- **Issue ID**: DEF-01
- **Severity**: BLOCKER | CRITICAL | MAJOR | MINOR
- **Target Role for Remediation**: Senior Android Developer | Software Architect | Product Owner
- **Upstream Artifact Ref**: `COMP-SPEC-[ID]` | `PRD-[ID]` | `Source File:Line`
- **Reproduction Steps**:
  1. Initialize component in state X
  2. Dispatch action Y with payload Z
  3. Observe system output
- **Expected Result**: System maintains valid UI state and displays localized feedback
- **Actual Result**: System throws unexpected exception or enters invalid state
