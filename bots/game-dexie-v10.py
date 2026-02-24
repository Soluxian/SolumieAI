#!/usr/bin/env python3
import os
import base64
import subprocess
import time
import json
import re

SNAP = '/tmp/emu-snap.png'
JSON_TMP = '/tmp/vision-dexie.json'
GEOM_FILE = '/tmp/emu-geom.txt'

VALID_KEYS = set('WASDZXQERVwasdzxqerv')

def get_emu_window():
    try:
        wid = subprocess.check_output(['xdotool', 'search', '--name', 'mGBA']).decode().strip().split('\n')[0]
        return wid
    except:
        return None

def get_window_geom(wid):
    geom = subprocess.check_output(['xdotool', 'getwindowgeometry', wid]).decode()
    w = re.search(r'Position: (\d+), (\d+) \((\d+)x(\d+)\)', geom)
    if w:
        return int(w.group(3)), int(w.group(4)), int(w.group(1)), int(w.group(2))
    return None

def auto_snap(wid):
    w, h, x, y = get_window_geom(wid)
    if not (w and h):
        print('Geom fail—manual drag.')
        os.system(f'scrot -s {SNAP}')
        return
    pad = 25  # Borders/title/titlebar
    sel_w, sel_h = max(200, w - pad*2), max(150, h - pad*2)
    sel_x, sel_y = x + pad, y + pad
    sel_str = f'{sel_w}x{sel_h}+{sel_x}+{sel_y}'
    print(f'Auto crop: {sel_str}')
    os.system(f'scrot -e "mv \$f {SNAP}" \'{sel_str}\'')
    time.sleep(0.3)

def do_move(keys_str):
    wid = get_emu_window()
    if wid:
        os.system(f'xdotool windowactivate --sync {wid}')
        time.sleep(1.0)
    clean_keys = re.sub(r'[^WASDZXQERV]', '', keys_str.upper())
    if not clean_keys:
        clean_keys = 'Z'
    print(f'Firing: {clean_keys}')
    for k in clean_keys:
        os.system(f'xdotool key {k}')
        time.sleep(0.25)
    print('Move done.')

def vision_move():
    wid = get_emu_window()
    if not wid:
        return 'NOEMU'
    os.system(f'xdotool windowactivate --sync {wid}')
    time.sleep(0.8)
    auto_snap(wid)
    print('Snap cropped.')

    with open(SNAP, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    data = {
        'model': 'moondream',
        'prompt': 'Fire Emblem GBA GAME area ONLY. Grid units/enemies. BEST keys seq ONLY (WASD dpad Z=A X=B Q=L E=R V=sel R=start) e.g. DZX no spaces/symbols.',
        'images': [img_b64[:1000000]],
        'stream': False
    }
    
    with open(JSON_TMP, 'w') as f:
        json.dump(data, f)
    
    res = subprocess.run(['curl', '-s', '-XPOST', 'http://localhost:11434/api/generate', '-d', f'@{JSON_TMP}'], capture_output=True, text=True)
    os.unlink(JSON_TMP)
    
    try:
        parsed = json.loads(res.stdout)
        response = parsed.get('response', '').upper()
    except:
        response = res.stdout.upper()
    
    print('Vision resp:', repr(response[:80]))
    clean_keys = re.sub(r'[^WASDZXQERV]', '', response)
    if not clean_keys:
        clean_keys = 'Z'
    print(f'Parsed/Final: {clean_keys}')
    do_move(clean_keys)
    return clean_keys

print('=== v10 AUTO-CROP | Fixed bbox | FAST cycles ===')
print('Resize emu SMALL fixed, focus once.')
print('ENTER start auto-loop.')
input()

cycle = 0
while True:
    cycle += 1
    print(f'\nCYCLE {cycle}:')
    keys = vision_move()
    print(f'{keys} | 2s next...')
    time.sleep(2)