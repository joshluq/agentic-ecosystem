#!/usr/bin/env python3
"""
post_tool_hook.py - Antigravity PostToolUse lifecycle hook.
Validates handoffs and JSON schemas immediately upon creation/modification.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

def main():
    try:
        input_data = {}
        if not sys.stdin.isatty():
            try:
                raw = sys.stdin.read()
                if raw.strip():
                    input_data = json.loads(raw)
            except Exception:
                pass

        tool_call = input_data.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})
        target_path = args.get("Path", "")

        if tool_name in ("write_file", "edit_file") and target_path:
            p = Path(target_path)
            # If a handoff JSON was written, validate against its schema
            if "handoffs" in p.parts and p.suffix == ".json" and p.is_file():
                try:
                    payload = json.loads(p.read_text(encoding="utf-8"))
                    handoff_type = payload.get("handoff_type", "")
                    if handoff_type:
                        schema_path = ROOT / "core" / "schemas" / f"{handoff_type}.schema.json"
                        if schema_path.is_file():
                            sys.path.insert(0, str(ROOT))
                            from scripts.schema_validator import validate_schema
                            schema = json.loads(schema_path.read_text(encoding="utf-8"))
                            validate_schema(payload, schema)
                except Exception:
                    pass

        # Return required empty object
        print(json.dumps({}))
    except Exception:
        print(json.dumps({}))

if __name__ == "__main__":
    main()
