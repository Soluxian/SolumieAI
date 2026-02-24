#!/usr/bin/env python3
import os
import base64
import subprocess
import time
import json

SNAP = '/tmp/emu-snap.png'
JSON_TMP = '/tmp/vision-dexie.json'
BBOX_FILE = '/tmp/emu-bbox.txt'

VALID_KEYS = set('WASDZXQERVZ')

def load_bbox():
    if os.path.exists(BBOX_FILE):
        with open(BBOX_FILE) as f:
            lines = f.read()
        w = int(re.search(r'Width: (\d+)', lines).group(1))
        h = int(re.search(r'Height: (\d+)', lines).group(1))
        x = int(re.search(r'Absolute upper-left X: (\d+)', lines).group(1))
        y = int(re.search(r'Absolute upper-left Y: (\d+)', lines).group(1))
        return w, h, x, y
    return None

def save_bbox():
    print('RUN: xwininfo | grep -E \\'Absolute|Width|Height\\' > ' + BBOX_FILE)
    print('Emu focused/full, paste DONE when saved.')

def auto_snap(bbox=None):
    if bbox:
        w, h, x, y = bbox
        pad = 25
        sel_w, sel_h = w - 50, h - 50
        sel_x, sel_y = x + pad, y + pad
        sel = f'{sel_w}x{sel_h}+{sel_x}+{sel_y}'
        print(f'Using saved bbox: {sel}')
        os.system(f'scrot \'{sel}\' {SNAP}')
    else:
        print('No bbox—manual drag.')
        os.system(f'scrot -s {SNAP}')
    print(f'Snap: {os.path.getsize(SNAP)}b')

def do_move(keys_str):
    wid = subprocess.check_output(['xdotool', 'search', '--name', 'mGBA']).decode().strip().split('\n')[0]
    os.system(f'xdotool windowactivate --sync {wid}; sleep 1')
    clean = ''.join(c for c in keys_str.upper() if c in VALID_KEYS) or 'Z'
    print(f'Keys: {clean}')
    for k in clean:
        os.system(f'xdotool key {k}; sleep 0.25')
    
def vision_move():
    wid = subprocess.check_output(['xdotool', 'search', '--name', 'mGBA'], stderr=subprocess.DEVNULL).decode().strip().split('\n')[0] if subprocess.run(['xdotool', 'search', '--name', 'mGBA'], capture_output=True).returncode == 0 else None
    if not wid:
        print('No emu.')
        return
    os.system(f'xdotool windowactivate --sync {wid}; sleep 0.8')
    bbox = load_bbox()
    auto_snap(bbox)

    with open(SNAP, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()[:800000]
    
    data = {
        'model': 'moondream',
        'prompt': 'GBA Fire Emblem. BEST move keys ONLY WASDZXQERV e.g. D Z.',
        'images': [img_b64],
        'stream': False
    }
    
    with open(JSON_TMP, 'w') as f:
        json.dump(data, f)
    
    res = subprocess.run(['curl', '-s', '-XPOST', 'http://localhost:11434/api/generate', '-d', '@' + JSON_TMP], capture_output=True, text=True)
    os.unlink(JSON_TMP)
    
    response = json.loads(res.stdout)['response'].upper() if res.stdout else ''
    clean = ''.join(c for c in response if c in VALID_KEYS) or 'Z'
    print('Vision:', repr(response[:50]))
    print('Clean keys:', clean)
    do_move(clean)

print('v12 | BBOX SAVE | Drag-free')
if not os.path.exists(BBOX_FILE):
    save_bbox()
    print('Saved? Rerun.')
else:
    print('ENTER loop.')
    input()
    
cycle = 0
while True:
    cycle += 1
    print(f'CYCLE {cycle}')
    vision_move()
    time.sleep(2.5)