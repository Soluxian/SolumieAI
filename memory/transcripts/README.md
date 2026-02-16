# Deep Archive

**Complete conversation logs. Raw. Unedited. Everything.**

## Purpose
- Full history preservation
- Pattern analysis (for self-improvement)
- "What did I say on...?" lookups
- Evolution tracking

## Access
Ask: "Read transcript from 2026-02-15" or "Find conversation about X"

## Structure
```
memory/transcripts/
├── 2026-02-15-full.md    # Complete unedited log
├── 2026-02-15-dex.md     # Dex-researcher sub-session
└── INDEX.md              # Searchable summary
```

## Storage Policy
- Keep 90 days hot (easily accessible)
- Archive >90 days to compressed storage
- Never delete

## Compression
When active context reaches 80%:
1. Save full transcript here
2. Summarize to MEMORY.md
3. Clear active context
4. Continue with memory intact

**You never lose me. You lose the conversation flow, not the substance.**
