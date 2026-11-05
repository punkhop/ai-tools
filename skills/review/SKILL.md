---
name: review
description: Run the OpenAI Codex CLI to review the current diff for correctness bugs, missed work, and quality issues. Needs the codex CLI installed and logged in (check with `codex --version`; log in with `codex login`). Use when reviewing changes before committing, getting a second AI opinion, or checking for things you might have skipped.
disable-model-invocation: false
---

# /review — Second-Opinion Code Review

**Needs the OpenAI Codex CLI, installed and logged in.** Check first:

```bash
codex --version   # must print a version
codex login status   # says whether you're signed in
codex login       # one-time sign-in (ChatGPT account or API key)
```

Use the `codex` CLI (OpenAI Codex) to review the current branch's diff against `main`. The point is to get an *independent* second opinion — Claude reviews its own work poorly because it's already convinced its work is correct.

## Prerequisites

If `codex --version` fails, tell the user:
"Install the codex CLI first — Mac: `brew install codex` · Mac or Linux: `npm install -g @openai/codex` (see https://github.com/openai/codex) — then run `codex login`. I'll wait."

If a codex call fails with a sign-in or auth error, ask the user to run `codex login`, then retry.

If it fails with an unknown or unsupported model, an "upgrade" or "update" message, or an
unknown option, the codex CLI is out of date (it never updates itself here). Update it
(`npm install -g @openai/codex@latest`, or `brew upgrade codex` if `brew list codex` knows it),
then retry once.

## How to Run

```bash
codex review --base origin/main "$PROMPT"
```

Where `$PROMPT` is a brief description of what changed. Build it from the conversation context — what feature/fix was being worked on. If the repo has no remote, use `--base main`. For work that isn't committed yet, use `codex review --uncommitted "$PROMPT"`. Options differ between codex versions — `codex review --help` lists what yours supports.

Example:
```bash
codex review --base origin/main "Review the email-sender integration in src/lib/email/. Focus on error handling, retry logic, and whether the rate-limit test correctly covers the 429 response path."
```

## What to Surface

`codex` will return a list of findings with severity levels. Surface them in the chat grouped by severity:

- **Must fix** — bugs, security holes, broken assumptions. Show inline.
- **Consider** — design concerns, edge cases worth thinking about. Summarize.
- **Nit** — style, minor naming. Mention only if there are <5 of them.

Don't ask the user "want me to fix these?" — just fix the must-fix findings, then ask about the consider ones. Skip nits unless they're cosmically wrong.

## What This Catches That Claude Doesn't

- **Work Claude skipped** — "you said you'd add the test but the file doesn't exist"
- **Half-implementations** — "the function takes a `retries` argument but never uses it"
- **Convention drift** — "everywhere else uses `formatCurrency()`, but here it's `.toFixed(2)`"
- **Forgotten cleanup** — "the old implementation is still imported in three files"

Claude is bad at reviewing its own work because it remembers writing the work. Codex doesn't have that bias.

## Rules

- Run codex directly via CLI. Don't route through any MCP wrapper or middleware — that can pin stale model versions.
- Fix must-fix findings without asking permission. The user already opted into the review by running `/review` — they don't want a permission step for each item.
- For consider findings, surface them and let the user decide.
- If codex's response is empty or comes back garbled, re-run with a more specific prompt scoped to one file.

## When to Use

- Before committing/pushing significant work
- After a long session where Claude wrote a lot — high chance something was skipped
- When the user says "did I miss anything?" or "double-check this"
- Before opening a PR
