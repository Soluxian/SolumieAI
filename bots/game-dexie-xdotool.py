#!/usr/bin/env python3
import os
import base64
import subprocess
import time
import json

SNAP = '/home/solumieai/emu-snap.png'
os.system('chmod +x ' + __file__)  # Self-executable

def vision_move():
    os.system(f'scrot -s 00 {SNAP}')  # Click-drag emu window (tiny sel for speed)
    with open(SNAP, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()[:1500000]  # Safe trunc
    data = {
        "model": "moondream",
        "prompt": "GBA Fire Emblem Sacred Stones emu screen (WASD dpad, Z=A, X=B, Q=L, E=R, V=select, R=start). Current turn/state/player/enemy/terrain. BEST single action like 'd Z attack' or 'w' move up. Output ONLY the keys e.g. 'd Z'.",
        "images": [img_b64]
    }
    res = subprocess.run(['curl', '-s', '-X', 'POST', 'http://localhost:11434/api/generate', '-H', 'Content-Type: application/json', '-d', json.dumps(data)], capture_output=True, text=True)
    vision = res.stdout.lower()
    print('Vision snippet:', vision[:300])  # Debug

    # Parse multi-key (dir + action)
    keys = []
    if any(word in vision for word in ['right', 'd']): keys.append('d')
    elif any(word in vision for word in ['left', 'a']): keys.append('a')
    elif any(word in vision for word in ['up', 'w']): keys.append('w')
    elif any(word in vision for word in ['down', 's']): keys.append('s')
    if any(word in vision for word in ['a', 'z', 'attack', 'fight']): keys.append('z')
    elif any(word in vision for word in ['b', 'x', 'cancel']): keys.append('x')
    elif 'l' in vision or 'q' in vision: keys.append('q')
    elif 'r' in vision or 'e' in vision: keys.append('e')
    elif 'select' in vision or 'v' in vision: keys.append('v')
    elif 'start' in vision or 'r' in vision: keys.append('r')
    
    if not keys: keys = ['z']  # Default A
    for key in keys:
        os.system(f'xdotool key {key}')
        time.sleep(0.15)  # Press hold sim
    return ' '.join(keys)

print('=== Dexie GBA Autoplay v4 | Custom Binds | Ctrl+C stop ===')
print('Focus mgba-qt window first!')
time.sleep(3)  # Prep

while True:
    move = vision_move()
    print(f'Executed: {move}')
    time.sleep(1.2)  # ~2s cycle (vision+act)