# Antigravity Skill Anatomy & Progressive Disclosure Reference

This guide details the structural and architectural specifications required for creating resilient, high-performance skills within the agentic ecosystem.

---

## 1. Directory Structure Standard

Every skill must be packaged as a directory conforming to this layout:

```text
skills/<skill_name>/
├── SKILL.md            # Mandatory: Main instruction file with YAML frontmatter
├── scripts/            # Optional: Deterministic automation scripts (Python, Bash)
├── references/         # Optional: Deep architectural manuals, API schemas, specifications
├── resources/          # Optional: Templates, static assets, configuration fixtures
└── examples/           # Optional: End-to-end sample implementations and usage patterns
```

---

## 2. Frontmatter Specifications

The `SKILL.md` file MUST open with a strict YAML frontmatter block:

```yaml
---
name: <unique-kebab-name>
description: >-
  <Third-person description stating EXACTLY what the skill does,
   when to trigger it, and key boundary conditions. Min 20 characters.>
---
```

### Critical Frontmatter Rules:
1. **Name Matching**: `name` must be lowercase alphanumeric with hyphens (`[a-z0-9-]+`) and match the enclosing directory name identically.
2. **Third-Person Phrasing**: Use objective, third-person wording:
   - ✅ *Good*: "Architects and validates Jetpack Compose UI components following MVI and 4-layer UI standards."
   - ❌ *Bad*: "I can help you build Android UI components when you ask me."
3. **Trigger Specificity**: Clearly articulate both trigger scenarios and anti-triggers (when *not* to activate), preventing accidental routing collisions.

---

## 3. The 3-Tier Progressive Disclosure Model

To preserve the agent's context window and optimize inference speed:

1. **Discovery Tier (Always Available)**:
   - Only `name` and `description` from the YAML frontmatter are indexed in the agent's initial prompt context.
2. **Activation Tier (Loaded On-Demand)**:
   - When the user's intent matches the description, the agent executes `view_file` on `SKILL.md`.
   - `SKILL.md` should be concise (< 150 lines) and focus on procedural steps, decision trees, and validation gates.
3. **Deep Execution Tier (Sub-document Progressive Fetch)**:
   - Heavy API tables, database schemas, or lengthy guides reside in `references/*.md`.
   - The agent only reads specific reference files when navigating complex branches of the procedure.

---

## 4. Deterministic Helper Scripts (`scripts/`)

Follow these principles when providing automation scripts:
- **Zero Foreign Dependencies**: Rely exclusively on standard library (`sys`, `os`, `pathlib`, `json`, `re`, `argparse`, `urllib`).
- **Fail-Fast Exit Codes**: Exit with `0` on success and non-zero (`1`, `2`) on failure.
- **Clear CLI Interface**: Provide `--help`, flag arguments, and deterministic outputs.
