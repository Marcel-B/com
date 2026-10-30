---
untertitel: Music with local AI models
vision: Make your own songs without any of it going to a cloud. Tonwerk-AI is meant to be the studio where AI models on
  your own Mac compose, sing, paint and edit, while being as easy to use as a music app on your phone.
kurz: Songs, voices, covers and videos made by models running on your own Mac, controlled from your phone, a browser or
  native apps.
links:
- text: Tonwerk-AI on tonwerk.studio
  url: https://tonwerk.studio/ai/
- text: Download the Mac app (DMG)
  url: https://github.com/Marcel-B/Tonwerk-AI/releases/latest/download/Tonwerk-AI.dmg
- text: Source on GitHub
  url: https://github.com/Marcel-B/Tonwerk-AI
features:
- titel: Generate songs
  wozu: An idea becomes a song. A style and lyrics are enough; add a score if you like.
  verhalten:
  - Two song models to choose from, YuE2 and ACE-Step 1.5.
  - Every song's progress is shown live, even after reloading the page.
  - A draft can be rendered in full quality later.
- titel: One queue for everything
  wozu: A job is never refused just because another model is busy.
  verhalten:
  - Only as much is loaded as fits into memory; the other jobs wait.
  - Waiting jobs survive a restart.
- titel: Lyrics
  wozu: Lyrics in the right format, even when you have none at hand.
  verhalten:
  - Drafts in German or English from keywords, locally with LM Studio or with Claude.
  - A photo can replace or add to the keywords.
  - A revision changes only what was asked for; the rest stays word for word.
- titel: Open as a Logic project
  wozu: A generated song should live on in Logic Pro, not just as an audio file.
  verhalten:
  - The score becomes MIDI and a ready Logic Pro project with the audio track.
  - Backing vocals can be added, in parallel, as a drone or as a choir.
  - The score is also available as MusicXML.
- titel: Voices and stems
  wozu: Take a song apart and have it sung by another voice.
  verhalten:
  - Songs and your own files are split into stems, the vocals also without reverb.
  - Seed-VC sings the vocals again with a reference voice; the rest is mixed back underneath.
  - Any track can be turned into MIDI with Basic Pitch.
- titel: Speech lab and singing
  wozu: Try local speech and singing models, with your own voice.
  verhalten:
  - Several text-to-speech models can be compared with the same text.
  - A recording of your own serves as a voice to clone.
  - SoulX-Singer sings notes and words.
- titel: Covers and music videos
  wozu: A song should be ready to publish with a picture and a video.
  verhalten:
  - Covers are painted by local image models, optionally in the style of your own templates.
  - Videos show an analyser and lyrics subtitles, or photos cut to the beat.
  - A small version for sharing, the full one for uploading.
- titel: Library and player
  wozu: Listen to, rate and find what you made, on the road too.
  verhalten:
  - Stars, notes, search and playlists that also play offline.
  - A notification tells you when a song is ready.
  - A backup goes to Nextcloud every night.
- titel: Apps for Mac, iPhone and iPad
  wozu: The same work, natively instead of in a browser.
  verhalten:
  - The Mac app is signed and updates itself.
  - iPhone and iPad get the app through TestFlight.
  - A demo works without a server of your own.
- titel: Labelled as AI-generated
  wozu: It should always be clear what came from a model.
  verhalten:
  - Audio, videos and painted covers carry a machine-readable label in their metadata.
  - Your own recordings, photos, MIDI and scores stay unlabelled.
roadmap:
  jetzt:
  - Test ACE-Step, singing with SoulX-Singer, painted covers, photo videos and timed lyrics on the Mac with the real models
  - A second Mac as a helper for jobs
  als_naechstes:
  - Put a sung version instead of the original voice into the Logic project
  - 'Localisation: the apps for Mac, iPhone and iPad in English too (the web interface already speaks it)'
steckbrief:
- name: Platform
  wert: A Mac with Apple Silicon as the server; browser, iPhone, iPad and Mac as the interface
- name: Licence
  wert: PolyForm Noncommercial 1.0.0
---

## Technology

An ASP.NET Core Minimal API (.NET 10) with SQLite, a Vue 3 frontend with PrimeVue, native apps in SwiftUI. The models run
as Python processes alongside (PyTorch, MLX, acestep.cpp), only as many as fit into memory.
