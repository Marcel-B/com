---
titel: fil-O-mat auf Android und iPhone einrichten
beschreibung: Die Apps installieren, mit dem Server verbinden, Drucker anlegen und die ersten Musterplättchen mit NFC-Tags versehen.
datum: 2026-10-30
reihenfolge: 2
---

Die Apps sind der Teil von fil-O-mat, den du jeden Tag in der Hand hast. Mit ihnen liest und beschreibst du die
NFC-Tags auf den Musterplättchen, lagerst Spulen ein und legst sie in Drucker. Diese Anleitung setzt einen laufenden
Server voraus, siehe [Den fil-O-mat-Server einrichten](/projekte/fil-o-mat/server-einrichten.html).

## Was du brauchst

- ein Android-Handy mit NFC (ab Android 7) oder ein iPhone ab iOS 17; NFC geht nur auf echten Geräten, nicht im
  Emulator oder Simulator
- für Android: einen Rechner mit [Android Studio](https://developer.android.com/studio)
- für das iPhone: einen Mac mit Xcode 16 oder neuer und ein Apple-Developer-Konto, denn ohne dieses gibt Apple einer
  App keinen NFC-Zugriff
- NFC-Tags vom Typ NTAG213, NTAG215 oder NTAG216 als Aufkleber, für jedes Musterplättchen einen
- die Adresse deines Servers, etwa `http://192.168.1.50:8080`, und den API-Schlüssel, falls du einen gesetzt hast

Die Apps gibt es nicht in den Stores. Du baust sie aus dem Quelltext, den du so holst:

```sh
git clone https://github.com/Marcel-B/fil-o-mat.git
```

## 1. Android-App installieren

1. In Android Studio **File → Open** wählen und den Ordner `fil-o-mat/android-app` öffnen. Android Studio lädt die
   Abhängigkeiten von selbst.
2. Am Handy die Entwickleroptionen und USB-Debugging einschalten und es per Kabel anschließen.
3. Das Handy oben als Ziel wählen und auf **Run** (▶) drücken. Die App startet danach auf dem Handy.

Ein Update installierst du genauso; die Daten auf dem Handy bleiben dabei erhalten. Deinstalliere die App nicht,
solange sie noch nicht mit dem Server abgeglichen ist, sonst sind ihre lokalen Daten weg.

Unter GrapheneOS braucht die App die Berechtigung **Netzwerk**. Fehlt sie, scheitert der Abgleich mit der Meldung
„socket failed: EPERM“. Du schaltest sie in den Einstellungen der App unter **Berechtigungen** ein.

## 2. iPhone-App installieren

1. `fil-o-mat/ios-app/Filomat.xcodeproj` in Xcode öffnen.
2. Beim Target **Filomat** unter **Signing & Capabilities** dein Team wählen. Ist die Bundle-ID `com.filomat.app`
   schon vergeben, trag eine eigene ein, etwa `de.<deinname>.filomat`. Die NFC-Berechtigung ist schon eingetragen.
3. Das iPhone anschließen, als Ziel wählen und mit ⌘R starten.

Ohne Kabel geht es über TestFlight: GitHub Actions baut die App signiert und lädt sie hoch. Wie du das für dein
eigenes Konto einrichtest, steht in
[TESTFLIGHT.md](https://github.com/Marcel-B/fil-o-mat/blob/main/ios-app/TESTFLIGHT.md).

Beim ersten Verbinden fragt iOS, ob die App auf Geräte im lokalen Netzwerk zugreifen darf. Erlaube das, sonst
erreicht sie den Server im Heimnetz nicht.

## 3. Mit dem Server verbinden

Das geht in beiden Apps gleich:

1. Im Tab **Container** oben auf das Wolken-Symbol tippen.
2. Die Server-Adresse eintragen, zum Beispiel `http://192.168.1.50:8080`, und den API-Schlüssel, falls einer gesetzt
   ist.
3. **Verbinden und abgleichen** tippen.

Beim Verbinden lädt die App hoch, was schon auf dem Gerät liegt, und übernimmt dann den gemeinsamen Stand. Dabei wird
nichts gelöscht. Danach geht jede Änderung sofort an den Server, und die App lädt alle zwei Minuten neu, solange sie
offen ist. Hast du schon mit beiden Apps gearbeitet, verbindest du zuerst die eine und dann die andere; danach
sehen beide dasselbe.

Unterwegs nimmst du die Tailscale-Adresse, etwa `http://filomat.<dein-tailnet>.ts.net:8080`. Dafür muss die
Tailscale-App auf dem Handy verbunden sein. Im Heimnetz funktioniert sie genauso.

Passen App und Server nicht zusammen, sagt die App das: „Backend veraltet“ heißt, du solltest den Server
aktualisieren (unter **Backend**), „App veraltet“ heißt, die App braucht ein Update.

## 4. Drucker anlegen

Im Tab **Drucker** legst du mit **+** jeden Drucker an. Jeder Drucker bekommt einen eigenen Container, in dem die
eingelegten Spulen stehen.

| Drucker | Typ in der App | Adresse | Schlüssel |
| --- | --- | --- | --- |
| Klipper, z. B. Voron | Klipper / Moonraker | `http://<drucker>:7125` | nur bei Moonraker-Anmeldung |
| Snapmaker U1 mit paxx12-Firmware | Snapmaker U1 (paxx12) | `http://<drucker>` | keiner |
| Prusa MK4, Core One, Mini, XL | Prusa (PrusaLink) | `http://<drucker>` | API-Schlüssel aus Einstellungen → Netzwerk → PrusaLink am Drucker |
| Anycubic Kobra X, S1, 3, 4 | Anycubic Kobra (LAN-Modus) | `http://<drucker>` | keiner; am Drucker den LAN-Modus einschalten |
| Bambu Lab P1S, P1P, X1, A1 | Bambu Lab (LAN) | `http://<drucker>` | Zugangscode aus den WLAN-Einstellungen am Drucker |

Nach dem Speichern fragt der Server den Drucker sofort ab. Klappt das, zeigt die App den Zustand mit laufendem Druck,
Temperaturen und belegten Slots. Bei Bambu-Druckern mit neuerer Firmware kann es nötig sein, am Drucker den
LAN-Modus mit Entwicklermodus einzuschalten; zeigt die App einen MQTT-Fehler, schau dort nach.

## 5. Sorten und Musterplättchen

fil-O-mat denkt in Sorten. Eine Sorte ist zum Beispiel „eSun PLA+ very peri“, mit Vorrat an vollen Spulen. Das
NFC-Tag klebt nicht auf der Spule, sondern auf einem Musterplättchen der Sorte. Es bleibt also, wenn eine Spule leer
ist. Jede angebrochene Spule bekommt eine kurze Nummer, die du mit einem Stift auf die Spule schreibst, und hat ihr
eigenes Restgewicht und ihren Platz: in einem Drucker oder im Lager.

1. Den Tag-Aufkleber auf das Musterplättchen kleben.
2. Im Tab **Filamente** eine neue Sorte anlegen: Hersteller, Material, Farbe, Temperaturen, Füll- und Leergewicht und
   wie viele volle Spulen du hast. Die Vorlagen füllen vieles schon aus.
3. **Auf Tag schreiben** tippen und das Handy an das Plättchen halten. Die App schreibt die Daten der Sorte im
   offenen OpenSpool-Format auf das Tag und merkt sich dessen Kennung. Drucker wie der Snapmaker U1 lesen dieses
   Format direkt.

Eine Sorte darf mehrere Plättchen haben, etwa eines an der Box und eines am Drucker. Alle zeigen auf denselben
Eintrag. Weitere Plättchen fügst du beim Bearbeiten der Sorte mit **Plättchen hinzufügen** an. Ob ein Plättchen richtig beschrieben ist, siehst du im Tab **Scannen** unter **Filament-Tag lesen**. Dort
steht alles, was auf dem Tag ist, und was fil-O-mat dazu weiß.

## 6. Einlagern und in den Drucker legen

Im Tab **Scannen** findest du die Abläufe für den Alltag:

- **Einlagern:** Plättchen scannen, wählen, ob die vollen Spulen der Sorte oder eine angebrochene Spule eingelagert
  werden, dann den Container scannen oder aus der Liste wählen. Container bekommen dafür ebenfalls ein Tag.
- **In Drucker einlegen:** Plättchen scannen, eine angebrochene Spule wählen oder eine neue anbrechen, dann Drucker
  und Slot antippen. Was dort vorher steckte, wandert ins Lager.
- **Vorrat:** volle und angebrochene Spulen je Sorte mit Gesamtgewicht und einer Liste zum Nachkaufen.
- **Lichtdurchlässigkeit erfassen:** den TD-Wert einer Sorte eintragen, etwa von einem TD-1.

Ab hier bucht der Server nach jedem Druck den Verbrauch auf die Spule, die im Drucker steckt. Damit das von selbst
passiert, ohne dass du nach jedem Spulenwechsel „In Drucker einlegen“ tippen musst, gibt es den
[NFC-Leser am Drucker](/projekte/fil-o-mat/nfc-leser-bauen.html).
