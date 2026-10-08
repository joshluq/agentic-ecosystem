# Authoritative Sources & Industry References for Agentic Development

This reference indexes canonical documentation, specifications, and whitepapers that define the state of the art in agentic software engineering.

---

## 1. Google Antigravity Platform & Agent Architecture
- **Antigravity Customization System (`agy-customizations`)**:
  - Progressive disclosure lifecycle (discovery tier vs activation tier vs deep reference tier).
  - Rules vs Skills vs Plugins vs Hooks precedence hierarchy.
  - Workspace scoping (`.agents/skills/`, `.agents/rules/`).
- **Antigravity SDK & Orchestration**:
  - Deterministic subagent dispatch (`invoke_subagent`).
  - Structured output schemas and tool boundary sandboxing.

---

## 2. Model Context Protocol (MCP) Standards
- **Specification Source**: [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- **Core Tenets**:
  - Decoupled server-client architecture for agent tools and resources.
  - Strongly typed JSON-RPC 2.0 schemas for tool inputs and outputs.
  - Separation between dynamic tools (active execution) and resources (passive context).

---

## 3. Context Engineering & Token Economy
- **Anthropic Research & Guides**:
  - *Context Engineering: Techniques for Effective Multi-Agent Systems* (prefix stabilization, KV-cache reusability, token budgets).
  - *Building Effective Agents* (Router, Orchestrator-Workers, Evaluator-Optimizer architectures).
- **Google DeepMind Agentic Principles**:
  - Strict minimization of conversational fluff ("chatter elimination").
  - Deterministic verification gates over conversational consensus.
  - Prefix-stable prompt structuring to maximize prompt cache hits.

---

## 4. Specification-Driven Development (SDD) & Contract Governance
- **OpenSpec Standard**:
  - Living specifications (`openspec/specs/`) vs active delta proposals (`openspec/changes/`).
  - Traceability from Business Rules (`BR-xx`) and Functional Requirements (`FR-xx`) to Acceptance Criteria (`AC-xx`).
- **JSON Schema (Draft-07 / 2020-12)**:
  - Machine-readable handoff contracts for agent-to-agent transitions.
  - Strict validation before downstream agent dispatch.
