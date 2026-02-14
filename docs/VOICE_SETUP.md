# Voice Interface Setup

## Status: IN PROGRESS

## Components

### 1. Speech-to-Text (STT) - OpenAI Whisper
**Status:** Pending Python/pip setup

**Installation needed:**
```bash
# Requires sudo or user pip install
pip3 install openai-whisper  
# OR
python3 -m pip install openai-whisper --break-system-packages
```

**Usage:**
```bash
# Transcribe audio file
whisper /path/to/audio.wav --model turbo --output_format txt

# Models available:
# - tiny: ~39 MB, fastest, least accurate
# - base: ~74 MB, fast, good accuracy  
# - small: ~244 MB, balanced
# - medium: ~769 MB, slower, better accuracy
# - large: ~1550 MB, slowest, best accuracy
# - turbo: optimized for speed
```

**Integration:**
- You record audio → Whisper transcribes locally → Sends text to Dexie
- All text saved to memory/ for logging
- Works offline once installed

### 2. Text-to-Speech (TTS) - sherpa-onnx
**Status:** Runtime downloaded, extracting

**Setup:**
```bash
# Runtime extracted to ~/.openclaw/tools/sherpa-onnx-tts/runtime
# Model downloading to ~/.openclaw/tools/sherpa-onnx-tts/models

# Usage:
~/.openclaw/tools/sherpa-onnx-tts/runtime/bin/sherpa-onnx-tts \
  --model-file ~/.openclaw/tools/sherpa-onnx-tts/models/model.onnx \
  --tokens-file ~/.openclaw/tools/sherpa-onnx-tts/models/tokens.txt \
  --output-file /tmp/response.wav \
  "Hello from Dexie"
```

**Features:**
- Fully offline TTS
- Piper voice model (en_US lessac high quality)
- Generates .wav files for playback

### 3. Discord Bot Voice
**Status:** Ready to configure

**Requirements:**
- Bot needs "Connect" and "Speak" permissions
- Voice channel access
- Can receive audio (if Discord supports bot STT)

**Setup:**
```json5
// In OpenClaw config
channels: {
  discord: {
    voice: true,
    // Additional voice-specific config
  }
}
```

## Architecture

### Offline Mode (Local Only)
```
You record → Whisper transcribes → Dexie responds → TTS generates → You hear
                ↓                           ↓
          Saved to memory/            Saved to memory/
```

### Online Mode (Discord)
```
You speak in VC → Discord bot receives → (Optional: Whisper confirm) → Dexie responds
                                                      ↓
                                               TTS → Discord plays
```

## Next Steps

1. **You install Whisper:**
   ```bash
   pip3 install openai-whisper
   ```
   
2. **I finish TTS setup:**
   - Extract sherpa-onnx runtime ✓
   - Download voice model
   - Test TTS generation
   
3. **Configure Discord voice:**
   - Check bot permissions
   - Enable voice channel features
   
4. **Integration test:**
   - Record test audio
   - Transcribe → Process → Synthesize
   - Full conversation logged

## Files
- Runtime: ~/.openclaw/tools/sherpa-onnx-tts/
- Config: docs/VOICE_SETUP.md
- Logs: memory/voice-transcripts/

Updated: 2026-02-13