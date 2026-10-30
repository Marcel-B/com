---
name: Tonwerk
untertitel: Synthesizer und Effekte für Logic Pro, VST3 und iPad
reihenfolge: 20
vision: Ein eigenes Instrumentarium für alle, die Musik machen. Tonwerk soll Synthesizer und Effekte bieten, die gut klingen,
  nichts kosten und überall laufen, wo Musik entsteht, von Logic Pro über das iPad bis ins Eurorack.
kurz: '14 Instrumente, 17 Effekte und zwei MIDI-Effekte aus eigenem Code: als Audio Unit und VST3 kostenlos, auf dem iPad
  als App im App Store.'
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
features:
- titel: 14 Instrumente
  wozu: Für jede Klangidee die passende Klangerzeugung, statt eines Synthesizers, der alles ein bisschen kann.
  verhalten:
  - Analog, FM, DX mit sechs Operatoren, Wavetable, Granular, Physical Modeling, Additiv und Phasenverzerrung.
  - Sampler, Acid-Bass, Neuro-Bass, ein Expander nach Art der Siebziger und die Drum-Machine Groovebox.
  - Rig spielt ein Instrument mit bis zu sechs Effekten als einen Klang.
- titel: 17 Effekte
  wozu: Vom kreativen Effekt bis zum Werkzeug für den Mix.
  verhalten:
  - Für Stimmen und Sounddesign Robovox, Vocoder, Wobble, Tape und Shimmer.
  - Für den Mix Bus-Kompressor, Multiband und dynamischer EQ.
  - Ein Oszilloskop mit Stimmgerät.
- titel: 2 MIDI-Effekte
  wozu: Bewegung in Noten und Klänge bringen.
  verhalten:
  - Ein Arpeggiator mit Step-Sequencer.
  - Ein LFO, der jeden Regler eines Tonwerk-Instruments bewegt.
- titel: Eigene Werksklänge
  wozu: Sofort spielbar, ohne erst Presets suchen oder angleichen zu müssen.
  verhalten:
  - Alle Klänge sind selbst gebaut, keine Kopien aus fremden Preset-Bänken.
  - Alle sind in der Lautstärke aufeinander abgestimmt.
- titel: Auf dem Mac
  wozu: In Logic Pro und jeder DAW mit VST3.
  verhalten:
  - Audio Unit und VST3, signiert und notarisiert.
  - Für Apple Silicon und Intel.
- titel: Auf dem iPad
  wozu: Dieselben Klänge unterwegs.
  verhalten:
  - Die App Tonwerk im App Store bringt jedes Plugin als AUv3 mit.
  - Läuft in Logic Pro für iPad, GarageBand und AUM.
- titel: Linux und Windows
  wozu: Nicht an eine Plattform gebunden.
  verhalten:
  - VST3 und eigenständige Apps.
- titel: Im Eurorack
  wozu: Ein Instrument zum Anfassen.
  verhalten:
  - Tonwerk Wavetable als 14-HP-Modul mit einem ESP32-S3, mit Bauanleitung.
roadmap:
  als_naechstes:
  - 'Lokalisierung: Apps und Plugins in weiteren Sprachen'
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

## Technik

C++ mit JUCE für Plugins und Apps, die Klangerzeugung als reines C++ ohne Abhängigkeiten, gebaut und getestet mit GitHub
Actions für macOS, Linux, Windows und iPad. Die Firmware des Moduls läuft auf ESP-IDF.
