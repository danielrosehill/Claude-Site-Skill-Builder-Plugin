#!/usr/bin/env python3
"""Drift probe skeleton for a site plugin.

Reads profiles/<site-id>.json, re-checks the load-bearing facts, prints one line per
check, and exits non-zero if anything moved. Adapt per site; do not generalise it.

Checks that need a signed-in session cannot run here — run those as a documented
browser sequence and record the result alongside this output.
"""
import json
import pathlib
import sys
import urllib.request

UA = "site-skill-builder drift probe (contact: see repo README)"
TIMEOUT = 20


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.status, resp.geturl(), resp.read().decode("utf-8", "replace")


def classify(body):
    """A 200 is not a verdict. Name what the body actually is."""
    low = body.lower()
    if len(body) < 4000 and ("challenge" in low or "are you a robot" in low):
        return "challenge"
    if "sign in" in low and "password" in low and len(body) < 20000:
        return "login-wall"
    if len(body) < 2000:
        return "empty-shell"
    return "page"


def main(profile_path):
    profile = json.loads(pathlib.Path(profile_path).read_text())
    failures = 0

    for name, url in profile.get("probe_urls", {}).items():
        try:
            status, final, body = fetch(url)
        except Exception as exc:                      # noqa: BLE001 - report, don't raise
            print(f"BLOCKED: {name} — {exc}")
            failures += 1
            continue

        kind = classify(body)
        if kind != "page":
            print(f"CHANGED: {name} — served a {kind} at HTTP {status}")
            failures += 1
            continue

        expected = profile.get("probe_expect", {}).get(name)
        if expected and expected not in body:
            print(f"CHANGED: {expected!r} not found on {name} ({final})")
            failures += 1
            continue

        print(f"OK: {name}")

    print(f"\n{'DRIFT' if failures else 'CLEAN'}: {failures} check(s) moved")
    return 1 if failures else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: probe.py profiles/<site-id>.json", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
