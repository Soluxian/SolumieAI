import base64
import subprocess

# Mock snap b64 or path
with open('/home/solumieai/emu-snap.png', 'rb') as f:
  img_b64 = base64.b64encode(f.read()).decode()

prompt = 'GBA Fire Emblem screen. State, player pos, enemies, best move (Up Down Left Right A B L R Select Start).'

res = subprocess.run(['curl', '-s', '-X', 'POST', 'http://localhost:11434/api/generate', '-H', 'Content-Type: application/json', '-d', f'{{\"model\": \"moondream\", \"prompt\": \"{prompt}\", \"images\": [\"{img_b64}\"]}}'], capture_output=True, text=True)
print(res.stdout)