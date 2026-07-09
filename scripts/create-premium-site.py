#!/usr/bin/env python3
"""Create a new premium website project from the local Astro starter.

Free/local workflow. No GitHub/API actions, no secrets copied.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
DEFAULT_STARTER = HOME / "web-starters" / "premium-astro"
EXCLUDE_DIRS = {".git", "node_modules", "dist", "docs", ".astro", "test-results", "playwright-report"}
EXCLUDE_FILES = {".DS_Store"}


BRIEF_TEMPLATE = """# Project Intake

Project:
Owner:
Date:

## Goal

What should this website achieve?

-

## Audience

Who is it for and what do they care about?

-

## Primary CTA

Main conversion action:

-

Secondary CTA / risk reducer:

-

## References

Add 3–10 URLs or screenshots. For each, note what to borrow as a principle and what to avoid.

| Reference | Like | Avoid |
|---|---|---|
|  |  |  |

## Brand mood

- [ ] Premium
- [ ] Clean
- [ ] Bold
- [ ] Local/trustworthy
- [ ] Technical
- [ ] Luxury
- [ ] Playful
- [ ] Editorial
- [ ] Cinematic

Notes:

-

## Assets

- Logo:
- Photos/video:
- Product screenshots:
- Icons/illustrations:
- Testimonials/case studies:
- Proof points:

## Constraints

Must include:

-

Must avoid:

-

Claims needing proof:

-

Legal/privacy requirements:

-

## Surface and direction

Surface: Decide / Learn / Compare / Explore / Configure / Operate / Monitor

Direction statement:

-

## Delivery

Stack/deploy target:
Urgency/fidelity:
Launch risk:
"""

REFERENCE_TEMPLATE = """# References

Use this folder for project-local references. Do not add private/client screenshots unless approved for this project.

## How to add

```bash
python3 ~/design-references/scripts/add-reference.py landing-pages example https://example.com --title "Example" --screenshot
```

Then copy or link the useful reference notes here.

## Reference summary

| Name | Source | Principle to use | What not to copy |
|---|---|---|---|
|  |  |  |  |

## Direction statement

Write the final synthesis before designing:

-
"""

QA_PLAN_TEMPLATE = """# QA Plan

Use before delivery.

## Required checks

- [ ] `npm run qa:full`
- [ ] Desktop screenshot reviewed
- [ ] Mobile screenshot reviewed
- [ ] CTA path checked
- [ ] Lead form labels/status/honeypot checked if form is used
- [ ] `qa/reports/performance-budget.json` reviewed
- [ ] `qa/website-qa-template.md` filled
- [ ] Strict secret scan before public GitHub push
- [ ] Live URL verified after deploy

## Slop audit notes

Score 0–10:

Issues:

-

Repairs:

-

## Delivery notes

-
"""

PROJECT_LOG_TEMPLATE = """# Project Log

## Setup

Created from `premium-astro-starter`.

## Decisions

-

## Checks

-

## Deploys

-
"""


AGENTS_TEMPLATE = """# Project Agent Instructions

This project was created from `premium-astro-starter`.

## Rules

- Keep changes minimal, practical, and conversion-focused.
- Use `copy/project-intake.md` before major design changes.
- Use `references/README.md` before styling from references.
- Do not invent testimonials, logos, metrics, case studies, or customer outcomes.
- Do not commit secrets, `.env*`, customer data, private uploads, or private screenshots.
- Run `npm run qa:full` before delivery.
- Fill `qa/website-qa-template.md` and `qa/qa-plan.md` for serious delivery.
- Public GitHub/deploy requires secret scan and approval.
"""


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-._")
    return value or "premium-site"


def titleize(slug: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[-_]+", slug) if part)


def ignore(_dir: str, names: list[str]) -> set[str]:
    return {name for name in names if name in EXCLUDE_DIRS or name in EXCLUDE_FILES or name.startswith(".env")}


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def update_package_json(project_dir: Path, package_name: str) -> None:
    for filename in ["package.json", "package-lock.json"]:
        p = project_dir / filename
        if not p.exists():
            continue
        data = json.loads(p.read_text())
        data["name"] = package_name
        data["version"] = "0.1.0"
        if filename == "package.json":
            data["private"] = True
        if isinstance(data.get("packages"), dict) and "" in data["packages"]:
            data["packages"][""]["name"] = package_name
            data["packages"][""]["version"] = "0.1.0"
        p.write_text(json.dumps(data, indent=2) + "\n")


def update_readme(project_dir: Path, title: str, package_name: str) -> None:
    p = project_dir / "README.md"
    original = p.read_text() if p.exists() else ""
    intro = f"# {title}\n\nCreated from `premium-astro-starter`.\n\n## Project checklist\n\n- [ ] Fill `copy/project-intake.md` and `copy/landing-brief.md`\n- [ ] Add 3–10 references in `references/README.md`\n- [ ] Replace placeholder copy/assets\n- [ ] Run `npm run qa:full`\n- [ ] Fill `qa/website-qa-template.md` and `qa/qa-plan.md` before delivery\n- [ ] Run strict secret scan before public GitHub/deploy\n\nPackage: `{package_name}`\n\n---\n\n"
    p.write_text(intro + original)


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content)


def prepare_project(project_dir: Path, title: str) -> None:
    (project_dir / "references" / "screenshots").mkdir(parents=True, exist_ok=True)
    (project_dir / "references" / "assets").mkdir(parents=True, exist_ok=True)
    (project_dir / "assets" / "raw").mkdir(parents=True, exist_ok=True)
    (project_dir / "public" / "images").mkdir(parents=True, exist_ok=True)
    (project_dir / "qa" / "reports").mkdir(parents=True, exist_ok=True)
    (project_dir / "notes").mkdir(exist_ok=True)
    for marker in [
        project_dir / "references" / "screenshots" / ".gitkeep",
        project_dir / "references" / "assets" / ".gitkeep",
        project_dir / "assets" / "raw" / ".gitkeep",
        project_dir / "public" / "images" / ".gitkeep",
        project_dir / "qa" / "reports" / ".gitkeep",
    ]:
        marker.touch()
    stale_report = project_dir / "qa" / "reports" / "performance-budget.json"
    if stale_report.exists():
        stale_report.unlink()
    (project_dir / "copy" / "project-intake.md").write_text(BRIEF_TEMPLATE.replace("Project:\n", f"Project: {title}\n"))
    (project_dir / "references" / "README.md").write_text(REFERENCE_TEMPLATE)
    (project_dir / "qa" / "qa-plan.md").write_text(QA_PLAN_TEMPLATE)
    (project_dir / "notes" / "project-log.md").write_text(PROJECT_LOG_TEMPLATE)
    write_if_missing(project_dir / "AGENTS.md", AGENTS_TEMPLATE)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a premium Astro website project.")
    parser.add_argument("name", help="Project name/slug, e.g. luxury-law-landing")
    parser.add_argument("--dir", type=Path, default=HOME / "web-projects", help="Parent directory for the new project")
    parser.add_argument("--starter", type=Path, default=DEFAULT_STARTER, help="Starter path")
    parser.add_argument("--title", default=None, help="Human title for README/intake")
    parser.add_argument("--no-install", action="store_true", help="Skip npm install")
    parser.add_argument("--no-git", action="store_true", help="Skip git init")
    args = parser.parse_args()

    slug = slugify(args.name)
    title = args.title or titleize(slug)
    package_name = slug
    starter = args.starter.expanduser().resolve()
    parent = args.dir.expanduser().resolve()
    project_dir = parent / slug

    if not starter.exists():
        raise SystemExit(f"Starter not found: {starter}")
    if project_dir.exists():
        raise SystemExit(f"Destination already exists: {project_dir}")

    parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(starter, project_dir, ignore=ignore)
    update_package_json(project_dir, package_name)
    update_readme(project_dir, title, package_name)
    prepare_project(project_dir, title)

    if not args.no_install:
        run(["npm", "install"], project_dir)
    if not args.no_git:
        run(["git", "init", "-b", "main"], project_dir)
        run(["git", "add", "."], project_dir)
        run(["git", "commit", "-m", "feat: create premium site"], project_dir)

    print(f"project_dir={project_dir}")
    print(f"package_name={package_name}")
    print("next_steps:")
    print("- Fill copy/project-intake.md and copy/landing-brief.md")
    print("- Add references/screenshots in references/README.md")
    print("- Replace placeholder copy/assets")
    print("- Run npm run qa:full")
    print("- Fill qa/qa-plan.md and qa/website-qa-template.md")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Command failed: {' '.join(exc.cmd)}", file=sys.stderr)
        raise SystemExit(exc.returncode)
