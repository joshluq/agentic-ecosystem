# Token Economy & Budgeting Guidelines for Antigravity Skills

Maintaining context budget hygiene is vital for keeping multi-agent ecosystems fast, responsive, and free of hallucination drift.

---

## 1. Context Budget Limits

| Asset Type | Recommended Limit | Hard Ceiling | Strategy when Exceeded |
|---|---|---|---|
| Frontmatter `description` | 30–80 words | 120 words | Tighten trigger verbs, eliminate filler words. |
| `SKILL.md` body | < 120 lines (~1,500 tokens) | 200 lines (~3,000 tokens) | Split background docs into `references/`. |
| `references/*.md` | < 300 lines (~4,000 tokens) | 500 lines (~6,500 tokens) | Segment into focused topic-specific files. |

---

## 2. Common Anti-Patterns & Remediations

### Anti-Pattern 1: Monolithic Runbook
- ❌ **Mistake**: Pasting 800 lines of API endpoint documentation and database schemas directly into `SKILL.md`.
- ✅ **Remediation**: Keep `SKILL.md` procedural (Step 1 -> Step 2 -> Step 3) and link to `[API Reference](./references/api_reference.md)`.

### Anti-Pattern 2: Conversational Fluff
- ❌ **Mistake**: Adding introductory chatter like "Welcome! In this guide we will explore the wonderful world of Docker deployments...".
- ✅ **Remediation**: Use imperative, bulleted, action-oriented checklists.

### Anti-Pattern 3: Duplicate General Knowledge
- ❌ **Mistake**: Re-explaining basic Python or Git commands that the underlying model already knows intimately.
- ✅ **Remediation**: Only document project-specific commands, flags, conventions, or proprietary scripts.
