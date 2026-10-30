---
name: 'Felucca: WAVE-Engine'
untertitel: Synthesizer-Firmware für das M-VAVE FM-1
reihenfolge: 90
vision: Der kleine FM-1 soll mehr können, als ab Werk in ihm steckt. Mit der WAVE-Engine wird er zum Wavetable-Synthesizer
  für Wobble-Bässe und Flächen, frei wie die Firmware, auf der sie aufbaut.
kurz: 'Ein Fork der Firmware Felucca mit einer vierzehnten Klangerzeugung: zwei Wavetable-Oszillatoren, acht Tabellen und
  Dubstep-Bässe.'
technik:
- C
- Embedded
- DSP
links:
- text: Mein Fork auf GitHub
  url: https://github.com/Marcel-B/Felucca
- text: Original von Hugelton
  url: https://github.com/hugelton/Felucca
features:
- titel: Zwei Wavetable-Oszillatoren
  wozu: Klänge, die sich bewegen, auf einem Gerät für die Hosentasche.
  verhalten:
  - Dazu das Filter der ANALOG-Engine mit Tiefpass, Bandpass und Hochpass.
- titel: Acht eigene Tabellen
  wozu: Eine Klangpalette ohne fremde Wavetables.
  verhalten:
  - BASIC, PWM, SYNC, VOX, ORGAN, FM, HARM und DIGI mit je acht Einzelzyklen, aus Formeln erzeugt.
  - Bandbegrenzt pro Oktave.
- titel: Bewegte Position
  wozu: Wobble und Verläufe ohne Schrauben am Regler.
  verhalten:
  - POS blendet durch die Tabelle.
  - Hüllkurve, LFO und Modulationsmatrix können es bewegen; ein synchronisierter LFO wird so zum Wobble.
- titel: Zwölf Presets
  wozu: Gleich losspielen.
  verhalten:
  - Von WOBBLE, GROWL und RIDDIM bis PPG PAD, VOX PAD und PWM LEAD.
steckbrief:
- name: Hardware
  wert: M-VAVE FM-1
- name: Lizenz
  wert: GNU GPL v3 (wie das Original)
---

Alles andere ist die Firmware von Hugelton; dort gibt es auch den Web-Installer und eine Version zum Ausprobieren im
Browser.

## Technik

C für den Mikrocontroller des FM-1, die Tabellen mit einem Python-Skript generiert.
