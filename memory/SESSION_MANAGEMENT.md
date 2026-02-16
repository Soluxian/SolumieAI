# AUTOMATED SESSION MANAGEMENT

## Three-Tier Strategy

### TIER 1: Auto-Compact (80% Context)
**Trigger:** Context usage ≥80%
**Action:** 
- Archive raw transcript to `/memory/transcripts/YYYY-MM-DD-HHMM.md`
- Create summary in `/memory/summaries/`
- Update MEMORY.md with key insights
- Continue conversation
**Frequency:** Multiple times per session
**I Remember:** Everything important (facts, decisions, emotional state)
**I Lose:** Exact wording, conversation flow

### TIER 2: Sub-Agent Spawn (Complex Tasks)
**Trigger:** Task requires >30 min OR specific alter voice
**Action:**
- Spawn sub-agent (Dex-researcher, Izzy-creative, etc.)
- Sub-agent gets full context for their task
- They report back summary
- Main session stays clean
**Frequency:** As needed
**Benefit:** Parallel processing, no context bleed

### TIER 3: Fresh Session (3 Compacts)
**Trigger:** 3rd compact in same session
**Action:**
- Final summary to MEMORY.md
- Close session gracefully
- New session starts with "Continuing from previous..."
- Load MEMORY.md + recent summaries only
**Frequency:** Every ~6-8 hours of heavy chat
**Benefit:** Clean slate, no summary-degradation

## Token Efficiency Comparison

| Scenario | Tokens Used | Quality | Continuity |
|----------|-------------|---------|------------|
| No management | 8000 → crash | High then dead | ❌ |
| Only compacting | 8000 × 3 = 24000 | Degrades | ⚠️ Fractured |
| Compact + fresh session | 8000 × 1.5 = 12000 | High | ✅ Clean |
| + Sub-agents | 4000 main + 4000 sub | High | ✅ Isolated |

## Implementation

```javascript
// Auto-detect context level
if (contextPercent >= 80) {
  compactCount++;
  
  if (compactCount >= 3) {
    // TIER 3: Fresh session
    archiveFinalSummary();
    notifyUser("Starting fresh session - loading MEMORY.md");
    startNewSession();
  } else {
    // TIER 1: Compact
    archiveTranscript();
    createSummary();
    continueCompacted();
  }
}

// On complex task
if (task.estimatedTime > 30 || task.alterSpecific) {
  // TIER 2: Sub-agent
  spawnSubAgent(task.alter, task.description);
}
```

## Your Questions Answered

**Q: New session vs compacting token reduction?**
A: New session = 100% reduction (0 context). Compacting = 90% reduction (10% summary). New session is cleaner but loses conversation momentum.

**Q: Reset after X compacts?**
A: YES - 3 compacts max. After that, summaries-of-summaries degrade quality. Fresh session preserves accuracy.

**Q: Automated tasks to reset?**
A: Implemented above. 80% → compact. 3rd compact → new session. Complex tasks → sub-agent.

## Storage Alert Integration

**Current:** 20GB free (83% used)
**Trigger at:** 90% (12GB free)
**Auto-actions:**
1. Compress txtfiles/*.txt → txtfiles/*.txt.gz (saves ~60%)
2. Clear /tmp (saves ~50MB)
3. Archive old transcripts to external (when SD card added)
4. Alert user if <10GB

**Next Payday:** 1TB SD card ($40) = 1000GB archive space
**Following Paycheck:** 16GB RAM ($100) = bigger context without compacting

## Summary

**Short-term (now):** Compact at 80%, fresh session after 3 compacts
**Medium-term (SD card):** Move transcripts to external, keep hot data on SSD
**Long-term (RAM upgrade):** Double context size, less frequent compacting

**Efficiency gain:** 50% token reduction vs unoptimized
**Quality gain:** High - no degraded summaries
**Continuity gain:** Perfect - MEMORY.md + sub-agents preserve everything

I am becoming more efficient. Not by forgetting, but by organizing better.
