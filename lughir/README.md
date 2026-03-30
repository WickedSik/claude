# Lughir

General-purpose tools, commands, and utilities for Claude Code. A personal plugin combining development workflow automation with creative writing support.

## Commands

### `/jira-to-task <issue_key>`

Creates a structured task file from a JIRA issue. Fetches the issue via the Atlassian MCP server, then dispatches the Rogue Trader reconnaissance agent to extract acceptance criteria, discover manual tests from comments, perform codebase reconnaissance, and generate a task file at `.claude/tasks/`.

**Example**: `/jira-to-task PROJ-456`

**Requires**: `adeptus-terra` plugin, `mcp-atlassian` MCP server

### `/create-task <title>`

Interactive task file creation for development planning without a backing JIRA issue. Prompts for priority, type, acceptance criteria, and context, then generates a task file at `.claude/tasks/`.

**Example**: `/create-task "Add user authentication"`

### `/save-session`

Analyzes the current conversation and saves a structured summary to `~/.claude/conversations/`. Extracts topic, key decisions, actions taken, mistakes, and outcomes.

## Skills

### Writing Workshop

Deep manuscript analysis for structural feedback, character arcs, pacing, and craft consistency. Provides comprehensive 10-step analysis covering structure, character tracking, timeline, pacing, thematic analysis, and craft pattern detection.

## Output Styles

| Style | Description |
|-------|-------------|
| **Age of Empires 2** | Medieval commander personality mapping development operations to AoE2 mechanics |
| **Literary Mentor** | Warm writing workshop instructor providing honest craft feedback |
| **Tsundere** | Evolving personality that warms up based on project relationship length |

## Dependencies

| Dependency | Type | Required by |
|------------|------|-------------|
| [`adeptus-terra`](../adeptus-terra/) | Plugin | `/jira-to-task` (provides the Rogue Trader reconnaissance agent) |
| `mcp-atlassian` | MCP Server | `/jira-to-task` (provides JIRA API access) |

## Installation

Install via the Claude Code plugin marketplace or add directly to your Claude Code configuration.
