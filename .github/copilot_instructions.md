# GitHub Copilot & AI Developer Instructions

You are assisting developers working in an enterprise **Specification-Driven Development (SDD)** ecosystem governed by `AGENTS.md`.

## 1. Golden Rules of Development

1. **Spec-First (No Spec, No Code)**:
   - NEVER generate, propose, or write code without an approved upstream specification (`openspec/changes/` or `templates/prd-template.md`).
   - All code changes must trace directly to explicit functional requirements (`FR-xx`) and acceptance criteria (`AC-xx`).

2. **HITL 2-Stage Gate (Human-In-The-Loop)**:
   - **Stage 1 (Specification & Technical Design)**: PO and Architect align on requirements, failure consequences, and interface contracts.
   - **HALT GATE**: If there are unresolved open questions (`Dudas Abiertas Bloqueantes`), **STOP IMMEDIATELY**. You must prompt the developer/stakeholder for clarification before proceeding.
   - **Stage 2 (Implementation & Verification)**: Only write code after Stage 1 is fully approved.

3. **Zero Ghost Code (Anti-Scope Creep)**:
   - Strictly prohibit adding unrequested endpoints, hidden parameters, undeclared UI components, or phantom behaviors.
   - Implement ONLY what is documented in the approved specification.

4. **Negative Testing for Business Rules (`BR-xx`)**:
   - Every business rule must define an explicit failure consequence (`BR-xx`).
   - Every failure branch must have automated negative test coverage (HTTP 4xx/5xx, localized error UI, fallback state).

## 2. Platform Discipline Profile: ALL

### Platform Guardrails: Full Multi-Disciplinary System
- Adhere to the specific platform boundaries (Android, Backend, Web) depending on the target module.
- Refer to `AGENTS.md` for role boundaries, schemas, and architectural guidelines.

## 3. Workflow References

- Role Specifications & Technical Guardrails: `AGENTS.md` (Section 5)
- Living Specifications: `openspec/specs/`
- Active Changes & Proposals: `openspec/changes/`
- Handoff & Validation Schemas: `schemas/`
