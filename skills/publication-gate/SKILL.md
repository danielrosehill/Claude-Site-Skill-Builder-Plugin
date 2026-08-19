---
name: publication-gate
description: Classify every observation as publishable, private, or never-recorded before committing — plus the stop rule for security findings.
---

# Publication gate

Run before every commit to a site plugin, and immediately whenever something
surprising turns up. The classification rules live in
`references/publication-policy.md`; this skill applies them to a working tree.

## Steps

1. **Diff the working tree** of both the public plugin repo and the private workspace.
2. **Classify every added line** by the test: would writing this down publicly help
   someone abuse this service more than it helps a legitimate user drive their own
   account with an agent?
   - **Publishable** — URL grammar, identifiers, field meanings, page hierarchy, which
     route works as a plain statement, robots/ToS reading, handles and assertions.
   - **Private** — captures, session values, account-bound data, unlinked endpoints,
     request signing, and any defence analysis: which cookies, headers or timings a
     site checks, what the challenge looks like, what got through.
   - **Never recorded** — credentials, other people's data, anything obtained beyond
     the account's entitlement, any working bypass of an access control, rate limit or
     challenge, in code, prose, or a commit message.
3. **Move, don't delete.** Private content goes to the private workspace so the
   knowledge survives; only the "never" category is discarded.
4. **Check the commit message and branch name** as carefully as the diff — they are
   published too, and they are where a finding usually leaks.
5. **Scan for stray values**: bearer tokens, cookies, order numbers, addresses,
   customer ids, prices tied to a contract account.
6. **Report** what moved and what was dropped, then let the commit proceed.

## The stop rule

If the diff contains something that looks like a **flaw** rather than a feature — an
unauthenticated endpoint returning account data, a token in a response, an enumerable
identifier:

1. Stop interacting with the site. Do not probe or establish impact.
2. Do not build a skill on it, and do not document it as a route.
3. Quarantine the evidence in the private workspace under `findings/` with the date,
   the URL and what was seen.
4. Report it: `browser-data-capture:disclose-finding` if installed — it finds the
   contact via `security.txt`, `security@` or a bounty programme and drafts a
   courteous report. Otherwise draft the same by hand: what, when, how it was
   encountered, no exploit detail, an offer to clarify, no demands or deadline.
   **Ask the user before sending — it goes out in their name.**
5. Keep the public repo silent until the vendor has fixed it and is content with a
   mention. Record the disclosure date privately.

## Notes

Run this before the first commit of a new site plugin, not just before publishing.
Git history is published too, and a rewrite after the fact is not a fix.
