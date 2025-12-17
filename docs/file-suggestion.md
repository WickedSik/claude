# File Suggestion Script

> Claude documentation: [File Suggestion Setting](https://code.claude.com/docs/en/settings#file-suggestion-settings)

The default file suggestion script uses the `.gitignore` to exclude files and directories when using the `@` sign for finding files.
This is too limiting for my personal preference, so I created my own.

In your `$HOME/.claude/settings.json` you can add the following:

```json lines
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
```

> Note: the perspective of these changes are from a MacOS system, change as applicable to yours!

The `file-suggestion.sh` I use is the following:


```bash
#!/bin/bash

query=$(cat | jq -r '.query')
query_escaped=$(printf '%s' "$query" | sed 's/[*?[]/\\&/g')

# Expand CLAUDE_PROJECT_DIR to handle tilde properly
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR/#\~/$HOME}"

exclusion_file="$HOME/.claude/.suggestignore"
find_exclusions=()  # Initialize as array

# Load exclusions from file
if [ -f "$exclusion_file" ]; then
  while IFS= read -r pattern; do
    # Skip empty lines and comments
    [ -z "$pattern" ] || [[ "$pattern" =~ ^# ]] && continue
    pattern="${pattern%/}"  # Remove trailing slash
    find_exclusions+=(-o -path "$CLAUDE_PROJECT_DIR/$pattern")
  done < "$exclusion_file"
fi

{
  # Pass 1: Find matching files and directories
  if [ ${#find_exclusions[@]} -gt 0 ]; then
    find "$CLAUDE_PROJECT_DIR" \
      \( "${find_exclusions[@]:1}" \) -prune -o \
      -iname "*$query_escaped*" -print
  else
    find "$CLAUDE_PROJECT_DIR" \
      -iname "*$query_escaped*" -print
  fi

  # Pass 2: For each matching directory, list its contents
  if [ ${#find_exclusions[@]} -gt 0 ]; then
    find "$CLAUDE_PROJECT_DIR" \
      \( "${find_exclusions[@]:1}" \) -prune -o \
      -type d -iname "*$query_escaped*" -exec find {} -maxdepth 1 -mindepth 1 \;
  else
    find "$CLAUDE_PROJECT_DIR" \
      -type d -iname "*$query_escaped*" -exec find {} -maxdepth 1 -mindepth 1 \;
  fi
} | awk '!seen[$0]++' | awk -F'/' -v q="$query_escaped" '
  {
    score = 0
    depth = NF - 1
    score += (10 - depth)  # Shallower is better

    # Bonus for exact filename match
    if (tolower($NF) ~ "^" tolower(q) "$") score += 20

    # Bonus for preferred extensions
    if ($0 ~ /\.php$/) score += 5
    if ($0 ~ /\.sh$/) score += 5

    print score "\t" $0
  }
' | sort -rn | cut -f2- | sed "s|^$CLAUDE_PROJECT_DIR/||" | head -20
```

Of course, you can tweak both the scoring to get certain files higher in the list, and the various paths needed.

You can then create a `.suggestignore` file in your `$HOME/.claude` directory (or wherever you directed the `exclusion_file=` variable) which follows the same pattern as a `.gitignore` file. 

> Note: Unlike `.gitignore` files, which work hierarchically throughout a project, this script only reads exclusions from the single `.suggestignore` file specified by `$exclusion_file`.

Example:

```gitignore
# Dependency directories (any depth)
*/vendor
*/node_modules

# Version control (any depth)
*/.git

# Build artifacts (any depth)
*/dist
*/build
```

## Testing

Testing is fairly simple. Because of the way that Claude Code uses the suggestions, testing is executing a simple command

```bash
# Set project directory
export CLAUDE_PROJECT_DIR=~/path/to/project

# Search for 'searchterm'
~/.claude/file-suggestion.sh <<< '{"query":"searchterm"}'
```
