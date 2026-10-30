---
untertitel: Synthesizers and effects for Logic Pro, VST3 and iPad
vision: An instrument collection of its own for everyone who makes music. Tonwerk is meant to offer synthesizers and
  effects that sound good, cost nothing and run wherever music is made, from Logic Pro and the iPad to Eurorack.
kurz: '14 instruments, 17 effects and two MIDI effects from original code: free as Audio Unit and VST3, and as an app on
  the iPad App Store.'
links:
- text: tonwerk.studio
  url: https://tonwerk.studio/
- text: Get it on the App Store
  url: https://apps.apple.com/app/tonwerk/id6824013223
- text: Source on GitHub
  url: https://github.com/Marcel-B/Synth
features:
- titel: 14 instruments
  wozu: The right kind of synthesis for every sound idea, instead of one synthesizer that does a little of everything.
  verhalten:
  - Analog, FM, DX with six operators, wavetable, granular, physical modelling, additive and phase distortion.
  - A sampler, acid bass, neuro bass, a seventies-style expander and the Groovebox drum machine.
  - Rig plays an instrument with up to six effects as one sound.
- titel: 17 effects
  wozu: From creative effects to tools for the mix.
  verhalten:
  - For voices and sound design Robovox, vocoder, Wobble, Tape and Shimmer.
  - For the mix a bus compressor, multiband and dynamic EQ.
  - An oscilloscope with a tuner.
- titel: 2 MIDI effects
  wozu: Bring movement into notes and sounds.
  verhalten:
  - An arpeggiator with a step sequencer.
  - An LFO that moves any control of a Tonwerk instrument.
- titel: Factory sounds of its own
  wozu: Ready to play, without hunting for presets or matching their levels.
  verhalten:
  - Every sound is made from scratch, none copied from other preset banks.
  - All are matched in loudness.
- titel: On the Mac
  wozu: In Logic Pro and any DAW with VST3.
  verhalten:
  - Audio Unit and VST3, signed and notarised.
  - For Apple Silicon and Intel.
- titel: On the iPad
  wozu: The same sounds on the go.
  verhalten:
  - The Tonwerk app on the App Store brings every plugin as an AUv3.
  - Runs in Logic Pro for iPad, GarageBand and AUM.
- titel: Linux and Windows
  wozu: Not tied to one platform.
  verhalten:
  - VST3 and standalone apps.
- titel: In Eurorack
  wozu: An instrument to touch.
  verhalten:
  - Tonwerk Wavetable as a 14 HP module with an ESP32-S3, with build instructions.
roadmap:
  als_naechstes:
  - 'Localisation: apps and plugins in more languages'
steckbrief:
- name: Platform
  wert: macOS, Linux, Windows, iPad, Eurorack
- name: Price
  wert: free
- name: Licence
  wert: PolyForm Noncommercial 1.0.0
---

## Technology

C++ with JUCE for plugins and apps, the sound engines as plain C++ without dependencies, built and tested with GitHub
Actions for macOS, Linux, Windows and iPad. The module's firmware runs on ESP-IDF.
