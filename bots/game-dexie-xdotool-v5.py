#!/usr/bin/env python3
import os
import base64
import subprocess
import time
import json
import tempfile

SNAP = '/tmp/emu-snap.png'
JSON_TMP = '/tmp/vision-dexie.json'

def get_emu_window():
    try:
        wid = subprocess.check_output(['xdotool', 'search', '--name', 'mGBA']).decode().strip()
        return wid.split('\n')[0]  # First match
    except:
        print('Emu window not found—open mgba-qt & focus manually.')
        return None

def vision_move():
    wid = get_emu_window()
    if wid:
        os.system(f'xdotool windowactivate {wid}')
        time.sleep(0.2)
    
    os.system(f'scrot -s {SNAP}')  # Mouse-drag select emu screen FAST
    time.sleep(0.5)  # Snap settle
    
    with open(SNAP, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    data = {
        "model": "moondream",
        "prompt": "GBA Fire Emblem Sacred Stones screen ONLY (keys: W=up A=left S=down D=right Z=A X=B Q=L E=R V=select R=start). Turn/state/units/enemies. BEST action e.g. 'D Z attack nearest' or 'W'. Output ONLY keys like 'D Z'.",
        "images": [img_b64]
    }
    
    with open(JSON_TMP, 'w') as f:
        json.dump(data, f)
    
    res = subprocess.run(['curl', '-s', '-XPOST', 'http://localhost:11434/api/generate', '-H', 'Content-Type: application/json', '-d', f'@{JSON_TMP}'], capture_output=True, text=True)
    vision = res.stdout.lower()
    os.system(f'rm -f {JSON_TMP}')
    print('Vision:', vision[:400])

    # Robust parse
    keys = []
    dirs = {'right': 'd', 'r': 'd', 'left': 'a', 'l': 'a', 'up': 'w', 'u': 'w', 'down': 's', 'dwn': 's'}
    acts = {'a': 'z', 'attack': 'z', 'fight': 'z', 'b': 'x', 'cancel': 'x', 'l': 'q', 'shoulder l': 'q', 'r shoulder': 'e', 'select': 'v', 'menu': 'v', 'start': 'r', 'pause': 'r'}
    
    for k,v in dirs.items(): if k in vision: keys.append(v); break
    for k,v in acts.items(): if k in vision: keys.append(v); break
    
    if not keys: keys = ['z']
    
    for key in keys:
        os.system(f'xdotool key {key}')
        time.sleep(0.2)
    return ' '.join(keys)

print('=== Dexie Autoplay v5 | Auto-focus + Tmp JSON + Robust Parse ===')
print('1. mgba-qt ROM & (background if needed)')
print('2. Focus emu once, then script handles.')
time.sleep(2)

while True:
    move = vision_move()
    print(f'>> {move}')
    time.sleep(1.5)