# OpenRouter Model Fallback Strategy

## Current Setup
- Hardware: HP Laptop, 8GB RAM, 128GB SSD
- Primary Source: OpenRouter (free tier priority)
- Local Backup: Ollama (for offline mode)

## Model Chain (Priority Order)

### Tier 1: High-Quality Free Models
1. **openrouter/moonshotai/kimi-k2.5** - Current primary (you're on this now)
2. **openrouter/deepseek/deepseek-chat:free** - Strong reasoning, generous limits
3. **openrouter/google/gemini-2.0-flash-exp:free** - Fast, good for quick tasks
4. **openrouter/meta-llama/llama-3.3-70b-instruct:free** - Solid all-rounder
5. **openrouter/qwen/qwen-2.5-72b-instruct:free** - Good code/reasoning

### Tier 2: Medium Fallback
6. **openrouter/mistralai/mistral-7b-instruct:free** - Lightweight, reliable
7. **openrouter/nousresearch/hermes-3-llama-3.1-405b:free** - Large context
8. **openrouter/microsoft/phi-4:free** - Efficient

### Tier 3: Emergency / Rate-Limited
9. **openrouter/undi95/toppy-m-7b:free** - Community model
10. **Local Ollama fallback** - When all APIs fail

## Fallback Logic
- On rate limit (429): Wait 60s → Try next model
- On timeout: Immediate retry with Tier 2
- On 5xx error: Skip that model for 1 hour

## Monthly Refresh Routine
Check this file monthly for:
- New free models added to OpenRouter
- Rate limit changes
- Model deprecations
- Better alternatives discovered

Last Updated: 2026-02-12
