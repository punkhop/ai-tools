# Chat pages — the reply format, drawn in T3 Code (always on, T3 Code only)

Adds to `reply-format.md`; every rule there still holds. This file applies only in a T3 Code
thread (tools named `mcp__t3-code__…` exist). In a terminal or the Claude desktop app, ignore it:
replies stay markdown, never an HTML page.

## In T3 Code, the report is a chat-kit page

T3 Code renders HTML in the thread. Before the first reply that changes state, read
`~/.claude/ai-tools/chat/README.md` and load the T3 tools `html_preview` and
`html_render` (deferred tools — fetch them with ToolSearch). A markdown done report in a T3 thread
is the failure, not a fallback.

- Every reply that changes state is one page built only from the chat kit, in one of its five
  reply shapes. Never invent a new shape.
- The status bar is the glance, and it ends every page: Done · Answer questions · Your turn (a
  thing the user does by hand) · Working · Waiting.
- T3's sidebar shows Done the moment the turn ends, so a turn never ends on Working.
- Text under the page: one line at most, only what the page can't say. Every question the user
  asked gets its answer in the text, plainly, first — a page never swallows their question.
- A plain answer to a question, with nothing changed, is text only — no page.
