---
name: browser
description: Open a page in a private Chrome window and use it like a person would — click through the app, fill forms, take screenshots, read console errors — to check that something Claude built really works. Uses the chrome-devtools MCP with a fresh, throwaway profile, never the person's own logged-in Chrome. Use when someone types /browser, asks to "open it", "click through it", "check it in the browser", "screenshot the page", or after building or fixing anything that shows in a browser.
---

# /browser — open it and click through it

The person builds apps with Claude and does not read code. "It works" means it works on the
screen, so after building or fixing anything with a page, open the page and use it. Show them the
screenshot; describe what you saw in plain words.

## The browser

The `chrome-devtools` MCP (tools named `mcp__chrome-devtools__…`) starts its own Chrome window
with a **fresh, empty profile** each time (`--isolated`): no history, no saved passwords, nobody
logged in, and it is thrown away when the window closes. It never touches the person's own
Chrome, its tabs or its logins.

No `mcp__chrome-devtools__` tools? The piece isn't set up on this computer, or Claude hasn't been
restarted since. Say so in one line and suggest "check my ai-tools setup" (or `/doctor`).

## The usual walk

1. **Start the app** if it isn't running (`npm run dev` or whatever the project's README says) and
   note its address, e.g. `http://localhost:5173`. Wait until it answers.
2. **Open it:** `new_page` with the address (or `navigate_page` on the open one).
3. **Look:** `take_snapshot` gives the page as text with an id (`uid`) for every button, link and
   field. Use it to find what to click. It costs far less than a screenshot.
4. **Use it:** `click` (by `uid`), `fill` / `fill_form`, `press_key`, `wait_for` some text to show.
   Walk the path the person would: the main thing the app does, start to finish.
5. **Check for errors:** `list_console_messages` after each step. A red error is a bug even when the
   page looks fine; fix it at its source.
6. **Screenshot:** `take_screenshot` of what matters (the finished state, or the bug). For a phone
   view, `resize_page` to 390×844 first, or `emulate` a phone.
7. **Tell them:** what you did, what happened, the screenshot. Found a bug: fix it, then walk the
   same path again and show the after.

## Rules

- **Never the person's own Chrome.** Don't connect to their running browser, copy their profile or
  cookies, or ask them to turn on remote debugging. Need to be logged in? Fill in the app's sign-in
  form with a test account, or ask them for one; never their real password in the chat.
- **Don't steal their screen.** Open new pages with `background: true` where the tool allows it.
- **One window is yours.** Close the pages you opened when you're done (`close_page`); leave any you
  didn't open alone.
- **Public sites are fine to read and screenshot.** Don't sign up, buy, post or send anything on a
  real site unless the person asked for exactly that.
- Screenshots and snapshots fill the chat fast. Prefer `take_snapshot` for finding things and save
  screenshots for what the person should see.

## When it won't start

| What you see | What to do |
|---|---|
| "Could not find Chrome" | Install Google Chrome (google.com/chrome). Linux with only Chromium: re-add the MCP with `--executablePath "$(command -v chromium)"` (see START-HERE, browser stage). |
| Tools missing after setup | Claude has to restart once after an MCP is added. |
| The page is blank or "connection refused" | The app isn't running, or it's on another port; check the dev server's output. |
| Stuck or "page closed" errors | `list_pages`, pick yours with `select_page`, or close and open a new page. |
