---
name: close-out-session
description: End a browser-driven build or skill run cleanly — stop keep-alives, close only the tabs the agent opened, confirm what was committed, report to the user.
---

# Close out the session

The defined end of every browser-driven build and every `/site-drift` run. Skills
authored by this plugin end with the short form of it (steps 1–2).

## Steps

1. **Stop anything periodic.** `touch` the keep-alive stop file and confirm
   `keepalive_cdp.py` exited. Clear any in-page timer
   (`clearInterval(window.__siteKeepalive.id)`). Nothing the agent started may
   outlive the session.
2. **Close the tabs the agent opened, and only those.**
   - `claude-in-chrome`: `tabs_context_mcp`, then `tabs_close_mcp` for each tab in the
     session's MCP group, including the keep-alive tab. Never touch tabs outside the group;
     they are the user's.
   - Persistent agent browser: close the tabs this session opened. Leave the
     browser itself and its signed-in profile running, since that profile is what makes
     the next session work.
   - Headless Playwright/Puppeteer: close the browser context.
   If the user asked to leave a tab open to look at, leave that one and say so.
3. **Sweep the working tree.** Confirm `publication-gate` ran over the final diff,
   no raw captures, HARs, screenshots or response bodies sit in the public repo,
   and private material is in the private workspace. Remove scratch files the build
   created outside both repos.
4. **Commit and push** what was approved, if that hasn't happened yet.
5. **Report**, in this shape and nothing longer:

   ```
   <site> plugin: <built | extended | repaired> — <YYYY-MM-DD>

   Skills: <name> (rung n, verified live), <name> (...)
   Rejected/deferred: <n> — see notes/skill-roster.md
   Route: <route>   Session: <stable | keep-alive needed, <n> min timeout>
   Commits: <repo>@<sha> pushed; private workspace <updated | untouched>
   Closed: <n> tabs, keep-alive stopped
   Open items: <anything blocked, a challenge hit, a finding quarantined — or "none">
   ```

   Report a skill as working only if it was run live in step 10 of
   `author-durable-skill`. List unrun drafts under open items.

## Notes

If the session ended badly (timeout, challenge, blocked route), still run steps 1–2
before reporting. A half-finished build should leave no stray tabs or pings.
