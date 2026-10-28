#!/usr/bin/env python3
"""
Agentic Ecosystem - Project Installer & Hub-and-Spoke Deployer

Bootstraps the Agentic Ecosystem (Core Governance, Schemas, Templates, Atlassian Bridge, OpenSpec)
into any target repository with platform-specific discipline profiles:
- Android (Kotlin / Jetpack Compose / Gradle)
- Backend (Supabase / PostgreSQL / Edge Functions / Deno)
- Web (HTML/CSS / Astro / SEO / Legal Compliance)
- All (Comprehensive multi-disciplinary installation)

Usage:
    python scripts/install_to_project.py --target ../KmSafe --profile android
    python scripts/install_to_project.py --target ../kilomenos-backend --profile backend
    python scripts/install_to_project.py --target ../kilomenos-web --profile web
"""

import argparse
import datetime
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Optional, Set

CORE_SKILLS = {
    'openspec',
    'atlassian-bridge',
    'idea-lab',
    'ecosystem-optimizer',
    'skill-creator',
    'ecosystem-evolution',
    'confluence-wiki-docs',
}

PROFILE_SKILLS = {
    'android': CORE_SKILLS | {
        'android-staff-engineer-compose',
        'android-testing',
        'android-device',
        'android-quality',
        'new-feature',
        'fix-bug',
        'performance-optimization-tips',
        'po-digital-experience-fintech',
        'senior-debugging-engineer',
        'legal-compliance-audit',
    },
    'backend': CORE_SKILLS | {
        'supabase-db-triage',
        'supabase-edge-functions',
        'senior-debugging-engineer',
        'performance-optimization-tips',
        'new-feature',
        'fix-bug',
    },
    'web': CORE_SKILLS | {
        'legal-compliance-audit',
        'web-lighthouse-seo',
        'new-feature',
        'fix-bug',
    },
    'all': None,  # All skills
}

PROFILE_CONFIG_DEFAULTS = {
    'android': {"board_id": "1", "label": "android"},
    'backend': {"board_id": "1", "label": "backend"},
    'web': {"board_id": "1", "label": "web"},
    'all': {"board_id": "1", "label": ""},
}


def copy_dir(src: Path, dst: Path, overwrite: bool = True, filter_names: Optional[Set[str]] = None):
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in ('__pycache__', '.git', '.gradle', 'build'):
            continue
        if filter_names is not None and item.name not in filter_names:
            continue
        target = dst / item.name
        if item.is_dir():
            copy_dir(item, target, overwrite)
        else:
            if not target.exists() or overwrite:
                shutil.copy2(item, target)


def generate_profile_config(target_dir: Path, profile: str):
    config_file = target_dir / '.atlassian_config.json.example'
    meta = PROFILE_CONFIG_DEFAULTS.get(profile, PROFILE_CONFIG_DEFAULTS['all'])
    config_data = {
        "url": "https://joshluq-dev.atlassian.net",
        "email": "josh.luque@gmail.com",
        "api_token": "PASTE_YOUR_API_TOKEN_HERE",
        "project_key": "KILOMENOS",
        "board_id": meta["board_id"],
        "label": meta["label"],
        "confluence_space": "KILOMENOS"
    }
    config_file.write_text(json.dumps(config_data, indent=2) + "\n", encoding="utf-8")
    print(f"    -> Generated {config_file.name} for profile '{profile}'.")




def install_ecosystem(target_dir: Path, mode: str = 'both', profile: str = 'android', overwrite: bool = True, update_agents: bool = False, pack: Optional[str] = None):
    source_root = Path(__file__).resolve().parent.parent
    target_dir = target_dir.resolve()

    if not target_dir.exists():
        print(f"[ERROR] Target directory does not exist: {target_dir}")
        sys.exit(1)

    effective_pack = pack or profile
    allowed_skills = PROFILE_SKILLS.get(effective_pack)

    # Resolve pack directory: check packs/<pack>, then fallback to profiles/<pack>
    pack_dir = source_root / 'packs' / effective_pack
    if not pack_dir.is_dir():
        pack_dir = source_root / 'profiles' / effective_pack

    # Core directory
    core_dir = source_root / 'core'
    core_manifest_file = core_dir / 'manifest.json'
    core_version = "2.0.0"
    if core_manifest_file.is_file():
        try:
            core_version = json.loads(core_manifest_file.read_text(encoding="utf-8")).get("version", "2.0.0")
        except Exception:
            pass

    pack_manifest_file = pack_dir / 'pack.json' if pack_dir.is_dir() else None
    pack_version = "2.0.0"
    if pack_manifest_file and pack_manifest_file.is_file():
        try:
            pack_version = json.loads(pack_manifest_file.read_text(encoding="utf-8")).get("version", "2.0.0")
        except Exception:
            pass

    print("===========================================================")
    print("   Hub & Spoke Agentic Ecosystem Deployer (v2 Core + Packs)")
    print(f"   Source   : {source_root}")
    print(f"   Target   : {target_dir}")
    print(f"   Pack     : {effective_pack.upper()} ({len(allowed_skills) if allowed_skills else 'ALL'} skills)")
    print(f"   Mode     : {mode}")
    print("===========================================================")

    installed_files = []

    # 1. Install Skills (.agents/skills and .gemini/antigravity/skills)
    if mode in ('antigravity', 'both'):
        skills_dst = target_dir / '.gemini' / 'antigravity' / 'skills'
        agents_skills_dst = target_dir / '.agents' / 'skills'
        skills_src = source_root / 'skills'
        if not skills_src.is_dir():
            skills_src = source_root / '.agents' / 'skills'
            if not skills_src.is_dir():
                skills_src = source_root / '.gemini' / 'antigravity' / 'skills'
        print(f"\n[1] Installing filtered skills for pack '{effective_pack}'...")
        if skills_src.is_dir():
            # Standard Antigravity workspace path
            agents_skills_dst.mkdir(parents=True, exist_ok=True)
            copy_dir(skills_src, agents_skills_dst, overwrite, filter_names=allowed_skills)
            # Legacy/fallback path
            copy_dir(skills_src, skills_dst, overwrite, filter_names=allowed_skills)
        if agents_skills_dst.is_dir():
            installed = [p.name for p in agents_skills_dst.iterdir() if p.is_dir()]
            print(f"    -> Installed {len(installed)} skills in .agents/skills: {', '.join(sorted(installed))}")
        elif skills_dst.is_dir():
            installed = [p.name for p in skills_dst.iterdir() if p.is_dir()]
            print(f"    -> Installed {len(installed)} skills in .gemini/antigravity/skills: {', '.join(sorted(installed))}")
        else:
            print("    -> No skills installed.")

    # 2. Install SDD Contracts, Schemas, Templates & OpenSpec
    if mode in ('standalone', 'both'):
        # Universal Schemas from core/schemas (fallback: schemas/)
        schemas_src = core_dir / 'schemas' if (core_dir / 'schemas').is_dir() else source_root / 'schemas'
        dst_schemas = target_dir / 'schemas'
        print(f"\n[2] Installing schemas from {schemas_src} to {dst_schemas}...")
        copy_dir(schemas_src, dst_schemas, overwrite)

        # Templates: Pack-tailored or core/templates
        tmpl_dst = target_dir / 'templates'
        if pack_dir.is_dir() and (pack_dir / 'templates').is_dir():
            tmpl_src = pack_dir / 'templates'
            print(f"\n[2] Installing pack-tailored templates ({effective_pack}) to {tmpl_dst}...")
            copy_dir(tmpl_src, tmpl_dst, overwrite)
        else:
            tmpl_src = core_dir / 'templates' if (core_dir / 'templates').is_dir() else source_root / 'templates'
            print(f"\n[2] Installing templates to {tmpl_dst}...")
            copy_dir(tmpl_src, tmpl_dst, overwrite)

        # OpenSpec: Universal contracts + Pack-tailored specs
        openspec_dst = target_dir / 'openspec'
        print(f"\n[2] Installing openspec structure to {openspec_dst}...")
        (openspec_dst / 'changes').mkdir(parents=True, exist_ok=True)
        (openspec_dst / 'archive').mkdir(parents=True, exist_ok=True)
        contracts_src = core_dir / 'contracts' if (core_dir / 'contracts').is_dir() else source_root / 'openspec' / 'specs' / 'contracts'
        if contracts_src.is_dir():
            copy_dir(contracts_src, openspec_dst / 'specs' / 'contracts', overwrite)
        if pack_dir.is_dir() and (pack_dir / 'openspec' / 'specs').is_dir():
            print(f"    -> Installing pack living specs from {pack_dir.name}/{effective_pack}/openspec/specs...")
            copy_dir(pack_dir / 'openspec' / 'specs', openspec_dst / 'specs', overwrite)
        else:
            copy_dir(source_root / 'openspec' / 'specs', openspec_dst / 'specs', overwrite)

        # Copy PROJECT.md ONLY if not already existing
        proj_dst = target_dir / 'PROJECT.md'
        proj_src = pack_dir / 'PROJECT.md' if (pack_dir.is_dir() and (pack_dir / 'PROJECT.md').is_file()) else source_root / 'PROJECT.md'
        if proj_src.exists() and not proj_dst.exists():
            print(f"    -> Copying pack PROJECT.md to target root...")
            shutil.copy2(proj_src, proj_dst)
        elif proj_dst.exists():
            print(f"    -> Target already has PROJECT.md, preserving existing file.")

        # Copy or update AGENTS.md (Pack-specific if available)
        agents_dst = target_dir / 'AGENTS.md'
        agents_src = pack_dir / 'AGENTS.md' if (pack_dir.is_dir() and (pack_dir / 'AGENTS.md').is_file()) else source_root / 'AGENTS.md'
        if agents_src.exists():
            if not agents_dst.exists() or update_agents:
                action_str = "Updating" if agents_dst.exists() else "Copying"
                print(f"    -> {action_str} AGENTS.md ({effective_pack}) in target root...")
                shutil.copy2(agents_src, agents_dst)
            else:
                print(f"    -> Target already has AGENTS.md, preserving existing file (pass --update-agents to refresh).")

        # Copy core scripts & tests
        scripts_dst = target_dir / 'scripts'
        scripts_src = source_root / 'scripts'
        copy_dir(scripts_src, scripts_dst, overwrite)
        if pack_dir.is_dir() and (pack_dir / 'scripts').is_dir():
            print(f"    -> Installing pack-specific scripts ({effective_pack}) to {scripts_dst}...")
            copy_dir(pack_dir / 'scripts', scripts_dst, overwrite)

        tests_dst = target_dir / 'tests'
        tests_src = source_root / 'tests'
        copy_dir(tests_src, tests_dst, overwrite)

        # Install Antigravity 2.0 lifecycle hooks (.agents/hooks.json)
        hub_hooks = source_root / '.agents' / 'hooks.json'
        if hub_hooks.is_file():
            dst_hooks = target_dir / '.agents' / 'hooks.json'
            dst_hooks.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(hub_hooks, dst_hooks)
            print(f"    -> Installed .agents/hooks.json for Antigravity 2.0 lifecycle automation.")

        # Install FinOps models configuration (.agents/models.yaml)
        hub_models = source_root / 'core' / 'models.yaml'
        if hub_models.is_file():
            dst_models = target_dir / '.agents' / 'models.yaml'
            dst_models.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(hub_models, dst_models)
            print(f"    -> Installed .agents/models.yaml (Gemini 3.8 & FinOps routing).")

        # Generate profile/pack-tailored .atlassian_config.json.example
        generate_profile_config(target_dir, effective_pack)

        # Clean up deprecated copilot instructions if present
        deprecated_copilot = target_dir / '.github' / 'copilot_instructions.md'
        if deprecated_copilot.is_file():
            deprecated_copilot.unlink()
            print(f"    -> Removed deprecated {deprecated_copilot.relative_to(target_dir)}")

        # Generate .agentic.lock in target directory
        lock_data = {
            "core_version": core_version,
            "pack": effective_pack,
            "pack_version": pack_version,
            "installed_at": datetime.datetime.now(datetime.timezone.utc).isoformat() if hasattr(datetime, 'timezone') else datetime.datetime.utcnow().isoformat(),
            "mode": mode,
        }
        lock_file = target_dir / '.agentic.lock'
        lock_file.write_text(json.dumps(lock_data, indent=2) + "\n", encoding="utf-8")
        print(f"    -> Generated .agentic.lock (core={core_version}, pack={effective_pack}@{pack_version})")

    print("\n===========================================================")
    print(f"   🎉 Deployment Complete for Pack: {effective_pack.upper()}")
    print("   Project equipped with Spec-Driven Multi-Agent Governance.")
    print("===========================================================")


def main():
    parser = argparse.ArgumentParser(description="Install and configure Agentic Ecosystem by pack or profile.")
    parser.add_argument("--target", "-t", required=True, help="Target project root directory")
    parser.add_argument("--pack", choices=['android', 'backend', 'web', 'all'], default=None,
                        help="Discipline pack to install: 'android', 'backend', 'web', or 'all'")
    parser.add_argument("--profile", "-p", choices=['android', 'backend', 'web', 'all'], default='android',
                        help="Platform discipline profile (alias for --pack for backwards compatibility)")
    parser.add_argument("--mode", "-m", choices=['antigravity', 'standalone', 'both'], default='both',
                        help="Installation mode: 'antigravity', 'standalone', or 'both' (default: both)")
    parser.add_argument("--no-overwrite", action='store_true', help="Do not overwrite existing files")
    parser.add_argument("--update-agents", action='store_true', help="Overwrite AGENTS.md with the latest ecosystem role specifications")

    parser.add_argument("--force-during-freeze", action='store_true',
                        help="Bypass PROPAGATION_FREEZE.md (v2 in progress). Not recommended.")

    args = parser.parse_args()
    freeze_file = Path(__file__).resolve().parent.parent / "PROPAGATION_FREEZE.md"
    if freeze_file.exists() and not args.force_during_freeze:
        print(f"[FROZEN] Propagation disabled while v2 is in progress. See {freeze_file}")
        sys.exit(2)
    target_path = Path(args.target)
    selected_pack = args.pack or args.profile
    install_ecosystem(target_path, mode=args.mode, profile=selected_pack, overwrite=not args.no_overwrite, update_agents=args.update_agents, pack=selected_pack)


if __name__ == '__main__':
    main()

