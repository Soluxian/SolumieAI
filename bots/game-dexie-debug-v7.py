#!/usr/bin/env python3
import os
import base64
import subprocess
import time
import json

SNAP = '/tmp/emu-snap.png'
JSON_TMP = '/tmp/vision-dexie.json'

def get_emu_window():
    try:
        wid = subprocess.check_output(['xdotool', 'search', '--name', 'mGBA']).decode().strip().split('\n')[0]
        print(f'Found emu WINID: {wid}')
        return wid
    except:
        print('Emu hunt fail.')
        return None

print('DEBUG v7 | Step-by-step | Paste this log!')
wid = get_emu_window()
if wid:
    os.system(f'xdotool windowactivate --sync {wid}')
    print('1. Emu focused.')

print('2. scrot -s drag emu NOW...')
os.system(f'scrot -s {SNAP}')
print(f'Scrot done. SNAP: {os.path.exists(SNAP)} size {os.path.getsize(SNAP) if os.path.exists(SNAP) else 0}b')

with open(SNAP, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()
print('3. B64 ready, len:', len(img_b64))

data = {'model': 'moondream', 'prompt': 'GBA Fire Emblem. BEST keys WASD Z X Q E V R. ONLY \\\"D Z\\\".', 'images': [img_b64[:1000000]]}
with open(JSON_TMP, 'w') as f:
    json.dump(data, f)
print('4. JSON tmp written, size:', os.path.getsize(JSON_TMP))

res = subprocess.run(['curl', '-s', '-X', 'POST', 'http://localhost:11434/api/generate', '-d', f'@{JSON_TMP}'], capture_output=True)
print('5. Curl RC:', res.returncode)
print('Vision full:', res.stdout[:1000])
print('STDERR:', res.stderr.decode())

os.unlink(JSON_TMP)
os.unlink(SNAP)

# Test keys
print('6. Test key Z to emu...')
if wid:
    os.system(f'xdotool windowactivate {wid} key z')
print('Check emu for A-press reaction.')

print('Rerun after manual emu advance or paste for fix.')