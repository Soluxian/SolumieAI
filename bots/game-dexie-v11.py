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
        print('No emu.')
        return None

def get_window_geom(wid):
    geom_out = subprocess.check_output(['xdotool', 'getwindowgeometry', wid]).decode()
    print('Geom raw:', repr(geom_out[:200]))
    
    pos_match = re.search(r'Position: (\d+), (\d+)', geom_out)
    geom_match = re.search(r'Geometry: (\d+)x(\d+)', geom_out)
    if pos_match and geom_match:
        x, y = int(pos_match.group(1)), int(pos_match.group(2))
        w, h = int(geom_match.group(1)), int(geom_match.group(2))
        return w, h, x, y
    print('Geom parse fail.')
    return None

def auto_snap(wid):
    geom = get_window_geom(wid)
    if not geom:
        print('Geom fail → manual drag.')
        os.system(f'scrot -s {SNAP}')
        return
    w, h, x, y = geom
    pad_x = pad_y = 30  # Title/border
    sel_w = max(240, w - 60)
    sel_h = max(160, h - 60)
    sel_x = x + 15
    sel_y = y + pad_y
    sel_str = f'{sel_w}x{sel_h}+{sel_x}+{sel_y}'
    print(f'Auto bbox: {sel_str}')
    os.system(f'scrot \'{sel_str}\' {SNAP}')
    print(f'Snap size: {os.path.getsize(SNAP) if os.path.exists(SNAP) else 0}b')

def do_move(keys_str):
    wid = get_emu_window()
    if wid:
        os.system(f'xdotool windowactivate --sync {wid}')
        time.sleep(1.2)
    clean_keys = re.sub(r'[^WASDZXQERV]', '', keys_str.upper())
    if not clean_keys:
        clean_keys = 'Z'
    print(f'Firing: {clean_keys}')
    for k in clean_keys:
        os.system(f'xdotool key {k}')
        time.sleep(0.25)
    print('Done.')

def vision_move():
    wid = get_emu_window()
    if not wid:
        return
    os.system(f'xdotool windowactivate --sync {wid}')
    time.sleep(0.8)
    auto_snap(wid)

    with open(SNAP, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    data = {
        'model': 'moondream',
        'prompt': 'GBA Fire Emblem game canvas. Grid/pos. BEST keys ONLY WASD Z X Q E V R e.g. DZX no other.',
        'images': [img_b64[:1000000]],
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
        response = res.stdout.upper()
    
    print('Vision:', repr(response[:60]))
    clean_keys = re.sub(r'[^WASDZXQERV]', '', response)
    if not clean_keys:
        clean_keys = 'Z'
    print(f'Final keys: {clean_keys}')
    do_move(clean_keys)

print('v11 | FIXED GEOM PARSE | Auto bbox even better')
print('Small fixed emu. ENTER.')
input()

cycle = 0
while True:
    cycle += 1
    print(f'\n=== {cycle} ===')
    vision_move()
    time.sleep(2)