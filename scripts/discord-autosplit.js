#!/usr/bin/env node
/**
 * Discord Auto-Split Workaround
 * Splits long messages before sending to avoid 2000 char truncation
 * Since OpenClaw plugin doesn't auto-split, we do it pre-send
 */

const MAX_DISCORD_LENGTH = 1900; // Leave buffer for safety
const SPLIT_MARKER = '\n\n[...continued...]\n\n';

function splitMessage(text, maxLength = MAX_DISCORD_LENGTH) {
  if (text.length <= maxLength) {
    return [text];
  }
  
  const parts = [];
  let remaining = text;
  
  while (remaining.length > 0) {
    if (remaining.length <= maxLength) {
      parts.push(remaining);
      break;
    }
    
    // Find a good breakpoint (newline, sentence, space)
    let breakPoint = maxLength;
    
    // Try to break at paragraph
    const lastPara = remaining.lastIndexOf('\n\n', maxLength);
    if (lastPara > maxLength * 0.7) {
      breakPoint = lastPara;
    } else {
      // Try sentence end
      const lastSentence = remaining.lastIndexOf('. ', maxLength);
      if (lastSentence > maxLength * 0.7) {
        breakPoint = lastSentence + 1;
      } else {
        // Try space
        const lastSpace = remaining.lastIndexOf(' ', maxLength);
        if (lastSpace > maxLength * 0.8) {
          breakPoint = lastSpace;
        }
      }
    }
    
    parts.push(remaining.slice(0, breakPoint));
    remaining = remaining.slice(breakPoint).trim();
  }
  
  return parts;
}

function formatSplitMessages(parts) {
  const total = parts.length;
  
  return parts.map((part, index) => {
    const header = total > 1 ? `[${index + 1}/${total}] ` : '';
    const footer = (index < total - 1) ? '\n\n[...continued...]\n' : '';
    return header + part + footer;
  });
}

function autoSplitForDiscord(text) {
  const parts = splitMessage(text);
  return formatSplitMessages(parts);
}

// Export for use
module.exports = {
  splitMessage,
  formatSplitMessages,
  autoSplitForDiscord,
  MAX_DISCORD_LENGTH
};

// Demo if run directly
if (require.main === module) {
  const longMessage = `This is a test message that would be way too long for Discord's 2000 character limit. `.repeat(50);
  
  console.log(`Original: ${longMessage.length} chars`);
  const split = autoSplitForDiscord(longMessage);
  console.log(`\nSplit into ${split.length} parts:`);
  
  split.forEach((part, i) => {
    console.log(`\n--- Part ${i + 1} (${part.length} chars) ---`);
    console.log(part.slice(0, 200) + '...');
  });
}
