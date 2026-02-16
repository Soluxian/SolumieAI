# Ollama Model Check - 2026-02-16

## Available Models (9 total)
| Model | Size | Use Case | Status |
|-------|------|----------|--------|
| qwen3:0.6b | 522 MB | Quick tasks, testing | ✅ Fastest |
| qwen3:1.7b | 1.4 GB | Light reasoning | ✅ Good balance |
| qwen3:4b | 2.5 GB | Standard tasks | ✅ Reliable |
| qwen3:8b | 5.2 GB | Heavy reasoning | ✅ Best quality |
| ministral-3:3b | 3.0 GB | Alternative to Qwen | ⚠️ Slower |
| granite4:350m | 708 MB | Minimal tasks | ⚠️ Limited |
| lfm2.5-thinking:1.2b | 731 MB | Thinking tasks | ⚠️ Experimental |
| smollm2:135m | 270 MB | Micro tasks | ⚠️ Very limited |
| glm-ocr:q8_0 | 1.6 GB | OCR only | ⚠️ Specialized |

## Fallback Priority (Updated)
1. **qwen3:0.6b** - Speed priority (< 2 sec response)
2. **qwen3:1.7b** - Balance priority (quality + speed)
3. **qwen3:4b** - Quality priority (complex tasks)
4. **qwen3:8b** - Deep reasoning (research, sub-agents)

## Resource Usage
- Total disk: ~17 GB
- RAM per model: ~1-6 GB when loaded
- Recommendation: Load qwen3:1.7b as default, switch up/down as needed

## Performance Notes
- All models respond within acceptable range
- qwen3 family most reliable for general use
- 8b model best for creative/research sub-agents
- 0.6b perfect for heartbeat checks, quick queries

## Next Check
- Schedule: 12 hours
- Focus: Test reasoning quality on new tasks
