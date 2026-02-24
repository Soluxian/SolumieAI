#!/usr/bin/env python3
import os
import base64
import subprocess
import time
import json

SNAP = '/tmp/emu-snap.png'
JSON_TMP = '/tmp/vision-dexie.json'

# Your bbox: X0 Y32 W480 H341 crop game pad30
SEL_GEOM = '420x281+30+62'  # Hardcoded stable top-left

VALID_KEYS = set('WASDZXQERV')

def get_emu_window():
    try:
        wid = subprocess.check_output(['xdotool', 'search', '--name', 'mGBA']).decode().strip().split('\n')[0]
        return wid
    except:
        return None

def snap_game():
    os.system(f'scrot \\'{SEL_GEOM}\\' {SNAP}')
    print(f'Snap: {os.path.getsize(SNAP) if os.path.exists(SNAP) else 0}b')

def do_move(keys_str):
    wid = get_emu_window()
    if wid:
        os.system(f'xdotool windowactivate --sync {wid}; sleep 1')
    clean_keys = ''.join(c for c in keys_str.upper() if c in VALID_KEYS) or 'Z'
    print(f'Executing: {clean_keys}')
    for k in clean_keys:
        os.system(f'xdotool key {k}')
        time.sleep(0.25)
    print('Cycle keys done.')

def vision_move():
    wid = get_emu_window()
    if not wid:
        print('Emu not found.')
        return
    os.system(f'xdotool windowactivate --sync {wid}')
    time.sleep(0.8)
    snap_game()

    with open(SNAP, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()[:900000]
    
    data = {
        'model': 'moondream',
        'prompt': 'GBA Fire Emblem cropped game screen. Units enemies grid. BEST keys seq ONLY (W up A left S down D right Z A X B Q L E R V menu R start). e.g. D Z X no symbols/spaces.',
        'images': [img_b64],
        'stream': False
    }
    
    with open(JSON_TMP, 'w') as f:
        json.dump(data, f)
    
    res = subprocess.run(['curl', '-s', '-XPOST', 'http://localhost:11434/api/generate', '-d', f'@{JSON_TMP}'], capture_output=True, text=True)
    os.unlink(JSON_TMP)
    
    try:
        parsed = json.loads(res.stdout)
        response = parsed['response'].upper()
    except:
        response = ''
    
    print('Vision:', repr(response)[:80])
    clean_keys = ''.join(c for c in response if c in VALID_KEYS) or 'Z'
    print(f'Keys: {clean_keys}')
    do_move(clean_keys)

print('=== v13 HARDCODED BBOX | ZERO DRAG | 2x speed ===')
print('Emu top-left 480x341 fixed. ENTER.')
input()

cycle = 0
while True:
    cycle += 1
    print(f'\nCYCLE {cycle}:')
    vision_move()
    print('Next 2s...')
    time.sleep(2)