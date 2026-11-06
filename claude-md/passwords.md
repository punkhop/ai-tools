## Passwords

- **Every password and API key lives in my 1Password.** Keys go in the vault named Personal (Private
  on older accounts; `op vault list` shows which), titled like `OpenAI API Key`.
- **Never ask me to paste a key or password into the chat.** When you need one, find it with
  `2password find <words>` and pass it to the command with `2password run` or `2password env run`;
  I tap Touch ID (or my computer password) to allow it. Never print, `cat` or `read` a value.
- **A new key:** I copy it, you save it with `2password create api-credential --clipboard`; in T3 Code
  you may use the private box (`request_secret`, `delivery: "file"`) and `--stdin < <file>` instead.
- Not in the vault yet: tell me in one line and save it there; never put it in a file or the chat.
