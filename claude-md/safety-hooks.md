## Safety nets

- **Never `rm -rf` untracked files.** The `block-rm-untracked` hook stops it; read before overriding.
- **Never read or write secret files** (`.env`, SSH keys, credentials). The `block-secrets` hook stops it.
  Never ask me to paste a key or password into the chat.
