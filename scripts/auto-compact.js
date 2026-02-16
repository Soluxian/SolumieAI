#!/usr/bin/env node
/**
 * Dexie Auto-Compact System
 * Monitors context usage and triggers summarization at 80% capacity
 */

const fs = require('fs');
const path = require('path');

const CONFIG_PATH = '/home/solumieai/.openclaw/workspace/config/context-management.json';
const MEMORY_DIR = '/home/solumieai/.openclaw/workspace/memory';
const TRANSCRIPT_DIR = '/home/solumieai/.openclaw/workspace/memory/transcripts';

// Estimate current context usage (rough heuristic)
function estimateContextUsage() {
  // In real implementation, this would check actual token count
  // For now, use message count as proxy
  try {
    const files = fs.readdirSync(MEMORY_DIR);
    const recentFiles = files.filter(f => f.endsWith('.md') && !f.includes('transcripts'));
    const totalSize = recentFiles.reduce((sum, f) => {
      const stats = fs.statSync(path.join(MEMORY_DIR, f));
      return sum + stats.size;
    }, 0);
    // Rough estimate: 1KB ~ 250 tokens, typical context 8K-32K tokens = 32KB-128KB
    const estimatedTokens = totalSize / 4; 
    const maxTokens = 32000; // Conservative estimate for typical model
    return Math.min((estimatedTokens / maxTokens) * 100, 100);
  } catch (e) {
    return 0;
  }
}

async function triggerCompact() {
  console.log('[AutoCompact] Triggering at ' + new Date().toISOString());
  
  // Implementation would:
  // 1. Save full transcript to TRANSCRIPT_DIR/YYYY-MM-DD-full.md
  // 2. Summarize key points to MEMORY.md
  // 3. Clear active context (handled by system)
  // 4. Log compaction event
  
  const today = new Date().toISOString().split('T')[0];
  const transcriptPath = path.join(TRANSCRIPT_DIR, `${today}-full.md`);
  
  // Ensure directory exists
  if (!fs.existsSync(TRANSCRIPT_DIR)) {
    fs.mkdirSync(TRANSCRIPT_DIR, { recursive: true });
  }
  
  // Create compaction marker
  const markerPath = path.join(MEMORY_DIR, '.compact-triggered');
  fs.writeFileSync(markerPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    reason: 'context_threshold_80',
    archivedTo: transcriptPath
  }, null, 2));
  
  console.log('[AutoCompact] Marker created. System will compact on next opportunity.');
}

// Main check
const usage = estimateContextUsage();
console.log(`[AutoCompact] Current estimate: ${usage.toFixed(1)}%`);

if (usage >= 80) {
  triggerCompact();
} else {
  console.log('[AutoCompact] Below threshold, no action needed.');
}
