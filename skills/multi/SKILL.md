---
name: multi
description: Multi-model coordination — fan out a question across Claude, Codex (OpenAI), and optionally Gemini for adversarial review, deep planning, or consensus polling on architecture decisions. Needs the codex CLI installed and logged in (check with `codex --version`; log in with `codex login`). Use for big calls where you want diverse perspectives, not for routine tasks.
disable-model-invocation: false
---

# /multi — Multi-Model Coordination

**Needs the OpenAI Codex CLI, installed and logged in.** Check first:

```bash
codex --version    # must print a version
codex login status # says whether you're signed in
codex login        # one-time sign-in (ChatGPT account or API key)
gemini --version   # optional third voice
```

Orchestrate a question across multiple AI CLIs and synthesize the answers. Claude is the conductor; codex (and optionally gemini) are the additional voices.

## Prerequisites

If `codex --version` fails, tell the user: "This skill needs the codex CLI — Mac: `brew install codex` · Mac or Linux: `npm install -g @openai/codex` — then `codex login`. Without it, I can give you a single-model deep think but not a multi-model comparison."

If a codex call fails with a sign-in or auth error, ask the user to run `codex login`, then retry.

If it fails with an unknown or unsupported model, an "upgrade" or "update" message, or an
unknown option, the codex CLI is out of date (it never updates itself here). Update it
(`npm install -g @openai/codex@latest`, or `brew upgrade codex` if `brew list codex` knows it),
then retry once.

## Modes

### Mode 1: Adversarial review
For "is this approach right?"

Send the same question to codex (and gemini if available) phrased adversarially: "Tell me what's wrong with this plan." Synthesize the disagreements.

```bash
codex exec "Review this plan: [plan]. What's wrong with it? What did I miss? What would you do differently?"
```

### Mode 2: Deep planning
For "design X."

Send the same problem statement to each model with the same constraints. Let each propose a design independently. Then surface the differences.

```bash
codex exec "Design [thing] given [constraints]. Output: architecture diagram in ASCII, file structure, key decision points."
```

### Mode 3: Consensus poll
For "X or Y?"

Ask each model the binary question. Collect votes + reasoning. If they disagree, surface the disagreement explicitly — the user decides, not majority rule.

```bash
codex exec "[X] or [Y] for [use case]? One paragraph + final answer."
```

For gemini, the same prompt goes through `gemini -p "<prompt>"`.

## How to Run

1. **Frame the question once** — write the exact prompt you'll send to every model. Same prompt to each, so the comparison is fair.
2. **Fan out in parallel** — call each CLI in the background, collect results.
3. **Synthesize** — Claude reads all responses and produces a unified analysis:
   - Where they agree (probably right)
   - Where they disagree (the user's actual decision points)
   - Anything one model caught that others missed
4. **Recommend** — Claude states its own position last, with reasoning. Don't hide behind "the models said." Take a stance.

## Output Format

```markdown
## Multi-model consult: [topic]

### Where they agree
- [point everyone made]
- [another point]

### Where they disagree
- **Issue X**: Codex says A; Gemini says B; my position is A because Z
- **Issue Y**: ...

### One model caught
- Codex flagged [thing] that nobody else mentioned. Worth checking: [why].

### My recommendation
[Take a stance. Don't hedge.]
```

## Rules

- **Same prompt to every model.** No customizing per CLI — that biases the comparison.
- **Call CLIs directly.** Don't route through any wrapper or MCP — they can pin stale model versions or rephrase the prompt mid-flight.
- **Use the latest available model from each provider.** Each CLI's default is normally its newest model. If the user named a specific model, pass it explicitly (`codex exec -m <model> ...`); if that model isn't available, STOP and flag — don't silently fall back to an older one.
- **Take a stance in the synthesis.** "Three models said X" isn't a recommendation — what do *you* think is right and why?

## When to Use

- Architecture decisions where being wrong is expensive (database choice, auth model, deployment shape)
- Big migrations where you want adversarial review before starting
- "I think I'm missing something" moments where a fresh perspective helps
- NOT for routine tasks — overkill, slow, expensive

## When NOT to Use

- Quick syntax questions
- Anything where Claude alone is clearly sufficient
- Hot paths where latency matters — multi-model is slow
