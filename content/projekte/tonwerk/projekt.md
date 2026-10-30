---
name: Tonwerk
untertitel: Synthesizer und Effekte für Logic Pro, VST3 und iPad
reihenfolge: 20
kurz: '14 Instrumente, 17 Effekte und zwei MIDI-Effekte aus eigenem Code: als Audio Unit und VST3 kostenlos, auf dem iPad
  als App im App Store.'
einleitung: Instrumente und Effekte aus eigenem Code, vom analogen Synth über FM, Wavetable und Granular bis zum Acid-Bass
  und zur Drum-Machine, dazu Effekte für Vocals, Dubstep und den Mix.
technik:
- C++
- JUCE
- DSP
- AUv3
- VST3
links:
- text: tonwerk.studio
  url: https://tonwerk.studio/
- text: Im App Store laden
  url: https://apps.apple.com/de/app/tonwerk/id6824013223
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/Synth
steckbrief:
- name: Plattform
  wert: macOS, Linux, Windows, iPad, Eurorack
- name: Preis
  wert: kostenlos
- name: Lizenz
  wert: PolyForm Noncommercial 1.0.0
app:
  kategorie: MultimediaApplication
  plattformen: macOS, Linux, Windows, iPadOS
  url: https://tonwerk.studio/
  kostenlos: true
  store: https://apps.apple.com/de/app/tonwerk/id6824013223
---

## Was dazugehört

- **14 Instrumente:** Analog, FM, DX mit sechs Operatoren, Wavetable, Granular, Physical Modeling, Additiv, Phasenverzerrung, Sampler, Acid-Bass, Neuro-Bass, ein Expander nach Art der Siebziger, die Drum-Machine Groovebox und Rig, das ein Instrument mit bis zu sechs Effekten als einen Klang spielt.
- **17 Effekte** wie Robovox, Vocoder, Wobble, Tape, Shimmer, Bus-Kompressor, Multiband, dynamischer EQ und ein Oszilloskop mit Stimmgerät.
- **2 MIDI-Effekte:** ein Arpeggiator mit Step-Sequencer und ein LFO, der jeden Regler eines Tonwerk-Instruments bewegt.
- Eigene Werksklänge statt Kopien aus fremden Preset-Bänken, alle in der Lautstärke aufeinander abgestimmt.

## Wo es läuft

- **macOS:** Audio Unit für Logic Pro und VST3, signiert und notarisiert, für Apple Silicon und Intel.
- **Linux und Windows:** VST3 und eigenständige Apps.
- **iPad:** die App Tonwerk mit jedem Plugin als AUv3 für Logic Pro für iPad, GarageBand und AUM, im App Store.
- **Eurorack:** Tonwerk Wavetable als 14-HP-Modul mit einem ESP32-S3, mit Bauanleitung.

## Technik

C++ mit JUCE für Plugins und Apps, die Klangerzeugung als reines C++ ohne Abhängigkeiten, gebaut und getestet mit GitHub Actions für macOS, Linux, Windows und iPad. Die Firmware des Moduls läuft auf ESP-IDF.
