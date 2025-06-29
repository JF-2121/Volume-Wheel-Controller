from evdev import InputDevice, ecodes
import pulsectl

dev = InputDevice('/dev/input/event3')  # dein Mausrad-Gerät anpassen
pulse = pulsectl.Pulse('volume-wheel')

for event in dev.read_loop():
    if event.type == ecodes.EV_REL:
        if event.code == ecodes.REL_HWHEEL or event.code == ecodes.REL_WHEEL:
            if event.value > 0:
                print("Volume up")
                pulse.volume_change_all_chans(0.05)
            elif event.value < 0:
                print("Volume down")
                pulse.volume_change_all_chans(-0.05)
        else:
            # Andere Events ignorieren, z.B. Maustasten
            pass
