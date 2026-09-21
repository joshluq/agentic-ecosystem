#!/usr/bin/env python3
"""
atlassian_bridge.py - Jira & Confluence Integration Bridge for Android Agentic Ecosystem

Connects the multi-agent ecosystem (PO, Architect, Dev, QA, Debugger) to:
1. Jira Software: Ingest user stories, update task checklists, create crash bug tickets,
   and post feedback/clarification inquiries.
2. Confluence: Publish and maintain OpenSpec Living Specifications directly in the team wiki.

Authentication:
    Configure credentials via environment variables:
        export ATLASSIAN_URL="https://your-domain.atlassian.net"
        export ATLASSIAN_EMAIL="your-email@example.com"
        export ATLASSIAN_API_TOKEN="your-api-token"
        export CONFLUENCE_SPACE="DEV"
    Or pass via command-line arguments, or use --simulate for testing.
"""

import argparse
import base64
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# 1. ATLASSIAN CLIENT (HTTP & SIMULATION ENGINE)
# ==============================================================================

class AtlassianClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
        simulate: bool = False,
    ):
        self.simulate = simulate
        self.base_url = (base_url or os.environ.get("ATLASSIAN_URL", "")).rstrip("/")
        self.email = email or os.environ.get("ATLASSIAN_EMAIL", "")
        self.api_token = api_token or os.environ.get("ATLASSIAN_API_TOKEN", "")

        # Try reading local config file if credentials are empty
        config_path = ROOT_DIR / ".atlassian_config.json"
        if not self.base_url and config_path.is_file():
            try:
                cfg = json.loads(config_path.read_text(encoding="utf-8"))
                self.base_url = cfg.get("url", "").rstrip("/")
                self.email = cfg.get("email", "")
                self.api_token = cfg.get("api_token", "")
            except Exception:
                pass

        if not self.simulate and (not self.base_url or not self.email or not self.api_token):
            self.configured = False
        else:
            self.configured = True

    @property
    def auth_headers(self) -> Dict[str, str]:
        credentials = f"{self.email}:{self.api_token}"
        encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        return {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _http_request(self, method: str, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes an authenticated HTTP request to the Atlassian REST API."""
        if self.simulate:
            return {"simulated": True, "status": 200, "endpoint": endpoint, "method": method}

        if not self.configured:
            raise ValueError(
                "Atlassian credentials missing. Provide ATLASSIAN_URL, ATLASSIAN_EMAIL, and ATLASSIAN_API_TOKEN."
            )

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        data = json.dumps(payload).encode("utf-8") if payload else None
        req = urllib.request.Request(url, data=data, headers=self.auth_headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                status_code = resp.status
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else {"status": status_code}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else ""
            raise RuntimeError(f"Atlassian API Error ({e.code}) on {url}: {err_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error connecting to {url}: {e.reason}")

    # --------------------------------------------------------------------------
    # Jira Operations
    # --------------------------------------------------------------------------

    def test_connection(self) -> Dict[str, Any]:
        """Verifies connection and user permissions on Jira Cloud."""
        if self.simulate:
            return {
                "success": True,
                "simulated": True,
                "user": "developer@example.com",
                "display_name": "Antigravity Agent",
                "jira_status": "ONLINE",
            }
        data = self._http_request("GET", "rest/api/3/myself")
        return {
            "success": True,
            "simulated": False,
            "user": data.get("emailAddress"),
            "display_name": data.get("displayName"),
            "account_id": data.get("accountId"),
            "jira_status": "CONNECTED",
        }

    def get_jira_issue(self, issue_key: str) -> Dict[str, Any]:
        """Fetches issue details (summary, description, status, priority, comments)."""
        if self.simulate:
            return {
                "key": issue_key,
                "summary": f"Simulated Feature: {issue_key}",
                "status": "In Progress",
                "priority": "High",
                "description": (
                    "As a user, I want to export my vehicle balance to PDF so I have proof for the leasing company.\n\n"
                    "Acceptance Criteria:\n"
                    "- AC-1: Given an active contract, When I tap Export, Then a valid PDF is created."
                ),
                "comments_count": 1,
            }
        data = self._http_request("GET", f"rest/api/3/issue/{issue_key}")
        fields = data.get("fields", {})

        # Extract description text (Atlassian Document Format or string)
        desc = fields.get("description", "")
        if isinstance(desc, dict):
            desc = json.dumps(desc)

        return {
            "key": data.get("key"),
            "summary": fields.get("summary"),
            "status": fields.get("status", {}).get("name"),
            "priority": fields.get("priority", {}).get("name"),
            "description": desc,
            "issue_type": fields.get("issuetype", {}).get("name"),
        }

    def create_jira_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Story",
        priority: str = "Medium",
    ) -> Dict[str, Any]:
        """Creates a new Jira issue (Story, Bug, Task)."""
        if self.simulate:
            sim_key = f"{project_key}-101"
            return {
                "key": sim_key,
                "id": "10001",
                "self": f"https://example.atlassian.net/rest/api/3/issue/{sim_key}",
                "simulated": True,
            }

        # ADF format payload for Jira v3 API
        adf_desc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": description}],
                }
            ],
        }

        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": adf_desc,
                "issuetype": {"name": issue_type},
                "priority": {"name": priority},
            }
        }
        return self._http_request("POST", "rest/api/3/issue", payload)

    def add_jira_comment(self, issue_key: str, comment_text: str) -> Dict[str, Any]:
        """Posts a comment to a Jira ticket (e.g. for HITL feedback or clarification questions)."""
        if self.simulate:
            return {"comment_id": "9999", "issue_key": issue_key, "simulated": True}

        adf_comment = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": comment_text}],
                }
            ],
        }
        return self._http_request("POST", f"rest/api/3/issue/{issue_key}/comment", {"body": adf_comment})

    # --------------------------------------------------------------------------
    # Confluence Operations
    # --------------------------------------------------------------------------

    def publish_confluence_page(
        self,
        space_key: str,
        title: str,
        markdown_body: str,
        parent_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Publishes or updates a living specification in Confluence."""
        if self.simulate:
            return {
                "id": "20001",
                "title": title,
                "space": space_key,
                "url": f"https://example.atlassian.net/wiki/spaces/{space_key}/pages/20001",
                "simulated": True,
            }

        # Simple HTML conversion for Confluence Storage Format
        html_body = f"<pre>{markdown_body}</pre>"

        payload = {
            "title": title,
            "type": "page",
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": html_body,
                    "representation": "storage",
                }
            },
        }
        if parent_id:
            payload["ancestors"] = [{"id": parent_id}]

        return self._http_request("POST", "wiki/rest/api/content", payload)


# ==============================================================================
# 2. CLI WORKFLOW CONTROLLERS
# ==============================================================================

def cmd_check(client: AtlassianClient):
    print("===========================================================")
    print("   ATLASSIAN JIRA & CONFLUENCE CONNECTIVITY CHECK")
    print("===========================================================")
    print(f"Base URL  : {client.base_url or '(Not set - using simulation)'}")
    print(f"User      : {client.email or '(Not set)'}")
    print(f"Simulated : {client.simulate}")
    print("-----------------------------------------------------------")

    try:
        res = client.test_connection()
        print(f"✅ Connection Status : {res.get('jira_status')}")
        print(f"   Account User      : {res.get('user')}")
        print(f"   Display Name      : {res.get('display_name')}")
        if res.get("simulated"):
            print("   [INFO] Running in mock/simulation mode. No external network calls made.")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)


def cmd_fetch(client: AtlassianClient, issue_key: str, scaffold_openspec: bool = False):
    print(f"[*] Ingesting Jira ticket: {issue_key}...")
    try:
        issue = client.get_jira_issue(issue_key)
        print("-----------------------------------------------------------")
        print(f"Key      : {issue.get('key')}")
        print(f"Summary  : {issue.get('summary')}")
        print(f"Status   : {issue.get('status')}")
        print(f"Priority : {issue.get('priority')}")
        print("-----------------------------------------------------------")
        print("Description:")
        print(issue.get("description", "").strip())
        print("-----------------------------------------------------------")

        if scaffold_openspec:
            from scripts.openspec_cli import cmd_propose
            print(f"[*] Scaffolding OpenSpec proposal for {issue_key}...")
            cmd_propose(issue_key, title=issue.get("summary"))
    except Exception as e:
        print(f"❌ Error fetching issue: {e}")
        sys.exit(1)


def cmd_comment(client: AtlassianClient, issue_key: str, message: str):
    print(f"[*] Posting feedback comment to {issue_key}...")
    try:
        client.add_jira_comment(issue_key, message)
        print(f"✅ Comment posted successfully to {issue_key}.")
    except Exception as e:
        print(f"❌ Error posting comment: {e}")
        sys.exit(1)


def cmd_report_crash(client: AtlassianClient, project_key: str, defect_json_path: str):
    path = Path(defect_json_path)
    if not path.is_file():
        print(f"[ERROR] Defect file not found: {path}")
        sys.exit(1)

    defect = json.loads(path.read_text(encoding="utf-8"))
    summary = f"[CRASH] {defect.get('upstream_artifact_ref', 'Runtime')}: {defect.get('metadata', {}).get('exception_class', 'Fatal Error')}"
    description = (
        f"Automated crash report captured by Senior Debugging Engineer Tooling.\n\n"
        f"- Exception: {defect.get('metadata', {}).get('exception_class')}\n"
        f"- Message: {defect.get('metadata', {}).get('message')}\n"
        f"- Culprit File & Line: {defect.get('upstream_artifact_ref')}\n"
        f"- Thread: {defect.get('metadata', {}).get('thread')}\n"
        f"- Process: {defect.get('metadata', {}).get('process')}\n\n"
        f"Reproduction Steps:\n" + "\n".join(defect.get("reproduction_steps", [])) + "\n\n"
        f"Expected:\n{defect.get('expected')}\n\n"
        f"Actual:\n{defect.get('actual')}\n"
    )

    print(f"[*] Filing Jira Bug ticket for project '{project_key}'...")
    res = client.create_jira_issue(
        project_key=project_key,
        summary=summary,
        description=description,
        issue_type="Bug",
        priority="High" if defect.get("severity") == "CRITICAL" else "Highest",
    )
    print(f"✅ Bug ticket created: {res.get('key')} ({res.get('self', 'simulated')})")


def cmd_sync_confluence(client: AtlassianClient, space_key: str):
    specs_dir = ROOT_DIR / "openspec" / "specs"
    if not specs_dir.is_dir():
        print(f"[ERROR] Living specs directory not found: {specs_dir}")
        sys.exit(1)

    print(f"[*] Publishing OpenSpec Living Specifications to Confluence Space '{space_key}'...")
    specs = list(specs_dir.rglob("*.md"))
    for s in specs:
        title = f"Living Spec: {s.stem.replace('_', ' ').title()}"
        content = s.read_text(encoding="utf-8")
        print(f"    -> Publishing '{title}' ({s.name})...")
        res = client.publish_confluence_page(space_key, title, content)
        print(f"       ✅ Published: Page ID {res.get('id')}")

    print("===========================================================")
    print(f"   🎉 All {len(specs)} Living Specs Synchronized to Confluence!")
    print("===========================================================")


# ==============================================================================
# 3. CLI ARGUMENT PARSER
# ==============================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Jira & Confluence Integration Bridge for Android Agentic Ecosystem."
    )
    parser.add_argument("--url", help="Atlassian Cloud URL (e.g. https://domain.atlassian.net)")
    parser.add_argument("--email", help="Atlassian Account Email")
    parser.add_argument("--token", help="Atlassian API Token")
    parser.add_argument("--simulate", action="store_true", help="Run in mock/simulation mode without live credentials.")

    subparsers = parser.add_subparsers(dest="command", help="Bridge command to execute")

    # check
    subparsers.add_parser("check", help="Test Atlassian connection and permissions.")

    # fetch
    p_fetch = subparsers.add_parser("fetch", help="Fetch a Jira issue.")
    p_fetch.add_argument("issue_key", help="Jira issue key (e.g. KMSAFE-104)")
    p_fetch.add_argument("--scaffold-openspec", action="store_true", help="Scaffold an OpenSpec proposal from this issue.")

    # comment
    p_com = subparsers.add_parser("comment", help="Add a comment to a Jira issue.")
    p_com.add_argument("issue_key", help="Jira issue key")
    p_com.add_argument("message", help="Comment text or clarification question")

    # report-crash
    p_rc = subparsers.add_parser("report-crash", help="File a Jira Bug from a defect JSON ticket.")
    p_rc.add_argument("project_key", help="Target Jira Project Key (e.g. KMSAFE)")
    p_rc.add_argument("defect_json", help="Path to defect ticket JSON")

    # sync-confluence
    p_sync = subparsers.add_parser("sync-confluence", help="Publish OpenSpec living specs to Confluence.")
    p_sync.add_argument("space_key", help="Confluence Space Key (e.g. DEV, KMSAFE)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = AtlassianClient(
        base_url=args.url,
        email=args.email,
        api_token=args.token,
        simulate=args.simulate,
    )

    if args.command == "check":
        cmd_check(client)
    elif args.command == "fetch":
        cmd_fetch(client, args.issue_key, scaffold_openspec=args.scaffold_openspec)
    elif args.command == "comment":
        cmd_comment(client, args.issue_key, args.message)
    elif args.command == "report-crash":
        cmd_report_crash(client, args.project_key, args.defect_json)
    elif args.command == "sync-confluence":
        cmd_sync_confluence(client, args.space_key)


if __name__ == "__main__":
    main()
