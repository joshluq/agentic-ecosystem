#!/usr/bin/env python3
"""
sync_wiki_tree.py - Confluence 4-Pillar Wiki Synchronizer

Scans project specifications, schemas, ADRs, and domain models, then synchronizes
them into an organized Atlassian Confluence wiki tree:
  1. 🧠 Conceptos (Domain Concepts & Ubiquitous Language)
  2. 🗄️ Entidades (Data Models & Schemas)
  3. 🚀 Features (Living Specifications & PRDs)
  4. 🔄 Flows (System Flows & State Machines)

Usage:
    # Scan and preview the wiki tree without publishing
    python sync_wiki_tree.py --scan-only

    # Dry-run with simulated publishing
    python sync_wiki_tree.py --dry-run

    # Publish to Confluence Space
    python sync_wiki_tree.py --space KMSAFE
"""

import argparse
import base64
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def markdown_to_confluence_xhtml(md_text: str) -> str:
    """Converts standard Markdown into clean Confluence Storage XHTML."""
    lines = md_text.splitlines()
    xhtml_parts: List[str] = []
    in_code_block = False
    code_lang = "text"
    code_lines: List[str] = []
    in_table = False
    table_rows: List[str] = []

    for line in lines:
        # Code fence handling
        if line.startswith("```"):
            if in_code_block:
                in_code_block = False
                code_content = html.escape("\n".join(code_lines))
                macro = (
                    f'<ac:structured-macro ac:name="code">'
                    f'<ac:parameter ac:name="language">{code_lang}</ac:parameter>'
                    f'<ac:plain-text-body><![CDATA[{code_content}]]></ac:plain-text-body>'
                    f'</ac:structured-macro>'
                )
                xhtml_parts.append(macro)
                code_lines = []
            else:
                in_code_block = True
                code_lang = line[3:].strip() or "text"
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Table handling
        if line.strip().startswith("|") and line.strip().endswith("|"):
            if re.match(r"^\|(\s*[-:]+[-| :]*)\|?$", line.strip()):
                continue  # Divider line
            cells = [c.strip() for c in line.strip()[1:-1].split("|")]
            tag = "th" if not in_table else "td"
            cell_html = "".join(f"<{tag}>{html.escape(c)}</{tag}>" for c in cells)
            table_rows.append(f"<tr>{cell_html}</tr>")
            in_table = True
            continue
        elif in_table:
            in_table = False
            tbody = "".join(table_rows)
            xhtml_parts.append(f"<table><tbody>{tbody}</tbody></table>")
            table_rows = []

        stripped = line.strip()
        if not stripped:
            continue

        # Headers
        if stripped.startswith("### "):
            xhtml_parts.append(f"<h3>{html.escape(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            xhtml_parts.append(f"<h2>{html.escape(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            xhtml_parts.append(f"<h1>{html.escape(stripped[2:])}</h1>")
        elif stripped.startswith("- "):
            xhtml_parts.append(f"<ul><li>{html.escape(stripped[2:])}</li></ul>")
        elif stripped.startswith("> "):
            callout = html.escape(stripped[2:])
            macro = (
                f'<ac:structured-macro ac:name="info">'
                f'<ac:rich-text-body><p>{callout}</p></ac:rich-text-body>'
                f'</ac:structured-macro>'
            )
            xhtml_parts.append(macro)
        else:
            xhtml_parts.append(f"<p>{html.escape(stripped)}</p>")

    if in_table and table_rows:
        tbody = "".join(table_rows)
        xhtml_parts.append(f"<table><tbody>{tbody}</tbody></table>")

    return "".join(xhtml_parts)


class ConfluenceWikiManager:
    def __init__(
        self,
        base_url: str,
        email: str,
        token: str,
        space_key: str,
        simulate: bool = False,
    ):
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.token = token
        self.space_key = space_key
        self.simulate = simulate
        self.simulated_counter = 1000

    def _http(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self.simulate:
            self.simulated_counter += 1
            return {"id": str(self.simulated_counter), "title": data.get("title", "Simulated") if data else "Page"}

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        auth_bytes = f"{self.email}:{self.token}".encode("ascii")
        auth_header = f"Basic {base64.b64encode(auth_bytes).decode('ascii')}"

        body_bytes = json.dumps(data).encode("utf-8") if data else None
        req = urllib.request.Request(
            url,
            data=body_bytes,
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method=method,
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code} on {method} {url}: {err_body}")

    def find_page_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        if self.simulate:
            return None
        encoded = urllib.parse.quote(title)
        endpoint = f"wiki/rest/api/content?spaceKey={self.space_key}&title={encoded}&expand=version"
        res = self._http("GET", endpoint)
        results = res.get("results", [])
        return results[0] if results else None

    def upsert_page(
        self,
        title: str,
        body_markdown: str,
        parent_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        xhtml_content = markdown_to_confluence_xhtml(body_markdown)
        existing = self.find_page_by_title(title)

        if existing:
            # Update
            page_id = existing["id"]
            cur_version = existing.get("version", {}).get("number", 1)
            payload = {
                "id": page_id,
                "type": "page",
                "title": title,
                "space": {"key": self.space_key},
                "body": {"storage": {"value": xhtml_content, "representation": "storage"}},
                "version": {"number": cur_version + 1},
            }
            if parent_id:
                payload["ancestors"] = [{"id": parent_id}]
            res = self._http("PUT", f"wiki/rest/api/content/{page_id}", payload)
            res["action"] = "UPDATED"
            return res
        else:
            # Create
            payload = {
                "type": "page",
                "title": title,
                "space": {"key": self.space_key},
                "body": {"storage": {"value": xhtml_content, "representation": "storage"}},
            }
            if parent_id:
                payload["ancestors"] = [{"id": parent_id}]
            res = self._http("POST", "wiki/rest/api/content", payload)
            res["action"] = "CREATED"
            return res


def scan_project_wiki_tree(root_dir: Path) -> Dict[str, Any]:
    """Inspects repository artifacts and categorizes them into the 4 Wiki Pillars."""
    # Project Title
    proj_md = root_dir / "PROJECT.md"
    proj_name = root_dir.name
    if proj_md.is_file():
        m = re.search(r"^#\s+(.+)$", proj_md.read_text(encoding="utf-8"), re.MULTILINE)
        if m:
            proj_name = m.group(1).strip()

    # 1. Conceptos
    concepts = []
    if proj_md.is_file():
        concepts.append({
            "title": "Glosario y Reglas de Negocio Universales",
            "content": proj_md.read_text(encoding="utf-8")
        })

    # 2. Entidades
    entities = []
    schemas_dir = root_dir / "schemas"
    if not schemas_dir.is_dir():
        schemas_dir = root_dir / "core" / "schemas"
    if schemas_dir.is_dir():
        for s in sorted(schemas_dir.glob("*.schema.json")):
            name = s.stem.replace(".schema", "").replace("_", " ").title()
            entities.append({
                "title": f"Esquema: {name}",
                "content": f"# Esquema de Entidad: {name}\n\n```json\n{s.read_text(encoding='utf-8')}\n```"
            })

    # 3. Features
    features = []
    specs_dir = root_dir / "openspec" / "specs"
    if specs_dir.is_dir():
        for sp in sorted(specs_dir.glob("*.md")):
            f_name = sp.stem.replace("_", " ").title()
            features.append({
                "title": f"Feature: {f_name}",
                "content": sp.read_text(encoding="utf-8")
            })

    # 4. Flows
    flows = []
    adr_dir = root_dir / "docs" / "adr"
    if adr_dir.is_dir():
        for adr in sorted(adr_dir.glob("*.md")):
            a_name = adr.stem.replace("_", " ").title()
            flows.append({
                "title": f"Flujo ADR: {a_name}",
                "content": adr.read_text(encoding="utf-8")
            })
    else:
        # Default architecture flow from AGENTS.md state machine
        agents_md = root_dir / "AGENTS.md"
        if agents_md.is_file():
            flows.append({
                "title": "Flujo de Ciclo de Vida del Ecosistema (State Machine)",
                "content": agents_md.read_text(encoding="utf-8")
            })

    return {
        "project_name": proj_name,
        "pillars": {
            "conceptos": {
                "title": "1. 🧠 Conceptos (Domain Concepts & Ubiquitous Language)",
                "description": "Diccionario de términos, glosario del dominio y reglas invariantes.",
                "pages": concepts,
            },
            "entidades": {
                "title": "2. 🗄️ Entidades (Domain Models & Schemas)",
                "description": "Modelos de datos, tablas de base de datos y esquemas de contrato.",
                "pages": entities,
            },
            "features": {
                "title": "3. 🚀 Features (Living Specifications & PRDs)",
                "description": "Especificaciones vivas consolidadas, historias de usuario y criterios de aceptación.",
                "pages": features,
            },
            "flows": {
                "title": "4. 🔄 Flows (System Flows & State Machines)",
                "description": "Diagramas de secuencia, arquitectura de integraciones y máquinas de estado.",
                "pages": flows,
            },
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Synchronize repository into a 4-Pillar Confluence Wiki.")
    parser.add_argument("--space", type=str, help="Target Confluence Space Key (e.g. KMSAFE)")
    parser.add_argument("--scan-only", action="store_true", help="Scan local project and print wiki tree preview")
    parser.add_argument("--dry-run", action="store_true", help="Simulate synchronization without publishing")
    parser.add_argument("--config", type=str, default=".atlassian_config.json", help="Path to config file")

    args = parser.parse_args()
    root = Path(".").resolve()

    print("===========================================================")
    print("   📚 CONFLUENCE 4-PILLAR WIKI SYNCHRONIZER")
    print(f"   Root : {root}")
    print("===========================================================")

    tree = scan_project_wiki_tree(root)

    print(f"\n📦 Root Portal: '{tree['project_name']} — Architecture & Domain Wiki'")
    for key, p in tree["pillars"].items():
        print(f"  ├── {p['title']} ({len(p['pages'])} páginas)")
        for page in p["pages"]:
            print(f"  │    └── 📄 {page['title']}")

    if args.scan_only:
        print("\n[+] Scan complete. Terminated without remote sync (--scan-only).")
        sys.exit(0)

    # Resolve credentials
    config_file = root / args.config
    if not config_file.is_file():
        config_file = root / ".atlassian_config.json.example"

    url = "https://example.atlassian.net"
    email = "user@example.com"
    token = "token"
    space_key = args.space or "DEV"
    simulate = args.dry_run

    if config_file.is_file():
        try:
            cfg = json.loads(config_file.read_text(encoding="utf-8"))
            url = cfg.get("url", url)
            email = cfg.get("email", email)
            token = cfg.get("api_token", token)
            space_key = args.space or cfg.get("confluence_space", space_key)
            if "PASTE_YOUR_API_TOKEN" in token or args.dry_run:
                simulate = True
        except Exception:
            simulate = True
    else:
        simulate = True

    print(f"\n[*] Target Space : {space_key}")
    print(f"[*] Mode         : {'SIMULATED (Dry-Run)' if simulate else 'LIVE CONFLUENCE SYNC'}")

    manager = ConfluenceWikiManager(url, email, token, space_key, simulate=simulate)

    # 1. Root Portal
    root_title = f"{tree['project_name']} — Architecture & Domain Wiki"
    root_body = (
        f"# {root_title}\n\n"
        f"Living architecture and domain knowledge base for **{tree['project_name']}**.\n\n"
        f"### Wiki Navigation Pillars\n"
        f"- **1. 🧠 Conceptos**: Glosario y reglas del negocio.\n"
        f"- **2. 🗄️ Entidades**: Modelos de datos y esquemas de contrato.\n"
        f"- **3. 🚀 Features**: Especificaciones vivas y criterios de aceptación.\n"
        f"- **4. 🔄 Flows**: Diagramas de secuencia y estados del sistema.\n"
    )
    root_res = manager.upsert_page(root_title, root_body)
    root_id = root_res["id"]
    print(f"\n[+] Root Portal: '{root_title}' [{root_res.get('action', 'OK')}] (ID: {root_id})")

    # 2. Pillars and Child Pages
    for key, pillar in tree["pillars"].items():
        p_title = f"[{tree['project_name']}] {pillar['title']}"
        p_body = f"# {pillar['title']}\n\n{pillar['description']}\n"
        p_res = manager.upsert_page(p_title, p_body, parent_id=root_id)
        p_id = p_res["id"]
        print(f"  ├── Pillar: '{pillar['title']}' [{p_res.get('action', 'OK')}] (ID: {p_id})")

        for page in pillar["pages"]:
            sub_title = f"[{tree['project_name']}] {page['title']}"
            sub_res = manager.upsert_page(sub_title, page["content"], parent_id=p_id)
            print(f"  │    └── Published: '{page['title']}' [{sub_res.get('action', 'OK')}] (ID: {sub_res['id']})")

    print("\n===========================================================")
    print("   🎉 4-PILLAR WIKI SYNCHRONIZATION COMPLETED!")
    print("===========================================================")


if __name__ == "__main__":
    main()
