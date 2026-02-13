#!/bin/bash
# Ollama local subagent - for lightweight tasks without API calls

MODEL="${1:-qwen3:0.6b}"
PROMPT="$2"

if [ -z "$PROMPT" ]; then
    echo "Usage: $0 <model> '<prompt>'"
    echo "Available models:"
    ollama list | tail -n +2
    exit 1
fi

echo "Running $MODEL locally..."
ollama run "$MODEL" "$PROMPT" 2>/dev/null