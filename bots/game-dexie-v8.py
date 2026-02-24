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
        wid = subprocess.check_output(['xdotool', 'search', '--name', 'mGBA']).decode().strip().split('\n')[0]
        print(f'WINID: {wid}')
        return wid
    except:
        print('Emu MIA.')
        return None

def do_move(keys_str):
    wid = get_emu_window()
    if wid:
        os.system(f'xdotool windowactivate --sync {wid}')
        time.sleep(1.0)  # HP lag buffer
    for k in keys_str.split():
        print(f'Firing {k}...')
        os.system(f'xdotool key {k}')
        time.sleep(0.3)
    print('Move done. PAUSE 3s OBSERVE...')

def vision_move():
    wid = get_emu_window()
    if wid:
        os.system(f'xdotool windowactivate --sync {wid}')
        time.sleep(0.8)

    print('\nDRAG emu screen (crosshair)...')
    os.system(f'scrot -s {SNAP}')
    time.sleep(0.5)

    with open(SNAP, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()
    print('Snap b64 ok.')

    data = {'model': 'moondream', 'prompt': 'Fire Emblem GBA screen. Keys WASD dpad Z A X B Q L E R V select R start. BEST sequence ONLY e.g. \\\"D Z\\\" or \\\"W\\\".', 'images': [img_b64[:1500000]]}
    with open(JSON_TMP, 'w') as f:
        json.dump(data, f)

    res = subprocess.run(['curl', '-s', '-XPOST', 'http://localhost:11434/api/generate', '-d', f'@{JSON_TMP}'], capture_output=True, text=True)
    os.unlink(JSON_TMP)
    vision = res.stdout.lower()
    print('Vision:', [line for line in vision.splitlines() if 'response' in line][:3])

    # Extract responses
    responses = re.findall(r'"response":"([^"]*)"', vision)
    keys_str = ' '.join(''.join(responses).upper().strip('"! ,').split()) or 'Z'
    print(f'Parsed keys: {keys_str}')
    do_move(keys_str)

print('=== v8 HUMAN-TIMED | 1-3s buffers | Drag per cycle ===')
print('Emu open. Hit ENTER to start loop.')
input()

cycle = 0
while True:
    cycle += 1
    print(f'\n--- Cycle {cycle} ---')
    vision_move()
    print('Next cycle in 4s...')
    time.sleep(4)