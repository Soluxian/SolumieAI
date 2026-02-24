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

def snap_game():
    os.system(f"scrot {SEL_GEOM} {SNAP}")
    if os.path.exists(SNAP):
        print(f'Snap {os.path.getsize(SNAP)}b')
        return True
    print('Scrot fail—try manual.')
    os.system(f"scrot -s {SNAP}")
    return os.path.exists(SNAP)

def vision_move():
    wid = get_emu_window()
    if not wid:
        return
    os.system(f'xdotool windowactivate --sync {wid}; sleep 1')
    if not snap_game():
        return

    with open(SNAP, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()[:700000]

    data = {
        'model': 'moondream',
        'prompt': 'Fire Emblem GBA battle. Units enemies. BEST keys D Z etc ONLY.',
        'images': [img_b64],
        'stream': False
    }

    with open(JSON_TMP, 'w') as f:
        json.dump(data, f)

    res = subprocess.run(['curl', '-s', '-XPOST', 'http://localhost:11434/api/generate', '-d', '@' + JSON_TMP, '--max-time', '20'], capture_output=True, text=True, timeout=25)
    os.unlink(JSON_TMP)

    print('RC:', res.returncode)
    if res.returncode:
        print('Err:', res.stderr)
        return

    try:
        response = json.loads(res.stdout)['response'].upper()
    except:
        response = ''

    print('Vision:', repr(response[:60]))
    clean_keys = ''.join(c for c in response if c in VALID_KEYS) or 'Z'
    print('Keys:', clean_keys)

    for k in clean_keys:
        os.system(f'xdotool key {k}; sleep 0.3')
    print('---')

print('v17 | SIMPLE SCROT + TIMEOUT')
print('Battle map. ENTER.')
input()

while True:
    vision_move()
    time.sleep(2)