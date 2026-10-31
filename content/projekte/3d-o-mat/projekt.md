---
name: 3d-o-mat
untertitel: Aus einem Bild ein 3D-Modell
reihenfolge: 65
vision: Aus einem Foto oder einer Idee soll ein 3D-Modell werden, das man drehen, in ein Spiel setzen oder drucken kann.
  3d-o-mat macht das mit KI-Modellen auf dem eigenen Mac, ohne Cloud und ohne 3D-Kenntnisse.
kurz: Bild hochladen oder malen lassen, freistellen, mit TRELLIS.2 in ein texturiertes 3D-Modell umwandeln, ansehen, mit
  Skelett versehen und als GLB herunterladen.
technik:
- Python
- FastAPI
- React
- three.js
- TRELLIS.2
links:
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/3d-o-mat
features:
- titel: Bild hochladen und freistellen
  wozu: Ein gewöhnliches Foto reicht als Vorlage, auch mit Hintergrund.
  verhalten:
  - PNG, JPEG und WebP werden angenommen.
  - Hat das Bild schon Transparenz, bleibt sie; sonst entfernt rembg den Hintergrund.
  - Danach wird das Bild quadratisch auf das Objekt zugeschnitten.
- titel: Bild prüfen lassen
  wozu: Bevor ein Modell minutenlang rechnet, wissen, ob die Vorlage taugt.
  verhalten:
  - Gemma beurteilt, ob ein einzelnes Objekt vollständig und scharf im Bild ist, und gibt Tipps.
- titel: Bilder malen lassen
  wozu: Ein Modell bekommen, auch wenn kein passendes Foto da ist.
  verhalten:
  - Aus einer Idee schreibt Gemma Bild-Prompts für eine gute Vorlage.
  - img-o-mat malt ein bis vier Bilder mit FLUX.2 Klein 4B, Z-Image Turbo oder Krea 2 Turbo.
  - Jedes gemalte Bild wird wie ein hochgeladenes freigestellt und behält den Vermerk, dass es KI-generiert ist.
- titel: In 3D umwandeln
  wozu: Aus dem Bild wird ein Modell mit Texturen, ohne selbst zu modellieren.
  verhalten:
  - TRELLIS.2 erzeugt ein GLB mit PBR-Texturen; Textur, Flächen, Auflösung und Seed sind wählbar.
  - Aufträge laufen nacheinander, der Fortschritt steht in der Liste.
  - Musik aus Tonwerk hat auf dem Rechner Vorrang; ein Auftrag wartet dann und sagt, worauf.
- titel: Ansehen und herunterladen
  wozu: Das Ergebnis prüfen und in Blender, Godot oder Unity weiterverwenden.
  verhalten:
  - Das Modell lässt sich im Browser drehen und als GLB herunterladen.
- titel: Skelett einsetzen
  wozu: Eine Figur bewegen, statt nur eine Statue zu haben.
  verhalten:
  - SkinTokens setzt Knochen und Gewichte ein, bei Menschen mit Mixamo-Namen, sodass Mixamo-Animationen direkt passen.
  - Sieben Proben (Gehen, Schlag, Tritt, Drehtritt, Arme heben, Kniebeuge, Umfallen) zeigen im Browser, ob das Skelett sitzt.
  - Die Proben lassen sich als Animationen im GLB mitnehmen, etwa in Godots AnimationPlayer.
- titel: Für den 3D-Drucker
  wozu: Ein Modell als Figur ins Regal stellen, statt es nur am Bildschirm zu drehen.
  verhalten:
  - Jedes fertige Modell lässt sich als 3MF oder STL in Millimetern herunterladen, mit wählbarer Höhe.
  - Die Datei ist wasserdicht; offene Stellen und hauchdünne Flächen werden geschlossen, die Oberfläche bleibt glatt.
  - Auf Wunsch steht die Figur auf einem runden Sockel.
  - Gedruckt wird nur die Form; was nur in die Textur gemalt ist, etwa Augen oder Muster, fehlt.
- titel: Alles auf dem eigenen Rechner
  wozu: Bilder und Modelle verlassen das Haus nicht.
  verhalten:
  - Alle Modelle laufen lokal auf einem Mac; die Dateien liegen auf einer eigenen Platte.
  - Ist die Platte nicht da, nimmt die Seite nichts an.
- titel: Deutsch oder Englisch, hell oder dunkel
  wozu: Die Seite in der eigenen Sprache und dem gewohnten Farbschema benutzen.
  verhalten:
  - Die Oberfläche gibt es auf Deutsch und Englisch; ohne Wahl folgt sie der Sprache des Browsers.
  - Gemma prüft Bilder und antwortet in der gewählten Sprache.
  - Das Farbschema ist hell, dunkel oder folgt dem System; beide Wahlen merkt sich der Browser.
roadmap:
  jetzt:
  - Figuren vor dem Druck in eine Haltung stellen, mit fertigen Haltungen, von Hand oder per Beschreibung an Gemma
  als_naechstes:
  - 'Lokalisierung: Meldungen und Fehlertexte des Servers auch auf Englisch'
  spaeter:
  - Farbige Druckdateien für Drucker mit mehreren Filamenten
  - Warnung vor Stellen, die zum Drucken zu dünn sind
  - Beim Malen gleich eine Statuen-Haltung wählen, die sich gut drucken lässt
steckbrief:
- name: Plattform
  wert: Web; Docker in einem Proxmox-Container, Rechnen auf einem Mac mit Apple Silicon
- name: Lizenz
  wert: MIT
---

## Technik

Die Website ist eine Python-App mit FastAPI und einer React-Oberfläche, die in einem Docker-Container läuft und selbst
keine Daten hält. Gerechnet wird auf einem Mac mit Apple Silicon: TRELLIS.2 in MLX für Bild zu 3D, SkinTokens für das
Skelett, Gemma 4 in LM Studio zum Prüfen und Prompten, img-o-mat zum Malen. Eine gemeinsame Schranke verteilt die
Modelle auf dem Mac zwischen 3d-o-mat und Tonwerk, lädt sie bei Bedarf und entlädt sie nach kurzer Pause wieder.
