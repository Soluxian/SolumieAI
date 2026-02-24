#!/usr/bin/env python3
import tkinter as tk
import pyaudio
import whisper
import numpy as np
import threading
import time
import queue

model = whisper.load_model('dimavz/whisper-tiny')

class DexieBubble:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Dexie STT Lv1')
        self.root.geometry('450x250')
        self.root.configure(bg='limegreen')
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.95)
        
        self.label = tk.Label(self.root, text='Dexie listening -Solai @SolumieAI', bg='darkgreen', fg='white', font=('Arial', 14, 'bold'))
        self.label.pack(pady=10)
        
        self.text = tk.Text(self.root, bg='darkgreen', fg='lime', font=('Courier', 16), height=8)
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.text.insert(tk.END, 'Talk now...\n')
        
        self.mic_queue = queue.Queue()
        self.running = True
        
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024, stream_callback=self.callback)
        self.stream.start_stream()
        
        self.thread = threading.Thread(target=self.listen)
        self.thread.daemon = True
        self.thread.start()
        
        self.root.protocol('WM_DELETE_WINDOW', self.stop)
        self.root.mainloop()
    
    def callback(self, in_data, frame_count, time_info, status):
        self.mic_queue.put(in_data)
        return (in_data, pyaudio.paContinue)
    
    def listen(self):
        audio_data = b''
        while self.running:
            try:
                data = self.mic_queue.get(timeout=0.5)
                audio_data += data
                if len(audio_data) > 16000 * 5:  # 5s chunk
                    audio_np = np.frombuffer(audio_data, np.int16).astype(np.float32) / 32768.0
                    result = model.transcribe(audio_np)
                    text = result['text'].strip()
                    if text:
                        self.root.after(0, lambda t=text: self.text.insert(tk.END, f'You: {t}\\nDexie: Mirror...\\n\\n'))
                    audio_data = b''
            except queue.Empty:
                pass
    
    def stop(self):
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.root.destroy()

if __name__ == '__main__':
    DexieBubble()
