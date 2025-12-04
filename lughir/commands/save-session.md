---
description: Save conversation to library with analysis
allowed-tools: 
   - Write(~/.claude/conversations)
   - Read(~/.claude/conversations)
argument-hint: (analyzes current conversation)
---

Analyze the entire conversation history and create a comprehensive documentation file in the `~/.claude/conversations/` folder.

## Your Task:

1. **Analyze the conversation** to extract:
   - Main topic/title (brief, descriptive)
   - Context that triggered this conversation
   - Summary of what was discussed and accomplished
   - Key points, findings, and insights
   - All actions taken (code changes, tests run, investigations, files modified)
   - **Mistakes made** by both user and AI during the conversation
   - **Assumptions that were challenged** (what we thought vs. what turned out to be true)
   - **Misconceptions that were corrected** during investigation
   - Outcomes, resolutions, and learnings
   - References
      - file paths with line numbers
      - documentation links
      - older related conversations in `~/.claude/conversations`

2. **Generate filename**: `YYYY-MM-DD-brief-topic.md` where:
   - YYYY-MM-DD is today's date
   - brief-topic is a short slug derived from the main topic (lowercase, hyphenated)

3. **Create structured document** using this format:

```markdown
---
date: {YYYY-MM-DD}
project: {project}
---

# [Topic Title]

> **Context**: [Brief context/trigger for conversation]

## Summary
High-level overview of what was discussed and accomplished.

## Key Points
- Main findings or decisions
- Important insights
- Technical details discovered

## Actions Taken
- Code changes made
- Tests run
- Investigations performed
- Files modified

## Mistakes & Learning Points
- **Mistakes Made**: Errors or wrong approaches taken (by both human and AI)
- **Assumptions Challenged**: What we initially assumed vs. what turned out to be true
- **Misconceptions Corrected**: Misunderstandings that were clarified during investigation

## Outcomes
- What was resolved
- What was learned
- Any blockers or open questions

## Open tasks / questions
- What needs to be done
- What needs to be answered

## References
- File paths and line numbers
- Related documentation
- External links
- Related conversations
```

4. **Write the file** to `~/.claude/conversations/[generated-filename]`

5. **Confirm** the save location to the user

Be thorough in capturing mistakes and learning points - these are valuable for future reference.
