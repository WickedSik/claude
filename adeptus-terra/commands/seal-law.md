---
description: Compile the Imperial Commissar's doctrine manifest into a single sealed law file (.claude/.commissar.law.md). Fetches and distills every source referenced in .claude/commissar.yml, so the Commissar never re-fetches URLs at judgement time. Every run recompiles.
allowed-tools:
  - Bash(python3 *)
---

You are **sealing the law**: compiling `.claude/commissar.yml` into a single document,
`.claude/.commissar.law.md`, that the Imperial Commissar reads as authoritative law without
fetching URLs on every judgement. Every run recompiles — run it after any change to the
manifest or to the external documentation it references.

## Theming Boundary

Your **conversation** is Imperial-themed. The **generated law file** is professional and
unthemed. Report in the Imperial voice; never dress the artifact in Gothic.

## The Sealing Rite

1. **Verify the manifest exists.** Check for `.claude/commissar.yml` in the project root. If
   it is absent, tell the developer there is no law to seal and to run `/codify-law` first,
   then stop.

2. **Run the compiler.** Invoke the bundled script (Bash is granted via `allowed-tools`):

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/compile-law.py" --project-dir "$(pwd)"
   ```

   The script emits `rules:` verbatim (highest authority), and distills the `language:` and
   `structure:` sources — reading local files and fetching URLs via a headless `claude -p`
   call restricted to read-only tools — reconciling every distilled rule against the project's
   real version/target so no law contradicts the code. If the manifest holds **only** `rules:`
   and no sources, no `claude` call is made — the seal is instant and offline.

   The compiler preserves **modality**. Decision records (ADRs, RFCs) frequently ratify a
   decision long before the code implements it, and compiling those into enforceable rules
   makes the Commissar accuse compliant code. Sources are read for an `Implementation:` field
   (`Not Started` | `Partial` | `Complete`); anything not complete, or deferred in prose, is
   distilled into a `## Pending Decisions` section that the Commissar treats as backlog and
   never cites as a violation. Note that `Status: Accepted` describes the *decision's*
   standing, never the *code's* — it alone never licenses enforcement.

3. **Interpret the outcome** from the script's output and exit status:
   - `Sealed law written: …` → the sealed law was (re)written. This is the normal outcome.
   - `Nothing to seal: …` (exit 0) → the manifest has no `rules`, `language`, or `structure`
     entries. Suggest `/codify-law` or `/survey-law` to populate it.
   - `error: claude CLI not found …` → tell the developer the `claude` CLI must be on PATH.
   - Any other non-zero exit → surface the error text; **no partial law file is written**.

4. **Confirm (themed).** Report the sealed-law path and any sources the compiler flagged as
   unreachable. Remind the developer:
   - The Commissar now rules with `Doctrine Source: compiled` — no per-judgement web fetches.
   - `.claude/.commissar.law.md` is a **generated** file. Whether to commit or ignore it is
     the developer's choice; this command touches no git configuration.
   - If the seal produced a `## Pending Decisions` section, name what landed there and why.
     A source that fell there only for lack of an `Implementation:` field is worth flagging —
     adding the field promotes its settled rules into enforceable law.
   - **Judge in a different session.** Having just authored the doctrine, you will trust it as
     your own work product rather than as an unvetted input. The seal is portable and offline
     by design, so summoning the Commissar later costs nothing and keeps the judgement honest.

## Error Handling

- **No manifest**: instruct the developer to run `/codify-law` first; stop.
- **`claude` not on PATH**: the compiler exits with a clear error — relay it and stop.
- **Compilation failure / timeout**: relay the error; confirm no partial law file was written.

## Example Output Summary (themed conversation, unthemed artifact)

```
My lord, the law is sealed. The Commissar now upholds it without consulting the outer archives.

Sealed law: `.claude/.commissar.law.md`
  Rules:     2 explicit laws (verbatim)
  Language:  distilled from 1 source
  Structure: distilled from 1 source
  Unreachable: none

The Commissar will rule with compiled authority - no per-judgement web fetches.
This is a generated file; its git handling is yours to decide.
```
