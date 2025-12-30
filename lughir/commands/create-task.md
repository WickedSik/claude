---
description: Create a structured task file for development planning
args:
  - name: title
    description: Task title/summary (e.g., "Add user authentication", "Fix cart validation")
    required: true
---

You are tasked with creating a structured task file for development planning through interactive information gathering.

**Task Title**: `{{title}}`

Execute the following operations:

## 1. Initial Information Gathering

Use `AskUserQuestion` to collect the following information in a single question set:

**Question 1 - Priority**:
- Header: "Priority"
- Options: Critical, High, Medium (Recommended), Low
- Description for each explaining urgency level

**Question 2 - Task Type**:
- Header: "Type"
- Options: Feature, Bug Fix, Refactor, Documentation
- Description for each explaining the nature of work

## 2. Acceptance Criteria Collection (Required)

Acceptance criteria are **mandatory** for task creation. They may be broadly scoped but must be provided.

After receiving priority and type, prompt the user:

> "Please provide the acceptance criteria for this task. These define what 'done' looks like.
>
> You can provide them as:
> - A numbered list (1. First criterion, 2. Second criterion)
> - Bullet points
> - Plain text (I'll format them)
>
> Criteria can be broadly scoped (e.g., 'User can log in successfully') or detailed."

Wait for the user to provide acceptance criteria before proceeding.

**If user response is unclear or empty**: Ask again, explaining that at minimum one acceptance criterion is needed to define the task's completion state.

## 3. Context Collection (Optional)

Use `AskUserQuestion` to ask:

**Question - Additional Context**:
- Header: "Context"
- Options:
  - "I'll provide context" - User will describe the situation/goal
  - "Skip" - No additional context needed

If user chooses to provide context, wait for their input.

## 4. Code Discovery (Optional)

Use `AskUserQuestion` to ask:

**Question - Code Search**:
- Header: "Code Search"
- Options:
  - "Search by keywords" - User provides keywords to find related files
  - "Skip search" - No code reconnaissance needed

If user chooses to search:
- Ask for 2-3 keywords related to the task
- Use `Grep` to search for these keywords in common locations:
  - `src/` for source code
  - `tests/` for existing test coverage
- Limit search to finding 5-10 most relevant files
- Do NOT perform deep code analysis - this is pre-task preparation only

## 5. Task File Generation

Generate a sanitized filename from the title:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Limit to 50 characters

Create a markdown file at `.claude/tasks/{sanitized-title}.md` following the template structure below.

### Formatting Guidelines

- **Markdown newlines**: Use 2 trailing spaces at the end of a line to create a line break in rendered markdown
- **Status/Priority block**: Each field MUST end with 2 spaces before the newline for proper rendering
- **Code blocks**: Use appropriate language identifiers for syntax highlighting
- **Hierarchical lists**: Use proper nesting with 3-space indentation

### Task File Template

**IMPORTANT**: Replace all `{placeholders}` with actual data from user input.

**NOTE**: Add 2 trailing spaces after each metadata field value for proper markdown rendering.

```markdown
# {Task Title}

**Status**: Not Started
**Priority**: {Priority}
**Type**: {Task Type}
**Created**: {current date YYYY-MM-DD}

---

## Acceptance Criteria

{Convert user-provided criteria to numbered list format:}
{1. First acceptance criterion}
{2. Second acceptance criterion}
{   1. Sub-criterion (indented with 3 spaces)}
{   2. Another sub-criterion}
{3. Third acceptance criterion}

---

## Context & Goal

{If user provided context, include it here}

{If skipped: "No additional context provided."}

---

## Related Files (Initial Reconnaissance)

{If code search performed, list files found}
{Format: `path/to/file.ext` - Brief description of relevance}

{If skipped or no files found: "No code reconnaissance performed. Consider searching for: {suggested keywords from title}"}

---

## Test Coverage

{If test files found during search, list them}
{If none: "No existing test coverage identified. Consider adding tests during implementation."}

---

## Implementation Notes

- [ ] Review acceptance criteria before starting
- [ ] Identify dependencies and blockers
- [ ] Consider test coverage requirements
- [ ] Update this file as implementation progresses

---

## Notes

- Task file created on {current date/time}
- Update status as work progresses: Not Started → In Progress → Review → Done
```

## Output Requirements

After generating the task file:
1. Confirm the file path where the task was created
2. Provide a brief summary:
   - Number of acceptance criteria items
   - Number of related files found (or "skipped" if no search)
3. Suggest next steps for the developer

## Error Handling

- If title is empty: Request a valid task title
- If acceptance criteria not provided after prompting: Ask again - AC is required
- If code search finds nothing: This is acceptable - note it in the task file

## Example Output Summary

```
Task file created: `.claude/tasks/add-user-authentication.md`

Summary:
- Acceptance Criteria: 5 items defined
- Related Files: 3 files found
- Test Coverage: 1 existing test file identified

Next Steps:
1. Review the generated task file
2. Begin implementation planning
```
