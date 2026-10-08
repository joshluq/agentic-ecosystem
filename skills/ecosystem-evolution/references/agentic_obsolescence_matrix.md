# Agentic Obsolescence Matrix — Modern vs. Legacy Patterns

This matrix serves as the evaluation rubric when auditing the ecosystem for architectural drift and outdated agentic practices.

---

## 1. Pattern Comparison Rubric

| Domain | Legacy / Anti-Pattern (OBSOLETE) | Modern Agentic Standard (CURRENT) | Severity |
|---|---|---|---|
| **Multi-Agent Coordination** | Conversational chat loops ("What do you think, Architect?") | **Artifact-Driven State Machine** with JSON schema handoffs on disk | Critical |
| **Context Loading** | Injecting entire manuals into the system prompt at turn 0 | **3-Tier Progressive Disclosure** (Discovery $\rightarrow$ Activation $\rightarrow$ Reference) | High |
| **Tool Execution** | Describing CLI execution in natural language prompts | **Deterministic Helper Scripts** (`scripts/`) with strict exit codes | High |
| **Data Contracts** | Ad-hoc Markdown summaries passed between agents | **Typed Schemas (Draft-07)** validated prior to dispatch | Critical |
| **Prompt Tone & Structure** | Conversational prose, polite preambles, and conversational fillers | **Imperative Checklists**, bulleted protocols, and zero chatter | Medium |
| **Platform Boundaries** | Single monolithic instruction file containing all technologies | **Domain-Isolated Packs** with automated leakage linters | High |
| **Specification Lifecycles** | Writing code directly from raw user prompts ("Ghost Code") | **Spec-First (SDD)** with Human-in-the-Loop (HITL) approval gates | Critical |
| **Prompt Caching** | Dynamically altering early lines of prompts in every turn | **Prefix Stabilization** (invariant rules first, dynamic context last) | Medium |

---

## 2. Evaluation Criteria

When auditing an ecosystem component:
- **Green (Modern)**: Conforms strictly to modern patterns. High cache efficiency, deterministic handoffs.
- **Yellow (Advisory)**: Functional but sub-optimal (e.g. `SKILL.md` approaching line limit, minor redundant instructions).
- **Red (Deprecation Candidate)**: Legacy anti-pattern present (unstructured transitions, conversational chatter, platform leakage).
