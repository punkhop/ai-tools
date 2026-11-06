#!/usr/bin/env python3
"""recent-sessions.py — SessionStart hook: Claude starts knowing what you worked on lately.

Reads the session notes /note writes in ~/memory/sessions/ (a dated .md file, or a dated folder
with SESSION-NOTE.md inside) and prints a short list: the newest notes for the project in this
folder first, with what was left unfinished last time, then the newest notes overall. Whatever a
SessionStart hook prints reaches Claude as context; the person doesn't see it.

Reads only file names and the first lines of a few notes. Changes nothing, needs no network,
prints nothing when there are no notes. Never blocks a session.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SESSIONS = Path.home() / "memory" / "sessions"
NEWEST, FOR_PROJECT, LEFTOVERS = 5, 3, 5


def notes():
    """Every session note, newest first: (path, modified time)."""
    found = []
    for entry in SESSIONS.iterdir():
        path = entry / "SESSION-NOTE.md" if entry.is_dir() else entry
        if path.suffix == ".md" and path.is_file():
            found.append((path, path.stat().st_mtime))
    return [p for p, _ in sorted(found, key=lambda x: x[1], reverse=True)]


def read(path):
    """Title, project, the one-line purpose and the leftover lines of a note."""
    text = path.read_text(errors="replace")[:20000]
    name = path.parent.name if path.name == "SESSION-NOTE.md" else path.stem
    project = re.search(r"^project:\s*(\S+)", text, re.M)
    title = re.search(r"^#\s+(.+)", text, re.M)
    purpose = re.search(r"^##\s*purpose\s*\n+(.+)", text, re.M | re.I)
    left = re.search(r"^##\s*leftovers\s*\n(.*?)(?=^##\s|\Z)", text, re.M | re.I | re.S)
    return {
        "name": name,
        "project": project.group(1).strip("\"'") if project else "",
        "title": title.group(1).strip() if title else name,
        "purpose": purpose.group(1).strip() if purpose else "",
        "left": [l.strip() for l in (left.group(1) if left else "").splitlines() if l.strip().startswith("-")],
    }


def this_project(cwd):
    """The name /note gives this folder's project: the git remote's repo name, else the folder name."""
    try:
        url = subprocess.run(["git", "-C", cwd, "remote", "get-url", "origin"],
                             capture_output=True, text=True, timeout=1).stdout.strip()
    except Exception:
        url = ""
    if url:
        return re.sub(r"\.git$", "", url.rstrip("/").rsplit("/", 1)[-1].rsplit(":", 1)[-1])
    return os.path.basename(cwd.rstrip("/"))


def line(note):
    out = f"- {note['name']}: {note['title']}"
    return out + (f"\n  {note['purpose']}" if note["purpose"] else "")


def main():
    try:
        cwd = json.load(sys.stdin).get("cwd") or os.getcwd()
    except Exception:
        cwd = os.getcwd()
    if not SESSIONS.is_dir():
        return
    paths = notes()
    if not paths:
        return
    project = this_project(cwd)
    mine = []
    if project and Path(cwd).resolve() != Path.home().resolve():
        for path in paths[:200]:
            note = read(path)
            if note["project"] == project:
                mine.append(note)
                if len(mine) == FOR_PROJECT:
                    break
    rest = [read(p) for p in paths[:NEWEST + FOR_PROJECT]]
    rest = [n for n in rest if n["name"] not in {m["name"] for m in mine}][:NEWEST]

    print("## Recent sessions (from ~/memory/sessions)")
    print()
    if mine:
        print(f"Last time in **{project}**:")
        print("\n".join(line(n) for n in mine))
        if mine[0]["left"]:
            print("Left unfinished then:")
            print("\n".join("  " + l for l in mine[0]["left"][:LEFTOVERS]))
        print()
    if rest:
        print("Newest notes:" if mine else "Newest notes, to pick up where they left off:")
        print("\n".join(line(n) for n in rest))
    print()
    print("Open a note before relying on it; when the person says \"where were we\", start from these.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
