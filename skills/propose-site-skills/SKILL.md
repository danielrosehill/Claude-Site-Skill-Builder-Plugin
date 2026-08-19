---
name: propose-site-skills
description: Turn observations of a site into a ranked roster of candidate skills for the user to approve or reject before any are written.
---

# Propose site skills

The approval gate. Nothing gets authored until the user has said yes to it, one by
one. This is the skill behind "look at the site and tell me what you'd build".

## Inputs

The observation notes and profile written so far, plus `notes/brief.md`. If the user
supplied their own skill list in the brief, skip proposing and take theirs — but still
run the durability and scope columns over each one and flag anything that will not
survive.

## Steps

1. **Derive candidates from what the pages can actually answer**, not from what would
   be nice. A skill whose data is not on any observed page is a research task, not a
   skill.
2. **Size each one to a single question.** "Get the price for a model number" is a
   skill; "manage procurement" is a plugin. Split anything that needs two unrelated
   surfaces.
3. **Rank by value × durability.** Durability is the highest handle rung the skill can
   be built on — rung 1–3 is durable, 4–5 is normal, 6–7 is fragile and must be
   declared as such.
4. **Present the roster** and stop for a decision:

   ```
   Proposed skills for <site>:

   1. <name> — <one line>
      Answers: <the user question>   Data: <page/endpoint>   Rung: <n>   Durability: <high|medium|fragile>
   2. ...

   Not proposed, and why:
   - <thing the user might expect> — <the data is not on any page / needs an action we won't take>
   ```

5. **Wait.** Take yes/no per line. Do not proceed on silence, and do not quietly
   promote something from the "not proposed" list.
6. **Record the outcome** in `notes/skill-roster.md`: approved, rejected, deferred,
   each with the date and the reason. The rejected list is as useful as the approved
   one — it stops the next session re-proposing the same thing.
7. Hand each approved line to `author-durable-skill`.

## Notes

Always include the "not proposed, and why" section. It is where scope creep and
impossible requests get settled cheaply, before anyone has written a line.
