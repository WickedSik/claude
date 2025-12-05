---
description: Create a task file from a JIRA issue with acceptance criteria, tests, and code state analysis
args:
  - name: issue_key
    description: JIRA issue key (e.g., PROJ-123, TASK-456)
    required: true
---

You are tasked with transforming a JIRA issue into a structured task file for development planning.

**Issue Key**: `{{issue_key}}`

Execute the following reconnaissance and documentation operations:

## 1. Intelligence Gathering (JIRA Reconnaissance)

Use `mcp__mcp-atlassian__jira_get_issue` to fetch:
- Fields: `description,summary,issuetype,status,assignee,reporter,labels,priority,comment`
- Expand: `renderedFields`
- Comment limit: 100

## 2. Acceptance Criteria Extraction

Parse the issue description to extract the *Acceptance Criteria* section:
- Look for section headers: `*Acceptance Criteria*` or `*Goal*` followed by criteria
- **Convert to numbered list format**: Transform the criteria into nested numbered lists
  - Main criteria: Use `1.`, `2.`, `3.`, etc.
  - Sub-criteria: Use indented numbered lists (indent with 3 spaces, then `1.`, `2.`, etc.)
  - Preserve logical grouping and hierarchy from JIRA
- Include any context from `*Context / Current Situation*` and `*Goal*` sections
- Capture `*Extra context*` if present

## 3. Manual Test Discovery

Scan ALL comments for manual test plans created by testers:
- Search for patterns: `h2. Test Plan:`, `h3. TEST`, `TEST 1:`, `TEST 2:`, etc.
- Extract test descriptions, steps, and expected results
- Categorize tests by status:
  - **Failed tests**: Lines containing `(x)` markers
  - **Passing tests**: Lines containing `(/)` markers
- Preserve test author and timestamp
- Note: These are MANUAL tests by QA, separate from unit/integration tests

## 4. Code State Verification (Quick Reconnaissance)

Perform rapid file search to identify related code:
- Use `Grep` to search for issue key (e.g., `PROJ-123`) in code comments
- Search for key terms from the issue summary (extract 2-3 main keywords)
- Look in common locations:
  - `src/Core/` for business logic
  - `src/Storefront/` for frontend
  - `src/Transfer/` for integrations
  - `tests/` for existing test coverage
- Limit search to finding 5-10 most relevant files
- Do NOT perform deep code analysis - this is pre-task preparation only

## 5. Task File Generation

Create a markdown file at `.claude/tasks/{{issue_key}}-{sanitized-title}.md` following the template structure below.

### Formatting Guidelines

- **Markdown newlines**: Use 2 trailing spaces at the end of a line to create a line break in rendered markdown
- **Status/Priority/Assignee block**: Each field (Status, Priority, Assignee, Reporter) MUST end with 2 spaces before the newline for proper rendering
  - Example: `**Status**: In Progress  ` (note the 2 spaces after "Progress")
- **Code blocks**: Use appropriate language identifiers (e.g., `json`, `php`, `bash`) for syntax highlighting, use `json lines` for commented json snippets.
- **Hierarchical lists**: Preserve the exact nesting structure from JIRA (bullets vs. numbered lists)
- **File paths**: Use backticks for file paths and include brief descriptions of relevance

### Task File Template

**IMPORTANT**: This is a TEMPLATE. Replace all `{placeholders}` with actual data from the JIRA issue.

**NOTE**: Add 2 trailing spaces after each metadata field value (Status, Priority, Assignee, Reporter) for proper markdown rendering.

```markdown
# [{{issue_key}}] {Issue Summary}

**Status**: {Current JIRA Status}
**Priority**: {Priority}
**Assignee**: {Assignee Name}
**Reporter**: {Reporter Name}

---

## ❌ Failed Tests

{If manual tests exist with (x) markers, list them here}
{Each test should include: test name, failed assertion, tester name, date}
{If no failed tests, write: "No failed manual tests found."}

---

## ✓ Passing Tests

{If manual tests exist with (/) markers, list them here}
{Keep this section brief - just test names and high-level coverage}
{If no passing tests, write: "No manual tests found yet."}

---

## Acceptance Criteria

{Convert criteria to numbered list format with nested numbering:}
{1. First acceptance criterion}
{2. Second acceptance criterion}
{   1. Sub-criterion (indented with 3 spaces)}
{   2. Another sub-criterion}
{3. Third acceptance criterion}

---

## Context & Goal

{Extract from *Context / Current Situation* and *Goal* sections}

---

## Extra Context

{Include *Extra context* section if present in JIRA}
{Include relevant code snippets or examples from JIRA description}

---

## Related Files (Initial Reconnaissance)

{List of 5-10 files found during code search}
{Format: `path/to/file.php` - Brief description of relevance}

{If no files found: "No direct code references found. Begin with keyword search for: {key terms}"}

---

## Unit/Integration Test Coverage

{Search for related test files in tests/Unit/ and tests/Integration/}
{List existing test coverage if found}
{If none: "No automated test coverage found. Consider adding tests to prevent regression."}

---

## Notes

- This task file was auto-generated from JIRA on {current date/time}
- Manual tests are maintained by QA team in JIRA comments
- Automated tests should be added during implementation to prevent regression
```

## Output Requirements

After generating the task file:
1. Confirm the file path where the task was created
2. Provide a brief summary:
   - Number of acceptance criteria items
   - Number of failed manual tests (if any)
   - Number of passing manual tests (if any)
   - Number of related files found
3. Highlight any failed tests that need immediate attention
4. Suggest next steps for the developer

## Error Handling

- If issue not found: Report clear error with issue key
- If no AC section found: Note this in the task file and flag for manual review
- If comments are disabled/empty: Note "No manual tests available"
- If code search finds nothing: This is acceptable - note it in the task file

## Example Task File

See `.claude/tasks/PROJ-123-example-feature.md` for a complete example of a properly generated task file.

This example demonstrates:
- ✓ Proper markdown formatting with 2-space newlines in the header section
- ✓ Structured acceptance criteria with hierarchical bullet points
- ✓ Context and goal sections extracted from JIRA
- ✓ Extra context with code snippets and field value documentation
- ✓ Related files grouped by category (infrastructure, pipelines, stock, docs)
- ✓ Test coverage analysis with recommendations
- ✓ Notes section with implementation guidance

**Key features from the example**:
- **Header block**: Each metadata field ends with 2 spaces for proper rendering
- **AC structure**: Converted to nested numbered list format (1, 2, 3... with indented sub-items as nested 1, 2, 3...)
- **Code snippets**: JSON example with proper syntax highlighting
- **File organization**: Related files grouped by functional area with brief descriptions
- **Implementation notes**: Includes architectural decisions (decorator pattern, plugin location, pipeline dependencies)
