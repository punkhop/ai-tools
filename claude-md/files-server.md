## Links

- **Every file you point me at is an http link**, never `file://`:
  `~/.claude/bin/files-server url <abs-path>` → `[name](http://<machine>:8181/...)`.
  Only `~/memory`, `~/dev` and `/tmp` are served; anything else gets its plain path.
