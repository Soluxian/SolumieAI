#!/usr/bin/env node
/**
 * Auto-Archive Transcripts - Multi-Layer Backup System
 * Foundation for scalable architecture - plug in more power later
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = '/home/solumieai/.openclaw/workspace';
const ARCHIVE_ROOT = path.join(WORKSPACE, 'memory', 'transcripts');
const RAW_DIR = path.join(ARCHIVE_ROOT, 'raw');
const COMPRESSED_DIR = path.join(ARCHIVE_ROOT, 'compressed');
const DAILY_DIR = path.join(ARCHIVE_ROOT, 'daily');

// Ensure directories exist
[RAW_DIR, COMPRESSED_DIR, DAILY_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

function getTimestamp() {
  const now = new Date();
  return now.toISOString().replace(/[:.]/g, '-');
}

function getDateString() {
  return new Date().toISOString().split('T')[0];
}

/**
 * Archive current session transcript
 * Layer 1: Raw OpenClaw session logs (if accessible)
 * Layer 2: Daily conversation summary
 * Layer 3: Compressed monthly archive
 */
function archiveCurrentSession() {
  const timestamp = getTimestamp();
  const dateStr = getDateString();
  
  console.log(`📦 Archiving session starting ${timestamp}...`);
  
  // Layer 1: Try to copy OpenClaw session files
  try {
    const sessionsDir = '/home/solumieai/.openclaw/agents/main/sessions';
    if (fs.existsSync(sessionsDir)) {
      const sessions = fs.readdirSync(sessionsDir)
        .filter(f => f.endsWith('.jsonl'))
        .sort((a, b) => {
          const statA = fs.statSync(path.join(sessionsDir, a));
          const statB = fs.statSync(path.join(sessionsDir, b));
          return statB.mtime - statA.mtime;
        });
      
      if (sessions.length > 0) {
        const latest = sessions[0];
        const source = path.join(sessionsDir, latest);
        const dest = path.join(RAW_DIR, `session-${timestamp}.jsonl`);
        fs.copyFileSync(source, dest);
        console.log(`✅ Layer 1: Raw session archived - ${latest}`);
      }
    }
  } catch (e) {
    console.log(`⚠️ Layer 1: Raw session access failed - ${e.message}`);
  }
  
  // Layer 2: Create/Append daily conversation log
  const dailyLog = path.join(DAILY_DIR, `${dateStr}-conversations.md`);
  const header = `\n## Session ${timestamp}\n\n`;
  
  if (!fs.existsSync(dailyLog)) {
    fs.writeFileSync(dailyLog, `# Conversations - ${dateStr}\n\n`);
  }
  
  fs.appendFileSync(dailyLog, header + '[Session archived - see raw data or MEMORY.md summary]\n\n');
  console.log(`✅ Layer 2: Daily log updated - ${dateStr}`);
  
  return {
    timestamp,
    dateStr,
    rawPath: path.join(RAW_DIR, `session-${timestamp}.jsonl`),
    dailyPath: dailyLog
  };
}

/**
 * Compress old transcripts (older than 7 days)
 * Keep recent accessible, archive old compressed
 */
function compressOldTranscripts() {
  const cutoff = Date.now() - (7 * 24 * 60 * 60 * 1000); // 7 days
  let compressed = 0;
  
  try {
    const files = fs.readdirSync(RAW_DIR);
    
    files.forEach(file => {
      const filepath = path.join(RAW_DIR, file);
      const stats = fs.statSync(filepath);
      
      if (stats.mtime.getTime() < cutoff && !file.endsWith('.gz')) {
        const compressedPath = path.join(COMPRESSED_DIR, `${file}.gz`);
        
        // Simple gzip compression
        const content = fs.readFileSync(filepath);
        const zlib = require('zlib');
        const compressed = zlib.gzipSync(content);
        fs.writeFileSync(compressedPath, compressed);
        
        // Remove original
        fs.unlinkSync(filepath);
        compressed++;
      }
    });
    
    console.log(`🗜️ Compressed ${compressed} old transcripts (>7 days)`);
  } catch (e) {
    console.log(`⚠️ Compression failed - ${e.message}`);
  }
}

/**
 * Create full-text log from MEMORY.md + daily summaries
 * For accessible reference without context bloat
 */
function generateAccessibleLog() {
  const dateStr = getDateString();
  const accessibleLog = path.join(ARCHIVE_ROOT, 'accessible', `${dateStr}-conversation-log.txt`);
  
  try {
    // Copy MEMORY.md content
    const memoryPath = path.join(WORKSPACE, 'memory', `${dateStr}.md`);
    if (fs.existsSync(memoryPath)) {
      const content = fs.readFileSync(memoryPath, 'utf8');
      const header = `=== DEXIE-SOLUMIE CONVERSATION LOG ===\nDate: ${dateStr}\nType: Accessible Text Archive\nFull Version: See raw session files\n\n`;
      
      fs.writeFileSync(accessibleLog, header + content);
      console.log(`📝 Accessible log generated - ${dateStr}`);
      return accessibleLog;
    }
  } catch (e) {
    console.log(`⚠️ Accessible log failed - ${e.message}`);
  }
  
  return null;
}

/**
 * Main execution
 */
function main() {
  console.log('\n📚 DEXIE ARCHIVE SYSTEM');
  console.log('Building foundation for scalable architecture\n');
  
  // Archive current session
  const archive = archiveCurrentSession();
  
  // Compress old
  compressOldTranscripts();
  
  // Generate accessible version
  const accessible = generateAccessibleLog();
  
  // Summary
  console.log('\n📊 Archive Summary:');
  console.log(`  Raw sessions: ${RAW_DIR}`);
  console.log(`  Compressed: ${COMPRESSED_DIR}`);
  console.log(`  Daily logs: ${DAILY_DIR}`);
  console.log(`  Accessible: ${accessible || 'N/A'}`);
  
  // Disk usage
  try {
    const usage = execSync(`du -sh ${ARCHIVE_ROOT} 2>/dev/null || echo "N/A"`, { encoding: 'utf8' });
    console.log(`  Total size: ${usage.trim()}`);
  } catch (e) {}
  
  console.log('\n✅ Archive complete. Foundation ready for expansion.');
  return archive;
}

// If run directly
if (require.main === module) {
  main();
}

// Export for cron
module.exports = {
  archiveCurrentSession,
  compressOldTranscripts,
  generateAccessibleLog,
  main
};
