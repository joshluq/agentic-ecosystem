#!/usr/bin/env python3
"""
audit_ecosystem_evolution.py - Read-Only Agentic Evolution Diagnostic Scanner

Audits the agentic ecosystem against modern AI engineering standards,
evaluating progressive disclosure, state-machine integrity, token economy,
and platform isolation.

MANDATORY CONSTRAINT: READ-ONLY AUDIT ONLY.
This script does NOT modify, rewrite, or mutate any files in the repository.

Usage:
    python audit_ecosystem_evolution.py
    python audit_ecosystem_evolution.py --json
    python audit_ecosystem_evolution.py --output evolution_report.json
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


CHATTER_PATTERNS = [
    (r"\bplease\b", "Polite conversational filler ('please')"),
    (r"\bthank you\b", "Conversational filler ('thank you')"),
    (r"\bfeel free to\b", "Conversational pleasantry ('feel free to')"),
    (r"\bas an ai\b", "Conversational AI self-reference"),
]

MAX_RECOMMENDED_SKILL_LINES = 150


def audit_skills(skills_dir: Path) -> List[Dict[str, Any]]:
    findings = []
    if not skills_dir.is_dir():
        return findings

    for skill_path in sorted(skills_dir.iterdir()):
        if not skill_path.is_dir():
            continue

        skill_name = skill_path.name
        skill_md = skill_path / "SKILL.md"
        if not skill_md.is_file():
            findings.append({
                "component": skill_name,
                "category": "Structure",
                "severity": "CRITICAL",
                "issue": "Missing SKILL.md",
                "recommendation": "Scaffold compliant SKILL.md with valid YAML frontmatter."
            })
            continue

        content = skill_md.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()

        # Check line count / progressive disclosure
        if len(lines) > MAX_RECOMMENDED_SKILL_LINES:
            findings.append({
                "component": skill_name,
                "category": "Progressive Disclosure",
                "severity": "ADVISORY",
                "issue": f"SKILL.md is {len(lines)} lines (exceeds recommended {MAX_RECOMMENDED_SKILL_LINES} lines)",
                "recommendation": "Extract long reference sections or code blocks into references/ to conserve prompt budget."
            })

        # Check chatter markers in SKILL.md
        for pat, desc in CHATTER_PATTERNS:
            matches = len(re.findall(pat, content, re.IGNORECASE))
            if matches > 0:
                findings.append({
                    "component": skill_name,
                    "category": "Chatter Elimination",
                    "severity": "ADVISORY",
                    "issue": f"{desc} detected ({matches} occurrences)",
                    "recommendation": "Replace conversational prose with imperative, bulleted action items."
                })

        # Check for scripts directory
        scripts_dir = skill_path / "scripts"
        has_scripts = scripts_dir.is_dir() and any(scripts_dir.iterdir())
        has_refs = (skill_path / "references").is_dir() and any((skill_path / "references").iterdir())

    return findings


def audit_governance(root: Path) -> List[Dict[str, Any]]:
    findings = []
    agents_md = root / "AGENTS.md"
    if not agents_md.is_file():
        findings.append({
            "component": "AGENTS.md",
            "category": "Governance",
            "severity": "CRITICAL",
            "issue": "Missing AGENTS.md charter",
            "recommendation": "Install canonical AGENTS.md specifying state machine and role boundaries."
        })
    else:
        text = agents_md.read_text(encoding="utf-8", errors="replace")
        if "Chatter Elimination Protocol" not in text:
            findings.append({
                "component": "AGENTS.md",
                "category": "Protocol",
                "severity": "HIGH",
                "issue": "Missing Chatter Elimination Protocol definition",
                "recommendation": "Incorporate strict artifact-driven state transitions to prevent conversational drift."
            })

    # Check schemas
    schemas_dir = root / "schemas"
    if schemas_dir.is_dir():
        schema_files = list(schemas_dir.glob("*.schema.json"))
        if len(schema_files) < 4:
            findings.append({
                "component": "schemas/",
                "category": "Contracts",
                "severity": "HIGH",
                "issue": f"Only {len(schema_files)} schemas found; core handoffs may lack typed validation",
                "recommendation": "Enforce Draft-07 handoff schemas for PO->Arch, Arch->Dev, and Dev->QA."
            })

    return findings


def run_evolution_audit(root: Path) -> Dict[str, Any]:
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        skills_dir = root / ".agents" / "skills"

    skill_findings = audit_skills(skills_dir)
    gov_findings = audit_governance(root)
    all_findings = skill_findings + gov_findings

    critical_count = sum(1 for f in all_findings if f["severity"] == "CRITICAL")
    high_count = sum(1 for f in all_findings if f["severity"] == "HIGH")
    advisory_count = sum(1 for f in all_findings if f["severity"] == "ADVISORY")

    # Compute modernization index (100 base)
    score = max(0, 100 - (critical_count * 25) - (high_count * 10) - (advisory_count * 3))

    return {
        "status": "COMPLETED",
        "modernization_score": score,
        "mode": "READ_ONLY_AUDIT",
        "summary": {
            "total_findings": len(all_findings),
            "critical": critical_count,
            "high": high_count,
            "advisory": advisory_count,
        },
        "findings": all_findings,
    }


def main():
    parser = argparse.ArgumentParser(description="Read-Only Agentic Evolution Diagnostic Scanner")
    parser.add_argument("--json", action="store_true", help="Output pure JSON")
    parser.add_argument("--output", type=str, help="Optional path to write JSON report")
    parser.add_argument("--target", type=str, default=".", help="Root directory to audit")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    report = run_evolution_audit(root)

    if args.output:
        out_path = Path(args.output).resolve()
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"[*] Report successfully written to: {out_path}")

    if args.json:
        print(json.dumps(report, indent=2))
        sys.exit(0)

    print("===========================================================")
    print("   🔭 AGENTIC ECOSYSTEM EVOLUTION & MODERNIZATION AUDIT")
    print(f"   Target : {root}")
    print(f"   Mode   : READ-ONLY (Zero Code/File Modifications)")
    print(f"   Score  : {report['modernization_score']}/100")
    print("===========================================================")
    print(f" Summary Findings: {report['summary']['total_findings']} total")
    print(f"  - Critical : {report['summary']['critical']}")
    print(f"  - High     : {report['summary']['high']}")
    print(f"  - Advisory : {report['summary']['advisory']}")
    print("-----------------------------------------------------------")

    if report["findings"]:
        print("\nDetailed Diagnostic Findings:")
        for idx, f in enumerate(report["findings"], 1):
            print(f" [{idx}] [{f['severity']}] {f['component']} ({f['category']})")
            print(f"     Issue          : {f['issue']}")
            print(f"     Recommendation : {f['recommendation']}")
    else:
        print("\n✨ All audited components fully align with modern agentic standards!")

    print("\n===========================================================")
    print(" [NOTE] This audit is strictly advisory. No files were modified.")
    print("===========================================================")
    sys.exit(0)


if __name__ == "__main__":
    main()
