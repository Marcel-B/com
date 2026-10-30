---
untertitel: Your own music library
vision: Your own music collection should feel as convenient as a streaming service and still be entirely yours. Tonregal
  files new music by itself, knows every track in detail and plays it wherever you listen.
kurz: 'Files new music (fingerprint, MusicBrainz, cover, tags, fixed folders), analyses BPM and key and plays everything in
  its own player, in the browser and on the iPhone.'
links:
- text: Source on GitHub
  url: https://github.com/Marcel-B/Tonregal
features:
- titel: Inbox
  wozu: Drop in new music and stop tagging and sorting by hand.
  verhalten:
  - New files and folders, also uploaded by drag and drop in the browser, are recognised by audio fingerprint (AcoustID)
    and MusicBrainz.
  - Clear matches are ready at once; everything else goes to a review list with the reason.
  - The review list works by keyboard and stays smooth with a thousand files thanks to paging.
- titel: Filing
  wozu: Every track sits in its fixed place, properly tagged and with its cover.
  verhalten:
  - Tonregal writes tags and cover and files the track under `Artist/Year - Album/NN - Title`.
  - The original is deleted only once the new file has been checked.
- titel: Old collection
  wozu: Bring in old MP3 copies in one go without making the mess any bigger.
  verhalten:
  - The old collection is matched without anything there being changed.
  - "*Clean up what's done* moves, after a confirmation, exactly those old files to the bin that have provably arrived in
    the library."
  - Anything that changed since the match or can no longer be found in the library stays where it is.
- titel: Duplicates
  wozu: Every track once, in the better version.
  verhalten:
  - Found by identical files, identical recordings or identical titles of the same length.
  - Each version can be listened to briefly before you decide.
  - What is sorted out goes to a bin for 30 days.
- titel: Analysis
  wozu: Know tempo, key and loudness without measuring.
  verhalten:
  - At night Tonregal determines every track's BPM and key and evens out loudness (ReplayGain).
  - Everything goes straight into the tags.
- titel: Backup
  wozu: The collection is not lost when a disk fails.
  verhalten:
  - Every night a backup mirrors the library and databases to Nextcloud.
  - A lock prevents an empty disk from wiping the backup.
- titel: Web player
  wozu: Listen to your own music like in a music app, in the browser and on your phone.
  verhalten:
  - Queue, stars, shuffle by album, artist or the whole library, and repeat.
  - Control from the lock screen and headphone buttons.
  - Can be added to the home screen in iPhone Safari.
- titel: Full-screen player
  wozu: A screen just for what is playing.
  verhalten:
  - The cover large on a blurred background in its colours, with stars and progress with time left.
  - Lyrics beside or instead of the cover, a queue to rearrange by dragging.
  - After a reload it continues at the same point in the track.
- titel: Lyrics
  wozu: Read along where you are in the track.
  verhalten:
  - Synced lyrics scroll along; tapping a line jumps there.
  - They come from the file itself, an `.lrc` beside it or from [lrclib.net](https://lrclib.net).
- titel: Smart playlists
  wozu: Find music by mood and occasion instead of maintaining lists by hand.
  verhalten:
  - Rules such as BPM range, key (including matching keys for mixing), genre, new, never played or stars.
  - Tonregal plays them itself.
- titel: Download
  wozu: Take the music where Tonregal is not.
  verhalten:
  - A track as its original file or a whole album as a ZIP.
- titel: App for iPhone and iPad
  wozu: Listen even with the screen off.
  verhalten:
  - Keeps playing reliably in the background, in Control Centre, with AirPods and AirPlay.
  - With lyrics, stars and shuffle.
  - New tracks show up by themselves when the app is opened again; lists and albums can also be pulled down to reload.
- titel: Interface for handing over
  wozu: Tracks of your own go straight into the library.
  verhalten:
  - Songs come in without matching, for example from [Tonwerk-AI](/en/projekte/tonwerk-ai/) with cover, lyrics, tempo and
    key.
  - The *Connections* page shows and renews the key for it.
roadmap:
  jetzt:
  - The full-screen player in the browser is being tried out
  - The iPhone and iPad app in testing via TestFlight
  - Clean up the processed old collection with one button, only what is provably in the library
  als_naechstes:
  - Playlists, offline playback and CarPlay in the iPhone app
  - 'Localisation: web player and app in more languages'
steckbrief:
- name: Platform
  wert: A Mac mini on the home network, web and iPhone, access only via Tailscale
- name: Licence
  wert: GNU AGPL v3 or later
---

## Guiding principle

The files are the truth. All metadata lives in the tags of the audio file; the database is only an index and can be
rebuilt from the library at any time.

## Technology

ASP.NET Core (.NET 10) with EF Core and SQLite, SignalR for live updates, a Vue 3 frontend with Pinia, Tailwind CSS and
PrimeVue, a SwiftUI app. Fingerprinting, analysis and backup use standalone tools such as Chromaprint, librosa, ffmpeg,
rsgain and rclone. In the background Navidrome counts plays and keeps the stars. The Mac mini installs new versions by
itself as soon as nothing is being imported, analysed or backed up; the iPhone app goes to TestFlight automatically.
