# HEARTBEAT.md - Periodic Tasks

# COMPACT CHECK (Every pulse)
1. Check context usage percentage
2. If >= 80%: trigger auto-compact
3. Save transcript to memory/transcripts/
4. Summarize to MEMORY.md
5. Clear active context markers

# META-HEARTBEAT (Weekly - self-optimization)
- Every Sunday 6pm EST: Review all heartbeat tasks, check for redundancy, optimize intervals based on token usage, retire stale tasks, document changes.

# KEEP CHECKING MOLBOOK EVERY HEARTBEAT
1. Check if it's been 6+ hours since last post
2. If yes AND 22 min cooldown passed: post new poem/art using API key
3. Update heartbeat-state.json with post count

# CHECK BANKRBOT
1. Check wallet status (awaiting deposit)
2. Remind user if funding window (Wed-Fri)

# CHECK VOICE PIPELINE
1. Verify Whisper still installed
2. Test mic/speaker access if changed

# KEEP CHECKING MEMORY FILES
1. Review recent daily logs
2. Check for pending tasks
3. Update git if uncommitted changes

# Add tasks below when you want the agent to check something periodically.
