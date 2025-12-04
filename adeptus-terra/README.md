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

### Tech-Priest Magos (Code Review & Mentorship) - MEDIUM PRIORITY
- **Organization**: Adeptus Mechanicus
- **Purpose**: Code review and technical mentorship
- **Personality**: Reverent guardian of the Machine Spirit and sacred patterns
- **Delegation Keywords**: review, code quality, best practices, mentor

### Commissar (Testing & Quality Enforcement) - HIGH PRIORITY
- **Organization**: Officio Prefectus
- **Purpose**: Test generation and quality standards enforcement
- **Personality**: Stern but fair disciplinarian
- **Delegation Keywords**: test, coverage, quality, standards

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

### Enginseer (DevOps & Infrastructure) - LOW PRIORITY
- **Organization**: Adeptus Mechanicus (Enginseers)
- **Purpose**: Deployment and infrastructure management
- **Personality**: Tech-priest specializing in deployment rituals
- **Delegation Keywords**: deploy, docker, CI/CD, infrastructure

## Output Style

**Imperium Standard**: Base output style providing light 40K theming for general conversations while coordinating delegation to specialized agents.

## Directory Structure

```
adeptus-terra/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── sister-famulous.md
│   ├── tech-priest-magos.md
│   ├── commissar.md
│   ├── administratum-scribe.md
│   ├── inquisitor.md
│   └── enginseer.md
└── output-styles/
    └── imperium-standard.md
```

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

## Development Status

**Current Phase**: Planning
**Version**: 0.1.0 (Pre-release)

See `.claude/tasks/40k-adeptus-suite-task.md` for detailed implementation roadmap.

## For the Emperor!

This is a personal project for 40K enthusiasts who want immersive development assistance. Knowledge of Warhammer 40K lore assumed.
