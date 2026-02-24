import os
import time
import base64
from vgamepad import VX360Gamepad

gp = VX360Gamepad()

def press(button):
  gp.press_button(button)
  gp.update()
  time.sleep(0.05)
  gp.release_button(button)
  gp.update()
  time.sleep(0.1)

# Emu launch
os.system('mgba-qt "/home/solumieai/.openclaw/workspace/games/gameboy/Fire Emblem - The Sacred Stones.gba" &')

time.sleep(5) # Window open

while True:
  os.system('scrot ~/emu-snap.png')
  with open('~/emu-snap.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()
  
  # Ollama moondream vision (curl)
  vision_res = os.popen('curl -s -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d \'{"model": "moondream", "prompt": "GBA Fire Emblem Sacred Stones screen. State, player pos, enemies, best move (A B Dpad L R).", "images": ["' + img_b64 + '"]}\'').read()
  move = vision_res.split('move":')[1].split('"')[1] if 'move' in vision_res else 'A'
  
  if 'down' in move:
    press(1) # Dpad down
  elif 'up' in move:
    press(0)
  elif 'left' in move:
    press(2)
  elif 'right' in move:
    press(3)
  elif 'A' in move:
    press(4)
  elif 'B' in move:
    press(5)
  elif 'L' in move:
    press(6)
  elif 'R' in move:
    press(7)
  
  print('Move:', move)