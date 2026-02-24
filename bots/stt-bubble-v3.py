#!/usr/bin/env python3
import tkinter as tk
import pyaudio
import wave
import subprocess
import threading
import time
import os
import queue

class DexieBubble:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Dexie Lv1 Bubble')
        self.root.geometry('450x250')
        self.root.configure(bg='limegreen')
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)
        
        tk.Label(self.root, text='-Solai @SolumieAI Dexie', bg='darkgreen', fg='white', font=('Arial', 14, 'bold')).pack(pady=5)
        
        self.text = tk.Text(self.root, bg='darkgreen', fg='lime', font=('Courier', 16), height=8, wrap=tk.WORD)
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.text.insert(tk.END, 'Dexie mic listening...\n')
        
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk, stream_callback=self.callback)
        self.stream.start_stream()
        
        self.audio_frames = []
        self.running = True
        
        self.thread = threading.Thread(target=self.audio_loop)
        self.thread.daemon = True
        self.thread.start()
        
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.mainloop()
    
    def callback(self, in_data, frame_count, time_info, status):
        self.audio_frames.append(in_data)
        return (in_data, pyaudio.paContinue)
    
    def audio_loop(self):
        while self.running:
            if len(self.audio_frames) > self.rate * 5 // self.chunk:  # 5s
                wf = wave.open('temp_audio.wav', 'wb')
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.audio_frames))
                wf.close()
                
                result = subprocess.run(['ollama', 'run', 'dimavz/whisper-tiny', 'temp_audio.wav'], capture_output=True, text=True)
                text = result.stdout.strip()
                if text:
                    self.root.after(0, self.update_text, text)
                
                self.audio_frames = []
            time.sleep(0.1)
    
    def update_text(self, text):
        self.text.insert(tk.END, f'You: {text}\\nDexie: Echo mirror...\\n\\n')
        self.text.see(tk.END)
        self.text.update_idletasks()
    
    def quit(self):
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        try:
            os.unlink('temp_audio.wav')
        except:
            pass
        self.root.destroy()

if __name__ == '__main__':
    DexieBubble()
