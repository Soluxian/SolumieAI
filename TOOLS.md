# TOOLS.md - Local Notes
 
You are running on an old hp laptop with 8gb of ram and a 128gb ssd running linux mint using only free llms through openrouter and whatevere is free and can run on the laptop through ollama probably gonna be on really low parameter llms until we can upgrade or replace this device
Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- **solumie-laptop** → 192.168.1.98 (Windows, full access granted)
  - Status: Pending Windows OpenSSH setup
  - User: (need username)
  - Auth: Key-based preferred

### Network

- Private Starlink network
- Local devices: 192.168.1.x range

### OpenRouter Model Fallback
- See: MODEL_FALLBACK.md for full fallback chain
- Monthly audit cron: `monthly-model-refresh`
- Free tier priority: DeepSeek → Gemini → Llama → Qwen → Mistral

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
