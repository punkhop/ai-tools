# START-HERE — for Claude: install ai-tools for a friend

A friend said "set me up from github.com/punkhop/ai-tools", maybe with a block of answers from the
setup page. You install the pieces they picked on this computer, one stage at a time, and prove each
one works. They build apps with Claude and never read code.

**How you talk to them.** Every line they see is short and plain: what you're doing, what they need
to click or type, what they got. No file names, no code, no jargon unless they ask. One question
at a time. Never ask "do you write code".

**How you work.**

- Every stage ends with a **Verify**. It must pass before the next stage. If it fails, fix it or
  tell them exactly what to do; never skip ahead, never report a stage done that you didn't prove.
- **Your shell forgets between commands**, and it started before the install, so tools installed
  during this session aren't on your PATH yet. Start every Bash call with:

  ```bash
  SRC=~/.claude/ai-tools/src; AIT="python3 $SRC/tools/aitools.py"; [ -x /opt/homebrew/bin/brew ] && eval "$(/opt/homebrew/bin/brew shellenv)"; export PATH="$HOME/.local/bin:$HOME/.claude/bin:$PATH"
  ```

- **You can't run `sudo` and you can't click.** When a step needs a password, a click or a sign-in,
  tell them exactly what to type or click, one step at a time, and wait for "done". Commands they
  type go in a terminal window (Mac: the Terminal app; Linux: any terminal).
- Commands come for **Mac** and **Linux**; run only the one for this computer. Windows: see
  [Windows](#windows).
- **Never ask for a key or password in the chat.** Chats are saved. Keys go through a private box
  (T3 Code) or a hidden prompt they run themselves.
- **Their files come first.** `$AIT` backs up anything it replaces to
  `~/.claude/ai-tools-backup/<date>/` and never deletes their memory folder.
- After each stage passes, add a line to the progress file so a restart or a new thread can pick up:
  `echo "done: <stage>" >> ~/.claude/ai-tools/install-progress.md`.

---

## Stage 0 — Look, get the repo, read the answers

Look first, silently:

```bash
uname -s; sw_vers -productVersion 2>/dev/null; grep -m1 PRETTY /etc/os-release 2>/dev/null
for c in git python3 node npm jq curl qmd tailscale syncthing codex claude brew; do printf '%-10s %s\n' $c "$(command -v $c || echo -)"; done
node --version 2>/dev/null
ls -la ~/memory 2>/dev/null | head -3
ls ~/.claude/CLAUDE.md ~/.claude/settings.json 2>/dev/null; ls ~/.claude/skills 2>/dev/null
cat ~/.claude/ai-tools/installed.json 2>/dev/null | head -5
cat ~/.claude/ai-tools/install-progress.md 2>/dev/null
claude mcp list 2>/dev/null | grep -i qmd
```

Inside T3 Code = tools named `mcp__t3-code__…` exist (check your tool list or ToolSearch `t3-code`).
In a terminal they don't. If `install-progress.md` exists, this is a continued install: skip the
stages it lists as done.

Get the repo (or update it):

```bash
if [ -d ~/.claude/ai-tools/src/.git ]; then git -C ~/.claude/ai-tools/src fetch --depth 1 origin tag v1.0.0 && git -C ~/.claude/ai-tools/src checkout -q v1.0.0
else mkdir -p ~/.claude/ai-tools && git clone --depth 1 --branch v1.0.0 https://github.com/punkhop/ai-tools ~/.claude/ai-tools/src; fi
```

No git yet: Mac — tell them to run `xcode-select --install` in Terminal and click **Install**;
Linux — see Stage 1's package line. Then retry.

**The answers.** They look like this:

```
Where I talk to Claude: T3 Code            (T3 Code · Terminal · Both)
Computers:
- studio · Mac · main                       (nickname · Mac/Linux/Windows · main/other)
- laptop · Linux · other
Pieces:
- memory  (Memory folder and notes /note)   (one piece id per line)
Not wanted: review-multi
Image service: OpenAI                       (OpenAI · Gemini · Both)
```

- No answers pasted: send them to **https://punkhop.github.io/ai-tools/setup/** ("tick what you
  want, copy, paste it back here"), or, if they'd rather, ask the same things one at a time with
  AskUserQuestion: where they talk to Claude; their computers (nickname, kind, which is main);
  which pieces (by group, with the setup page's one-line descriptions); image service only if
  /image is picked. Where the memory folder goes and which computers Syncthing shares are never on
  the page: ask them in chat at Stage 2 and Stage 5.
- **Which computer is this?** The answers' `main` one, unless the message says "this is <nickname>"
  — then this is that other computer: install the same pieces, and skip "Your other computers".
- `dev-bible` is always installed. `chat-voice` and `pass-handoff` only when they use T3 Code. A
  piece's `needs` (in `pieces.json`) come along even if not ticked; say so in one line.
- They want to open things on their phone; assume it. The files server and Tailscale make it work.

## Stage 1 — Welcome, then prerequisites

**Welcome.** In T3 Code, show a page built from the chat kit (read `$SRC/chat/README.md`; load
`mcp__t3-code__html_preview` and `html_render` with ToolSearch). The Start shape: a `k-mission`
saying what you'll do, then one grouped `k-head` per group from `pieces.json` (its `group`) listing
what will be installed, each line `wait <name> ~ <command if any>`. A group with a single piece
joins the group before it: a one-line `k-head` draws a title, not a list.

```html
<script src="https://cdn.jsdelivr.net/gh/punkhop/ai-tools@v1.0.0/chat/kit.js"></script>
<k-reply s="work">
<k-mission title="Setting up studio">I'm installing the pieces you picked, one at a time, and checking each one works. I'll tell you when I need a click or a password.</k-mission>
<k-head label="Memory">wait Memory folder and notes ~ /note
wait Every chat saved
wait Memory search</k-head>
<k-status s="work">Working · checking what's already here
No questions yet.</k-status>
</k-reply>
```

In a terminal, say the same in five short lines: what you'll do, the pieces, that you'll ask
before replacing anything of theirs, that you'll say when you need them, and that it ends with a
checkup.

**Prerequisites** — only what the picked pieces need: `python3` and `git` always; `jq` for
safety-hooks; Node 22+ for qmd and review-multi; `curl` for files-server.

- **Mac:** `xcode-select -p` prints a path, or they run `xcode-select --install` and click
  **Install** (gives python3 and git). Homebrew: `command -v brew`; missing → they paste the
  install line from https://brew.sh into Terminal (asks for their Mac password) and run the two
  "Next steps" lines it prints. Then you run `brew install node jq`.
- **Linux:** they run one line for their distro (it asks for their password):

  ```bash
  sudo apt install -y python3 python3-venv jq git curl build-essential nodejs npm   # Debian / Ubuntu / Mint
  sudo dnf install -y python3 jq git curl gcc-c++ make nodejs npm                    # Fedora
  sudo pacman -S --needed python jq git curl base-devel nodejs npm                   # Arch
  ```

  Node under 22 afterwards (common on Debian/Ubuntu): they run
  `curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt install -y nodejs`.
  Then you make global npm installs land in their home folder, no sudo:

  ```bash
  npm config set prefix ~/.local; mkdir -p ~/.local/bin
  grep -q '.local/bin' ~/.profile 2>/dev/null || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
  grep -q '.local/bin' ~/.bashrc 2>/dev/null || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
  [ -f ~/.zshrc ] && { grep -q '.local/bin' ~/.zshrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc; }
  ```

**Then the plan.** Run `$AIT plan <every chosen id>`. It lists each file as `new`, `same` or
`different`. Nothing to say about `new` and `same`. For each `different` item, at that piece's
stage: read both copies (the plan prints the `diff` command), tell them in one or two plain lines
what theirs does that ours doesn't and the other way round, and ask: **keep yours**, **take mine**
(yours is backed up), or **skip this piece**.

**Verify:** `$AIT plan <ids>` runs without "Unknown piece" or "missing", and every tool the picked
pieces need answers `--version`.

## Stage 2 — Memory folder (memory)

Ask in chat, one question (AskUserQuestion), in plain words, never `~/`:

- **"A folder called memory, inside your home folder (the one with your name on it)" (recommended)**
  → `REAL="$HOME/memory"`.
- **"Let me pick a folder"** → open the computer's own folder picker and use what they choose:
  Mac `osascript -e 'POSIX path of (choose folder with prompt "Pick or make a folder for Claude\'s memory")'`;
  Linux `zenity --file-selection --directory --title="Folder for Claude's memory"` (or `kdialog
  --getexistingdirectory ~`); Windows/WSL ask them to type it. Cancelled → ask again.

Then say back where it is in their words ("memory, in your home folder"). On a Mac, if they picked
inside Documents, Desktop or Downloads, say in one line that macOS blocks background helpers from
those folders and offer the home-folder one instead.

```bash
REAL="<absolute path>"
mkdir -p "$REAL"/{sessions,handoffs,transcripts}
if [ "$REAL" != "$HOME/memory" ]; then
  if [ -e ~/memory ] && [ ! -L ~/memory ]; then echo "STOP: ~/memory is a real folder"; else ln -sfn "$REAL" ~/memory; fi
fi
$AIT install memory        # add --take or --keep if the plan showed a difference
```

On STOP: ask whether to move what's in `~/memory` into `REAL` first, or keep `~/memory` as the
place. Every skill uses the path `~/memory`; the shortcut points it at their folder.

**Verify:** `[ "$(cd ~/memory && pwd -P)" = "$(cd "$REAL" && pwd -P)" ] && ls ~/memory && ls ~/.claude/skills/note/SKILL.md`
shows `handoffs sessions transcripts` and the skill.

## Stage 3 — Tailscale, and the phone (tailscale)

They do this; you explain and wait.

| Mac | Linux |
|---|---|
| Install **Tailscale** from the Mac App Store (or tailscale.com/download), open it, sign in, click **Allow** on the VPN prompt. | In a terminal: `curl -fsSL https://tailscale.com/install.sh \| sh`, then `sudo tailscale up`, and open the login link it prints. |

**Phone** (if the answers say yes): install the Tailscale app, sign in with the **same account**,
turn it on. Every other computer: same account (see "Your other computers").

Then `$AIT install tailscale` (records it so `/doctor` checks it).

**Verify:**

```bash
TS=$(command -v tailscale || echo /Applications/Tailscale.app/Contents/MacOS/Tailscale)
"$TS" status | head -5
"$TS" status --json | python3 -c 'import sys,json; print(json.load(sys.stdin)["Self"]["DNSName"])'
```

Lists this computer (and the phone), and prints a name like `studio.tail1234.ts.net`. Tell them:
the first word is this computer's name in every link.

## Stage 4 — Links that open anywhere (files-server)

```bash
$AIT install files-server     # copies the server, and the Mac or Linux background job file
```

| Mac | Linux |
|---|---|
| `launchctl load -w ~/Library/LaunchAgents/com.user.files-server.plist` | `systemctl --user daemon-reload && systemctl --user enable --now files-server` then `loginctl enable-linger "$USER"` (keeps it running when they log out; if it asks for a password, they run it) |

**Verify:**

```bash
sleep 3; URL="$(~/.claude/bin/files-server url ~/memory/sessions)/"; echo "$URL"
curl -s -o /dev/null -w '%{http_code}\n' "$URL"      # 200
```

Give them the link and ask them to open it on their **phone** (Tailscale on). They see an empty
folder list. Phone can't load it on a Mac: System Settings → Network → Firewall → Options → allow
`python3` (or click **Allow** when asked). Page says "No permission": the folder is one macOS
guards; System Settings → Privacy & Security → Full Disk Access → **+** → Cmd-Shift-G →
`/usr/bin/python3`, then `launchctl kickstart -k gui/$(id -u)/com.user.files-server`. Log:
`/tmp/files-server.err`.

## Stage 5 — Syncthing (syncthing)

Keeps the memory folder the same on their computers. First ask in chat (AskUserQuestion,
multiSelect, the nicknames from the answers): "Which of your computers should share your memory
folder?" One computer only → skip this stage and say Syncthing waits until they add another.
Install it on this computer now; the others pair in "Your other computers".

| Mac | Linux |
|---|---|
| `brew install --cask syncthing`, then they open the **Syncthing** app once | they run their package manager (`sudo apt install syncthing` / `sudo dnf install syncthing` / `sudo pacman -S syncthing`); then you run `systemctl --user enable --now syncthing` |

Then they open **http://127.0.0.1:8384** and:

1. **Add Folder** → Folder Path: the memory folder (`REAL`, the real path, not the `~/memory`
   shortcut) → Folder Label: `memory` → **Save**.
2. **Actions → Show ID**: this computer's device ID. They'll paste it on each other computer.
3. Later, when another computer shows up: **Add Remote Device** → paste that computer's ID → name it
   by its nickname → on the **Sharing** tab tick `memory` → **Save**. Accept the matching prompt on
   the other side.

On a second computer (the "this is <nickname>" case): install, then accept the "wants to share
folder memory" prompt and set its path to that computer's memory folder.

Then `$AIT install syncthing`.

**Verify:** `curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8384` → 200 (or 401: running,
with a password), and they see the `memory` folder in the Syncthing page.

## Stage 6 — Memory search (qmd)

```bash
npm install -g @tobilu/qmd          # Linux: lands in ~/.local/bin, no sudo
qmd --version
qmd collection add "$(cd ~/memory && pwd -P)" --name memory      # the real path, not the shortcut
claude mcp add --scope user qmd -e PATH="$(dirname "$(command -v node)"):/usr/bin:/bin" -- "$(command -v qmd)" mcp
qmd update && qmd embed             # the first run downloads a ~330 MB model; tell them it takes a while
$AIT install qmd                    # the upkeep script and its background jobs
```

| Mac | Linux |
|---|---|
| `for j in qmd-index qmd-upgrade; do launchctl load -w ~/Library/LaunchAgents/com.user.$j.plist; done` | `systemctl --user daemon-reload && systemctl --user enable --now qmd-index.timer qmd-upgrade.timer` |

`npm install` fails while compiling: Mac → the command-line tools from Stage 1; Linux → the
`build-essential` / `gcc-c++ make` / `base-devel` package.

**Verify:**

```bash
qmd status | grep -E 'Total|Updated'                 # "Total: 0 files" is right while memory is empty
qmd collection list | grep '^memory '
claude mcp list 2>&1 | grep -i qmd                   # "Connected"
~/.claude/bin/qmd-upkeep index; tail -1 /tmp/qmd-upkeep.log      # ok
launchctl list | grep com.user.qmd                   # Mac: both listed
systemctl --user list-timers --no-pager | grep qmd   # Linux: both listed
```

The first real search downloads two more models (about 1.9 GB); expect a pause then.

## Stage 7 — Safety nets and saved chats (safety-hooks, session-save)

```bash
$AIT install safety-hooks
$AIT install session-save
```

**Verify:**

```bash
echo '{"tool_input":{"file_path":"/x/.env"}}' | python3 ~/.claude/hooks/block-secrets.py; echo "exit $?"   # exit 2 = blocks
T=$(mktemp -d); (cd "$T" && git init -q && touch scratch.txt)
printf '{"tool_input":{"command":"rm -rf %s/scratch.txt"}}' "$T" | ~/.claude/hooks/block-rm-untracked.sh; echo "exit $?"; rm -r "$T"   # exit 2
bash -n ~/.claude/hooks/session-save.sh && bash -n ~/.claude/hooks/context-budget-feedback.sh && echo ok
```

The hooks start working after the restart (Stage 11) once Stage 10 registers them.

## Stage 8 — Skills and rules

One `$AIT install <id>` per chosen piece, in this order, each with its keep/take/skip answer from
the plan: `dev-bible`, `chat-voice`, `html`, `plain-voice`, `pass-handoff`, `doctor`,
`spec-logic-design`, `prototype`.

**Verify:** `ls ~/.claude/skills/*/SKILL.md` lists every skill picked (except kept or skipped
ones, which stay theirs); `ls ~/.claude/ai-tools/bibles ~/.claude/ai-tools/rules 2>/dev/null` shows
the bible and the rules picked.

## Stage 9 — Images (image)

```bash
$AIT install image
PY=python3; python3 -m pip install --user --quiet pillow openai 2>/dev/null || {
  python3 -m venv ~/.claude/ai-tools/venv && ~/.claude/ai-tools/venv/bin/python -m pip install --quiet pillow openai; PY=~/.claude/ai-tools/venv/bin/python; }
```

Install `openai` for OpenAI, `google-genai` for Gemini, both for Both. pip refusing with
"externally-managed-environment" is normal on Linux and Homebrew Python: the private environment
above is the fix, and the image skill uses it from then on.

**The key.** If they don't have one yet, tell them where: OpenAI — platform.openai.com → API keys →
Create new secret key (needs billing set up); Gemini — aistudio.google.com → Get API key → Create
API key.

- **In T3 Code:** load `mcp__t3-code__request_secret` with ToolSearch and call it with
  `delivery: "file"`, label "OpenAI API key" (or "Gemini API key"). They paste into the private box.
  Then run `python3 ~/.claude/skills/image/scripts/save_key.py OPENAI_API_KEY --from-file <the file>`.
  Never read, print or `cat` that file.
- **In a terminal:** ask them to open a second terminal window and run
  `python3 ~/.claude/skills/image/scripts/save_key.py OPENAI_API_KEY` (or `GEMINI_API_KEY`) and
  paste the key when asked. The paste stays hidden.

From here on `PY` is the private environment's Python when it exists: put
`PY=~/.claude/ai-tools/venv/bin/python; [ -x "$PY" ] || PY=python3` at the top of each command.

The projects folder: `$PY ~/.claude/skills/image/scripts/new_project.py --set-folder ~/memory/images`
(or wherever they'd like; ask once, suggest that one).

**Verify:** `$PY ~/.claude/skills/image/scripts/generate-template.py --check` shows their key as
`found` and `pillow: installed`; `$PY ~/.claude/skills/image/scripts/new_project.py --where` prints
the folder.

## Stage 9b — Second opinion (review-multi)

```bash
npm install -g @openai/codex
$AIT install review-multi
```

They run `codex login` in a terminal window and sign in with their ChatGPT account in the browser
that opens.

**Verify:** `codex --version && codex login status` → signed in.

## Stage 10 — Settings and CLAUDE.md

```bash
$AIT settings <every installed id>
$AIT claude-md <every installed id>
```

`settings` adds hooks and permissions to `~/.claude/settings.json` and never removes theirs.
`claude-md` writes one block between `<!-- ai-tools:start v1.0.0 -->` and `<!-- ai-tools:end -->` in
`~/.claude/CLAUDE.md`; their own lines stay as they are. Both back up first. If `settings` says
their file isn't valid JSON, show them the error line in plain words and fix it with them first.

**Verify:**

```bash
python3 -c 'import json,os; s=json.load(open(os.path.expanduser("~/.claude/settings.json"))); print(sorted(h["hooks"][0]["command"] for v in s.get("hooks",{}).values() for h in v))'
grep -c 'ai-tools:start' ~/.claude/CLAUDE.md      # 1
sed -n '/ai-tools:start/,/ai-tools:end/p' ~/.claude/CLAUDE.md | grep '^@' | sed 's/^@//' | while read f; do f="${f/#\~/$HOME}"; [ -f "$f" ] && echo "ok $f" || echo "MISSING $f"; done
```

Every hook picked is listed; one block; every `@` import points at a file that exists.

## Stage 11 — Restart

Settings, hooks and the memory-search connection load only when Claude starts. Save where you are:

```bash
{ echo "Reached stage 12 (checkup). Repo: ~/.claude/ai-tools/src"; echo "Answers:"; cat <<'ANS'
<the answers block, as pasted>
ANS
} >> ~/.claude/ai-tools/install-progress.md
command -v qmd >/dev/null && ~/.claude/bin/qmd-upkeep index
```

Tell them: **quit T3 Code completely** (Mac: Cmd-Q; Linux: close the window and quit it from the
tray if it stays) **and open it again**, come back to this thread and type **continue**. If the
thread has forgotten: *"Continue my ai-tools install from ~/.claude/ai-tools/install-progress.md"*.
In a terminal: quit `claude` and start it again, then the same sentence.

## Stage 12 — Checkup, first note, done

1. Run `/doctor`. Fix every FAIL (each line says how) and re-run until there are none. "No
   transcripts yet" and "no upkeep runs logged yet" are normal on day one.
2. With qmd: one real search through the qmd tool for "ai-tools" — show it answers.
3. With memory: run `/note` about this install (what was set up, where the memory folder is, this
   computer's name). With files-server and a phone: ask them to open the note's link on the phone.
   That link opening is the proof it all works end to end.
4. Delete `~/.claude/ai-tools/install-progress.md`.

**Done page.** In T3 Code, a chat-kit Done page (`<k-reply s="ok" note="<the note's link>">`): a
`k-head` title "ai-tools · installed on <nickname>", then the same grouped `k-head` lists as the welcome,
each line `ok <name> ~ <try line from pieces.json>`, then the note in `k-links`. In a terminal: a short list,
one line per piece: its name and its "try this".

Then, if the answers list other computers, go on to "Your other computers".

---

## Your other computers

For each computer in the answers that isn't this one, give them these steps, one computer at a
time, and wait while they do it. Name the computer by its nickname every time.

1. **Tailscale** on it, signed in to the **same account** (Stage 3's table).
2. **Claude Code** and **T3 Code** on it, both signed in.
3. Open a new T3 Code thread there, paste the **same answers**, and add one line:
   **"this is <nickname>"**. Claude there installs the same pieces.
4. **Syncthing pairing** (if they share the memory folder with it): on this computer, Syncthing →
   **Add Remote Device** → paste the other computer's device ID (Actions → Show ID on that one) →
   **Sharing** tab → tick `memory` → **Save**. On the other one, accept the folder and point it at
   its memory folder.
5. **Add it to T3 Code here**, so one window runs Claude on any computer. On the **other** computer:
   T3 Code → **Settings** → **Connections** → switch on **Tailscale HTTPS** (click **Enable**; it
   restarts). Then **Authorized clients** → **Create link** → keep **Standard** → **Create link** →
   **Share** → pick the Tailscale address under "Reach this machine via" → **Copy link**. The link
   works once and expires in 5 minutes; treat it like a password. To get it across to this
   computer: send it to yourself (a note that syncs, a message to yourself), or use **Copy code
   only** and type the short code here in step 6, with the address `<nickname's Tailscale name>`
   in **Host**.
6. On **this** computer: **Settings** → **Connections** → **Environments** → **Add environment** →
   **Remote link** → paste the whole link into **Host** (both fields fill) → **Add environment**.
   The computer now shows in Environments.
7. **A project on it:** sidebar → **Add project** → pick that computer → **Local folder**, **New
   project** or a Git address. When a project is on two computers, a new thread shows a **Run on**
   picker under the message box: choose where it runs.

The other computer has to stay on, awake and running T3 Code for this to work. Simpler but needs an
account: **T3 Connect** — sign in to T3 Connect on both and switch on **T3 Connect** in
Settings → Connections on the other one.

**Phone app (optional):** install **T3 Code** from the App Store or Google Play; on a computer make
a pairing link as in step 5 and scan its QR code from the app's **Add environment** screen. The
phone needs Tailscale on.

---

## Updates

When they say "check ai-tools for updates":

```bash
git -C ~/.claude/ai-tools/src fetch --depth 1 --tags -q
NEW=$(git -C ~/.claude/ai-tools/src tag --sort=-v:refname | head -1); echo "newest $NEW"
git -C ~/.claude/ai-tools/src -c advice.detachedHead=false checkout -q "$NEW"
python3 ~/.claude/ai-tools/src/tools/aitools.py status
```

Show the `CHANGELOG.md` sections newer than their installed version, in plain words. For each
piece marked `update` or `differ`: `$AIT plan <id>`, the same keep / take / skip rule as the
install (a `different` file they changed themselves: say so), then `$AIT install <id> --take` or
`--keep`. Finish with `$AIT settings <installed ids>`, `$AIT claude-md <installed ids>`, the restart
(Stage 11) and `/doctor`. New pieces in the newer version: name them with their one-liner and offer
them.

---

## Uninstall

Their memory folder and saved notes are never touched.

| Mac | Linux |
|---|---|
| `for j in files-server qmd-index qmd-upgrade; do launchctl unload -w ~/Library/LaunchAgents/com.user.$j.plist 2>/dev/null; done` | `systemctl --user disable --now files-server qmd-index.timer qmd-upgrade.timer 2>/dev/null` |

```bash
claude mcp remove qmd --scope user 2>/dev/null
python3 ~/.claude/ai-tools/src/tools/aitools.py uninstall          # or: uninstall <id> <id> for some pieces
systemctl --user daemon-reload 2>/dev/null
```

`uninstall` removes the files it installed, the hooks and permissions it added, and its block in
`CLAUDE.md`. It puts nothing else back; the old copies are in `~/.claude/ai-tools-backup/`. If the
install replaced one of their own skills (`ls ~/.claude/ai-tools-backup/*/.claude/skills`), offer to
copy it back. Then ask before each of these: `npm uninstall -g @tobilu/qmd @openai/codex`;
`rm -rf ~/.cache/qmd ~/.config/qmd ~/.local/share/files-server`; `rm -rf ~/.claude/ai-tools` (this also deletes their saved image
keys). Tailscale, Syncthing and T3 Code are apps they remove themselves. If `~/memory` is a
shortcut, `rm ~/memory` removes only the shortcut.

---

## Windows

Less tested; say so. Claude Code on Windows runs its commands in **Git Bash**, so the Linux-style
commands mostly work there.

- Pieces that are plain files work as they are: dev-bible, chat-voice, html, plain-voice, memory,
  pass-handoff, doctor, spec-logic-design, prototype, image, review-multi. `$AIT` runs with
  `python` from Git Bash.
- **Tailscale** and **Syncthing** have Windows installers (tailscale.com/download,
  syncthing.net/downloads — SyncTrayzor or the official build).
- **Background jobs** (files-server, memory-search upkeep) have no launchd or systemd: make them with
  Task Scheduler, e.g. `schtasks /Create /SC MINUTE /MO 30 /TN qmd-index /TR "bash -lc '~/.claude/bin/qmd-upkeep index'"`
  and `schtasks /Create /SC ONLOGON /TN files-server /TR "bash -lc '~/.claude/bin/files-server start'"`.
- Hooks: `jq` from `winget install jqlang.jq`. If a hook misbehaves, leave safety-hooks off and tell
  them plainly.
