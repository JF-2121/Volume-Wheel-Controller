#!/usr/bin/env python3
from evdev import InputDevice, ecodes
import pulsectl

dev = InputDevice('/dev/input/event3')  # Pfad anpassen
pulse = pulsectl.Pulse('volume-wheel')

ctrl_pressed = False

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY and event.code in (ecodes.KEY_LEFTCTRL, ecodes.KEY_RIGHTCTRL):
        ctrl_pressed = (event.value == 1)
    if ctrl_pressed and event.type == ecodes.EV_REL and event.code == ecodes.REL_HWHEEL:
        if event.value > 0:
            print("Volume up")
            pulse.volume_change_all_chans(0.05)
        elif event.value < 0:
            print("Volume down")
            pulse.volume_change_all_chans(-0.05)
