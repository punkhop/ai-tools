#!/usr/bin/env python3
"""Save an API key to ~/.claude/ai-tools/keys.env (readable only by you). Never prints the key.

Run it yourself in a terminal window and paste the key when asked (the paste stays hidden):
  python3 ~/.claude/skills/image/scripts/save_key.py OPENAI_API_KEY
  python3 ~/.claude/skills/image/scripts/save_key.py GEMINI_API_KEY

Or from a file holding only the key (the file is left as it was):
  python3 save_key.py GEMINI_API_KEY --from-file /path/to/file

Or, when the key lives in 1Password, save only where it is (the key itself never touches disk):
  python3 save_key.py OPENAI_API_KEY --ref "op://Personal/OpenAI API Key/credential"
"""

import argparse
import getpass
import os
import sys
from pathlib import Path

KEYS_FILE = Path.home() / ".claude" / "ai-tools" / "keys.env"
NAMES = ("OPENAI_API_KEY", "GEMINI_API_KEY")


def main() -> None:
    ap = argparse.ArgumentParser(description="Save an API key without showing it.")
    ap.add_argument("name", choices=NAMES)
    ap.add_argument("--from-file", metavar="PATH", help="read the key from this file instead of asking")
    ap.add_argument("--ref", metavar="OP_REF", help="save a 1Password op:// reference instead of the key")
    args = ap.parse_args()

    if args.ref:
        value = args.ref.strip()
        if not value.startswith("op://") or "\n" in value:
            sys.exit("A 1Password reference starts with op://; nothing was saved.")
    elif args.from_file:
        value = Path(args.from_file).expanduser().read_text().strip()
    else:
        value = getpass.getpass(f"Paste your {args.name} (it stays hidden), then press Return: ").strip()
    if not args.ref and (not value or "\n" in value or " " in value):
        sys.exit("That doesn't look like a key; nothing was saved.")

    KEYS_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = KEYS_FILE.read_text().splitlines() if KEYS_FILE.exists() else []
    lines = [l for l in lines if not l.strip().removeprefix("export ").startswith(args.name + "=")]
    lines.append(f"{args.name}={value}")
    fd = os.open(KEYS_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write("\n".join(lines) + "\n")
    os.chmod(KEYS_FILE, 0o600)
    print(f"Saved {args.name} to {KEYS_FILE}")


if __name__ == "__main__":
    main()
