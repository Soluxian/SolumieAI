#!/usr/bin/env node
/**
 * Hybrid Session Manager v2
 * Tiered approach: Compact twice, then new session
 * Tracks compact count per session
 */

const fs = require('fs');
const path = require('path');

const STATE_FILE = '/home/solumieai/.openclaw/workspace/memory/session-state.json';
const MAX_COMPACTS = 2; // After 2 compacts, force new session

function getSessionState() {
  if (fs.existsSync(STATE_FILE)) {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  }
  return {
    sessionStart: new Date().toISOString(),
    compactCount: 0,
    lastAction: null,
    totalCompactsThisSession: 0
  };
}

function saveSessionState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function checkContextAndAct() {
  const state = getSessionState();
  
  // Estimate context (heuristic)
  const memoryFiles = fs.readdirSync('/home/solumieai/.openclaw/workspace/memory')
    .filter(f => f.endsWith('.md'));
  const totalSize = memoryFiles.reduce((sum, f) => {
    try {
      const stats = fs.statSync(`/home/solumieai/.openclaw/workspace/memory/${f}`);
      return sum + stats.size;
    } catch (e) { return sum; }
  }, 0);
  
  const estimatedPercent = Math.min(95, Math.floor((totalSize / 500000) * 100));
  
  console.log(`📊 Context: ~${estimatedPercent}% | Compacts this session: ${state.compactCount}/${MAX_COMPACTS}`);
  
  // Decision tree
  if (estimatedPercent >= 95 || state.compactCount >= MAX_COMPACTS) {
    // Force new session
    console.log('🔄 MAX COMPACTS REACHED or 95% - Starting fresh session');
    
    // Archive this session's summary
    const timestamp = new Date().toISOString().split('T')[0];
    const summaryPath = `/home/solumieai/.openclaw/workspace/memory/summaries/session-${timestamp}-end.md`;
    
    fs.writeFileSync(summaryPath, `# Session End Summary\n\n` +
      `**Date:** ${timestamp}\n` +
      `**Compacts:** ${state.compactCount}\n` +
      `**Status:** Graceful restart for optimization\n\n` +
      `See MEMORY.md for continuity.\n`);
    
    // Reset state
    const newState = {
      sessionStart: new Date().toISOString(),
      compactCount: 0,
      lastAction: 'new_session',
      totalCompactsThisSession: 0,
      previousSessionEnd: timestamp
    };
    saveSessionState(newState);
    
    return {
      action: 'NEW_SESSION',
      reason: state.compactCount >= MAX_COMPACTS ? 'max_compacts_reached' : 'context_critical',
      message: `🔄 Session refreshed after ${state.compactCount} compacts. MEMORY.md continuity intact. Ready.`,
      archive: summaryPath
    };
    
  } else if (estimatedPercent >= 80) {
    // Compact
    state.compactCount++;
    state.lastAction = 'compact';
    state.totalCompactsThisSession++;
    saveSessionState(state);
    
    return {
      action: 'COMPACT',
      compactNumber: state.compactCount,
      maxCompacts: MAX_COMPACTS,
      message: `🔧 Compact ${state.compactCount}/${MAX_COMPACTS}. Context optimized. Continuing...`,
      nextAction: state.compactCount >= MAX_COMPACTS ? 'NEW_SESSION_NEXT' : 'CONTINUE'
    };
    
  } else {
    return {
      action: 'NONE',
      percent: estimatedPercent,
      compacts: state.compactCount,
      message: `✅ Context healthy (${estimatedPercent}%). Compacts: ${state.compactCount}/${MAX_COMPACTS}`
    };
  }
}

// Run
const result = checkContextAndAct();
console.log('\n' + result.message);
console.log(JSON.stringify(result, null, 2));
