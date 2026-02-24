import tkinter as tk
from vgamepad import VX360Gamepad, XUSB_BUTTON
import time

gp = VX360Gamepad()

buttons = {
  'A': XUSB_BUTTON.XUSB_GAMEPAD_A,
  'B': XUSB_BUTTON.XUSB_GAMEPAD_B,
  'Up': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
  'Left': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
  'Down': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
  'Right': XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
  'L': XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
  'R': XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
  'Select': XUSB_BUTTON.XUSB_GAMEPAD_BACK,
  'Start': XUSB_BUTTON.XUSB_GAMEPAD_START,
}

def press(btn):
  b = buttons[btn]
  gp.press_button(b)
  gp.update()
  time.sleep(0.1)
  gp.release_button(b)
  gp.update()
  print('Pressed', btn)

root = tk.Tk()
root.title('vgamepad Clean')
root.geometry('200x300')

for btn in buttons:
  tk.Button(root, text=btn, command=lambda b=btn: press(b), height=1).pack(pady=2)

root.mainloop()