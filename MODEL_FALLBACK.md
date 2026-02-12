# OpenRouter Model Fallback Strategy

## Primary Model
- `openrouter/moonshotai/kimi-k2.5` - Default main model (when available)

## Free Tier Fallback Chain (40+ models for maximum uptime)

### Tier 1: High-Capability Leaders
1. `openrouter/deepseek/deepseek-chat:free` - DeepSeek v3, excellent reasoning
2. `openrouter/deepseek/deepseek-r1:free` - DeepSeek R1 reasoning model
3. `openrouter/tngtech/deepseek-r1t2-chimera:free` - Reasoning + chat hybrid
4. `openrouter/google/gemini-2.5-flash-preview:free` - Google's latest fast model
5. `openrouter/google/gemini-2.0-flash-exp:free` - Fast multimodal
6. `openrouter/meta-llama/llama-3.3-70b-instruct:free` - Meta's best open model
7. `openrouter/meta-llama/llama-3.1-405b-instruct:free` - Massive context window
8. `openrouter/nousresearch/hermes-3-llama-3.1-405b:free` - Large context, roleplay

### Tier 2: Specialized & Efficient
9. `openrouter/qwen/qwen2.5-72b-instruct:free` - Alibaba's best general model
10. `openrouter/qwen/qwen3-coder:free` - Code-specialized
11. `openrouter/qwen/qwen2.5-vl-72b-instruct:free` - Strong vision capabilities
12. `openrouter/anthropic/claude-3.5-haiku:free` - Anthropic efficiency
13. `openrouter/microsoft/phi-4:free` - Microsoft's Phi-4
14. `openrouter/nvidia/llama-3.1-nemotron-70b-instruct:free` - Helpful assistant
15. `openrouter/google/gemma-2-9b-it:free` - Google's efficient 9B
16. `openrouter/microsoft/phi-3.5-mini-instruct:free` - Lightweight but capable

### Tier 3: High-Volume & Reliable
17. `openrouter/anthracite-org/magnum-v4-72b:free` - Roleplay/creative
18. `openrouter/mistralai/mistral-nemo:free` - Efficient 12B
19. `openrouter/01-ai/yi-34b-chat:free` - Bilingual capable
20. `openrouter/01-ai/yi-1.5-34b-chat:free` - Yi 1.5 series
21. `openrouter/huggingfaceh4/zephyr-7b-beta:free` - Lightweight fallback
22. `openrouter/huggingfaceh4/zephyr-7b-alpha:free` - Alternative Zephyr
23. `openrouter/openchat/openchat-3.5-7b:free` - Conversational focus
24. `openrouter/teknium/openhermes-2.5-mistral-7b:free` - Hermes variant

### Tier 4: Additional Free Options
25. `openrouter/perplexity/sonar:free` - Perplexity's free tier
26. `openrouter/cohere/command-r:free` - Cohere Command-R
27. `openrouter/cohere/command-r-plus:free` - Cohere Command-R+
28. `openrouter/ai21/jamba-1.5-mini:free` - AI21 Labs model
29. `openrouter/sao10k/l3-lunaris-8b:free` - Creative specialized
30. `openrouter/aisingapore/sea-lion-7b-instruct:free` - Southeast Asian languages
31. `openrouter/liquid/lfm-40b:free` - Liquid AI model
32. `openrouter/moonshotai/moonlight-16b-a3b-instruct:free` - Moonshot light

### Tier 5: Emerging & Experimental
33. `openrouter/internlm/internlm2_5-20b-chat:free` - InternLM series
34. `openrouter/internlm/internlm2_5-7b-chat:free` - Smaller InternLM
35. `openrouter/THUDM/glm-4-9b-chat:free` - Tsinghua GLM-4
36. `openrouter/fireworks/firefunction-v2:free` - Function calling focused
37. `openrouter/snowflake/snowflake-arctic-instruct:free` - Enterprise focused
38. `openrouter/cognitivecomputations/dolphin-llama-3-70b:free` - Uncensored variant
39. `openrouter/undi95/remm-slerp-l2-13b:free` - Merge model
40. `openrouter/Gryphe/MythoMax-L2-13b:free` - Creative writing
41. `openrouter/PygmalionAI/mythalion-13b:free` - Roleplay specialized
42. `openrouter/NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO:free` - Mixtral variant

## Local Ollama Fallback (When all OpenRouter tiers exhausted)
- `qwen2.5:7b` or `qwen2.5:3b` - Local Qwen via Ollama
- `smollm2` - Ultra-lightweight local fallback
- `gemma2:2b` - Tiny but functional
- `phi3:mini` - Microsoft Phi-3 mini

## Usage Strategy
1. **Primary**: MoonShot Kimi 2.5 (paid tier preferred)
2. **Automatic Fallback**: OpenClaw handles OpenRouter 429 rate limits
3. **Local Backup**: Ollama when completely offline

## Monthly Maintenance Schedule
- **When**: 3 AM on the 1st of every month
- **Action**: Audit model status, remove dead models, add new free releases
- **Log**: All changes tracked in memory/YYYY-MM-DD.md files

Last Updated: 2026-02-12
Next Audit: 2026-03-01 03:00 EST
