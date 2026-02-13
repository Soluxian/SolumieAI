# Ollama Local Model Integration

## Purpose
Use local LLMs for:
- Offline fallback when internet/API is unavailable
- Simple tasks (summarization, quick checks) without API cost
- Subagent processing without OpenRouter calls
- Always-available lightweight inference

## Available Models
```
glm-ocr:q8_0          1.6 GB   OCR tasks
smollm2:135m          270 MB   Ultra-lightweight
granite4:350m         708 MB   Reasoning
ministral-3:3b        3.0 GB   General purpose
lfm2.5-thinking:1.2b  731 MB   Thinking/reasoning
qwen3:1.7b            1.4 GB   General purpose
qwen3:0.6b            522 MB   Fast/simple
qwen3:4b              2.5 GB   Balanced
qwen3:8b              5.2 GB   Heavy reasoning
```

## Usage
```bash
# Quick simple task
./tools/ollama_subagent.sh qwen3:0.6b "Summarize this in one sentence"

# Background task (no API cost)
./tools/ollama_subagent.sh qwen3:4b "Analyze this text and extract key points"

# Offline mode (when OpenRouter fails)
./tools/ollama_subagent.sh qwen3:8b "Complex reasoning task"
```

## Heartbeat Integration
- Ollama health check every 20 minutes
- Fallback routing configured
- Offline mode automates local-only operation

## When to Use Ollama vs OpenRouter

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| Quick summaries | Ollama (qwen3:0.6b) | Fast, no API cost |
| Complex reasoning | OpenRouter | Better quality |
| Offline mode | Ollama | No internet needed |
| Heavy subagent tasks | OpenRouter | Parallel processing |
| Simple regex/logic | Ollama | Instant response |
| Creative writing | OpenRouter | Better coherence |

## Model Speed Hierarchy
1. **smollm2:135m** - Fastest (270MB)
2. **qwen3:0.6b** - Fast (522MB)  
3. **lfm2.5-thinking:1.2b** - Good speed (731MB)
4. **granite4:350m** - Balanced (708MB)
5. **qwen3:1.7b** - Better quality (1.4GB)
6. **ministral-3:3b** - Slower (3GB)
7. **qwen3:4b** - Heavy (2.5GB)
8. **qwen3:8b** - Slowest (5.2GB)

## RAM Considerations
With 8GB total system RAM:
- Use qwen3:0.6b or qwen3:1.7b for general tasks
- Only load qwen3:8b when necessary
- qwen3:4b is the sweet spot for quality vs memory

## Offline Mode Trigger
When OpenRouter returns 429 or connection errors:
1. Check Ollama availability
2. Route to qwen3:4b for most tasks
3. Route to qwen3:0.6b for simple checks
4. Log fallback event for review

Updated: 2026-02-13