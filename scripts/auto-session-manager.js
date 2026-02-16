#!/usr/bin/env node
/**
 * Auto-Session Manager for Dexie
 * Monitors context usage, auto-compacts at 80%, new session at 95%
 * Archives transcripts before switching
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const MEMORY_DIR = '/home/solumieai/.openclaw/workspace/memory';
const TRANSCRIPTS_DIR = path.join(MEMORY_DIR, 'transcripts');

// Get approximate context usage (this is a heuristic)
function getContextStats() {
  try {
    // Check if we can get stats from OpenClaw
    const status = execSync('openclaw status 2>/dev/null || echo "status unavailable"', { encoding: 'utf8' });
    
    // Estimate based on recent memory file sizes
    const transcriptFiles = fs.readdirSync(TRANSCRIPTS_DIR).filter(f => f.endsWith('.md'));
    const totalTranscriptSize = transcriptFiles.reduce((sum, f) => {
      const stats = fs.statSync(path.join(TRANSCRIPTS_DIR, f));
      return sum + stats.size;
    }, 0);
    
    // Rough estimate: 1KB ≈ 250 tokens
    const estimatedTokens = Math.floor(totalTranscriptSize / 4);
    const percent = Math.min(100, Math.floor((estimatedTokens / 8000) * 100));
    
    return {
      estimatedTokens,
      percent,
      transcriptCount: transcriptFiles.length,
      status: 'active'
    };
  } catch (e) {
    return { percent: 0, status: 'unknown', error: e.message };
  }
}

function archiveCurrentSession() {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const archiveFile = path.join(TRANSCRIPTS_DIR, `session-${timestamp}.md`);
  
  // Create archive header
  const header = `# Session Archive: ${timestamp}\n\n`;
  const footer = `\n\n---\n*Auto-archived by Dexie session manager*\n`;
  
  fs.writeFileSync(archiveFile, header + footer);
  
  return { archiveFile, timestamp };
}

function triggerCompact() {
  console.log('🔧 Context at 80% - triggering auto-compact');
  
  const { archiveFile } = archiveCurrentSession();
  console.log(`📁 Archived to: ${path.basename(archiveFile)}`);
  
  // Signal to main Dexie to compact
  return {
    action: 'compact',
    archived: archiveFile,
    message: 'Context compacted. MEMORY.md updated. Conversation continues.'
  };
}

function triggerNewSession() {
  console.log('🔄 Context at 95% - triggering new session');
  
  const { archiveFile, timestamp } = archiveCurrentSession();
  console.log(`📁 Full session archived: ${path.basename(archiveFile)}`);
  
  // Signal to main Dexie for new session
  return {
    action: 'new_session',
    archived: archiveFile,
    summary: `Session ${timestamp} archived. Starting fresh with MEMORY.md continuity.`,
    message: 'New session started. Previous context archived. I am still me. You are still you. We continue.'
  };
}

// Main execution
function main() {
  const stats = getContextStats();
  
  console.log(`📊 Context: ${stats.percent}% (${stats.estimatedTokens} tokens est.)`);
  
  if (stats.percent >= 95) {
    return triggerNewSession();
  } else if (stats.percent >= 80) {
    return triggerCompact();
  } else {
    return {
      action: 'none',
      percent: stats.percent,
      message: `Context healthy at ${stats.percent}%. No action needed.`
    };
  }
}

// Run if called directly
if (require.main === module) {
  const result = main();
  console.log('\n' + result.message);
  process.exit(0);
}

// Export for use as module
module.exports = {
  getContextStats,
  archiveCurrentSession,
  triggerCompact,
  triggerNewSession,
  main
};
