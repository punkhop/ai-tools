#!/usr/bin/env python3
# files-server-serve.py — static http server, identical to `python3 -m http.server`
# but it SWALLOWS client-disconnect noise. Stock http.server dumps a full traceback
# every time a client hangs up mid-response (BrokenPipe/ConnectionReset) — a browser
# closing a tab, a curl ^C. Those aren't errors, and they would fill files-server.err.
# socketserver calls handle_error for any request-thread exception and prints it by
# default — we override that one point.
#
# Usage: files-server-serve.py <port> <directory> [bind-address]
import sys, os, re, json, io
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8181
directory = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
# Bind address. Defaults to 0.0.0.0 when run by hand, but files-server.sh passes this
# machine's Tailscale address, so the served folders (memory, dev, /tmp) are reachable
# only over Tailscale — not by every device on the home or cafe Wi-Fi.
bind = sys.argv[3] if len(sys.argv) > 3 else "0.0.0.0"


class QuietServer(ThreadingHTTPServer):
    daemon_threads = True
    # socketserver's default listen backlog is 5: a page with a dozen images opens more connections
    # than that at once and the overflow is refused, so pictures draw as broken.
    request_queue_size = 128

    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, (BrokenPipeError, ConnectionResetError)):
            return  # client hung up mid-response — expected, not an error
        super().handle_error(request, client_address)


class NoCacheHandler(SimpleHTTPRequestHandler):
    """Never let a browser reuse a file without asking us first.

    Stock SimpleHTTPRequestHandler sends Last-Modified and NOTHING else. With no
    Cache-Control, the browser falls back to the heuristic in RFC 9111 §4.2.2 —
    roughly 10% of the time since Last-Modified — and reuses the file WITHOUT
    revalidating. So a stylesheet edited an hour ago is served from cache for
    the next six minutes, and the page you are looking at is not the page on
    disk.

    Everything this server hosts is a live working artifact —
    a report being rewritten, a prototype being iterated on — so there is no
    case where serving a stale copy is the behaviour anyone wants.

    `no-cache` is not `no-store`: the browser keeps the copy and revalidates,
    so an unchanged file still costs one 304 and no body. Free, and correct.
    """

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    # --- byte ranges, so audio and video actually work -----------------------
    # Stock SimpleHTTPRequestHandler ignores Range and answers 200 with the whole
    # file. A browser then cannot seek a <video> and will not start playing a long
    # clip until the entire thing has arrived. Every clip and screen recording
    # served from here needs this; without it a video link is a download link.
    def send_head(self):
        md = self._markdown_page()
        if md is not None:
            return md
        rng = self.headers.get("Range")
        m = re.fullmatch(r"bytes=(\d*)-(\d*)", rng.strip()) if rng else None
        if not m:
            return super().send_head()
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        try:
            f = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None
        size = os.fstat(f.fileno()).st_size
        first, last = m.group(1), m.group(2)
        if first == "":
            if last == "":
                f.close()
                return super().send_head()
            start, end = max(0, size - int(last)), size - 1
        else:
            start = int(first)
            end = min(int(last), size - 1) if last else size - 1
        if start >= size or start > end:
            f.close()
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None
        f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        return _Slice(f, end - start + 1)


    # --- markdown reads as a page in a browser --------------------------------
    # A .md link opened in a browser (T3 Code's built-in one included) used to show
    # raw text. A browser asks for text/html, so it gets the file drawn with the
    # report stylesheet; curl, agents and `?raw` still get the bytes on disk.
    MD_PAGE = r"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<link rel="stylesheet" href="/assets/report.css"></head>
<body><article class="r-md" id="md"></article>
<script id="src" type="application/json">{src}</script>
<script type="module">
import {{ marked }} from "https://cdn.jsdelivr.net/npm/marked@15/lib/marked.esm.js";
const text = JSON.parse(document.getElementById("src").textContent)
  .replace(/^---\n[\s\S]*?\n---\n/, "");
document.getElementById("md").innerHTML = marked.parse(text);
</script></body></html>"""

    def _markdown_page(self):
        path = self.translate_path(self.path)
        query = self.path.partition("?")[2]
        if (not path.lower().endswith((".md", ".markdown")) or "raw" in query.split("&")
                or "text/html" not in (self.headers.get("Accept") or "")
                or not os.path.isfile(path)):
            return None
        with open(path, encoding="utf-8", errors="replace") as f:
            src = json.dumps(f.read()).replace("</", "<\\/")
        body = self.MD_PAGE.format(title=os.path.basename(path), src=src).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        return io.BytesIO(body)

class _Slice:
    """File object that stops at `remaining` bytes, for shutil.copyfileobj."""

    def __init__(self, f, remaining):
        self.f, self.remaining = f, remaining

    def read(self, n=-1):
        if self.remaining <= 0:
            return b""
        if n is None or n < 0:
            n = self.remaining
        chunk = self.f.read(min(n, self.remaining))
        self.remaining -= len(chunk)
        return chunk

    def close(self):
        self.f.close()


handler = partial(NoCacheHandler, directory=directory)
with QuietServer((bind, port), handler) as httpd:
    httpd.serve_forever()
