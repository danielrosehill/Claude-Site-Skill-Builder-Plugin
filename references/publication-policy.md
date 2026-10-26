# What gets published, what stays private, what never gets written down

A site plugin is built by looking closely at somebody else's service. Most of what
you learn is ordinary integration detail and publishing it harms nobody. A minority
is the provider's defensive posture or a live weakness, and publishing that is
harmful whether or not it was easy to find.

Classify **every** observation before it is committed. The classification is part of
the work, not a review step at the end.

## The test

> Would writing this line down publicly help someone abuse this service, more than it
> helps a legitimate user drive their own account with an agent?

If yes → private. If it describes a *flaw* rather than a *feature* → stop and follow
the incidental-finding rule below.

## Publishable (the public plugin repo)

- URL grammar and route taxonomy; how identifiers are formed and validated.
- Which of the vendor's own documented APIs exist and what they return.
- The meaning of fields, units, pack quantities, tax and currency semantics.
- Page hierarchy: what lives at which level, where the data actually is.
- Which access route works for a normal user (browser vs plain fetch) as a plain
  statement of fact, without the defence analysis behind it.
- The vendor's `robots.txt` reading and terms-of-service constraints.
- Everything in the durability doctrine: handles, verification, breakage signals.

## Private (the paired private dev repo only)

- Raw captures: HAR files, saved DOM, response bodies, screenshots of account pages.
- Anything session-bound: cookies, bearer tokens, CSRF values, device ids.
- Account-specific data: contract prices, order history, addresses, internal
  customer numbers, anything about other people.
- Endpoints discovered in bundles but not linked from any public UI.
- Request signing, nonce derivation, and similar client-side crypto detail.
- Defence observations: which vendor, which cookies, which headers or timings are
  checked, what the challenge looks like, what did and did not get through.

That last bullet is the one that feels most useful to write up and must not be
published. "Route X is not available to scripts, use the browser" is publishable.
"Route X checks these four cookies and fails when the TLS fingerprint is Y" is not.

## Never recorded anywhere

- Credentials, in any file, including private ones. Reference the password manager.
- Another user's data, however incidentally obtained.
- Anything acquired by exceeding what the account is entitled to do.
- A working bypass of an access control, a rate limit, or a bot challenge — not in
  code, not in prose, not in a commit message, not as a "note for later".

## Conduct while observing

- Drive the site at human speed. No parallel fan-out, no retry storms. Operating
  detail (pace budgets, handing a challenge to the user, what's out of bounds):
  `anti-bot-posture.md`.
- One attempt at a blocked route, then route around it or stop. Never iterate
  against a challenge — that is the line between using a site and attacking it.
- In an authenticated session, stay read-only unless the user has explicitly asked
  for a state-changing skill and confirmed the specific action.
- Respect `robots.txt` as a statement of intent even where it is not enforced.
- Prefer the vendor's supported route when one exists, even if it is slower.

## Incidental findings: the stop rule

Mapping a site occasionally surfaces something that looks like a security problem —
an endpoint returning data without auth, a token in a response body, an identifier
that looks enumerable. When that happens:

1. **Stop.** Do not probe, enumerate, or try to establish impact. One observation is
   already enough to report; a second is testing someone else's system.
2. **Do not build on it.** No skill uses it, no profile documents it as a route.
3. **Quarantine the evidence** in the private dev repo under `findings/`, with the
   date, the URL, and what was seen. Never in the public repo. Never in a commit
   message or a branch name.
4. **Report it.** Use `browser-data-capture:disclose-finding` if that plugin is
   installed — it locates the contact via `security.txt`, `security@`, or a bug
   bounty programme and drafts a courteous report. If it is not installed, draft the
   same thing by hand: what you saw, when, how you came across it, no exploit
   detail, an offer to clarify, no demands and no deadline.
5. **Say nothing publicly** until the vendor has fixed it and is comfortable with a
   mention. Record the disclosure date privately so the timeline is not lost.

Ask the user before sending anything. Disclosure is correspondence in their name.
