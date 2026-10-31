---
titel: NFC-Leser für den Drucker bauen
beschreibung: Ein ESP32 mit NFC-Leser erkennt, welches Musterplättchen am Drucker steckt, und meldet es dem Server. Mit Teileliste, Verdrahtung, ESPHome und Haltern zum Drucken.
datum: 2026-10-30
reihenfolge: 3
---

Der Snapmaker U1 liest die NFC-Tags seiner Spulen selbst. Andere Drucker können das nicht, und dort müsstest du nach
jedem Spulenwechsel in der App „In Drucker einlegen“ tippen. Der NFC-Leser nimmt dir das ab: Am Drucker hängt ein
Halter mit einem Fach pro Slot. Du steckst das Musterplättchen der Sorte hinein, die du gerade einlegst, ein ESP32
liest es und meldet dem Server, welches Plättchen in welchem Slot steckt. Der Server legt die Spule dieser Sorte in den
Slot und bucht den Verbrauch des nächsten Drucks darauf.

Diese Anleitung ist der dritte Teil nach [dem Server](/projekte/fil-o-mat/server-einrichten.html) und
[den Apps](/projekte/fil-o-mat/apps-einrichten.html). Die Musterplättchen müssen schon in der App einer Sorte
zugeordnet sein.

## Welche Variante für welchen Drucker

| Drucker | Aufbau | ESPHome-Datei |
| --- | --- | --- |
| ein Slot, z. B. Prusa MK4S, Mini oder Bambu P1S mit externer Spule | ESP32-C3 mit Display und ein PN532, ein Fach | `fach-1x-pn532.yaml` |
| Prusa Core One mit MMU3 | ESP32-DevKit und fünf RC522, ein Leser pro Fach | `fach-5x-rc522.yaml` |
| viele Slots, z. B. Anycubic Kobra X mit ACE | ESP32-C3 mit Display und ein PN532 im Tipp-Modus: Plättchen antippen, Slot per Taste wählen | `tippen-pn532.yaml` |

Erprobt ist bisher die Variante mit einem Fach an einem Prusa MK4S. Die MMU3-Variante mit fünf Lesern und der
Tipp-Modus sind fertig gebaut und übersetzen fehlerfrei, liefen aber noch nicht am Drucker. Fang deshalb am besten
mit einem Drucker mit einem Slot an.

## Was du brauchst

Für einen Drucker mit einem Slot oder für den Tipp-Modus:

- ein ESP32-C3-Board mit eingebautem 0,42"-OLED (oft als HW-675 verkauft, 20,7 × 25 mm)
- ein PN532-NFC-Modul (die rote Platine mit zwei kleinen Schaltern für I²C und SPI)
- vier Kabel, etwa Dupont-Kabel mit Buchse
- ein USB-C-Kabel zum Flashen und ein USB-Netzteil für den Dauerbetrieb

Für die MMU3 mit fünf Fächern:

- ein ESP32-DevKit mit 38 Pins (ESP32-WROOM-32)
- fünf RC522-Module
- Kabel für den gemeinsamen SPI-Bus, am bequemsten über ein Stück Lochrasterplatine
- ein Micro-USB-Kabel und ein USB-Netzteil

Für die Halter:

- Neodym-Scheibenmagnete mit 12 mm Durchmesser und gut 2,6 mm Höhe; damit haftet der Halter am Rahmen des Druckers
- Filament ohne Metall- oder Kohlefaser, also zum Beispiel PLA oder PETG; Fasern mit Metall oder Kohle können das
  Funkfeld dämpfen

Außerdem einen Rechner mit Python 3, einen Lötkolben und deine Musterplättchen mit NTAG-Tags.

## 1. Verdrahten

**PN532 am ESP32-C3.** Stell zuerst die beiden Schalter am PN532 auf I²C: Schalter 1 auf ON, Schalter 2 auf OFF.
Der Leser hängt am selben I²C-Bus wie das Display des C3, dafür reichen vier Leitungen:

| PN532 | VCC | GND | SDA | SCL |
| --- | --- | --- | --- | --- |
| ESP32-C3 | 3V3 | GND | GPIO5 | GPIO6 |

Am C3 lötest du die vier Kabel direkt an, ohne Stiftleiste; so passt er später in den Halter. Am PN532 steckst du sie
auf die vierpolige Leiste.

**Fünf RC522 am ESP32-DevKit.** Alle Leser hängen parallel an Strom und an den drei Datenleitungen des SPI-Busses.
Nur die Leitung SDA (sie dient hier als Chip-Auswahl) bekommt jeder Leser einzeln. RST kommt an 3,3 V, IRQ bleibt
frei.

| RC522 | 3.3V | GND | SCK | MOSI | MISO | RST |
| --- | --- | --- | --- | --- | --- | --- |
| ESP32-DevKit (alle Leser) | 3V3 | GND | GPIO18 | GPIO23 | GPIO19 | 3V3 |

| Slot | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| SDA an | GPIO26 | GPIO17 | GPIO16 | GPIO4 | GPIO13 |

Schließ die Leser nie an 5 V an. Sowohl PN532 als auch RC522 laufen hier mit 3,3 V.

## 2. ESPHome installieren

Die Leser laufen mit [ESPHome](https://esphome.io). Installiere es einmal in einer eigenen Python-Umgebung und hol
das Repository mit den fertigen Konfigurationen:

```sh
python3 -m venv ~/esphome
~/esphome/bin/pip install esphome
git clone https://github.com/Marcel-B/fil-o-mat.git
cd fil-o-mat/reader
```

Danach heißt der Befehl `~/esphome/bin/esphome`. Wenn du ihn kurz als `esphome` aufrufen willst, trag einmal einen
Alias ein:

```sh
echo 'alias esphome=~/esphome/bin/esphome' >> ~/.zshrc && source ~/.zshrc
```

Der ESP32-C3 braucht keinen Treiber. Erkennt dein Rechner das DevKit nicht, fehlt meist der CP210x-Treiber von
Silicon Labs.

## 3. Zugangsdaten und Drucker eintragen

Kopiere die Beispieldatei und trag dein WLAN und die Adresse des Servers ein:

```sh
cp secrets.example.yaml secrets.yaml
```

```yaml
wifi_ssid: "MeinWLAN"
wifi_password: "…"
filomat_url: "http://192.168.1.50:8080"
filomat_api_key: ""
ota_password: ""
```

Nimm bei `filomat_url` die Adresse im Heimnetz mit `http`, nicht die Tailscale-Adresse: Der ESP32 kommt nicht ins
Tailnet. Ist im Server ein API-Schlüssel gesetzt, gehört er nach `filomat_api_key`. Die Datei `secrets.yaml` bleibt
auf deinem Rechner und wird nicht ins Repository übernommen.

Jetzt brauchst du die ID des Druckers. Öffne im Browser `http://192.168.1.50:8080/api/printers`. Bei jedem Drucker
steht `"id": "…"` neben dem Namen. Mit API-Schlüssel geht das im Terminal:

```sh
curl -H "X-Api-Key: …" http://192.168.1.50:8080/api/printers
```

Leg für jeden Drucker eine kleine eigene Datei an, die die gemeinsame Konfiguration einbindet, hier `mk4s.yaml`:

```yaml
substitutions:
  name: filomat-mk4s
  friendly_name: fil-O-mat MK4S
  printer_id: "ID aus /api/printers"

packages:
  fach: !include fach-1x-pn532.yaml
```

Für die MMU3 bindest du `fach-5x-rc522.yaml` ein, für den Tipp-Modus `tippen-pn532.yaml`. Weil deine Datei nur die
drei Werte enthält, kommen spätere Verbesserungen mit `git pull` von selbst dazu.

## 4. Flashen und prüfen

Schließ den ESP32 per USB an und starte:

```sh
esphome run mk4s.yaml
```

Der erste Lauf lädt die Werkzeuge und dauert fünf bis zehn Minuten. Fragt ESPHome nach dem Anschluss, wähl den
USB-Eintrag, etwa `/dev/cu.usbmodem…` beim C3 oder `/dev/cu.usbserial…` beim DevKit. Taucht keiner auf, halt die
BOOT-Taste gedrückt, während du das Kabel einsteckst. Später, wenn der ESP32 im WLAN ist, gehen Updates ohne Kabel:
Dann wählst du den Eintrag „Over The Air“.

Nach dem Hochladen läuft das Log weiter. Daran siehst du, ob alles stimmt:

- `Connected` mit einer IP-Adresse: Der ESP32 ist im WLAN.
- Beim I²C-Scan `Found device at address 0x24` (PN532) und `0x3C` (Display).
- Halte ein Plättchen an den Leser. Dann folgt eine Zeile mit `Backend: HTTP 200` und `"state":"known"`.

```text
Backend: HTTP 200 {"slots":[{"slot":0,"tag":"0423BC53CB2A81","state":"known","label":"eSun PLA #1",…}]}
```

Das Display zeigt „Eingelegt“ mit der Sorte und der Spulennummer, und in der App steckt die Spule jetzt im Drucker.
Bei der MMU3 legst du ein Plättchen nacheinander an jeden Leser. Im Log muss es im richtigen Slot erscheinen; steht
es woanders, sind zwei SDA-Leitungen vertauscht.

Das Log kannst du jederzeit wieder ansehen:

```sh
esphome logs mk4s.yaml
```

## 5. Halter drucken

Die Halter haben vorn ein Fach für das Musterplättchen und dahinter eine Tasche für den Leser. Magnete im Boden
halten sie am Rahmen des Druckers. Sie sitzen unter dem Leser und damit außerhalb seiner Antenne, denn direkt
dahinter würden sie den Empfang stören. Gedruckt wird stehend, mit dem Boden aufs Bett; Stützen brauchst du keine.

Ein wichtiges Maß ist der Abstand zwischen Plättchen und Leser. Der PN532 liest ein Plättchen erst ab etwa einem
Zentimeter Abstand und ab gut zwei Zentimetern zuverlässig. Der Halter für den PN532 hält deshalb 25 mm Abstand und
ist dadurch 41 mm tief. In dem Klotz dazwischen steckt gleich der ESP32-C3: Er wird von links eingeschoben, das
Display schaut oben heraus, die USB-C-Buchse links. Darunter ist Platz für die Kabel, ein Schlitz führt sie nach
hinten zum Leser.

| Teil | Für | Größe (B × T × H) | Dateien |
| --- | --- | --- | --- |
| Leser-Halter PN532 mit Rastnase: zwei Nasen halten den C3 | ein Slot, Tipp-Modus | 45 × 41 × 57 mm | [3MF](/dateien/fil-o-mat/LeserHalter-PN532-Rastnase.3mf), [STL](/dateien/fil-o-mat/LeserHalter-PN532-Rastnase.stl) |
| Leser-Halter PN532 mit Stopfen: ein zweites Teil mit USB-Loch verschließt die Öffnung | ein Slot, Tipp-Modus | 45 × 41 × 57 mm, Stopfen daneben | [3MF](/dateien/fil-o-mat/LeserHalter-PN532-Stopfen.3mf), [STL](/dateien/fil-o-mat/LeserHalter-PN532-Stopfen.stl) |
| Leser-Halter RC522, fünf Fächer | MMU3 | 209 × 17 × 73 mm | [3MF](/dateien/fil-o-mat/LeserHalter-RC522-5er.3mf), [STL](/dateien/fil-o-mat/LeserHalter-RC522-5er.stl) |
| Gehäuse für das ESP32-DevKit, Kasten mit Deckel | MMU3 | 72 × 63 × 28 mm | [3MF](/dateien/fil-o-mat/ESP-Gehaeuse-DevKit.3mf), [STL](/dateien/fil-o-mat/ESP-Gehaeuse-DevKit.stl) |
| Tag-Halter ohne Leser, ein Fach | Plättchen nur ablegen, z. B. am U1 | 43 × 11 × 46 mm | [3MF](/dateien/fil-o-mat/TagHalter-CoreOne.3mf), [STL](/dateien/fil-o-mat/TagHalter-CoreOne.stl) |
| Tag-Halter ohne Leser, fünf Fächer | MMU3 ohne Leser | 209 × 11 × 46 mm | [3MF](/dateien/fil-o-mat/TagHalter-5er.3mf), [STL](/dateien/fil-o-mat/TagHalter-5er.stl) |
| Passungstest für die Magnete: fünf Einschübe, von links nach rechts strammer | vor dem ersten Halter | 85 × 4 × 18 mm | [3MF](/dateien/fil-o-mat/Magnet-Passungstest.3mf), [STL](/dateien/fil-o-mat/Magnet-Passungstest.stl) |

Die 3MF-Dateien öffnest du direkt im Slicer; beim Halter mit Stopfen und beim DevKit-Gehäuse liegen beide Teile schon
nebeneinander. Die STL-Dateien enthalten dieselben Teile.

Die Halter mit eingebautem C3 und der RC522-Halter sind neu und noch nicht im Dauerbetrieb erprobt. Druck zuerst den
Passungstest und prüf mit einem Leser, ob die Reichweite durch den gedruckten Halter reicht.

So baust du den PN532-Halter zusammen:

1. Die Magnete von unten in die Einschübe drücken.
2. Den PN532 von oben in die hintere Tasche schieben, die Bauteile nach hinten, die glatte Seite zum Plättchen. Die
   Stiftleiste schaut oben heraus.
3. Den C3 mit den angelöteten Kabeln von links in den Klotz schieben, bis die Rastnasen greifen oder der Stopfen
   sitzt, und die Kabel durch den Schlitz zur Stiftleiste führen.
4. Den Halter an den Rahmen setzen und ein Plättchen ins Fach stecken.

## 6. Halter an deine Teile anpassen

Alle Teile entstehen aus kleinen Python-Skripten. Jedes Maß ist darin ein Parameter, den du beim Aufruf ändern
kannst. Du brauchst dafür die Pakete `manifold3d` und `numpy`:

```sh
python3 -m venv ~/halter
~/halter/bin/pip install manifold3d numpy
~/halter/bin/python leserhalter.py                          # PN532 mit Rastnase
~/halter/bin/python leserhalter.py lock=stopfen             # PN532 mit Stopfen
~/halter/bin/python leserhalter.py reader=rc522 count=5     # fünf RC522 für die MMU3
~/halter/bin/python leserhalter.py sep=20                   # weniger Abstand zwischen Plättchen und Leser
```

| Skript | Erzeugt |
| --- | --- |
| [leserhalter.py](/dateien/fil-o-mat/leserhalter.py) | Leser-Halter mit PN532 oder RC522, wahlweise mit eingebautem C3 |
| [esp_gehaeuse.py](/dateien/fil-o-mat/esp_gehaeuse.py) | Gehäuse für DevKit (`board=devkit`) oder eine einzelne Schiene für den C3 (`board=c3`) |
| [taghalter_coreone.py](/dateien/fil-o-mat/taghalter_coreone.py) | Tag-Halter ohne Leser, `count=5` für fünf Fächer |
| [magnet_passungstest.py](/dateien/fil-o-mat/magnet_passungstest.py) | Passungstest für die Magnete |

Die Parameter stehen mit Erklärung oben in jedem Skript, etwa `mag_d` und `mag_h` für andere Magnete oder `slot_w`
und `slot_h` für größere Musterplättchen. Das Ergebnis ist jeweils eine 3MF-Datei im aktuellen Ordner.

## 7. So arbeitest du damit

- **Ein Fach pro Slot:** Spule einlegen, Plättchen in das Fach stecken, fertig. Das Display zeigt die Sorte mit
  Spulennummer. Herausziehen ändert nichts am Bestand. Die Spule bleibt eingelegt, bis ein anderes Plättchen kommt
  oder du sie in der App umlegst.
- **Tipp-Modus:** Plättchen an den Leser halten, das Display zeigt die Sorte. Mit der BOOT-Taste wählst du den Slot,
  jeder Druck einen weiter (bei der Kobra X 1–4 im Gerät, 5–8 in der ACE). Vier Sekunden nach dem letzten Druck kommt
  die Spule in diesen Slot. Ohne Tastendruck bricht der Leser nach 15 Sekunden ab.
- **Unbekanntes Plättchen:** Das Display zeigt „Unbekannt“, und mit eingerichtetem ntfy kommt eine Meldung aufs
  Handy. Ordne das Plättchen in der App einer Sorte zu und steck es neu ein.

## Wenn etwas nicht geht

| Was du siehst | Ursache | Was hilft |
| --- | --- | --- |
| `command not found: esphome` | ESPHome liegt nicht im Pfad | `~/esphome/bin/esphome` aufrufen oder den Alias eintragen |
| ESP32 taucht beim Flashen nicht auf | nicht im Flash-Modus oder ein reines Ladekabel | BOOT gedrückt halten beim Einstecken, anderes Kabel |
| kein `0x24` im I²C-Scan | Schalter am PN532 nicht auf I²C oder SDA und SCL vertauscht | Schalter 1 ON, 2 OFF; Kabel an GPIO5 und GPIO6 tauschen |
| Plättchen wird nicht erkannt | zu nah am Leser oder Magnet vor der Antenne | Abstand vergrößern, Magnete außerhalb der Antenne |
| Display „nicht erreichbar“ | falsche Adresse oder die Tailscale-Adresse eingetragen | Adresse im Heimnetz in `secrets.yaml`, dann neu flashen |
| Display „Fehler 404“ | Server zu alt oder falsche `printer_id` | Server aktualisieren, ID unter `/api/printers` prüfen |
| Display „Fehler 401“ | API-Schlüssel fehlt oder ist falsch | `filomat_api_key` in `secrets.yaml` |
| ein Slot der MMU3 flackert im Log | benachbarte RC522 stören sich | mehr Abstand zwischen den Lesern |

Die Adresse und alle anderen Werte werden beim Bauen fest in die Firmware geschrieben. Nach jeder Änderung an
`secrets.yaml` oder deiner Druckerdatei flashst du also mit `esphome run` neu. Mehr Details zur Verdrahtung und zum
Verhalten des Servers stehen im
[README des Lesers](https://github.com/Marcel-B/fil-o-mat/blob/main/reader/README.md).
