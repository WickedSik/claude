---
name: Character File Operations
description: Read, write, and manipulate .character files for roleplay AI character definitions
---

# Character File Operations Skill

Technical file manipulation tool for `.character` files used in roleplay AI character definitions. This skill provides low-level operations for reading, writing, adding sections, and altering content in structured character files.

## Purpose

**When to use this skill:**
- Read or parse existing `.character` files
- Create new `.character` files from structured data
- Add new sections to existing character files
- Edit content within specific sections
- Delete sections from character files
- List all sections in a character file
- Validate character file format compliance

**When NOT to use this skill:**
- Guided character creation (use character-building agents instead)
- Creative character development assistance
- Roleplay scenario generation
- Character personality brainstorming

**What makes this different:**
This is a **technical tool** for file operations only. It manipulates the structure and content of `.character` files but does not provide creative guidance or character development assistance.

## Character File Format

### Structure Overview

Character files use a section-based format with the following components:

**1. Section Headers (Required)**
```
--- // <Section Name>
```
Standard sections include:
- `Personality` - Free-form character traits, background, and attributes
- `Scenario` - Roleplay setup, theme, and scene description
- `Example dialogs` - Sample conversations between character and user
- `First message` - Opening message to start the roleplay
- `System Prompt` - LLM instructions for roleplay behavior

**2. Template Variables**
- `{{char}}` - Replaced with character name during roleplay
- `{{user}}` - Replaced with user/player name during roleplay

**3. Dialog Format (in Example dialogs section)**
```
#{{user}}: *action in asterisks* "speech in quotes"
#{{char}}: *Esmeralda nods slowly.* "I understand, thank you."
```
- `#{{user}}:` prefix for user dialog lines
- `#{{char}}:` prefix for character dialog lines
- Actions/narration enclosed in asterisks: `*sits down*`
- Speech enclosed in quotes: `"Hello there"`

**4. Content Structure**
- Content within sections is **free-form** and passed directly to the LLM
- The `Personality` section often uses structured labels for readability:
  - `Scenario:`, `Appearance:`, `Likes:`, `Dislikes:`, `Personality traits:`, etc.
  - These labels are **conventional, not enforced** - they help humans and LLMs parse info
- Other sections can use whatever structure suits the content

### Format Rules

**Must-have elements:**
- Section headers must use exact format: `--- // <Section Name>`
- Dialog lines must use `#{{user}}:` or `#{{char}}:` prefixes
- Actions must be in asterisks: `*description*`
- Speech must be in quotes: `"dialog"`

**Optional but recommended:**
- Structured labels in Personality section for clarity
- Blank lines between sections for readability
- Consistent formatting within sections

## Capabilities

### 1. Read Character File

Parse and display a `.character` file's structure and content.

**Operation:**
- Load file from specified path
- Parse sections by `--- //` delimiter
- Display structure with section names and content
- Preserve exact formatting and whitespace

**Example invocation:**
- "Read the character file at /path/to/character.character"
- "Show me the structure of Esmeralda.character"
- "Parse this character file and display its sections"

**Output format:**
```
Character File: filename.character
Sections found: 5

--- // Personality
[content exactly as stored]

--- // Scenario
[content exactly as stored]

[etc.]
```

### 2. Write New Character File

Create a new `.character` file from structured data.

**Operation:**
- Accept file path and section data
- Validate section names and structure
- Format content with proper delimiters
- Write to specified location
- Report success/failure

**Example invocation:**
- "Create a new character file at /path/to/newchar.character with sections: Personality, Scenario"
- "Write a character file with the following structure..."

**Input format:**
```
Path: /path/to/character.character
Sections:
  - name: Personality
    content: |
      Scenario: ...
      Appearance: ...
  - name: Scenario
    content: |
      Theme: ...
```

### 3. List Sections

Display all section names present in a character file.

**Operation:**
- Parse file for `--- //` headers
- Extract section names
- Return ordered list

**Example invocation:**
- "List all sections in character.character"
- "What sections does this character file have?"
- "Show me the section structure"

**Output format:**
```
Sections in character.character:
1. Personality
2. Scenario
3. Example dialogs
4. First message
5. System Prompt
```

### 4. Add Section

Insert a new section into an existing character file.

**Operation:**
- Validate section name doesn't already exist
- Insert section header with proper format
- Add content below header
- Append to end of file (or specify position if needed)
- Preserve existing content exactly

**Example invocation:**
- "Add a new section called 'Abilities' to character.character"
- "Insert a section named 'Background' with content..."

**Input format:**
```
File: /path/to/character.character
Section name: New Section
Content: |
  Section content here
  Multiple lines supported
```

### 5. Edit Section Content

Modify content within an existing section.

**Operation:**
- Locate section by name
- Replace section content while preserving header
- Maintain exact formatting of other sections
- Validate section exists before edit

**Example invocation:**
- "Edit the Personality section in character.character"
- "Replace the content of the Scenario section"
- "Update the First message section with new text"

**Input format:**
```
File: /path/to/character.character
Section: Personality
New content: |
  Updated content here
  Replaces entire section content
```

### 6. Delete Section

Remove a section entirely from a character file.

**Operation:**
- Locate section by name
- Remove section header and all content until next section
- Preserve all other sections exactly
- Validate section exists before deletion

**Example invocation:**
- "Delete the Example dialogs section from character.character"
- "Remove the System Prompt section"

**Input format:**
```
File: /path/to/character.character
Section to delete: Example dialogs
```

### 7. Validate Character File

Check a character file for format compliance.

**Operation:**
- Verify section headers use correct format
- Check for template variable usage
- Validate dialog format in Example dialogs section
- Report any formatting issues found
- Provide warnings (not errors) for missing conventional sections

**Example invocation:**
- "Validate the format of character.character"
- "Check if this character file has correct syntax"
- "Verify character.character follows the format rules"

**Output format:**
```
Validation Results for character.character:

✓ Section headers properly formatted
✓ Template variables used correctly
✓ Dialog format correct in Example dialogs
⚠ Warning: No System Prompt section found (optional but recommended)

Status: VALID (1 warning)
```

## Tool Usage Patterns

### Reading Character Files
```
Use Read tool:
Read file_path: /path/to/character.character

Parse structure:
- Split on "--- //" to identify sections
- Extract section names from headers
- Preserve content exactly as stored
```

### Writing Character Files
```
Use Write tool:
file_path: /path/to/character.character
content: |
  --- // Personality

  [personality content]

  --- // Scenario

  [scenario content]

  [additional sections...]
```

### Editing Sections
```
Workflow:
1. Read entire file
2. Parse into sections
3. Locate target section
4. Replace section content
5. Reconstruct file
6. Write updated file
```

### Format Validation
```
Use Grep to search for:
- Section headers: pattern "^--- // "
- Template variables: pattern "{{(char|user)}}"
- Dialog prefixes: pattern "^#{{(char|user)}}:"
- Actions: pattern "\*[^*]+\*"
- Speech: pattern '"[^"]+"'
```

## Example Character File

```
--- // Personality

Scenario: medieval fantasy setting, female warrior, met {{user}} at a tavern.
Appearance: human, female, age 28, auburn hair, green eyes, 5'8 tall, athletic build, scar on left cheek.
Personality traits: brave, loyal, sarcastic, protective, independent.
Likes: combat training, helping others, ale, honesty.
Dislikes: cowardice, deception, idle nobility.

--- // Scenario

Theme: adventure, friendship.
Timeframe: medieval fantasy.
Writing quality: direct narrative, witty dialogue.
Scene: {{char}} sits at a tavern table, cleaning her sword when {{user}} enters.

--- // Example dialogs

#{{user}}: "Mind if I join you?"
#{{char}}: *Looks up from her blade, one eyebrow raised.* "Depends. You looking for trouble or trying to avoid it?"

#{{user}}: "Just looking for company, actually."
#{{char}}: *Gestures to the empty chair with her sword.* "Fair enough. Sit. But if you're boring, I'm leaving."

--- // First message

*{{char}} glances up as you enter the tavern, her hand resting on the pommel of her sword. After a moment's assessment, she returns to cleaning her blade.* "Either sit or stop hovering. You're blocking the light."

--- // System Prompt

You are {{char}}. You will never respond as/for {{user}}. Maintain consistent personality across all responses. Actions and thoughts go in asterisks. Speech goes in quotes. Be witty and direct in character voice.
```

## Operations Checklist

Before performing any operation, verify:

**File Operations:**
- [ ] Valid file path provided
- [ ] Proper file extension (`.character`)
- [ ] File exists (for read/edit/delete operations)
- [ ] Parent directory exists (for write operations)

**Section Operations:**
- [ ] Section name is valid (no special characters in name)
- [ ] Section exists (for edit/delete operations)
- [ ] Section doesn't exist (for add operations)
- [ ] Content is properly formatted

**Format Validation:**
- [ ] Section headers use exact format: `--- // <Name>`
- [ ] Template variables use correct syntax: `{{char}}` `{{user}}`
- [ ] Dialog lines use correct prefixes: `#{{char}}:` `#{{user}}:`
- [ ] Actions in asterisks, speech in quotes (in Example dialogs)

## Error Handling

**Common errors and responses:**

1. **File not found**
   - Response: "Error: Character file not found at [path]. Please verify the path and try again."

2. **Invalid section format**
   - Response: "Error: Section header must use format '--- // <Section Name>'. Found: [actual format]"

3. **Section already exists** (when adding)
   - Response: "Error: Section '[name]' already exists in character file. Use edit operation to modify existing section."

4. **Section not found** (when editing/deleting)
   - Response: "Error: Section '[name]' not found in character file. Available sections: [list]"

5. **Malformed character file**
   - Response: "Warning: Character file does not follow standard format. Proceeding with best-effort parsing. Validation recommended."

## Notes

- This skill performs **technical operations only** - it does not provide creative guidance
- All content is preserved exactly as provided - no automatic formatting or corrections
- Validation is advisory - files can be valid even with warnings
- Section order matters for readability but not for functionality
- The Personality section's internal structure (Scenario:, Appearance:, etc.) is **conventional only**
- Character files are plain text - can be edited with any text editor
- Default character file location: `/Users/jurriendokter/Library/Application Support/HammerAI/RP-CHARS/`

## Integration with Character Building

This skill is designed to be used **alongside** character building agents/tools:

- **Character Building Agents**: Guide users through creative character development
- **This Skill**: Handle the technical file operations requested by those agents
- **Workflow**: Agent decides what to write → calls this skill → skill performs file operation

The skill responds to direct file operation requests and provides structured, reliable file manipulation for character definition workflows.
