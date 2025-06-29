#!/usr/bin/env python3
from evdev import InputDevice, ecodes
import pulsectl

dev = InputDevice('/dev/input/event3')  # Anpassen auf dein Gerät

pulse = pulsectl.Pulse('volume-wheel')

def change_volume(delta):
    default_sink_name = pulse.server_info().default_sink_name
    sink = pulse.get_sink_by_name(default_sink_name)
    vol = sink.volume
    new_values = [min(max(v + delta, 0.0), 1.0) for v in vol.values]
    new_vol = pulsectl.PulseVolumeInfo(new_values)
    pulse.volume_set(sink, new_vol)

for event in dev.read_loop():
    if event.type == ecodes.EV_REL and event.code == ecodes.REL_HWHEEL:
        if event.value < 0:
            print("Volume up")
            change_volume(0.05)
        elif event.value > 0:
            print("Volume down")
            change_volume(-0.05)
    # Alles andere ignorieren, also auch REL_WHEEL (normales Scrollrad)
