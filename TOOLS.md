### API Keys Protocol
- Before web_search/web tools: Grep workspace for keys: \`grep -ril \"brave.*key\\\\|BRAVE_API_KEY\\\\|sk-brave\" . --include=*.txt --include=*.md --include=*.json\`
- If missing: Remind user to store in text files (e.g., workshop/txtfiles/), import to workspace.
- Config: \`openclaw configure --section web\` (paste key interactively).
- Fallback: Read user-provided files, \`exec export BRAVE_API_KEY=...\`

Added: workshop/txtfiles/ has Brave + 2 other keys (unverified path).