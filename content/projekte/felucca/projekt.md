---
name: 'Felucca: WAVE-Engine'
untertitel: Synthesizer-Firmware für das M-VAVE FM-1
reihenfolge: 90
kurz: 'Ein Fork der Firmware Felucca mit einer vierzehnten Klangerzeugung: zwei Wavetable-Oszillatoren, acht Tabellen und
  Dubstep-Bässe.'
einleitung: 'Felucca ist eine freie Multi-Engine-Firmware für den kleinen Synthesizer M-VAVE FM-1. In meinem Fork kommt eine
  vierzehnte Engine dazu: WAVE.'
technik:
- C
- Embedded
- DSP
links:
- text: Mein Fork auf GitHub
  url: https://github.com/Marcel-B/Felucca
- text: Original von Hugelton
  url: https://github.com/hugelton/Felucca
steckbrief:
- name: Hardware
  wert: M-VAVE FM-1
- name: Lizenz
  wert: GNU GPL v3 (wie das Original)
---

## Die WAVE-Engine

- **Zwei Wavetable-Oszillatoren** und das Filter der ANALOG-Engine (Tiefpass, Bandpass, Hochpass).
- **Acht Tabellen** mit je acht Einzelzyklen, aus Formeln erzeugt statt aus fremden Wavetables: BASIC, PWM, SYNC, VOX, ORGAN, FM, HARM und DIGI, bandbegrenzt pro Oktave.
- **POS** blendet durch die Tabelle; Hüllkurve, LFO und Modulationsmatrix können es bewegen, ein synchronisierter LFO wird so zum Wobble.
- **Zwölf Presets** von WOBBLE, GROWL und RIDDIM bis PPG PAD, VOX PAD und PWM LEAD.

Alles andere ist die Firmware von Hugelton; dort gibt es auch den Web-Installer und eine Version zum Ausprobieren im Browser.

## Technik

C für den Mikrocontroller des FM-1, die Tabellen mit einem Python-Skript generiert.
