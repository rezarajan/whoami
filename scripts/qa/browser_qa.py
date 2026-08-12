#!/usr/bin/env python3
"""Behavioral QA for the CV/resume site, driven over the Chrome DevTools
Protocol with a stdlib-only WebSocket client (no pip dependencies).

Usage:
    (cd hugo && hugo server --port 1313 &)   # site must be running
    scripts/qa/browser_qa.py [port]          # default 1313

Asserts the interaction invariants documented in CLAUDE.md:
  - scroll-spy: the active nav section matches the section at the top of the
    viewport (fixed 25% activation line), with the last section taking over
    only at true page bottom;
  - nav clicks pin the clicked section, including in the mobile pill bar,
    and small subsequent scrolls do not steal the highlight;
  - floating controls hide on scroll-down, return on scroll-up, and sit at
    the bottom corner whenever the sticky nav bar layout is active
    (portrait AND landscape below 88rem);
  - certificate links open the in-page preview modal without navigation,
    and Escape closes it.

Exits non-zero if any check fails.
"""
import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import time
import urllib.request

SITE_PORT = sys.argv[1] if len(sys.argv) > 1 else "1313"
CDP_PORT = 9333
BASE = f"http://localhost:{SITE_PORT}"
FAILURES = []


# --- minimal CDP client -----------------------------------------------------

def ws_connect(url):
    path = url.split(f":{CDP_PORT}")[1]
    s = socket.create_connection(("127.0.0.1", CDP_PORT))
    key = base64.b64encode(os.urandom(16)).decode()
    req = (
        f"GET {path} HTTP/1.1\r\nHost: 127.0.0.1:{CDP_PORT}\r\n"
        "Upgrade: websocket\r\nConnection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(req.encode())
    buf = b""
    while b"\r\n\r\n" not in buf:
        buf += s.recv(4096)
    assert b"101" in buf.split(b"\r\n")[0], buf
    return s


def _recv_exact(s, n):
    buf = b""
    while len(buf) < n:
        chunk = s.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("closed")
        buf += chunk
    return buf


def ws_send(s, payload):
    mask = os.urandom(4)
    header = b"\x81"
    n = len(payload)
    if n < 126:
        header += bytes([0x80 | n])
    elif n < 65536:
        header += bytes([0x80 | 126]) + struct.pack(">H", n)
    else:
        header += bytes([0x80 | 127]) + struct.pack(">Q", n)
    s.sendall(header + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))


def ws_recv(s):
    b1, b2 = _recv_exact(s, 2)
    n = b2 & 0x7F
    if n == 126:
        n = struct.unpack(">H", _recv_exact(s, 2))[0]
    elif n == 127:
        n = struct.unpack(">Q", _recv_exact(s, 8))[0]
    if b2 & 0x80:
        _recv_exact(s, 4)
    return _recv_exact(s, n)


class Tab:
    def __init__(self, width, height, url):
        for browser in ("google-chrome", "chromium", "chromium-browser"):
            if shutil.which(browser):
                break
        else:
            raise SystemExit("no chrome/chromium found")
        self.proc = subprocess.Popen(
            [browser, "--headless", "--disable-gpu",
             f"--remote-debugging-port={CDP_PORT}",
             "--force-prefers-reduced-motion",  # deterministic, instant scrolls
             f"--window-size={width},{height}", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        tab = None
        for _ in range(50):
            try:
                req = urllib.request.Request(
                    f"http://127.0.0.1:{CDP_PORT}/json/new?{url}", method="PUT")
                tab = json.loads(urllib.request.urlopen(req).read())
                break
            except Exception:
                time.sleep(0.2)
        if not tab:
            raise SystemExit("could not open CDP tab; is the site running?")
        self.sock = ws_connect(tab["webSocketDebuggerUrl"])
        self.msg_id = 0
        time.sleep(1.5)  # page load

    def rpc(self, method, params=None):
        self.msg_id += 1
        ws_send(self.sock, json.dumps(
            {"id": self.msg_id, "method": method, "params": params or {}}).encode())
        while True:
            msg = json.loads(ws_recv(self.sock))
            if msg.get("id") == self.msg_id:
                return msg.get("result", {})

    def js(self, action, read, wait_ms=450):
        # Act, wait for rAF/scroll handlers to settle, then read state.
        result = self.rpc("Runtime.evaluate", {
            "expression": "(async () => { " + action + "; "
                          f"await new Promise(r => setTimeout(r, {wait_ms})); "
                          + read + "; return window.__qa__; })()",
            "awaitPromise": True, "returnByValue": True,
        })
        return result.get("result", {}).get("value")

    def close(self):
        self.proc.terminate()
        self.proc.wait()


def check(name, actual, expected):
    ok = actual == expected
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {actual!r}"
          + ("" if ok else f" (expected {expected!r})"))
    if not ok:
        FAILURES.append(name)


ACTIVE = ("window.__qa__ = (document.querySelector('.cv-nav a.active')"
          " || {textContent: 'NONE'}).textContent.trim()")
HIDDEN = ("window.__qa__ = ('controlsHidden' in document.documentElement.dataset)"
          " ? 'hidden' : 'visible'")
CLICK_EDU = 'document.querySelector(".cv-nav a[href=\'#education\']").click()'


# --- scroll-spy: desktop ----------------------------------------------------
print("== scroll-spy (desktop 1600x1000) ==")
t = Tab(1600, 1000, f"{BASE}/")
check("at top", t.js("window.scrollTo(0, 0)", ACTIVE), "Summary")
check("mid scroll", t.js(
    "document.querySelector('#experience').scrollIntoView()", ACTIVE), "Experience")
check("click education", t.js(CLICK_EDU, ACTIVE), "Education")
check("true bottom", t.js(
    "window.scrollTo(0, document.documentElement.scrollHeight)", ACTIVE, 700), "Courses")
t.close()

# --- scroll-spy: mobile pill bar --------------------------------------------
print("== scroll-spy (mobile 390x844) ==")
t = Tab(390, 844, f"{BASE}/")
check("click education", t.js(CLICK_EDU, ACTIVE), "Education")
check("nudge keeps it", t.js("window.scrollBy(0, 40)", ACTIVE, 700), "Education")
check("second nudge", t.js("window.scrollBy(0, 40)", ACTIVE, 700), "Education")
check("true bottom", t.js(
    "window.scrollTo(0, document.documentElement.scrollHeight)", ACTIVE, 700), "Courses")

# --- floating controls ------------------------------------------------------
print("== floating controls (mobile 390x844) ==")
check("visible at top", t.js("window.scrollTo(0, 0)", HIDDEN, 700), "visible")
check("hidden scrolling down", t.js(
    "window.scrollTo(0, 300); window.scrollBy(0, 400)", HIDDEN, 700), "hidden")
check("visible scrolling up", t.js("window.scrollBy(0, -200)", HIDDEN, 700), "visible")
t.close()

print("== floating controls (landscape 844x390) ==")
t = Tab(844, 390, f"{BASE}/")
check("pills below sticky nav", t.js(
    "void 0",
    "var r = document.querySelector('.theme-slider').getBoundingClientRect();"
    "var n = document.querySelector('.cv-nav').getBoundingClientRect();"
    "window.__qa__ = (r.top > n.bottom) ? 'clear-of-nav' : 'overlapping'"), "clear-of-nav")
t.close()

# --- certificate preview modal ----------------------------------------------
print("== certificate preview modal (desktop 1600x1000) ==")
t = Tab(1600, 1000, f"{BASE}/")
check("opens in page", t.js(
    "document.querySelector('a[data-pdf-preview]').click()",
    "var m = document.querySelector('.pdf-modal');"
    "window.__qa__ = (!m.hidden && location.pathname.indexOf('certificates') < 0)"
    " ? 'open-in-page' : 'wrong'"), "open-in-page")
check("escape closes", t.js(
    "document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}))",
    "window.__qa__ = document.querySelector('.pdf-modal').hidden"
    " ? 'closed' : 'open'"), "closed")
t.close()

print(f"\n{len(FAILURES)} failure(s)" if FAILURES else "\nall checks passed")
sys.exit(1 if FAILURES else 0)
