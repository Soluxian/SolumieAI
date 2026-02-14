#!/bin/bash
# Simple voice test - records 5 seconds, transcribes, responds via TTS

RECORDING_DIR="/tmp/voice-test"
mkdir -p "$RECORDING_DIR"

echo "Recording 5 seconds of audio..."
# Requires: sudo apt install alsa-utils or similar
# timeout 5 arecord -f cd -t wav "$RECORDING_DIR/input.wav" 2>/dev/null

echo "Test mode: Using text input instead"
read -p "Say something: " USER_INPUT

echo "Processing: $USER_INPUT"

# Log to memory
mkdir -p /home/solumieai/.openclaw/workspace/memory/voice-transcripts
echo "[$(date -Iseconds)] USER: $USER_INPUT" >> /home/solumieai/.openclaw/workspace/memory/voice-transcripts/$(date +%Y-%m-%d).log

# Generate response TTS (when ready)
# ~/.openclaw/tools/sherpa-onnx-tts/runtime/bin/sherpa-onnx-offline-tts \
#   --model-file ~/.openclaw/tools/sherpa-onnx-tts/models/model.onnx \
#   --tokens-file ~/.openclaw/tools/sherpa-onnx-tts/models/tokens.txt \
#   --output-file "$RECORDING_DIR/response.wav" \
#   "Response goes here"

echo "TTS output would play here"