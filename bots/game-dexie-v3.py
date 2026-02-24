import os
import base64
import subprocess
import time
import json
from vgamepad import VX360Gamepad, XUSB_BUTTON

gp = VX360Gamepad()

SNAP = '/home/solumieai/emu-snap.png'
JSON_TMP = '/tmp/game-dexie.json'

print('Manual emu open ROM, Ctrl+C stop. Snaps', SNAP)

while True:
  os.system(f'scrot {SNAP}')
  with open(SNAP, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

  prompt = 'GBA Fire Emblem Sacred Stones screen. State, player units, enemies, terrain, best move (Up Down Left Right A B L R Select Start). Output ONLY move like \"Right A fight\".'

  data = {
    "model": "moondream",
    "prompt": prompt,
    "images": [img_b64]
  }

  with open(JSON_TMP, 'w') as f:
    json.dump(data, f)

  res = subprocess.run(['curl', '-s', '-X', 'POST', 'http://localhost:11434/api/generate', '-H', 'Content-Type: application/json', '-d', f'@{JSON_TMP}'], capture_output=True, text=True)

  vision = res.stdout
  move = 'A'
  if 'Right' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
  if 'Left' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
  if 'Up' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
  if 'Down' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
  if 'A' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_A)
  if 'B' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_B)
  if 'Start' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_START)
  if 'Select' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_BACK)

  print('Vision:', vision[:200])
  print('Move:', move)
  time.sleep(1)

def press(b):
  gp.press_button(b)
  gp.update()
  time.sleep(0.1)
  gp.release_button(b)
  gp.update()