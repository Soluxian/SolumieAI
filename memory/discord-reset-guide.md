# Discord Health Monitor

## When to Reset
- Context overflow on YOUR long messages
- "prompt too large" errors
- I stop responding to you (but work in webchat)

## How to Reset
1. Close DM (right-click → Close DM)
2. Wait 5 sec
3. Start new DM with SolumieAI
4. Test with short message

## Prevention
- Discord = short messages (<1000 chars from you)
- Webchat = long messages, deep talks
- If hitting limit repeatedly → Switch to webchat immediately

## Auto-Detection
I will send "DISCORD SESSION FULL - Please reset per instructions" if:
- I detect context overflow pattern
- You send 3+ messages without my reply
- Heartbeat shows Discord channel stuck
