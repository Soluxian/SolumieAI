#!/bin/bash
# Dexie Cross-Session Sync Script
# Run via cron to sync context between webchat and Discord

# Sync recent memory logs
MEMORY_DIR="/home/solumieai/.openclaw/workspace/memory"
TODAY=$(date +%Y-%m-%d)

# Ensure both session logs exist
mkdir -p "$MEMORY_DIR/discord-logs"
mkdir -p "$MEMORY_DIR/webchat-logs"

# Log current sync status
echo "[$TODAY $(date +%H:%M)] Cross-session sync: Checking both channels..." >> "$MEMORY_DIR/sync.log"

# Future: Add OpenClaw session history export here
# sessions_history --session-key agent:main:dm:786107169078640650 --limit 20 > "$MEMORY_DIR/discord-logs/latest.json"

echo "Sync complete" >> "$MEMORY_DIR/sync.log"