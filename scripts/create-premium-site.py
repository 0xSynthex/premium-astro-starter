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
    p = project_dir / "package.json"
    data = json.loads(p.read_text())
    data["name"] = package_name
    data["version"] = "0.1.0"
    data["private"] = True
    p.write_text(json.dumps(data, indent=2) + "\n")


def update_readme(project_dir: Path, title: str, package_name: str) -> None:
    p = project_dir / "README.md"
    original = p.read_text() if p.exists() else ""
    intro = f"# {title}\n\nCreated from `premium-astro-starter`.\n\n## Project checklist\n\n- [ ] Fill `copy/landing-brief.md`\n- [ ] Add references under `references/` or `~/design-references`\n- [ ] Replace placeholder copy/assets\n- [ ] Run `npm run qa`\n- [ ] Fill `qa/website-qa-template.md` before delivery\n\nPackage: `{package_name}`\n\n---\n\n"
    p.write_text(intro + original)


def prepare_project(project_dir: Path) -> None:
    (project_dir / "references").mkdir(exist_ok=True)
    (project_dir / "assets" / "raw").mkdir(parents=True, exist_ok=True)
    (project_dir / "public" / "images").mkdir(parents=True, exist_ok=True)
    for marker in [project_dir / "references" / ".gitkeep", project_dir / "assets" / "raw" / ".gitkeep", project_dir / "public" / "images" / ".gitkeep"]:
        marker.touch()


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a premium Astro website project.")
    parser.add_argument("name", help="Project name/slug, e.g. luxury-law-landing")
    parser.add_argument("--dir", type=Path, default=HOME / "web-projects", help="Parent directory for the new project")
    parser.add_argument("--starter", type=Path, default=DEFAULT_STARTER, help="Starter path")
    parser.add_argument("--title", default=None, help="Human title for README")
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
    prepare_project(project_dir)

    if not args.no_install:
        run(["npm", "install"], project_dir)
    if not args.no_git:
        run(["git", "init", "-b", "main"], project_dir)
        run(["git", "add", "."], project_dir)
        run(["git", "commit", "-m", "feat: create premium site"], project_dir)

    print(f"project_dir={project_dir}")
    print(f"package_name={package_name}")
    print("next_steps:")
    print("- Fill copy/landing-brief.md")
    print("- Add references/screenshots")
    print("- Replace placeholder copy/assets")
    print("- Run npm run qa")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Command failed: {' '.join(exc.cmd)}", file=sys.stderr)
        raise SystemExit(exc.returncode)
