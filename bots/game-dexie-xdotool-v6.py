#!/usr/bin/env python3
import os
import base64
import subprocess
import time
import json
import re

SNAP = '/tmp/emu-snap.png'
JSON_TMP = '/tmp/vision-dexie.json'

def get_emu_window():
    try:
        # Broader match for 'mGBA - 0.10.2'
        wid = subprocess.check_output(['xdotool', 'search', '--name', 'mGBA', 'search', '--class', 'mgba-qt']).decode().strip()
        return wid.split('\n')[0]
    except subprocess.CalledProcessError:
        print('No mGBA window—open manually.')
        return None

def vision_move():
    wid = get_emu_window()
    if wid:
        os.system(f'xdotool windowactivate --sync {wid}')
        time.sleep(0.3)
        print('Activated emu window.')
    
    print('\\n=== DRAG SELECT: Crosshair cursor - BOX emu screen QUICK (top-left to bottom-right) ===')
    os.system(f'scrot -s {SNAP}')
    time.sleep(0.5)
    
    with open(SNAP, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    data = {
        'model': 'moondream',
        'prompt': 'GBA Fire Emblem emu screen. Keys: WASD dpad Z=A X=B Q=L E=R V=select R=start. State/turn/units/enemies. BEST keys e.g. D Z attack or W. ONLY output keys like \\\"D Z\\\".',
        'images': [img_b64[:2000000]]
    }
    
    with open(JSON_TMP, 'w') as f:
        json.dump(data, f)
    
    res = subprocess.run(['curl', '-s', '-XPOST', f'http://localhost:11434/api/generate', '-d', f'@{JSON_TMP}'], capture_output=True, text=True)
    os.unlink(JSON_TMP)
    vision = res.stdout.lower()
    print('Vision out:', vision[:500])

    # Dict parse
    dirs = {'right': 'd', 'righ': 'd', 'left': 'a', 'lef': 'a', 'up': 'w', 'u': 'w', 'down': 's', 'dn': 's'}
    acts = {'a': 'z', 'attack': 'z', 'fight': 'z', 'confirm': 'z', 'b': 'x', 'cancel': 'x', 'back': 'x', 'l shoulder': 'q', 'l': 'q', 'r shoulder': 'e', 'r': 'e', 'select': 'v', 'menu': 'v', 'start': 'r', 'pause': 'r'}
    
    keys = []
    for k, v in dirs.items():
        if k in vision:
            keys.append(v)
            break
    for k, v in acts.items():
        if k in vision:
            keys.append(v)
            break
    if not keys:
        keys = ['z']
    
    for key in keys:
        os.system(f'xdotool key {key}')
        time.sleep(0.2)
    return keys

print('Dexie v6 | Auto-focus mGBA - 0.10.2 | Fixed syntax/scrot/curl')
print('Open emu FOREGROUND first, then run this.')
time.sleep(2)

while True:
    keys = vision_move()
    print(f'Keys fired: {' '.join(keys)}')
    time.sleep(1.5)