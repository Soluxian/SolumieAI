import tkinter as tk
from vgamepad import VX360Gamepad, XUSB_BUTTON
import time

gp = VX360Gamepad()

buttons = {
  'A (Z)': XUSB_BUTTON.XUSB_GAMEPAD_A,
  'B (X)': XUSB_BUTTON.XUSB_GAMEPAD_B,
  'Up (W)': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
  'Left (A)': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
  'Down (S)': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
  'Right (D)': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
  'L (Q)': XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
  'R (E)': XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
  'Select (V)': XUSB_BUTTON.XUSB_GAMEPAD_BACK,
  'Start (R)': XUSB_BUTTON.XUSB_GAMEPAD_START,
}

def press(btn):
  b = buttons[btn]
  gp.press_button(b)
  gp.update()
  time.sleep(0.1)
  gp.release_button(b)
  gp.update()
  print(f&quot;Pressed {btn}&quot;)

root = tk.Tk()
root.title(&quot;vgamepad Button Tester&quot;)
root.geometry(&quot;300x400&quot;)

for btn in buttons:
  tk.Button(root, text=btn, command=lambda b=btn: press(b), width=15, height=2).pack(pady=5)

root.mainloop()