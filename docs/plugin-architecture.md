---
title      : Claude Code Plugin Architecture Reference
description: Quick reference for building Claude Code marketplace plugins
last_update: 2025-12-11
---

# Claude Code Plugin Architecture Reference

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
- **Tool selection**: Thoughtfully select minimal toolsets matching agent responsibilities
  - Grant only tools needed for the agent's specific role
  - Examples: Edit for code-modifying agents, Bash for security scanners, Write for documentation generators
  - Avoid granting all tools unless necessary

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

**Scope**: Main conversation only, not agent contexts

**Typical Use Cases**:
- Overall communication tone
- Light thematic flavoring
- General guidance and principles
- NOT typically used for task routing or specialization

**Important Clarification - Delegation Capability**:

Output styles **CAN technically delegate** to agents via the Task tool in the system prompt, despite common documentation suggesting otherwise. This is a **design preference**, not a technical limitation.

**Trade-offs of output style delegation**:

*Drawbacks*:
- Creates tight coupling between output style and agents
- Centralized coordination logic can be harder to maintain
- Single point of failure if output style is disabled
- Goes against separation of concerns principle

*Advantages*:
- **Deterministic delegation**: Known community issue - agents often fail to auto-delegate unless explicitly mentioned by users
- **Reliable coordination**: AI-driven delegation proves unreliable in practice for plugin agents
- **Continuous immersion**: Themed suites can maintain experience throughout workflow
- **Explicit control**: Predictable behavior instead of hoping AI recognizes keywords

**When delegation is appropriate**:
- Themed suites requiring continuous immersion in main conversation
- Explicit coordination of multiple specialists needed
- User experience depends on theatrical presentation of agent work
- **AI-driven delegation proves unreliable** (common community experience)

**Proven working example**: `adeptus-terra/output-styles/imperium-standard.md` successfully coordinates specialist agents via explicit Task tool invocations in system prompt, providing continuous 40K immersion while delegating to functional agents.

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

## Advanced Feature: Agent-Output Style Coordination

**Optional Pattern**: Agents can produce structured output that output styles parse and present with thematic enhancement.

**Discovery Note**: This pattern was validated during development of the `adeptus-terra` plugin. Initial implementation proved that output styles CAN delegate via Task tool invocations in system prompts, contradicting common documentation. See `.claude/tasks/imperium-standard-output-style.md` for implementation details and architectural discoveries.

**Why this matters**: The community actively experiences issues with agents not being automatically delegated unless explicitly mentioned by users. AI-driven delegation (via agent descriptions alone) proves unreliable in practice. Output style delegation provides deterministic coordination when automatic delegation fails.

### How This Works

**The Coordination Flow**:
```
User requests analysis
    ↓
Output style delegates to specialist agent
    ↓
Agent performs analysis, produces structured assessment
    ↓
Agent returns to main conversation
    ↓
Output style parses structured block, presents dramatically
```

### Why Use This Pattern

**Benefits**:
- **Quantified metrics**: Agents provide objective scores (e.g., "Purity: 68/100")
- **Consistent assessment**: Standardized format across all analyses
- **Theatrical presentation**: Output style adds thematic framing without compromising technical accuracy
- **Separation of concerns**: Agent focuses on analysis, output style handles presentation
- **Tracking over time**: Numeric scores enable progress measurement

**When to use**:
- Building themed development suites (e.g., 40K, fantasy, sci-fi)
- Want dramatic presentation of technical findings
- Need quantified quality/security/architecture metrics
- Multiple specialist agents with similar output needs

**When NOT to use**:
- Pure function-focused agents without theming
- Simple code review without dramatic presentation
- Agents that don't produce assessments (e.g., documentation generators)

### Implementation Example

**Agent Output** (tech-priest-magos.md):
~~~markdown
## Machine Spirit Status Assessment

**CRITICAL**: Conclude EVERY code review with this structured assessment.

### Assessment Format

Always end analysis with:

```
═══════════════════════════════════════════
⚙ MACHINE SPIRIT STATUS ASSESSMENT ⚙
═══════════════════════════════════════════
Purity Rating: [X]/100
Corruption Detected: [Y] instances
Tech-Heresy Level: [LEVEL]
═══════════════════════════════════════════
```

### Scoring Guidelines

**Purity Rating Calculation (0-100)**:
- Start at 100, deduct points for issues:
  - Critical issues (-15 each): Security vulnerabilities, data integrity risks
  - High priority (-10 each): SOLID violations, tight coupling, missing tests
  - Medium priority (-5 each): Code smells, duplicate code
  - Low priority (-2 each): Style issues, TODOs

**Tech-Heresy Level**:
- NONE: No serious violations
- MINOR: Small SOLID violations, simple code smells
- MODERATE: Multiple pattern violations, missing tests
- SEVERE: Security issues, major architectural violations
- CRITICAL: Data integrity risks, system-wide failure

### Integration Notes

The output style will parse this assessment block and present it
dramatically. This enables:
- Quantified code quality metrics
- Consistent assessment across reviews
- Theatrical presentation by output style
- Tracking improvements over time
```

**Output Style Presentation** (imperium-standard.md):
```markdown
## Presenting Specialist Reports

When Tech-Priest Magos provides Machine Spirit assessment:

**Parse the block and present based on Purity Rating**:

- **90-100 (Blessed)**:
  - "My lord, the Tech-Priest Magos reports the Machine Spirit is PLEASED."
  - "Purity Rating: 92/100 - blessed code, minimal corruption."

- **50-74 (Corrupted)**:
  - "My lord, the Tech-Priest Magos reports CORRUPTION has taken root."
  - "Purity Rating: 68/100 - the Machine Spirit is TROUBLED."
  - "12 instances of corruption detected. Sanctification rituals REQUIRED."

- **0-24 (Abomination)**:
  - "By the Throne! The Tech-Priest Magos reports an ABOMINATION!"
  - "Purity Rating: 18/100 - the Machine Spirit is in ANGUISH."
~~~

### Real-World Examples

**Example 1: Security Assessment**
```
Agent produces:
═══════════════════════════════════════════
🛡 SECURITY THREAT ASSESSMENT 🛡
═══════════════════════════════════════════
Threat Level: ELEVATED
Vulnerabilities: 7 identified
Risk Rating: 42/100
Critical Flaws: 2
═══════════════════════════════════════════

Output style presents:
"My lord, the Inquisitor reports HERESY DETECTED! Risk Rating: 42/100.
7 vulnerabilities identified, including 2 CRITICAL flaws. Immediate
purging required."
```

**Example 2: Architecture Analysis**
```
Agent produces:
═══════════════════════════════════════════
⚜ ARCHITECTURAL GOVERNANCE ASSESSMENT ⚜
═══════════════════════════════════════════
Structural Integrity: 62/100
Dependency Conflicts: 8 detected
Governance Level: STRAINED
Technical Debt: SIGNIFICANT
═══════════════════════════════════════════

Output style presents:
"My lord, Sister Famulous reports STRAINED architectural relations.
Structural Integrity: 62/100. 8 dependency conflicts threaten stability.
Diplomatic mediation recommended."
```

### Design Considerations

**Keep Agent Output Parseable**:
- Use consistent formatting (ASCII borders, specific line patterns)
- Include all metrics in predictable locations
- Document the exact format in agent instructions
- Provide scoring methodology in agent

**Output Style Responsibilities**:
- Parse the structured block (look for border patterns, extract metrics)
- Add thematic framing based on severity levels
- Preserve technical accuracy - never alter agent's findings
- Present highlights, user can read full agent output in context

**Maintain Separation**:
- Agent: Technical analysis + structured metrics
- Output style: Theatrical presentation + framing
- Never let theming obscure technical precision

### Alternative Approaches

If you don't need coordination:

**Simple Agent Output**: Just provide analysis without structured blocks
**Simple Output Style**: Just provide tone without parsing agent output
**Hybrid**: Agent provides structured output, but output style doesn't parse it (metrics still useful for user)

This pattern is **optional**. Many excellent agent suites work perfectly well without this coordination.

---

## Common Pitfalls

### ⚠️ TRADE-OFF: Output style delegation vs AI-driven delegation
```markdown
# Option A: Output style delegation (explicit)
When user asks about architecture, use Task tool to invoke sister-famulous agent...

# Option B: Agent description delegation (AI-driven)
description: |
  Use PROACTIVELY for architecture decisions...
```

**Option A (Output style delegation)**:
- ✅ Deterministic, reliable coordination
- ✅ Solves community issue of agents not auto-delegating
- ❌ Tight coupling, harder maintenance
- **Use when**: Themed suites, unreliable auto-delegation, explicit control needed

**Option B (AI-driven delegation)**:
- ✅ Separation of concerns, easier maintenance
- ✅ Follows conventional pattern
- ❌ Known community issue: agents often fail to auto-delegate
- **Use when**: Pure functional agents, auto-delegation works reliably

See "Advanced Feature: Agent-Output Style Coordination" section for implementation details.

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
