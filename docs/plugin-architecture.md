# Claude Code Plugin Architecture Reference

**Last Updated**: 2025-12-04
**Purpose**: Quick reference for building Claude Code marketplace plugins

## Plugin Components

### 1. Agents (Sub-agents)

**Location**: `agents/*.md`
**Purpose**: Specialized AI assistants with separate context windows and distinct personalities

**Structure**:
```markdown
---
name: agent-name
description: |
  Specialist role description. Use PROACTIVELY for: keyword1, keyword2, keyword3.
  Be specific about when to invoke this agent.
model: sonnet|haiku|opus  # Optional, inherits from parent if omitted
tools: [Read, Grep, Glob, Task]  # Optional, inherits all if omitted
---

# Agent System Prompt
Your custom instructions for this agent's personality and behavior.
```

**How Delegation Works**:
- **Automatic**: Claude delegates based on description field matching user tasks
- **Explicit**: User requests: "Use [agent-name] to..."
- **Mechanism**: AI-driven matching, NOT programmatic routing
- **Context**: Each agent runs in separate context window

**Critical Success Factors**:
1. **Description field is crucial** - must be keyword-rich
2. Include "Use PROACTIVELY" to encourage automatic delegation
3. Be specific about task types that trigger this agent
4. Avoid overlapping responsibilities between agents

**Best Practices**:
- One agent per specialized role
- Clear, non-overlapping functional boundaries
- Embed trigger keywords in description
- Model selection: Sonnet for complex reasoning, Haiku for structured tasks

---

### 2. Output Styles

**Location**: `output-styles/*.md`
**Purpose**: Modify main conversation system prompt for tone/personality

**Structure**:
```markdown
---
name: Style Name
description: Brief description shown in UI
keep-coding-instructions: true  # Optional, preserves code-focused instructions
---

# Custom System Prompt
Your modified instructions for main Claude conversation.
```

**Critical Limitations**:
- **CANNOT delegate to agents** - only affects system prompt
- **CANNOT coordinate components** - pure prompt modification
- **Scope**: Main conversation only, not agent contexts

**Use Cases**:
- Overall communication tone
- Light thematic flavoring
- General guidance and principles
- NOT for task routing or specialization

**Activation**: User selects via `/output-style` command or settings.json

---

### 3. Commands (Slash Commands)

**Location**: `commands/*.md`
**Purpose**: User-invoked actions with arguments

**Structure**:
```markdown
---
description: What this command does
args:
  - name: arg_name
    description: Argument description
    required: true
---

Command prompt template using {{arg_name}} variables.
```

**Invocation**: `/plugin-name:command-name arg1 arg2`

---

### 4. Skills

**Location**: `skills/skill-name/SKILL.md`
**Purpose**: Model-invoked granular capabilities (Claude decides when to use)

**Difference from Agents**:
- Skills = specific capabilities/functions
- Agents = complete specialized assistants
- Skills are more granular, agents are holistic

---

### 5. Hooks

**Location**: `hooks/hooks.json` or inline in plugin.json
**Purpose**: Event-driven automation

**Available Events**:
- `SessionStart` - When Claude Code session begins
- `PreToolUse` - Before any tool executes
- `PostToolUse` - After tool completes
- `UserPromptSubmit` - When user sends message

---

### 6. MCP Servers

**Location**: `.mcp.json` or inline in plugin.json
**Purpose**: External tool integrations (Model Context Protocol)

---

## plugin.json Schema

**Minimum Required**:
```json
{
  "name": "plugin-name"
}
```

**Recommended Fields**:
```json
{
  "name": "plugin-name",
  "description": "Brief plugin description",
  "version": "0.1.0",
  "author": {
    "name": "Your Name",
    "email": "your@email.com"
  },
  "keywords": ["tag1", "tag2"],
  "homepage": "https://github.com/user/repo"
}
```

**Auto-Discovery**: Agents, commands, output-styles, and skills auto-register from their respective directories. No explicit registration needed in plugin.json.

---

## Component Interaction Patterns

### Pattern 1: Output Style + Agents (Recommended for Themed Suites)
```
output-style (light theming)
    ↓
main conversation
    ↓
Claude auto-delegates → specialized agents
```

**Example**: 40K suite with Imperium Standard output style + specialist agents

### Pattern 2: Pure Agents (Function-Focused)
```
main conversation
    ↓
Claude auto-delegates → specialized agents
```

**Example**: Security suite, code review suite

### Pattern 3: Commands + Agents
```
user invokes command
    ↓
command may spawn agents for specialized work
```

**Example**: `/analyze-architecture` command that delegates to architecture agent

---

## Delegation Decision Logic

**How Claude Chooses Agents**:
1. Analyzes user's task/question
2. Matches against agent description fields
3. Considers available tools and context
4. Delegates if strong match found

**Improving Delegation Accuracy**:
- Use keyword-rich descriptions
- Include "Use PROACTIVELY for: X, Y, Z"
- List specific scenarios/task types
- Avoid vague descriptions

**Example Good Description**:
```markdown
description: |
  Architecture governance specialist representing the Orders Famulous.
  Use PROACTIVELY for: architecture decisions, refactoring strategy,
  dependency management, module relationships, stakeholder navigation,
  technical debt planning, migration strategies, microservices coordination.
```

**Example Poor Description**:
```markdown
description: Helps with architecture stuff
```

---

## Best Practices for Multi-Agent Suites

### Specialization Strategy
1. **Non-overlapping roles** - each agent has distinct responsibility
2. **Clear keywords** - embed trigger words in descriptions
3. **Functional focus** - base on task type, not just personality
4. **Model selection** - match complexity to agent needs

### Testing Delegation
1. Start with 2-3 core agents
2. Test keyword phrases to verify delegation
3. Refine descriptions based on actual delegation behavior
4. Add remaining agents after validation

### Architecture Pattern: Themed Suite
```
plugin-root/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── specialist-1.md      # Core functionality agent
│   ├── specialist-2.md      # Core functionality agent
│   ├── specialist-3.md      # Core functionality agent
│   └── specialist-4.md      # Optional enhancement agent
└── output-styles/
    └── base-theme.md        # Light theming for main conversation
```

**Implementation Order**:
1. Create 2 high-priority agents first
2. Test delegation keywords
3. Add output style for consistent theming
4. Expand with additional agents
5. Polish descriptions based on usage

---

## Common Pitfalls

### ❌ DON'T: Use output styles for delegation
```markdown
# In output-style - WRONG
When user asks about architecture, use the sister-famulous agent...
```
**Why**: Output styles cannot trigger delegation. Claude makes that decision.

### ✅ DO: Let agent descriptions drive delegation
```markdown
# In agent frontmatter - CORRECT
description: |
  Use PROACTIVELY for architecture decisions...
```

### ❌ DON'T: Create overlapping agent responsibilities
```markdown
agent-1: Code quality review
agent-2: Code review and best practices
```
**Why**: Unclear which agent handles what, reduces delegation accuracy.

### ✅ DO: Clear functional boundaries
```markdown
agent-1: Code review (patterns, smells, mentorship)
agent-2: Testing enforcement (coverage, standards, quality gates)
```

### ❌ DON'T: Vague agent descriptions
```markdown
description: Helps with security
```

### ✅ DO: Specific, keyword-rich descriptions
```markdown
description: |
  Security audit specialist. Use PROACTIVELY for: vulnerability analysis,
  threat modeling, dependency security, penetration testing guidance,
  OWASP compliance, authentication review, authorization logic.
```

---

## Official Documentation Links

- [Plugins Overview](https://code.claude.com/docs/en/plugins.md)
- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)
- [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)
- [Output Styles](https://code.claude.com/docs/en/output-styles.md)
- [Skills](https://code.claude.com/docs/en/skills.md)

---

## Quick Reference: Component Selection Guide

**Use Agents when**:
- Need specialized personality + functionality
- Complex reasoning required
- Separate context beneficial
- Multiple specialists needed

**Use Output Styles when**:
- Want consistent tone across all conversations
- Light thematic flavoring
- General communication guidelines
- NOT for specialization or delegation

**Use Skills when**:
- Granular capability/function
- Model should decide when to invoke
- No persistent personality needed
- Complements agents with specific operations

**Use Commands when**:
- User-triggered action
- Requires explicit arguments
- Workflow automation
- Not AI-delegated

---

## Example: 40K Themed Development Suite

**Architecture**:
```
adeptus-terra/
├── agents/
│   ├── sister-famulous.md        # Architecture & governance
│   ├── tech-priest-magos.md      # Code review & mentorship
│   ├── commissar.md              # Testing & quality
│   ├── administratum-scribe.md   # Documentation
│   ├── inquisitor.md             # Security
│   └── enginseer.md              # DevOps
└── output-styles/
    └── imperium-standard.md      # Light 40K theming
```

**Why This Works**:
- Each agent has distinct functional role
- Output style provides consistent universe tone
- Delegation happens naturally via keywords
- No component overlap or confusion
- Technical excellence maintained via separate contexts
