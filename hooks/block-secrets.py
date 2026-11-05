#!/usr/bin/env python3
"""
PreToolUse hook to block reads/writes that expose sensitive files.
Exit codes: 0 = allow, 1 = error, 2 = block + tell Claude why
"""
import json
import sys
from pathlib import Path

# Exact filenames to block
SENSITIVE_FILES = {
    '.env',
    '.env.local',
    '.env.development',
    '.env.production',
    '.env.staging',
    'secrets.json',
    'secrets.yaml',
    'secrets.yml',
    'credentials.json',
    'service-account.json',
    'id_rsa',
    'id_ed25519',
    'id_ecdsa',
    '.npmrc',   # often contains tokens
    '.pypirc',  # python package tokens
}

# Path substrings to block
SENSITIVE_PATTERNS = [
    '/.ssh/',
    '/private_keys/',
    '/.gnupg/',
    '/keychain/',
]


def is_sensitive(file_path: str) -> tuple[bool, str]:
    path = Path(file_path)

    if path.name in SENSITIVE_FILES:
        return True, f"sensitive file: {path.name}"

    for pattern in SENSITIVE_PATTERNS:
        if pattern in file_path:
            return True, f"sensitive directory: {pattern}"

    if 'private' in path.name.lower() and ('key' in path.name.lower() or path.suffix in ['.pem', '.key']):
        return True, f"appears to be a private key: {path.name}"

    return False, ""


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_input = data.get('tool_input', {})
    file_path = tool_input.get('file_path') or tool_input.get('path') or ''

    if not file_path:
        sys.exit(0)

    is_blocked, reason = is_sensitive(file_path)

    if is_blocked:
        print(f"BLOCKED: Access to '{file_path}' denied ({reason}). "
              "If you need this file, ask the user to provide the relevant values.",
              file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()
