#!/usr/bin/env python3
import os
import base64
import subprocess
import time
import json
import re

SNAP = '/tmp/emu-snap.png'
JSON_TMP = '/tmp/vision-dexie.json'

VALID_KEYS = set('WASDZXQERVwasdzxqerv')

def get_emu_window():
    try:
        wid = subprocess.check_output(['xdotool', 'search', '--name', 'mGBA']).decode().strip().split('\n')[0]
        print(f'WINID: {wid}')
        return wid
    except:
        return None

def do_move(keys_str):
    wid = get_emu_window()
    if wid:
        os.system(f'xdotool windowactivate --sync {wid}')
        time.sleep(1.2)
    clean_keys = ''.join(c for c in keys_str.upper() if c in VALID_KEYS)
    if not clean_keys:
        clean_keys = 'Z'
    print(f'Firing clean: {clean_keys}')
    for k in clean_keys:
        os.system(f'xdotool key {k}')
        time.sleep(0.3)
    print('Move complete. 4s obs...')

def vision_move():
    wid = get_emu_window()
    if wid:
        os.system(f'xdotool windowactivate --sync {wid}')
        time.sleep(1.0)

    print('\nDRAG emu...')
    os.system(f'scrot -s {SNAP}')
    time.sleep(0.5)

    with open(SNAP, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()
    print('Snap ready.')

    data = {
        'model': 'moondream',
        'prompt': 'GBA Fire Emblem screen. Ignore UI. Units/enemies grid. BEST move keys ONLY (W up A left S down D right Z A X B Q L E R V sel R start). Output ONLY e.g. \\\"DZ\\\" NO quotes/symbols.',
        'images': [img_b64[:1200000]],
        'stream': False  # Single JSON!
    }
    
    with open(JSON_TMP, 'w') as f:
        json.dump(data, f)

    res = subprocess.run(['curl', '-s', '-XPOST', 'http://localhost:11434/api/generate', '-d', f'@{JSON_TMP}'], capture_output=True, text=True)
    os.unlink(JSON_TMP)
    
    try:
        parsed = json.loads(res.stdout)
        response = parsed.get('response', '').lower()
    except:
        response = res.stdout.lower()
    
    print('Vision response:', repr(response[:100]))
    
    # Filter + greedy match
    keys_str = ''.join(c for c in response if c.upper() in VALID_KEYS)
    if len(keys_str) < 1:
        keys_str = 'Z'
    print(f'Parsed: {keys_str}')
    do_move(keys_str)

print('v9 | NO-STREAM + JUNK FILTER | Clean keys only')
print('Emu ready? ENTER.')
input()

cycle = 0
while True:
    cycle += 1
    print(f'\n=== CYCLE {cycle} ===')
    vision_move()
    time.sleep(4)