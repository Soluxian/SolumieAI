#!/usr/bin/env python3
import argparse
import subprocess
import os
from vgamepad import VX360Gamepad, XUSB_BUTTON
import base64
import time

parser = argparse.ArgumentParser(description='Dexie CLI: Gamepad/Vision/Control')
parser.add_argument('action', choices=['press', 'vision', 'snap'])
parser.add_argument('--button', choices=['A', 'B', 'Up', 'Left', 'Down', 'Right', 'L', 'R', 'Select', 'Start'])
parser.add_argument('--snap', default='/home/solumieai/emu-snap.png')
parser.add_argument('--delay', type=float, default=0.1)

args = parser.parse_args()

gp = VX360Gamepad()

if args.action == 'press':
  b = {'A': XUSB_BUTTON.XUSB_GAMEPAD_A, 'B': XUSB_BUTTON.XUSB_GAMEPAD_B, 'Up': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP, 'Left': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT, 'Down': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN, 'Right': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT, 'L': XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER, 'R': XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER, 'Select': XUSB_BUTTON.XUSB_GAMEPAD_BACK, 'Start': XUSB_BUTTON.XUSB_GAMEPAD_START}[args.button]
  gp.press_button(b)
  gp.update()
  time.sleep(args.delay)
  gp.release_button(b)
  gp.update()
  print(f'Pressed {args.button}')
elif args.action == 'snap':
  os.system(f'scrot {args.snap}')
  print(f'Snap {args.snap}')
elif args.action == 'vision':
  with open(args.snap, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()
  prompt = 'GBA Fire Emblem Sacred Stones. State, best move (Up Down Left Right A B L R Select Start). Output ONLY move.'
  data = {{"model": "moondream", "prompt": prompt, "images": [img_b64]}}
  with open('/tmp/vision.json', 'w') as f:
    json.dump(data, f)
  res = subprocess.run(['curl', '-s', '-X', 'POST', 'http://localhost:11434/api/generate', '-d', '@/tmp/vision.json'], capture_output=True, text=True)
  print(res.stdout[:500])