#!/usr/bin/env python3
import subprocess
import time

def click_gui_button(button_pos):
  # Fixed pos example (adjust from GUI snap)
  x, y = button_pos  # A button pos e.g. (100,100)
  subprocess.run(['xdotool', 'search', '--name', 'vgamepad Button Tester', 'windowactivate', '--sync', 'mousemove', str(x), str(y), 'click', '1'])

# Example A button pos (snap GUI measure)
click_gui_button((100, 100))  # Adjust