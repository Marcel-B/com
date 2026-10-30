---
titel: Setting up Tonwerk-AI on a Mac
beschreibung: From a fresh Mac with Apple Silicon to the first song, reachable from the iPhone through Tailscale.
---

## What you need

- a Mac with Apple Silicon and macOS 14 or later, at least 16 GB of memory (24 GB and more is comfortable)
- about 20 GB of free space
- for access on the road: [Tailscale](https://tailscale.com) on the Mac and the iPhone

## 1. Set up with a script

On a Mac with nothing but macOS installed, one script sets everything up:

```sh
xcode-select --install
git clone https://github.com/Marcel-B/Tonwerk-AI.git ~/repos/Tonwerk-AI
~/repos/Tonwerk-AI/deploy/setup-mac.sh
```

It checks the Mac and installs what is missing: Homebrew, uv, ffmpeg, Node.js and the .NET 10 SDK. Then it fetches a tested version of YuE2, downloads the models (about 7 GB), publishes Tonwerk-AI as a service and starts the model once as a test. The script can run as often as you like; it skips whatever is already there.

More features come with options, for example `--voices` for other voices, `--images` for painted covers, `--ace` for ACE-Step as a second song model or `--all` for everything.

## 2. Reach it from the iPhone

The server only listens on the Mac itself. Tailscale makes it reachable, only for your own devices and with HTTPS:

```sh
tailscale serve --bg --https=8443 5090
```

Then open `https://<mac-name>.<tailnet>.ts.net:8443/` on the iPhone and add the page via **Share → Add to Home Screen**. Do not put it on the open internet with `tailscale funnel`, since the interface has no login of its own.

## 3. The first song

On the **Create** page you enter a style (the building blocks help) and lyrics. If you have none, LM Studio drafts some from a few keywords. **Generate** puts the job into the queue, and you watch its progress live. Finished songs are in the library, where you can rate them, open them as a Logic project or share them.

## 4. Updates

At the end, `setup-mac.sh` switches on automatic updates. Every five minutes a service looks for new versions and installs them as soon as Tonwerk-AI is not computing anything:

```sh
~/repos/Tonwerk-AI/deploy/update.sh status
```

## Apps instead of the browser

There are native apps for Mac, iPhone and iPad that control the same server. Download the Mac app [as a DMG](https://github.com/Marcel-B/Tonwerk-AI/releases/latest/download/Tonwerk-AI.dmg); how to connect it is explained (in German) on [tonwerk.studio/ai](https://tonwerk.studio/ai/einrichtung.html).
