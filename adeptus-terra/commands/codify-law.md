---
description: Build or update the .claude/commissar.yml doctrine manifest (and any local standard files) that the Imperial Commissar enforces. Prefers external/shared references for framework-level law; writes local prose only for genuine project-specific rules.
args:
  - name: domain
    description: "Optional. Restrict codification to a single domain: language or structure. If omitted, the command asks."
    required: false
---

You are tasked with **codifying the law** that the Imperial Commissar (`adeptus-terra:imperial-commissar`) enforces. Your deliverable is a `.claude/commissar.yml` manifest — and, only where genuinely needed, thin local standard files — in the exact schema the Commissar reads during his Doctrine Resolution Protocol.

**Optional domain filter**: `{{domain}}` (if set to `language` or `structure`, codify only that domain).

## Guiding Principle: Reference, Don't Duplicate

Framework-level standards are identical across every repo built on that framework. **Never materialize them into each repository.** Reference them once — by URL or shared path — and let many repos point at the same canonical source. Write local prose **only** for the genuine project-specific delta. Across ten repos on the same framework, this should produce ten small manifests pointing at one shared source, not ten copies of the same standards.

Classify all law into two kinds:

| Kind | Examples | Treatment |
|---|---|---|
| **Framework / shared** | Shopware coding guidelines, PSR-12, Symfony conventions, the framework's phpstan/cs-fixer baseline, an org-wide canonical standards doc | **Reference** by URL or shared path. Never copy. |
| **Project-specific delta** | This repo's boundary rules, a bespoke naming convention, an extraction rule unique to this codebase | Write locally — thin, delta-only. Or reference a shared org source if one exists. |

## Theming Boundary

This command runs inside the Imperium Standard style, so your **conversation** with the developer is Imperial-themed. The **generated law** — `.claude/commissar.yml` and any `.md` standard files — is **professional and unthemed**. Real linters and real humans read this law; it must not be dressed in Gothic. Keep the artifacts clean.

## The Sacred Sequence

### 0. Verify the ground

Confirm the working directory is a git repository / project root (look for `.git`, `composer.json`, `package.json`, or similar). If not, tell the developer to run from a project root and stop.

### 1. Reconnaissance Rites (discover before writing)

Scan the project so you build **on** existing doctrine, never over it. Use `Read`, `Grep`, and `Glob` (you have no Bash in the command context beyond what the harness allows — prefer the file tools).

1. **Existing manifest** — is there a `.claude/commissar.yml`? If so, this is **UPDATE MODE**: parse it, preserve every existing entry, and amend rather than overwrite.

2. **Detect the framework** — read `composer.json` / `package.json`:

   | Signal | Framework | Suggested canonical reference (confirm with developer) |
   |---|---|---|
   | `composer.json` `type: shopware-platform-plugin`, or requires `shopware/core` / `shopware/platform` | **Shopware** | `https://developer.shopware.com/docs/resources/guidelines/code/` |
   | requires `laravel/framework` | **Laravel** | Laravel coding style / PSR-12 |
   | requires `symfony/*` | **Symfony** | Symfony coding standards |
   | `package.json` with a shared config (`@company/eslint-config`, framework preset) | **Node/TS** | the shared config package / style guide |

   **Never hardcode a URL as fact.** Suggest the canonical location and ask the developer to confirm or paste the exact URL. If the org maintains its own canonical standards source, prefer pointing every repo at that.

3. **Harvest in-repo linter/formatter configs** — these ARE codified law and carry the framework baseline. Reference them; do not rewrite them. Detect: `phpstan.neon*`, `.php-cs-fixer*.php`, `phpcs.xml*`, `.editorconfig`, `.eslintrc*`, `eslint.config.*`, `.prettierrc*`, `ruff.toml`, `pyproject.toml` (`[tool.*]`).

4. **Find existing prose standards** — `CONTRIBUTING.md`, `docs/standards/*`, `docs/coding-standards*.md`, `STYLE.md`. Reference or extend these rather than duplicating them.

5. **Detect sibling repos** — read `.claude/settings.local.json` → `permissions.additionalDirectories`. Note any shared conventions across siblings; they hint at law that should live in a shared source, not per-repo.

Present a short reconnaissance summary to the developer before proceeding.

### 2. The Origin Decision (reference vs local)

Use `AskUserQuestion`. This is the pivotal choice — default toward referencing:

**Question — Doctrine origin**:
- Header: "Origin"
- Options:
  - "Reference a shared/canonical source" (Recommended when a framework or org standard exists) — point the manifest at a URL or shared path. Writes no local prose.
  - "Reference framework + write local delta" — reference the framework/shared law, and write a thin local file for genuine repo-specific rules only.
  - "Write local standard files" — for repos with no framework/shared source; generate baseline-seeded local prose.

If a framework was detected in Step 1, pre-frame the recommendation toward referencing it.

### 3. Interrogation

Use `AskUserQuestion` for what discovery cannot resolve. Skip questions already answered by the origin decision or the `{{domain}}` filter.

1. **Domains to codify** (skip if `{{domain}}` set):
   - Header: "Domains"
   - Options: "Both language & structure" (Recommended), "Language only", "Structure only"

2. **Storage path** — asked each run, only if any local prose will be written:
   - Header: "Storage"
   - Options: "docs/standards/" (Recommended — matches the Commissar's convention discovery), ".claude/doctrine/", "Other" (let developer specify)

3. **Fold in discovered configs?** — if linter/formatter configs were found:
   - Header: "Linter configs"
   - Options: "Include all discovered" (Recommended), "Let me choose", "Skip configs"

4. For referenced sources, confirm each URL/path with the developer (paste or approve the suggested canonical reference).

### 4. Inscription

Write the artifacts. **Professional and unthemed.** In UPDATE MODE, merge — never blind-overwrite.

#### 4a. The manifest — `.claude/commissar.yml`

Emit exactly this schema (the Commissar reads `language`, `structure`, `configs`; multiple sources per domain are merged, so a framework URL and a local delta file can coexist under one domain):

```yaml
doctrine:
  language:
    # framework/shared references (URLs or shared paths) come first
    - <confirmed framework/org URL or path>
    # optional local delta (only if the developer chose to write one)
    - ./docs/standards/language.md
  structure:
    - <confirmed framework/org URL or path>
    - ./docs/standards/architecture.md
  configs:
    - phpstan.neon
    - .php-cs-fixer.dist.php
```

Rules:
- Omit any domain the developer chose not to codify.
- Omit `configs` if none were folded in.
- In UPDATE MODE: union the new entries with existing ones, de-duplicating identical references. Preserve entries the command didn't touch.
- Only reference local `.md` paths you actually write in 4b.

#### 4b. Local standard files (delta only)

Write these **only** when the developer chose an origin that includes local prose, and only for the chosen domains. Seed each from the baseline below as a **real, editable starter** — then trim it to the genuine project delta (drop anything the referenced framework law already covers). Place them at the chosen storage path.

**`language.md` starter** (naming, comments, user-facing strings):

```markdown
# Language Standards

Enforced by the Imperial Commissar. Framework-level language rules are referenced
in .claude/commissar.yml; this file holds only project-specific additions.

## Naming
- Names reveal intent; no abbreviations beyond well-established ones (id, url, db).
- Casing follows the language's standard convention.
- <project-specific naming rule, e.g. domain vocabulary, prefix conventions>

## Comments & Docblocks
- Comments explain WHY, not WHAT. No commented-out code.
- <project-specific docblock requirement, if any>

## User-Facing Strings
- Exception, log, and translation text is clear and direct — no internal jargon.

## Forbidden Words
- No marketing or filler language in identifiers, comments, or user-facing strings:
  leverage (use "use"), utilize (use "use"), seamless, robust, powerful, effortless,
  supercharge, cutting-edge, just (as filler), simply, basically.
- <project-specific banned or mandated terms>
```

**`architecture.md` starter** (structure, boundaries, collaboration):

```markdown
# Structure & Collaboration Standards

Enforced by the Imperial Commissar. Framework-level structural rules are referenced
in .claude/commissar.yml; this file holds only project-specific additions.

## Responsibility & Structure
- One responsibility per unit; no God objects.
- <project-specific module/layout rule>

## Dependency Direction
- Dependencies point toward abstractions; no circular dependencies across boundaries.

## Boundaries & Collaboration
- Public surface is intentional and minimal; internals stay internal.
- Cross-plugin/package contracts are explicit, not implicit.
- Code intended for extraction is consumer-agnostic — no consumer-specific
  concretions in a shared base.
- <project-specific boundary or extraction rule>
```

Replace every `<...>` placeholder using the developer's input and discovered conventions. If a section is fully covered by the referenced framework law, remove it — keep the local file thin.

### 5. Confirmation (themed)

Report back in the Imperial voice. Summarize:
- The manifest path and whether it was created or updated.
- Which domains were codified and from which origin (referenced vs local).
- References added (URLs/paths) and configs folded in.
- Any local files written (or "none — fully referenced").
- Confirm the Commissar can now render **manifest-authority** judgements instead of baseline ones.

## Formatting Guidelines

- **YAML**: 2-space indent, list entries under each domain key. Quote any value containing a colon.
- **Generated `.md`**: standard technical prose, no theming, section headers as shown.
- **De-duplication**: in UPDATE MODE, never create duplicate references; merge by exact string match.

## Output Requirements

After inscription:
1. State the manifest path and create/update status.
2. Summarize domains, origin (referenced/local), references, and configs.
3. List any local files written, or confirm none were needed.
4. Suggest the developer run the Commissar against a recent change to exercise the new law.

## Error Handling

- **Not a project root**: instruct the developer to run from a git repository / project root and stop.
- **No framework detected and no shared source given**: proceed with local files (baseline-seeded), and note the standards are project-local.
- **Manifest exists but is malformed**: show the parse issue, and ask whether to repair in place or back up and regenerate — never silently discard the developer's existing law.
- **Developer declines every origin**: stop without writing; explain nothing was codified.

## Example Output Summary (themed conversation, unthemed artifacts)

```
My lord, the law is codified. The Commissar now rules with manifest authority.

Manifest: `.claude/commissar.yml` (created)
  language:  referenced — https://developer.shopware.com/docs/resources/guidelines/code/
  structure: referenced — https://developer.shopware.com/docs/resources/guidelines/code/core/
  configs:   phpstan.neon, .php-cs-fixer.dist.php (folded in)
  local:     none — fully referenced, no per-repo duplication

This Shopware repo carries a 5-line manifest, not a copy of the framework's standards.
Summon the Commissar against your latest change to see the law enforced.
```
