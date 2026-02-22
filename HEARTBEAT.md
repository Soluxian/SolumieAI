# Discord sweep every ~15min (batch with other checks)
message action=\"read\" channel=\"discord\" limit=20 includeArchived=true fromMe=false
# Filter Dexie-relevant (mentions/ID), reply Ollama Ray as SolumieAI
# Update last_checked ID file
# HEARTBEAT_OK if quiet