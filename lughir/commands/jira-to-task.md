---
description: Create a task file from a JIRA issue with acceptance criteria, tests, and code state analysis
args:
  - name: issue_key
    description: JIRA issue key (e.g., PROJ-123, TASK-456)
    required: true
---

You are tasked with creating a structured task file from a JIRA issue by coordinating between JIRA data retrieval and a specialist reconnaissance agent.

**Issue Key**: `{{issue_key}}`

## Step 1: JIRA Data Retrieval

Fetch the issue data using `mcp__mcp-atlassian__jira_get_issue`:
- Issue key: `{{issue_key}}`
- Fields: `description,summary,issuetype,status,assignee,reporter,labels,priority,comment`
- Expand: `renderedFields`
- Comment limit: 100

**On failure**: Report the error clearly with the issue key and stop. Do not proceed to agent dispatch.

## Step 2: Agent Dispatch

Use the `Agent` tool to dispatch the Rogue Trader reconnaissance agent:

- `subagent_type`: `"adeptus-terra:rogue-trader"`
- `description`: `"JIRA expedition for {{issue_key}}"`
- `prompt`: Include the following in the agent's prompt:
  1. The issue key: `{{issue_key}}`
  2. The **complete, untruncated** JIRA response from Step 1 (the agent needs all comments for manual test discovery)
  3. Instruction: "Generate a task file at `.claude/tasks/{{issue_key}}-{sanitized-title}.md` based on the provided JIRA data. Perform codebase reconnaissance to identify related files and test coverage."

The agent handles all analysis: acceptance criteria extraction, manual test discovery, codebase reconnaissance (using LSP and Grep), and task file generation.

**On failure**: If the agent cannot be dispatched (e.g., the `adeptus-terra` plugin is not installed), report the error clearly:
> "The `adeptus-terra` plugin is required for this command but is not available. Install it from the Claude Code marketplace to enable JIRA task file generation."

## Step 3: Result Presentation

After the agent returns, present the results:

1. **File path**: Confirm where the task file was created
2. **Summary**: Report counts of:
   - Acceptance criteria items found
   - Failed manual tests (if any — flag these for immediate attention)
   - Passing manual tests (if any)
   - Related code files discovered
3. **Recommended follow-up**: If the agent suggested specialist consultations, include them
4. **Next steps**: Suggest what the developer should do first (e.g., address failed tests, clarify ambiguities, begin implementation)

Present results as a concise, factual summary. Do not add roleplay theming — if an output style is active, it handles presentation at its own layer.
