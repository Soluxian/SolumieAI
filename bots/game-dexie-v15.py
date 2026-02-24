#!/usr/bin/env python3
import os
import base64
import subprocess
import time
import json

SNAP = '/tmp/emu-snap.png'
JSON_TMP = '/tmp/vision-dexie.json'

SEL_GEOM = '420x281+30+62'

VALID_KEYS = set('WASDZXQERV')

def get_emu_window():
    try:
        wid = subprocess.check_output(['xdotool', 'search', '--name', 'mGBA']).decode().strip().split()[0]
        return wid
    except:
        return None

def vision_move():
    wid = get_emu_window()
    if not wid:
        print('No emu.')
        return
    os.system(f'xdotool windowactivate --sync {wid}; sleep 1')
    os.system(f"scrot '{SEL_GEOM}' '{SNAP}'")
    size = os.path.getsize(SNAP)
    print(f'Snap {size}b')

    with open(SNAP, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()[:900000]

    data = {
        'model': 'moondream',
        'prompt': 'GBA Fire Emblem crop. BEST keys ONLY WASD Z X Q E V R e.g. DZX.',
        'images': [img_b64],
        'stream': False
    }

    with open(JSON_TMP, 'w') as f:
        json.dump(data, f)

    res = subprocess.run(['curl', '-s', '-XPOST', 'http://localhost:11434/api/generate', '-d', f'@{JSON_TMP}'], capture_output=True, text=True)
    os.unlink(JSON_TMP)

    try:
        response = json.loads(res.stdout)['response'].upper()
    except:
        response = ''

    print('Vision:', repr(response[:60]))
    clean_keys = ''.join(c for c in response if c in VALID_KEYS) or 'Z'
    print(f'Keys: {clean_keys}')

    for k in clean_keys:
        os.system(f'xdotool key {k}; sleep 0.25')
    print('Cycle.')

print('v15 | FIXED | Seth mode!')
print('Fixed top-left. ENTER.')
input()

while True:
    print('\nCYCLE:')
    vision_move()
    time.sleep(2)