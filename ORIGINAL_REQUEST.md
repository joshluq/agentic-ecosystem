# Original User Request

## Initial Request — 2026-09-17T14:36:14Z

Build a modular agentic framework and starter template for Android application development, comprising role definitions (AGENTS.md), runnable skills (SKILL.md with CLI/testing helpers), and structured handoff protocols for an Android developer's daily workflow.

Working directory: C:\Users\josh_\.gemini\antigravity\scratch\android_agentic_ecosystem
Integrity mode: demo

## Requirements

### R1. Agent Roles and Contract Handoffs
Define clear role specifications (in `AGENTS.md` and rule files) for the primary Android lifecycle roles: Product Owner, Software Architect, Senior Android Developer (Kotlin/Compose), and QA/Testing Engineer. Include standardized contract schemas (PRD markdown template, Architecture Decision Record template, and API/Component interface format) governing how artifacts pass between roles to eliminate unstructured agent chatter.

### R2. Specialized Android Development Skills
Create runnable skills adhering to the standard Antigravity skill structure (`skills/<skill-name>/SKILL.md` with YAML frontmatter containing non-empty `name` and `description`). Skills must cover:
- Android CLI and emulator interaction (using `android-cli` capabilities for building, inspecting layouts, and launching emulators).
- Automated unit testing and UI test generation (JUnit/MockK/Turbine/Compose rules).
- Code linting, sanity verification, and debugging triage.

### R3. Self-Contained Verification Suite & Walkthrough
Provide an automated validation suite and a concrete demonstration showing how a feature request flows through each role (PO -> Architect -> Android Dev -> QA) and produces verified, linted code and test artifacts.

## Acceptance Criteria

### Specification & Skill Integrity
- [ ] All skill directories contain a valid `SKILL.md` with non-empty YAML frontmatter (`name` and `description`).
- [ ] Role definitions include machine-readable input and output contract specifications for each transition.

### Automated Verification
- [ ] An automated test/validation script runs successfully without manual intervention and confirms the integrity of all skills, roles, and schema contracts.
- [ ] The walkthrough pipeline executes end-to-end and validates generated artifacts against the acceptance criteria.
