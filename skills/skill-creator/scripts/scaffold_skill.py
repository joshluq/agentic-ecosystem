#!/usr/bin/env python3
"""
scaffold_skill.py - Antigravity Skill Scaffolder & Validator

Generates and audits standard-compliant Antigravity skills according to
ecosystem guidelines and progressive disclosure standards.

Usage:
    # Scaffold a new skill non-interactively
    python scaffold_skill.py --name custom-deploy --description "Deploys services to staging..." --target .agents/skills

    # Scaffold with optional folders and helper scripts
    python scaffold_skill.py --name custom-deploy --description "Deploys services..." --scripts deploy.py,verify.py --references api_guide.md

    # Validate an existing skill
    python scaffold_skill.py --validate .agents/skills/custom-deploy
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


MAX_SKILL_MD_LINES = 150
MIN_DESCRIPTION_CHARS = 20


SKILL_MD_TEMPLATE = """---
name: {name}
description: {description}
---

# {title}

{overview}

---

## When to Use This Skill

- Use when: [Describe primary trigger scenario]
- Do NOT use when: [Describe boundary or when another skill/rule applies]

---

## Workflow Steps

### Step 1: [Initial Step / Pre-condition Verification]
- Check prerequisites and inputs:
  [Describe input requirements or verification checks]

### Step 2: [Core Procedure Execution]
{execution_step}

### Step 3: [Verification & Post-condition Check]
- Verify successful outcome:
  [Describe how the agent checks logs, outputs, or test results]

---

## Troubleshooting & Edge Cases

| Issue / Failure | Root Cause | Remediation Action |
|---|---|---|
| [Error condition 1] | [Underlying cause] | [Deterministic recovery step] |
| [Error condition 2] | [Underlying cause] | [Deterministic recovery step] |
"""

REFERENCE_MD_TEMPLATE = """# {title} — Reference Guide

This document contains deep technical details, API references, or background schemas.
It is read on-demand by the agent via progressive disclosure to save context window tokens.

---

## 1. Overview & Technical Specifications

[Add detailed schemas, environment variables, or API specs here]

---

## 2. Parameter Reference

| Parameter | Type | Required | Description |
|---|---|---|---|
| `param_example` | string | Yes | Description of parameter usage |
"""

PYTHON_SCRIPT_TEMPLATE = """#!/usr/bin/env python3
\"\"\"
{script_name} - Helper script for {skill_name} skill.

Standard library only.
\"\"\"

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Helper script for {skill_name}")
    parser.add_argument("--check", action="store_true", help="Perform sanity check")
    args = parser.parse_args()

    print("[*] Running {script_name} for {skill_name}...")
    if args.check:
        print("[+] Sanity check passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
"""


def to_title_case(kebab_name: str) -> str:
    return " ".join(word.capitalize() for word in kebab_name.split("-"))


def validate_skill(skill_dir: Path) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    if not skill_dir.is_dir():
        return False, [f"Path is not a directory: {skill_dir}"]

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return False, [f"Missing required SKILL.md in: {skill_dir}"]

    content = skill_md.read_text(encoding="utf-8", errors="replace")

    # 1. Frontmatter delimiter check
    if not content.startswith("---"):
        errors.append("SKILL.md does not start with YAML frontmatter delimiter '---'")

    match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    if not match:
        errors.append("SKILL.md frontmatter is not closed with '---'")
        return False, errors

    fm_text = match.group(1)

    # 2. Name validation
    name_match = re.search(r"^name:\s*([a-z0-9-]+)", fm_text, re.MULTILINE)
    if not name_match:
        errors.append("Missing or invalid 'name' in frontmatter (must be lowercase alphanumeric with hyphens)")
    else:
        declared_name = name_match.group(1)
        if declared_name != skill_dir.name:
            errors.append(f"Frontmatter name '{declared_name}' does not match directory name '{skill_dir.name}'")

    # 3. Description validation
    desc_match = re.search(r"^description:\s*(?:>-\s*)?([\s\S]*?)(?=\n[a-z0-9_-]+:|$)", fm_text, re.MULTILINE)
    if not desc_match:
        errors.append("Missing 'description' in frontmatter")
    else:
        clean_desc = re.sub(r"\s+", " ", desc_match.group(1)).strip()
        if len(clean_desc) < MIN_DESCRIPTION_CHARS:
            errors.append(f"Description is too short ({len(clean_desc)} chars, minimum is {MIN_DESCRIPTION_CHARS})")
        if clean_desc.lower().startswith("i ") or clean_desc.lower().startswith("my "):
            warnings.append("Description should use third-person phrasing (e.g. 'Use this skill when...').")

    # 4. Token & Line budget check
    lines = content.splitlines()
    if len(lines) > MAX_SKILL_MD_LINES:
        warnings.append(
            f"SKILL.md has {len(lines)} lines (exceeds recommended {MAX_SKILL_MD_LINES} lines). "
            "Consider moving large documentation to references/ to conserve prompt token budget."
        )

    # 5. Check scripts directory if present
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for script_file in scripts_dir.iterdir():
            if script_file.suffix == ".py":
                try:
                    compile(script_file.read_text(encoding="utf-8", errors="replace"), script_file.name, "exec")
                except SyntaxError as e:
                    errors.append(f"Syntax error in script {script_file.name}: {e}")

    # 6. Report warnings
    for w in warnings:
        print(f"  [WARN] {w}")

    return len(errors) == 0, errors


def scaffold_skill(
    name: str,
    description: str,
    target_base: Path,
    scripts: Optional[List[str]] = None,
    references: Optional[List[str]] = None,
    with_examples: bool = False,
) -> Path:
    name = name.strip().lower()
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
        raise ValueError(f"Skill name '{name}' must be lowercase alphanumeric kebab-case (e.g., 'deploy-service').")

    if len(description.strip()) < MIN_DESCRIPTION_CHARS:
        raise ValueError(f"Description must be at least {MIN_DESCRIPTION_CHARS} characters.")

    skill_dir = target_base / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    title = to_title_case(name)
    overview = f"The `{name}` skill provides standard procedures and automation for {name.replace('-', ' ')}."

    # Prepare execution step instructions
    if scripts:
        exec_lines = ["- Run the helper script:"]
        for s in scripts:
            exec_lines.append(f"  `python scripts/{s}`")
        execution_step = "\n".join(exec_lines)
    else:
        execution_step = "- Execute target workflow steps according to project specifications."

    clean_desc = re.sub(r"\s+", " ", description.strip())
    skill_md_content = SKILL_MD_TEMPLATE.format(
        name=name,
        description=clean_desc,
        title=title,
        overview=overview,
        execution_step=execution_step,
    )

    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_md_content.strip() + "\n", encoding="utf-8")
    print(f"  [+] Created {skill_md_path}")

    # Scripts directory
    if scripts:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        for s_name in scripts:
            s_name = s_name.strip()
            if not s_name:
                continue
            s_file = scripts_dir / s_name
            if not s_file.exists():
                if s_name.endswith(".py"):
                    s_file.write_text(
                        PYTHON_SCRIPT_TEMPLATE.format(script_name=s_name, skill_name=name),
                        encoding="utf-8",
                    )
                else:
                    s_file.write_text("#!/usr/bin/env bash\nset -euo pipefail\necho '[*] Running helper...'\n", encoding="utf-8")
                print(f"  [+] Created script {s_file}")

    # References directory
    if references:
        ref_dir = skill_dir / "references"
        ref_dir.mkdir(parents=True, exist_ok=True)
        for r_name in references:
            r_name = r_name.strip()
            if not r_name:
                continue
            r_file = ref_dir / r_name
            if not r_file.exists():
                r_file.write_text(
                    REFERENCE_MD_TEMPLATE.format(title=to_title_case(r_name.replace(".md", ""))),
                    encoding="utf-8",
                )
                print(f"  [+] Created reference {r_file}")

    # Examples directory
    if with_examples:
        ex_dir = skill_dir / "examples"
        ex_dir.mkdir(parents=True, exist_ok=True)
        readme = ex_dir / "README.md"
        readme.write_text(f"# Examples for {title}\n\nAdd reference payloads, configurations, or sample code here.\n", encoding="utf-8")
        print(f"  [+] Created examples directory {ex_dir}")

    return skill_dir


def main():
    parser = argparse.ArgumentParser(description="Antigravity Skill Scaffolder & Validator")
    parser.add_argument("--name", type=str, help="Kebab-case skill name (e.g. staging-deployer)")
    parser.add_argument("--description", type=str, help="Third-person trigger description (min 20 characters)")
    parser.add_argument("--target", type=str, default=".agents/skills", help="Target base directory (default: .agents/skills)")
    parser.add_argument("--scripts", type=str, default="", help="Comma-separated helper scripts (e.g. runner.py,helper.sh)")
    parser.add_argument("--references", type=str, default="", help="Comma-separated reference markdown files (e.g. api_spec.md)")
    parser.add_argument("--with-examples", action="store_true", help="Include an examples/ directory")
    parser.add_argument("--validate", type=str, default="", help="Audit an existing skill directory")

    args = parser.parse_args()

    if args.validate:
        target_path = Path(args.validate).resolve()
        print(f"[*] Auditing skill at: {target_path}")
        ok, errors = validate_skill(target_path)
        if ok:
            print("[+] PASS: Skill structure and frontmatter are valid.")
            sys.exit(0)
        else:
            print("[!] FAIL: Validation errors detected:")
            for e in errors:
                print(f"    - {e}")
            sys.exit(1)

    if not args.name or not args.description:
        print("[!] Error: --name and --description are required when scaffolding a skill.")
        parser.print_help()
        sys.exit(1)

    script_list = [s.strip() for s in args.scripts.split(",") if s.strip()] if args.scripts else []
    ref_list = [r.strip() for r in args.references.split(",") if r.strip()] if args.references else []
    target_base = Path(args.target).resolve()

    print(f"[*] Scaffolding skill '{args.name}' under {target_base}...")
    try:
        created_dir = scaffold_skill(
            name=args.name,
            description=args.description,
            target_base=target_base,
            scripts=script_list,
            references=ref_list,
            with_examples=args.with_examples,
        )
        print(f"[*] Validating newly scaffolded skill...")
        ok, errors = validate_skill(created_dir)
        if ok:
            print(f"[+] Successfully scaffolded and validated skill at: {created_dir}")
            sys.exit(0)
        else:
            print(f"[!] Validation warning after scaffolding:")
            for e in errors:
                print(f"    - {e}")
            sys.exit(1)
    except Exception as exc:
        print(f"[ERROR] Failed to scaffold skill: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
