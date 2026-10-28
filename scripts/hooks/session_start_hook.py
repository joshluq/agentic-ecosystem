#!/usr/bin/env python3
"""
session_start_hook.py - Antigravity SessionStart lifecycle hook.
Runs ecosystem health verification on session startup.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

def main():
    try:
        # Read hook payload from stdin if available
        input_data = {}
        if not sys.stdin.isatty():
            try:
                raw = sys.stdin.read()
                if raw.strip():
                    input_data = json.loads(raw)
            except Exception:
                pass

        # Execute lightweight ecosystem health audit
        audit_script = ROOT / "skills" / "ecosystem-optimizer" / "scripts" / "ecosystem_audit.py"
        if not audit_script.is_file():
            audit_script = ROOT / ".agents" / "skills" / "ecosystem-optimizer" / "scripts" / "ecosystem_audit.py"

        if audit_script.is_file():
            sys.path.insert(0, str(audit_script.parent))
            from ecosystem_audit import run_ecosystem_audit
            report = run_ecosystem_audit(ROOT)
            if not report.get("success", False):
                errs = report.get("errors", [])
                msg = f"⚠️ Ecosystem Health Warning: {len(errs)} issue(s) detected during startup audit."
                print(json.dumps({"injectSteps": [{"systemMessage": {"systemMessage": msg}}]}))
                return

        # Pristine status or fallback: empty JSON object required by hook contract
        print(json.dumps({}))
    except Exception as e:
        # Hooks should be resilient and never crash the shell session
        print(json.dumps({}))

if __name__ == "__main__":
    main()
