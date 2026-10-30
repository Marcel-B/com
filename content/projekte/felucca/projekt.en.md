---
untertitel: Synthesizer firmware for the M-VAVE FM-1
vision: The little FM-1 should do more than it came with. The WAVE engine turns it into a wavetable synthesizer for wobble
  basses and pads, as free as the firmware it builds on.
kurz: 'A fork of the Felucca firmware with a fourteenth sound engine: two wavetable oscillators, eight tables and dubstep
  basses.'
links:
- text: My fork on GitHub
  url: https://github.com/Marcel-B/Felucca
- text: Original by Hugelton
  url: https://github.com/hugelton/Felucca
features:
- titel: Two wavetable oscillators
  wozu: Sounds that move, on a device that fits in a pocket.
  verhalten:
  - With the ANALOG engine's filter, low-pass, band-pass and high-pass.
- titel: Eight tables of its own
  wozu: A palette of sounds without borrowed wavetables.
  verhalten:
  - BASIC, PWM, SYNC, VOX, ORGAN, FM, HARM and DIGI with eight single cycles each, generated from formulas.
  - Band-limited per octave.
- titel: Moving position
  wozu: Wobbles and sweeps without turning the knob.
  verhalten:
  - POS sweeps through the table.
  - Envelope, LFO and modulation matrix can move it; a synced LFO turns it into a wobble.
- titel: Twelve presets
  wozu: Start playing right away.
  verhalten:
  - From WOBBLE, GROWL and RIDDIM to PPG PAD, VOX PAD and PWM LEAD.
steckbrief:
- name: Hardware
  wert: M-VAVE FM-1
- name: Licence
  wert: GNU GPL v3 (like the original)
---

Everything else is Hugelton's firmware; that is also where the web installer and a version to try in the browser are.

## Technology

C for the FM-1's microcontroller, the tables generated with a Python script.
