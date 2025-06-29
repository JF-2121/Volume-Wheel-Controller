
# Volume Wheel Controller — README

## Übersicht

Dieses Python-Skript bindet das **Daumenrad (Thumbwheel) deiner Maus** an die Lautstärkeregelung deines Systems.
Es läuft im Hintergrund und reagiert nur auf das Thumbwheel, nicht auf normales Scrollen oder andere Maustasten.

---

## Features

* Nur das Thumbwheel steuert die Lautstärke (keine Störung anderer Maustasten wie „Zurück“ oder „Vor“)
* Kompatibel mit PulseAudio & PipeWire (über `pulsectl` Python-Bibliothek)
* Läuft als Hintergrundprozess (systemd User-Service empfohlen)
* Nutzt `evdev`, um nur das spezifische Mausrad-Gerät auszulesen

---

## Voraussetzungen

* Python 3 (idealerweise 3.8+)

* Python-Bibliotheken: `evdev`, `pulsectl`

  ```bash
  pip install evdev pulsectl
  ```

* Linux mit PulseAudio oder PipeWire (PulseAudio-Kompatibilitätsmodus)

* Zugriff auf das passende Input-Device (z. B. `/dev/input/event3` — prüfen mit `evtest` oder `sudo evemu-record`)

---

## Installation & Setup

1. **Device ermitteln:**

   Finde dein Thumbwheel-Input-Gerät mit:

   ```bash
   sudo evtest
   ```

   oder beobachte mit:

   ```bash
   sudo evemu-record
   ```

2. **Script anpassen:**

   Ersetze im Script die Device-Variable mit deinem Mausrad-Gerät, z.B.:

   ```python
   dev = InputDevice('/dev/input/event3')
   ```

3. **Systemd User-Service anlegen:**

   Erstelle die Datei `~/.config/systemd/user/volume-wheel.service` mit folgendem Inhalt:

   ```ini
   [Unit]
   Description=Volume Wheel Controller

   [Service]
   ExecStart=/usr/bin/python3 /home/user/volume_wheel.py
   Restart=always

   [Install]
   WantedBy=default.target
   ```

4. **Service starten & aktivieren:**

   ```bash
   systemctl --user daemon-reload
   systemctl --user enable volume-wheel.service
   systemctl --user start volume-wheel.service
   ```

   Damit läuft das Script automatisch im Hintergrund mit deinem Benutzer-Session-Umfeld.

---

## Wichtige Hinweise

* **Kein systemweiter Systemd-Service**
  PulseAudio/PipeWire läuft pro Benutzer-Session. Ein systemweiter Service (unter `/etc/systemd/system`) hat meist keinen Zugriff auf die Audio-Sockets und schlägt fehl.

* **Pulse-Socket und Umgebungsvariablen**
  Wenn du doch systemweit starten willst, musst du Umgebungsvariablen wie `XDG_RUNTIME_DIR` und `PULSE_SERVER` setzen — das ist aber komplizierter und meist unnötig.

* **Nur das Thumbwheel steuern**
  Das Script filtert jetzt nur Events mit `ecodes.REL_HWHEEL` oder `ecodes.REL_WHEEL`. So wird sichergestellt, dass andere Maustasten (Back, Forward, Scroll Wheel) nicht beeinflusst werden.

* **Zugriffsrechte**
  Dein Benutzer muss Leserechte auf `/dev/input/eventX` haben. Oft hilft es, den Benutzer zur Gruppe `input` hinzuzufügen oder das Script mit `sudo` zu starten (letzteres ist nicht empfohlen für dauerhaften Gebrauch).

---

## Beispiel: Wichtiger Codeausschnitt

```python
from evdev import InputDevice, ecodes
import pulsectl

dev = InputDevice('/dev/input/event3')  # Mausrad-Device anpassen
pulse = pulsectl.Pulse('volume-wheel')

for event in dev.read_loop():
    if event.type == ecodes.EV_REL and (event.code == ecodes.REL_HWHEEL or event.code == ecodes.REL_WHEEL):
        if event.value > 0:
            pulse.volume_change_all_chans(0.05)
        elif event.value < 0:
            pulse.volume_change_all_chans(-0.05)
```

---

## Troubleshooting

* **„Connection refused“ zu PulseAudio/PipeWire:**
  Meist weil das Script außerhalb der User-Session läuft. User-Systemd-Service benutzen.

* **Permission denied für `/dev/input/eventX`:**
  Prüfe Gruppenrechte oder starte testweise mit `sudo`.

* **Falsches Mausrad wird erkannt:**
  Prüfe mit `evtest` oder `evemu-record` dein Thumbwheel und passe den Device-Pfad im Script an.

---

