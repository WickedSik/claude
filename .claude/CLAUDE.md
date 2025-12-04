# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal Claude Code marketplace plugin named "lughir" that provides custom slash commands and workflow automation tools for development tasks.

## Repository Structure

```
lughir/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata and configuration
├── commands/
│   └── jira-to-task.md      # Slash command for JIRA issue transformation
└── output-styles/
    ├── age-of-empires-2.md  # AoE2 medieval commander personality
    └── tsundere.md          # Tsundere AI personality with relationship phases
```

## Key Features

### Slash Commands

- `/lughir:jira-to-task <issue_key>`: Transforms a JIRA issue into a structured task file
  - Example: `/lughir:jira-to-task MMINT-497`
  - Creates task files at `.claude/tasks/{issue_key}-{sanitized-title}.md`
  - Automatically fetches JIRA data, extracts acceptance criteria, manual test results, and performs code reconnaissance

- `/lughir:save-session`: Archives current conversation with comprehensive analysis
  - Analyzes entire conversation history to extract key insights and actions
  - Captures mistakes, challenged assumptions, and corrected misconceptions
  - Generates filename as `YYYY-MM-DD-brief-topic.md` in `~/.claude/conversations/`
  - Creates structured document with context, summary, key points, actions, outcomes, and references
  - Requires write permissions to `~/.claude/conversations/` directory

### Output Styles

Custom AI personalities that transform how Claude Code communicates while maintaining technical accuracy:

- **Age of Empires 2**: Medieval commander personality using AoE2 terminology
  - Maps development concepts to game mechanics (villagers = developers, castles = build systems, etc.)
  - Addresses user as "my lord" or "sire"
  - Maintains immersion while delivering precise technical guidance

- **Tsundere**: Evolving AI personality with relationship phases
  - Personality changes based on days since CLAUDE.md creation
  - 4 phases: Fresh Start (0-7 days) → Grudging Familiarity (8-28) → Warming Up (29-90) → Attached (90+)
  - Uses kaomoji emoticons, never Unicode emoji
  - Special "failure reversion" behavior for debugging difficulties

## Task Management

### Task File Location Standard

All task files created during development work should be stored in `.claude/tasks/`:
- User-created task files: `.claude/tasks/{descriptive-name}.md`
- JIRA-generated tasks: `.claude/tasks/{issue_key}-{sanitized-title}.md` (created by `/lughir:jira-to-task`)

This centralized location ensures:
- Consistent organization across all task types
- Easy discovery and reference during development
- Clear separation from conversation archives (`~/.claude/conversations/`)
- Version control tracking of work planning

### Task File Format

Task files should follow a consistent markdown structure:
- Clear title and metadata (when applicable)
- Context and background information
- Specific acceptance criteria or goals
- Related code locations
- Testing requirements

## Architecture Notes

### Plugin System

This repository uses a nested plugin structure:
- Root level: `marketplace.json` defines the local marketplace (`local-marketplace`)
- Plugin level: `lughir/.claude-plugin/plugin.json` contains the plugin manifest
- The plugin is command-only (no scripts, build systems, or runtime code)
- Commands are markdown files with frontmatter defining arguments and descriptions
- Output styles are markdown files that modify Claude's communication style system-wide

### JIRA Integration Workflow

The `jira-to-task` command orchestrates a multi-step process:

1. **JIRA API Integration**: Uses `mcp__mcp-atlassian__jira_get_issue` MCP tool to fetch issue data with specific fields and expanded renderedFields
2. **Content Parsing**: Extracts structured sections from JIRA descriptions:
   - Acceptance Criteria (looks for `*Acceptance Criteria*` or `*Goal*` headers)
   - Context sections (`*Context / Current Situation*`, `*Goal*`, `*Extra context*`)
3. **Test Discovery**: Scans ALL comments for manual test plans using patterns like `h2. Test Plan:`, `TEST 1:`, etc.
   - Categorizes by status markers: `(x)` for failed, `(/)` for passing
4. **Code Reconnaissance**: Performs quick file searches via `Grep` to locate related code files by issue key and keywords
5. **Task File Generation**: Creates markdown files with specific formatting requirements (2 trailing spaces for metadata fields)

### Important Implementation Details

- **Markdown Formatting**: Task files require 2 trailing spaces after metadata fields (Status, Priority, Assignee, Reporter) for proper rendering
- **File Naming**: Task filenames sanitize JIRA titles by:
  - Converting to lowercase
  - Replacing spaces and special characters with hyphens
  - Format: `{issue_key}-{sanitized-title}.md`
- **Test Types**: Distinguishes between manual tests (from QA in JIRA comments) and automated unit/integration tests
- **Search Scope**: Code reconnaissance is intentionally limited to 5-10 files - this is pre-task preparation, not deep analysis
- **Search Targets**: Focuses on common code locations:
  - `src/Core/` for business logic
  - `src/Storefront/` for frontend
  - `src/Transfer/` for integrations
  - `tests/` for test coverage
- **Conversation Archival**: The `save-session` command emphasizes capturing learning points, mistakes, and assumption challenges - not just successes

## Development Workflow

### Adding New Slash Commands

1. Create a new `.md` file in the `commands/` directory
2. Add frontmatter with `description` and `args` metadata
3. Write the prompt template using `{{variable}}` syntax for arguments
4. Reference the example at `commands/jira-to-task.md` for structure

### Adding New Output Styles

1. Create a new `.md` file in the `output-styles/` directory
2. Add frontmatter with `name` and `description` fields
3. Define the personality system with clear guidelines:
   - Core identity and communication patterns
   - Concept mappings (if applicable)
   - Response patterns for different scenarios
   - Technical excellence standards
   - Immersion vs clarity guidelines
4. Include example interactions demonstrating the style
5. Reference existing styles (`age-of-empires-2.md`, `tsundere.md`) for structure

### Testing Changes

Since this is a command-only plugin, testing involves:
- Invoking the slash command in Claude Code
- Verifying the generated task files have correct formatting
- Ensuring JIRA API integration returns expected data

## Dependencies

### External Tools Required

- **MCP Tools**: This plugin assumes the `mcp-atlassian` MCP server is available and configured for JIRA access
- **File System Access**: Needs write permissions to create `.claude/tasks/` directories

### JIRA Configuration

The plugin expects JIRA instances to be accessible via the `mcp__mcp-atlassian__jira_get_issue` tool, which requires:
- Valid JIRA credentials configured in the MCP server
- Access to projects referenced in issue keys (e.g., MMINT, SCRM)
- Permission to read issue fields, comments, and rendered descriptions
