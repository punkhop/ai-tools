# Changelog

Newest first. Claude reads this when you say "check ai-tools for updates".

## v1.3.0

- **Orbit replaces the T3 Clawd theme (T3 Code only).** Orbit is a near-black theme built for
  reading all day, with a chartreuse green accent and a deep olive green in light mode. New chat is
  a green plus beside Search, and chat rows drop the project badge, Claude icon and PR badge. It is
  built from @rohit3a's T3 Clawd. Updating removes the T3 Clawd file; if you had it on, Claude
  switches you to Orbit, or pick another theme in **Settings → Appearance**.

## v1.2.0

- **T3 Clawd theme (T3 Code only).** A new optional piece under Extras: a Claude look for T3 Code,
  made by @rohit3a, with a simpler sidebar (New chat under search, no Projects buttons, Working
  under your recent chats). Off unless you tick it.

## v1.1.0

From Abbie's install, thank you Abbie.

- **Your memory folder stays where you keep it.** The install now always asks where your memory
  folder is (or where to make one) and remembers the answer. Every piece is written to use that
  folder, so there is no `~/memory` shortcut any more, and an update never points things back at
  `~/memory`. Updating from v1.0.0: Claude asks once, offering the folder you already use.
- **"Keep mine" sticks.** When you keep your own version of a file, later installs and updates leave
  it alone and don't ask again.
- **Memory search works when Node comes from nvm.** The install saves where qmd and Node live, and
  the 30-minute job uses them; before, it failed quietly for anyone using nvm.
- **Search by meaning is checked, not assumed.** The install proves notes are embedded, the
  30-minute job reports a failure when notes are left waiting, and the checkup warns when nothing is
  embedded or notes are piling up.
- **Renamed two commands** that clashed with Claude Code's own: /doctor is now **/checkup** and
  /status is now **/catchup**. The update removes the old ones.

## v1.0.0

First release. Twenty-four pieces to pick from on the setup page: the reply format, chat pages (T3 Code),
report pages, the memory folder with notes, saved chats, picking up where you left off, memory search,
fresh threads, Tailscale, links that open anywhere, Syncthing, the Development Bible, how Claude works,
safety nets, fewer "allow this?" prompts, passwords in 1Password, the checkup, project status, the
browser, plan before building, prototypes, images, a second opinion from Codex, and a status bar for
the terminal.

Works in T3 Code, the Claude desktop app's Code tab, and a terminal. Once a week, at the start
of a session, Claude checks for a newer ai-tools and mentions it once; nothing updates without
you asking. Memory search keeps itself current on its own.
