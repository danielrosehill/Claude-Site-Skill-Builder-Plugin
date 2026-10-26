#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["websockets>=12"]
# ///
"""Session keep-alive for a site driven through a CDP browser (a persistent agent browser).

While an agent is actively driving a signed-in session, this pings one lightweight
same-origin endpoint from inside the site's own tab, so the request carries the
user's real session, at a fixed interval. It stops by itself after --max-minutes, when the stop file
appears, when the tab closes, or when the session has already expired. It never
signs in and never touches credentials. An expired session is reported, not repaired.

Copy into a site plugin's scripts/ only when the profile records a short idle
timeout (profile.session.keepalive). For claude-in-chrome, which exposes no CDP
endpoint, use the in-page snippet in the session-keepalive skill instead.

Output: one JSON object per line. Exit codes: 0 stopped cleanly, 2 usage or no
matching tab, 3 session expired, 4 CDP connection lost.
"""
import argparse
import asyncio
import itertools
import json
import os
import random
import sys
import time
import urllib.request
from datetime import datetime, timezone

import websockets

PING_JS = """
(async () => {
  try {
    const r = await fetch(%s, {credentials: 'include', redirect: 'manual', cache: 'no-store'});
    return {status: r.status, type: r.type, href: location.href};
  } catch (e) {
    return {error: String(e), href: location.href};
  }
})()
"""


def emit(event, **fields):
    print(json.dumps({"t": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                      "event": event, **fields}), flush=True)


def find_target(cdp, origin):
    with urllib.request.urlopen(f"{cdp.rstrip('/')}/json/list", timeout=10) as resp:
        targets = json.load(resp)
    pages = [t for t in targets if t.get("type") == "page" and t.get("url", "").startswith(origin)]
    return pages[0] if pages else None


def expired(result, login_markers):
    """A session probe is expired if it is refused, redirected, or lands on a login URL."""
    if "error" in result:
        return False                        # network blip; let the next ping decide
    if result.get("status") in (401, 403, 419, 440):
        return True
    if result.get("type") == "opaqueredirect":
        return True                         # same-origin ping redirected: almost always to sign-in
    return any(m in result.get("href", "") for m in login_markers)


async def run(args):
    target = find_target(args.cdp, args.origin)
    if not target:
        emit("no-tab", origin=args.origin)
        return 2
    emit("start", tab=target["url"], ping=args.ping, every_s=args.every, max_min=args.max_minutes)

    deadline = time.monotonic() + args.max_minutes * 60
    ids = itertools.count(1)
    try:
        async with websockets.connect(target["webSocketDebuggerUrl"], max_size=None) as ws:
            while True:
                if args.stop_file and os.path.exists(args.stop_file):
                    emit("stop", reason="stop-file")
                    return 0
                if time.monotonic() >= deadline:
                    emit("stop", reason="max-minutes")
                    return 0

                msg_id = next(ids)
                await ws.send(json.dumps({
                    "id": msg_id, "method": "Runtime.evaluate",
                    "params": {"expression": PING_JS % json.dumps(args.ping),
                               "awaitPromise": True, "returnByValue": True},
                }))
                while True:
                    reply = json.loads(await ws.recv())
                    if reply.get("id") == msg_id:
                        break
                result = reply.get("result", {}).get("result", {}).get("value") or {"error": "no value"}
                emit("ping", **result)
                if expired(result, args.login_marker):
                    emit("expired", hint="ask the user to sign in again; do not re-authenticate")
                    return 3

                # +/-15% jitter so the pings don't fall on an exact beat
                wait = args.every * random.uniform(0.85, 1.15)
                await asyncio.sleep(min(wait, max(0.0, deadline - time.monotonic())))
    except (websockets.ConnectionClosed, OSError) as exc:
        emit("stop", reason="tab-closed-or-cdp-lost", detail=str(exc))
        return 4


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--cdp", default="http://127.0.0.1:9222", help="CDP HTTP endpoint")
    p.add_argument("--origin", required=True, help="tab URL prefix, e.g. https://app.example.com")
    p.add_argument("--ping", required=True,
                   help="same-origin path the site itself uses to check the session, e.g. /api/me")
    p.add_argument("--every", type=float, default=240, help="seconds between pings (default 240)")
    p.add_argument("--max-minutes", type=float, default=60, help="hard stop (default 60)")
    p.add_argument("--stop-file", help="stop as soon as this file exists")
    p.add_argument("--login-marker", action="append", default=["/login", "/signin", "/sign-in"],
                   help="URL fragment that means the tab is on a sign-in page (repeatable)")
    args = p.parse_args()
    if not args.ping.startswith("/"):
        p.error("--ping must be a same-origin path starting with /")
    sys.exit(asyncio.run(run(args)))


if __name__ == "__main__":
    main()
