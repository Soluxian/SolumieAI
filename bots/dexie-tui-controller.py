#!/usr/bin/env python3
import curses
from vgamepad import VX360Gamepad, XUSB_BUTTON
import time

gp = VX360Gamepad()

buttons = [
  ('A', XUSB_BUTTON.XUSB_GAMEPAD_A),
  ('B', XUSB_BUTTON.XUSB_GAMEPAD_B),
  ('Up', XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP),
  ('Left', XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT),
  ('Down', XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN),
  ('Right', XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT),
  ('L', XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER),
  ('R', XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER),
  ('Select', XUSB_BUTTON.XUSB_GAMEPAD_BACK),
  ('Start', XUSB_BUTTON.XUSB_GAMEPAD_START),
]

def main(stdscr):
  curses.curs_set(0)
  stdscr.nodelay(1)
  stdscr.timeout(100)
  current = 0

  while True:
    stdscr.clear()
    stdscr.addstr(0, 0, 'Dexie TUI vGamepad Controller (q=quit, enter/press=select)')
    for i, (name, _) in enumerate(buttons):
      if i == current:
        stdscr.addstr(i+2, 0, '> ' + name, curses.A_REVERSE)
      else:
        stdscr.addstr(i+2, 0, '  ' + name)
    stdscr.refresh()

    key = stdscr.getch()
    if key == ord('q'):
      break
    elif key == curses.KEY_UP:
      current = (current - 1) % len(buttons)
    elif key == curses.KEY_DOWN:
      current = (current + 1) % len(buttons)
    elif key == 10 or key == 32:  # Enter/space
      name, b = buttons[current]
      gp.press_button(b)
      gp.update()
      time.sleep(0.1)
      gp.release_button(b)
      gp.update()
      stdscr.addstr(len(buttons)+3, 0, f'Pressed {name}')
      stdscr.refresh()
      time.sleep(0.2)

curses.wrapper(main)