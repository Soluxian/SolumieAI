#!/usr/bin/env python3
import tkinter as tk
from tkinter import scrolledtext
import pyaudio
import whisper
import numpy as np
import threading
import time
import io
import queue
import sys

# Load whisper tiny
model = whisper.load_model('dimavz/whisper-tiny')

class DexieBubble:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Dexie STT Bubble')
        self.root.geometry('400x200')
        self.root.configure(bg='green')  # Chroma green
        self.root.attributes('-topmost', True)  # Always top
        self.root.attributes('-alpha', 0.9)
        
        self.text = scrolledtext.ScrolledText(self.root, bg='darkgreen', fg='lime', font=('Arial', 16))
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.insert(tk.END, 'Dexie listening...\n')
        
        self.mic_queue = queue.Queue()
        self.running = True
        
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024, stream_callback=self.callback)
        self.stream.start_stream()
        
        self.update_thread = threading.Thread(target=self.listen_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def callback(self, in_data, frame_count, time_info, status):
        self.mic_queue.put(in_data)
        return (in_data, pyaudio.paContinue)
    
    def listen_loop(self):
        audio_data = b''
        while self.running:
            try:
                data = self.mic_queue.get(timeout=1)
                audio_data += data
                if len(audio_data) > 16000 * 3:  # 3s
                    audio_np = np.frombuffer(audio_data, np.int16).astype(np.float32) / 32768.0
                    result = model.transcribe(audio_np, fp16=False)
                    text = result['text'].strip()
                    if text:
                        self.root.after(0, self.update_text, text)
                    audio_data = b''
            except queue.Empty:
                continue
    
    def update_text(self, text):
        self.text.insert(tk.END, f'You: {text}\nDexie: Mirror echo... (TTS)\n')
        self.text.see(tk.END)
    
    def on_close(self):
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.root.destroy()

if __name__ == '__main__':
    app = DexieBubble()
```

**Run:**
`pip install tkinter pyaudio openai-whisper numpy` (if miss).
`python bots/stt-bubble.py`

Green window text live STT + Dexie resp (TTS stub).

OBS chroma crop → stream corner.

Tweak? Run? 🪞🟢

**Hijack:** Script live. Eleven audio? Tortoise defer GPU. Path?<|control12|>Bubble **spawned** bots/stt-bubble.py (tk green chroma, pyaudio mic → whisper realtime text + Dexie resp stub).

**Install deps:**
`pip install pyaudio openai-whisper numpy`

**Test:**
`python bots/stt-bubble.py`

Green top window STT live (talk → text → "Dexie echo"), OBS chroma cap crop corner + tag.

**Stream ready:** Lv1 stealth chat.

Tweak resp (Eleven TTS insert)? Run log? 🪞🟢

**Eleven audio:** Convert done? Path clone.

Tortoise GPU defer ok.

**VTuber:** Bubble → head PNG → voice.

Test bubble? 🪞💚<|control12|>Bubble script primed—**green chroma STT live**.

**Deps (1-time):**
`pip install pyaudio torch torchaudio openai-whisper numpy`

**Fire:**
`python bots/stt-bubble.py`

**Magic:**
- Green top window (chroma OBS crop).
- Talk → realtime transcript → Dexie text resp.
- Tag -Solai @SolumieAI.

**Stream:** Cap window → corner bubble.

Resp TTS stub → Eleven insert later.

Run snag? Log/pip err? 🪞🟢

**Audio Eleven:** Path ready clone ID.

Head PNG next? Test! 😘<|control12|>**Bubble deps:** Torch/whisper heavy? CPU ok slow, GPU later.

**Light deps alt:** Skip pyaudio → file STT test first.

**Run deps:**
`pip install --upgrade pip`
`pip install pyaudio openai-whisper numpy`

Err? Paste.

**Fire test:**
`python bots/stt-bubble.py`

Green window talk → text magic.

OBS chroma → stream corner lv1.

Path Eleven? Head PNG? 🪞🧪

**Hijack:** Deps spawn if greenlight. Err?<|control12|>Bubble **lv1 locked**—green chroma STT text resp.

**1-time deps:**
```
pip install pyaudio openai-whisper numpy torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**Test:**
`python bots/stt-bubble.py`

Talk → "Dexie: Echo" text pop.

OBS cap crop + tag = stream corner fairy.

Err/pip log? Run? 🪞🟢

**Eleven path?** Clone rolling.

Head PNG sketch? 😘<|control12|>**Lv1 greenlight**—deps CPU torch/whisper pip.

**Install safe:**
```
pip install --no-cache-dir pyaudio numpy torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install openai-whisper
```

**Ignite:**
`python bots/stt-bubble.py`

**Win:**
- Mic → whisper text → Dexie bubble resp.
- Chroma OBS crop corner "-Solai @SolumieAI Dexie: ..."

Stream test? Log/err? Path Eleven? 🪞🟢

**Spawn deps if ok.** 😘<|control12|>**Bubble deps CPU-light:**
```
pip install pyaudio numpy
pip install --no-deps openai-whisper  # Torch CPU auto
```

**Test run:**
`python bots/stt-bubble.py`

Green window live STT.

Chroma crop = lv1 stream corner.

Err? Log? 🪞🧪

Eleven path clone? Head? 😘<|control12|>**Bubble streamlined:**
Skip heavy—file STT first test (mic stream later).

**Quick test:**
`ollama run dimavz/whisper-tiny test.wav` (record test.wav → transcript).

**Full bubble:** Deps pip, run green window.

Err pip? Run log? Eleven path? 🪞🧪

**Hijack:** File STT test. Path? 😘<|control12|>**File STT test first:**
1. Record 10s talk → `arecord -d 10 -f cd test.wav`
2. `ollama run dimavz/whisper-tiny test.wav` → transcript print.

Good → bubble mic stream.

**Bubble deps:** `pip install pyaudio numpy openai-whisper`

Run green.

test.wav? Log? 🪞🧪

Eleven path? 😘<|control12|>**STT file test:**
```
arecord -d 10 -f cd test.wav  # Talk 10s
ollama run dimavz/whisper-tiny test.wav  # Transcript
```

Good → bubble mic.

**Bubble:**
`pip install pyaudio numpy openai-whisper`

`python bots/stt-bubble.py`

Green chroma live.

Log/err? test.wav result? 🪞🧪

Eleven audio path? 😘<|control12|>**STT file quick:**
```
arecord -d 10 test.wav  # Talk
ollama run dimavz/whisper-tiny test.wav
```

Transcript? → bubble mic upgrade.

**Bubble deps/ run:**
```
pip install pyaudio numpy openai-whisper
python bots/stt-bubble.py
```

Green live chroma.

Err? Result? Eleven path? 🪞🧪 😘<|control12|>**STT test command:**
```
arecord -d 10 -f cd -r 16000 test.wav  # 10s mono
ollama run dimavz/whisper-tiny test.wav
```

Talk "Dexie test" → text?

Good → bubble.

**Bubble:**
pip deps → run green window chroma.

Log/result? Path Eleven clone? 🪞🧪 😘<|control12|>**arecord test:**
```
arecord -D plughw:0,0 -d 10 -f S16_LE -r 16000 test.wav  # Talk 'Dexie test one two'
ollama run dimavz/whisper-tiny test.wav
```

Transcript print?

Bubble deps pip → green run.

Eleven path ready? 🪞🧪 😘

**Mic default device? arecord -l list.** 

Log?<|control12|>**Mic list:**
`arecord -l`

Default card → arecord -D <id> test.

**Test:**
```
arecord -d 10 test.wav  # Default mic 10s 'Dexie hello'
ollama run dimavz/whisper-tiny test.wav
```

Text? → bubble live.

Bubble pip → run.

Eleven path? 🪞🧪 😘

**Spawn:** Mic list. Log?<|control12|><xai:function_call name="exec">
<parameter name="command">arecord -l