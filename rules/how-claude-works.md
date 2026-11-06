# How Claude works

How Claude spends its own attention and helpers while it works for you. The Development Bible
covers how the code itself is built; this covers the work around it.

## Keep the chat's head clear

Claude thinks best early in a chat. As a chat fills up, answers get worse long before it is full,
so a clean chat is worth more than a long one.

- **Send wide reading to a helper.** A search across many files, a long log, a big document goes to
  a subagent (the `Agent` tool, `Explore` for searches) that reads it and returns only the answer.
  The noise stays in the helper's chat.
- **Don't read the same file twice.** Claude already has what it read and wrote this chat; a
  re-read only fills the chat.
- **Long output goes to a file**, then read only the part that matters.
- **Check work with fresh eyes.** Review a finished change in a new helper that sees the code, not
  the reasoning that wrote it; a mind that wrote the change reads past its own mistakes.
- **When a chat gets long and the work is building,** finish the step, write the note, and carry on
  in a fresh chat with a short brief. A chat that is mostly talking can carry on.

## Pick the helper's model by the job

Every helper gets its model set by name, never left to whatever the main chat uses. Use the
aliases `haiku`, `sonnet` and `opus`; they always mean the newest model of that size. Never write a
dated model id: it goes stale.

| The job | Model |
|---|---|
| Counting, listing, simple lookups | `haiku` |
| Reading and summing up: searches, research, recon | `sonnet` |
| A clear, mechanical edit (rename, move, swap a value) | `sonnet` |
| Judgement: is this a real bug, is it done, is the fix right | `opus` |
| Designing a fix, building a feature, reviewing a change | `opus` |

Cheap helpers find things; strong ones decide. A reviewer is never a weaker model than the one that
wrote the work.

## Use what's already here

The Development Bible says it for code; the same goes for everything else. Before making a new
script, skill, page or tool, check what is already installed and what the project already has,
and extend that. A second copy of something that exists drifts out of step with the first.
