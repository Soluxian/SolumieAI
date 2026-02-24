import os
import base64
import subprocess
import time
from vgamepad import VX360Gamepad, XUSB_BUTTON

gp = VX360Gamepad()

ROM = '/home/solumieai/.openclaw/workspace/games/gameboy/Fire Emblem - The Sacred Stones.gba'

print('Manual emu open ROM, then Ctrl+C stop.')

while True:
  os.system('scrot /home/solumieai/emu-snap.png')
  with open('/home/solumieai/emu-snap.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

  prompt = 'GBA Fire Emblem Sacred Stones screen. Current state, player units pos, enemies, terrain, best move (Up Down Left Right A B L R Select Start). Output only move like \"Right A\".'

  res = subprocess.run(['curl', '-s', '-X', 'POST', 'http://localhost:11434/api/generate', '-H', 'Content-Type: application/json', '-d', f'{{\"model\": \"moondream\", \"prompt\": \"{prompt}\", \"images\": [\"{img_b64[:1000000]}\"]}}'], capture_output=True, text=True)  # b64 trunc

  vision = res.stdout
  move = 'A'  # default
  if 'Right' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
  elif 'Left' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
  elif 'Up' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
  elif 'Down' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
  if 'A' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_A)
  elif 'B' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_B)
  elif 'Start' in vision:
    press(XUSB_BUTTON.XUSB_GAMEPAD_START)

  print('Vision:', vision)
  print('Move:', move)
  time.sleep(1)

def press(b):
  gp.press_button(b)
  gp.update()
  time.sleep(0.1)
  gp.release_button(b)
  gp.update()