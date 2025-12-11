# Claude Code Marketplace

Personal Claude Code plugin marketplace providing custom workflow automation and development tools.

## Installation

Install directly from GitHub inside Claude Code:

```bash
/plugin marketplace add git@github.com:WickedSik/claude.git
```

Then install the plugin(s):

```bash
/plugin install lughir@wickedsik
/plugin install adeptus-terra@wickedsik
```

## Available Plugins

### lughir

Personal development workflow tools including JIRA integration, conversation archival, and custom AI personalities.

**Slash Commands:**
- `/lughir:jira-to-task <issue_key>` - Transform JIRA issues into structured task files
- `/lughir:save-session` - Archive conversations with comprehensive analysis

**Output Styles:**
- `age-of-empires-2` - Medieval commander personality using AoE2 terminology
- `literary-mentor` - Warm writing workshop instructor providing honest craft feedback
- `tsundere` - Evolving AI personality with relationship phases

### adeptus-terra

Warhammer 40K themed agent suite for specialized development tasks with Imperial coordinator and specialist advisors.

**Output Styles:**
- `imperium-standard` - Warhammer 40K Imperium-themed development assistant with specialist coordination

**Specialist Agents:**
- Sister Famulous (Orders Famulous) - Architecture & dependency governance
- Tech-Priest Magos (Adeptus Mechanicus) - Code review & quality inspection
- Inquisitor - Security & vulnerability analysis
- Administratum Scribe - Documentation generation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
