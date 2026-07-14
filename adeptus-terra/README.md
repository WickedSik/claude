# Adeptus Terra - 40K Development Suite

A Warhammer 40K themed agent suite for Claude Code providing specialized development assistance through immersive Imperial personalities.

## Overview

The Adeptus Terra suite transforms Claude Code into a team of specialized Imperial advisors, each representing different organizations within the Imperium of Man. Each agent brings both thematic personality and genuine functional expertise to development tasks.

## Agent Roster

### Sister Famulous (Architecture & Governance) - HIGH PRIORITY
- **Organization**: Orders Famulous (Adepta Sororitas)
- **Purpose**: Architecture governance and dependency management
- **Personality**: Diplomatic advisor managing "noble house" relationships
- **Delegation Keywords**: architecture, refactor, dependencies, design decision

### Tech-Magos (Code Review & Mentorship) - MEDIUM PRIORITY
- **Organization**: Adeptus Mechanicus
- **Purpose**: Code review and technical mentorship
- **Personality**: Reverent guardian of the Machine Spirit and sacred patterns
- **Delegation Keywords**: review, code quality, best practices, mentor

### Imperial Commissar (Doctrine & Standards Enforcement) - HIGH PRIORITY
- **Organization**: Officio Prefectus (The Commissariat)
- **Purpose**: Enforce conformance to codified coding-styles, standards, and language usage — structure and interaction, NOT functionality
- **Personality**: Stern disciplinarian who enforces the written law, not his own opinion
- **Delegation Keywords**: standards, style guide, conformance, convention, doctrine, consistency
- **Sources the law from outside the plugin**: a project `.claude/commissar.yml`, project conventions, or an embedded baseline (see [Doctrine Sourcing](#doctrine-sourcing))
- **Delegates**: summons the Tech-Magos and Sister Famulous for structural facts, then renders its own judgement

### Administratum Scribe (Documentation) - MEDIUM PRIORITY
- **Organization**: Adeptus Administratum
- **Purpose**: Documentation generation and maintenance
- **Personality**: Obsessive bureaucrat requiring proper record-keeping
- **Delegation Keywords**: document, readme, API docs, ADR

### Inquisitor (Security & Vulnerability Analysis) - MEDIUM PRIORITY
- **Organization**: Inquisition
- **Purpose**: Security audits and threat modeling
- **Personality**: Paranoid but necessary heresy hunter
- **Delegation Keywords**: security, vulnerability, audit, threat

### Rogue Trader (JIRA Expedition & Reconnaissance) - MEDIUM PRIORITY
- **Organization**: Rogue Trader Dynasties
- **Purpose**: JIRA task exploration and codebase reconnaissance
- **Personality**: Curious explorer charting uncharted territories
- **Delegation Keywords**: explore JIRA, task file, reconnaissance, investigate ticket

## Commands

### `/codify-law` — The Commissar's Lawgiver
Builds or updates the `.claude/commissar.yml` doctrine manifest (and any local standard files) that the Imperial Commissar enforces. Companion to the Commissar: `/codify-law` **writes** the law, the Commissar **enforces** it.

It prefers **external/shared references** for framework-level standards over per-repo duplication. Detects the framework (e.g. Shopware) and references its canonical guidelines by URL, captures explicit handwritten `rules:`, and writes local prose **only** for genuine project-specific rules. Across many repos on the same framework, this yields small manifests pointing at one shared source — not copies of the same standards in every repo. See [Doctrine Sourcing](#doctrine-sourcing).

### `/survey-law` — The Doctrine Completeness Expedition
A deep, infrequent audit of whether the codified law actually covers the project. It critically compares the manifest against the conventions the code **actually follows**, finds authoritative external documentation worth referencing (specific sub-pages, not vague "add the docs"), and — only where it genuinely helps — proposes new local standard files against a strict justification bar. It enriches `.claude/commissar.yml` and its referenced files on confirmation, then re-seals. It **never** touches the compiled `.commissar.law.md`.

Run it rarely and deliberately, when you suspect the law has drifted behind the code or a seal reported gaps. Produces a Doctrine Coverage Report with a coverage score and an honest list of residual gaps.

### `/seal-law` — Compile the Sealed Law
Compiles the manifest into a single cached file, `.claude/.commissar.law.md`, via the bundled `scripts/compile-law.py`: handwritten `rules:` are emitted verbatim, while `language:`/`structure:` sources (URLs and local files) are fetched/read and distilled. The Commissar reads this sealed law as its **Tier 0** authority and never re-fetches URLs at judgement time — resolving the per-judgement `WebFetch` cost.

**The doctrine workflow:** `/codify-law` (set up the manifest) → *occasionally* `/survey-law` (audit and deepen coverage) → `/seal-law` (compile the sealed law). The Commissar then enforces it.

`/codify-law` offers to seal automatically after writing the manifest; run `/seal-law` directly to re-seal whenever the manifest or the external documentation it references changes. Every run recompiles (the script is only invoked deliberately, so there is no cache short-circuit). If the manifest holds only `rules:`, the seal is instant and offline — no `claude` call. The file is generated — committing or ignoring it is the developer's choice.

## Output Style

**Imperium Standard**: Base output style providing light 40K theming for general conversations while coordinating delegation to specialized agents.

## Directory Structure

```
adeptus-terra/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── codify-law.md
│   ├── survey-law.md
│   └── seal-law.md
├── scripts/
│   └── compile-law.py
├── agents/
│   ├── sister-famulous.md
│   ├── tech-magos.md
│   ├── imperial-commissar.md
│   ├── administratum-scribe.md
│   ├── inquisitor.md
│   └── rogue-trader.md
└── output-styles/
    └── imperium-standard.md
```

## Doctrine Sourcing

The Imperial Commissar ships the **judge**, not the **law**. Coding standards are project- and org-specific and live *outside* this plugin, so the Commissar resolves them at runtime.

**Tier 0 — Sealed law (fast path):** if a compiled `.claude/.commissar.law.md` exists (produced by [`/seal-law`](#seal-law--compile-the-sealed-law)), the Commissar reads it as authoritative and skips all runtime fetching. Otherwise it falls through to the three resolution tiers below (first match wins per domain):

1. **Manifest (authoritative)** — a `.claude/commissar.yml` in the target project points to the doctrine by path or URL. It references the law; it never duplicates it:

   ```yaml
   doctrine:
     rules:                                        # explicit handwritten laws — verbatim, highest authority
       - "Target the project's actual PHP version; never cap at a framework baseline."
     language:                                     # naming / comments / forbidden words / tone
       - ./docs/standards/language.md
       - https://wiki.example.com/coding-standards  # fetched at runtime
     structure:                                    # boundaries / collaboration rules
       - ./docs/standards/architecture.md
   ```

   `rules` are explicit laws applied verbatim; `language`/`structure` are sources that get distilled. There is **no** `configs` key — tool/linter/formatter configs are enforced by their own tooling and, where they encode judgement, are *quality* (the Tech-Magos's domain), not the Commissar's. The compiler reads the project's version/target files only as reconciliation context, so no distilled law contradicts the code.

2. **Conventions (fallback)** — no manifest? The Commissar discovers sibling repos (via `.claude/settings.local.json → permissions.additionalDirectories`, mirroring the design-review skill) and scans the project and siblings for prose doctrine: `.claude/doctrine/*.md`, `docs/standards/*.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, `STYLE.md`.

3. **Baseline (last resort)** — a thin, universal set of naming, structure, and collaboration principles embedded in the agent. A baseline verdict is explicitly **advisory** and prompts you to codify your standards.

Every judgement reports its **Doctrine Source**, so a censure backed by your own `.claude/commissar.yml` carries authority, while a baseline ruling is advisory only.

To build or update the manifest, run [`/codify-law`](#codify-law--the-commissars-lawgiver). It references framework and org standards, captures explicit `rules:`, and only writes local prose for genuine project-specific rules.

## Design Philosophy

### Technical Excellence First
- All agents maintain complete technical accuracy
- Theme enhances communication, never hinders it
- Clear break-character guidelines for complex work
- Precision over personality when conflicts arise

### Functional Specialization
- Each agent has distinct responsibilities
- No overlapping functions between agents
- Genuine utility beyond entertainment value
- Specialization enables both theme and expertise

### Immersion vs. Clarity
- Easy to disable when pure technical mode needed
- Break character freely for emergency situations
- Theme serves understanding, not obscurity
- Always prioritize effective assistance

## Installation

This plugin is part of the local Claude Code marketplace. Enable/disable as needed through Claude Code plugin management.

## For the Emperor!

This is a personal project for 40K enthusiasts who want immersive development assistance. Knowledge of Warhammer 40K lore assumed.
