#!/usr/bin/env python3
"""Set up an image project folder, the same layout every time.

  python3 new_project.py --where                 # print the saved projects folder (or "not set")
  python3 new_project.py --set-folder ~/memory/images   # save where image projects live
  python3 new_project.py "Shop logo"             # make (or reuse) "<projects folder>/2026-11 Shop logo"
  python3 new_project.py "Shop logo" --compare   # same, with the side-by-side compare gallery

The projects folder is saved in ~/.claude/ai-tools/image.json. An existing project is reused and
nothing in it is overwritten. Prints the project's path last.
"""

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

CONFIG = Path.home() / ".claude" / "ai-tools" / "image.json"
HERE = Path(__file__).resolve().parent
FOLDERS = ["refs/style", "refs/donors", "refs/subject", "rounds", "picks", "finals", "tools"]
TOOLS = {  # skill file → project file (under tools/)
    "generate-template.py": "generate.py",
    "prices-example.json": "prices.json",
    "composite.py": "composite.py",
    "crop_donors.py": "crop_donors.py",
    "finalize.py": "finalize.py",
}


def saved_folder():
    if CONFIG.exists():
        folder = json.loads(CONFIG.read_text()).get("projects_folder")
        return Path(folder) if folder else None
    return None


def set_folder(raw: str) -> Path:
    folder = Path(raw).expanduser().resolve()
    folder.mkdir(parents=True, exist_ok=True)
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(CONFIG.read_text()) if CONFIG.exists() else {}
    data["projects_folder"] = str(folder)
    CONFIG.write_text(json.dumps(data, indent=2) + "\n")
    return folder


def copy_if_missing(src: Path, dst: Path, title: str = "") -> None:
    if dst.exists():
        return
    text = src.read_text()
    if title:  # the gallery's title, in its CONFIG block
        text = text.replace('title: "Gallery"', f"title: {json.dumps(title)}", 1)
        text = text.replace('const TITLE = "Compare";', f"const TITLE = {json.dumps(title)};", 1)
    dst.write_text(text)
    shutil.copymode(src, dst)


def main() -> None:
    ap = argparse.ArgumentParser(description="Set up an image project folder.")
    ap.add_argument("name", nargs="?", help='project name, e.g. "Shop logo"')
    ap.add_argument("--set-folder", metavar="PATH", help="save where image projects live")
    ap.add_argument("--where", action="store_true", help="print the saved projects folder")
    ap.add_argument("--compare", action="store_true", help="use the side-by-side compare gallery")
    args = ap.parse_args()

    if args.set_folder:
        print(set_folder(args.set_folder))
        if not args.name:
            return
    if args.where:
        print(saved_folder() or "not set")
        return
    if not args.name:
        ap.print_help()
        return
    folder = saved_folder()
    if not folder:
        sys.exit("No projects folder saved yet. Run with --set-folder PATH first.")

    safe = re.sub(r'[/\\:*?"<>|]+', " ", args.name).strip()
    pattern = re.compile(r"\d{4}-\d{2} " + re.escape(safe) + "$")
    existing = [p for p in folder.iterdir() if p.is_dir() and pattern.fullmatch(p.name)] if folder.exists() else []
    project = existing[0] if existing else folder / f"{date.today():%Y-%m} {safe}"
    for sub in FOLDERS:
        (project / sub).mkdir(parents=True, exist_ok=True)
    tools = project / "tools"
    for src, dst in TOOLS.items():
        copy_if_missing(HERE / src, tools / dst)
    gallery = "gallery-compare-template.html" if args.compare else "gallery-template.html"
    copy_if_missing(HERE / gallery, tools / "gallery.html", args.name)
    print(project)


if __name__ == "__main__":
    main()
