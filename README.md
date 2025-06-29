# Volume Wheel Controller

**Steuere die Systemlautstärke direkt per Mausrad an einem spezifizierten Eingabegerät unter Linux – ohne Desktop-Umgebung, ohne Keyboard-Shortcuts!**

## Was ist das?

Ein minimalistisches Python-Skript, das dein Mausrad-Event (`REL_HWHEEL`) abfängt und in Lautstärke-Anpassungen über PulseAudio bzw. PipeWire umwandelt. Ideal für Nutzer, die auf dedizierten Eingabegeräten (z.B. speziellen Mäusen, Trackpads oder anderen Eingabegeräten) eine schnelle und einfache Lautstärkeregelung per Scrollrad suchen.

## Features

* Erfasst direkt das Mausrad-Signal vom Linux-Input-Device (`/dev/input/eventX`)
* Steuert die Lautstärke via PulseAudio/PipeWire über das Python-PulseAudio-Client-API oder `pactl`
* Läuft als systemd-User-Service im Hintergrund — kein Terminal nötig
* Leicht anpassbar auf andere Eingabegeräte oder Aktionen
* Keine Abhängigkeit von Window-Managern, Desktop-Umgebungen oder zusätzlichen Tools
* Perfekt für minimalistische Setups oder spezialisierte Hardware-Workflows

## Installation

1. Python-Abhängigkeiten installieren:

   ```bash
   pip install evdev pulsectl
   ```
2. Skript an dein Eingabegerät anpassen (`/dev/input/eventX`)
3. Optional: systemd-User-Service anlegen und aktivieren

## Warum?

Weil Lautstärke-Regelung per Mausrad eigentlich simple Sache sein sollte – und manchmal will man keine schwergewichtigen Tools oder globale Hotkeys, sondern direkte Eingabeverarbeitung auf Linux-Ebene.

