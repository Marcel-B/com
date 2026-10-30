---
titel: Setting up Tonregal on a Mac from scratch
beschreibung: From an empty Mac with an external SSD to a running library with Navidrome, Tailscale, a nightly Nextcloud backup and the iPhone app, also for restoring after a failure.
---

Tonregal runs as a service on a Mac at home. The music, the database, the app itself and its logs live on an external
SSD so the internal disk stays free. Everything is reachable only through [Tailscale](https://tailscale.com), so only
by your own devices. This guide walks through the setup in the order in which the parts build on each other. If you are
restoring after a disk failure or onto a new Mac, step 4 brings the data back from Nextcloud; everything else is the
same.

## What you need

- a Mac with Apple Silicon (the app is built for `osx-arm64`) that stays on, a Mac mini for example
- an external SSD for the music, large enough for the whole collection
- a [Tailscale](https://tailscale.com) account, with Tailscale on the Mac and on the iPhone
- a Nextcloud with an app password for the backup
- a free AcoustID key from [acoustid.org](https://acoustid.org/new-application) for recognition by fingerprint
- for the iPhone app: access to the TestFlight version or an Apple developer account of your own

## 1. Prepare the Mac

In the Terminal, install the developer tools, [Homebrew](https://brew.sh) and what the build needs:

```sh
xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git node rclone
brew install --cask dotnet-sdk
```

Tonregal needs the .NET 10 SDK and Node.js 22 or later; `dotnet --version` and `node --version` tell you whether that
fits. The rest (Chromaprint, rsgain, uv, ffmpeg, Navidrome) is installed by the scripts later on.

Add Tailscale as an app from the App Store or from [tailscale.com](https://tailscale.com/download). Sign the Mac in to
your tailnet and switch on **HTTPS Certificates** under **DNS** in the Tailscale admin console, otherwise Tailscale
cannot issue a certificate later.

So the Mac does not fall asleep: in **System Settings → Energy** (**Energy Saver** on some models), prevent sleep and
let it start automatically after a power failure.

## 2. Set up the SSD

Format the SSD as **APFS** in Disk Utility and name it `T7`. The scripts expect everything under `/Volumes/T7/Musik`:

```sh
mkdir -p /Volumes/T7/Musik
```

A disk with another name works too: then run `export MUSIC_ROOT=/Volumes/<name>/Musik` before every script and read
the paths in this guide accordingly. Naming it `T7` is simpler.

Over time these folders appear under `Musik`:

| Folder | Contents |
| --- | --- |
| `Inbox/` | new music for Tonregal to recognise and file |
| `Library/` | the finished library, written only by Tonregal |
| `Altbestand/` | old MP3 copies that Tonregal only reads (optional) |
| `app/` | the published app, `tonregal.db` and your settings |
| `navidrome/` | Navidrome's settings and database |
| `logs/`, `update/`, `tools/`, `backups/` | logs, the state of automatic updates, analysis tools, database copies taken before every update |

## 3. Get the source

```sh
git clone https://github.com/Marcel-B/Tonregal.git ~/repos/Tonregal
cd ~/repos/Tonregal
```

The checkout stays on `main`; the automatic updates from step 9 only deploy from there.

## 4. Bring the data back from the backup (only when restoring)

If you are setting Tonregal up for the first time, skip this step.

First give rclone access to Nextcloud as described in step 8 (`rclone config create …`), then check that the backup is
there:

```sh
rclone lsd nextcloud:Musik            # shows Library and _state
rclone lsf --dirs-only nextcloud:Musik/_state
```

`_state/` holds one folder per day with `tonregal.db` and `navidrome.db`, for the last seven days. Take the newest and
bring back the databases and the library:

```sh
stand=$(rclone lsf --dirs-only nextcloud:Musik/_state | sort | tail -n1)
mkdir -p /Volumes/T7/Musik/{app,navidrome,Library}
rclone copy "nextcloud:Musik/_state/$stand" /Volumes/T7/Musik/app/ --include tonregal.db
rclone copy "nextcloud:Musik/_state/$stand" /Volumes/T7/Musik/navidrome/ --include navidrome.db
rclone copy nextcloud:Musik/Library /Volumes/T7/Musik/Library --progress
```

Depending on its size and your connection, the library can take hours; you can stop the command and start it again,
and it carries on where it was. The paths must be the same as before (`/Volumes/T7/Musik/…`), because Navidrome keeps
them as absolute paths in its database.

What comes back: every music file with its tags, covers, lyrics (`.lrc`) and smart playlists; from `tonregal.db` the
import history, the keys for the ingest interface (for Tonwerk-AI, for example) and the smart playlist rules; from
`navidrome.db` your Navidrome account, stars and play counts. Not in the backup are the inbox, the old collection and
`appsettings.Production.json`; keep its values (AcoustID key, Navidrome password) in your password manager.

If `tonregal.db` is missing altogether, that is no disaster: the database is only an index, and Tonregal reads the
library at start and rebuilds it.

## 5. Set up Navidrome

Navidrome delivers the audio behind the scenes, counts plays and keeps the stars. Tailscale must already be running,
because Navidrome listens on the Mac's Tailscale address:

```sh
./deploy/navidrome/setup-navidrome.sh
```

The script installs Navidrome and ffmpeg, creates the folders, writes `navidrome.toml` and sets up the service
`org.navidrome.server`.

**Full Disk Access:** The first time, the service usually does not start because macOS denies it the external SSD. The
script then names the program that needs access. In **System Settings → Privacy & Security → Full Disk Access**, add
exactly that path with **+** (in the file dialog, **Cmd+Shift+G** takes you to a path) and run the script again. After
`brew upgrade navidrome` the path changes; grant access again then.

At the end the script prints Navidrome's address. Open it in a browser and create the admin user on the first visit.
After a restore it already exists.

## 6. Deploy Tonregal

```sh
./deploy/deploy-tonregal.sh
```

The script installs Chromaprint, rsgain, uv and rclone, creates a Python environment for the tempo and key analysis on
the SSD, builds Tonregal with its web interface, copies it to `Musik/app` and sets up the service `de.bvelop.tonregal`.
Tonregal listens only on `http://localhost:5100`. At the end the script calls `/api/health` and stops with a message if
Tonregal does not answer. Here, too, access to the SSD may be missing the first time; grant it to the path it names
(`…/Musik/app/Tonregal.Web`) as in step 5 and run the script again.

Your own settings go into `/Volumes/T7/Musik/app/appsettings.Production.json`. The script leaves this file alone on
every update, and it never belongs in the repository:

```json
{
  "Tonregal": {
    "Metadata": { "AcoustIdApiKey": "<your AcoustID key>" },
    "Navidrome": { "User": "<Navidrome admin>", "Password": "<password>" }
  }
}
```

Without the AcoustID key Tonregal recognises no tracks by fingerprint, without the Navidrome account stars and play
counts do not work. After a change, restart the service:

```sh
launchctl kickstart -k gui/$(id -u)/de.bvelop.tonregal
curl http://localhost:5100/api/health
```

## 7. Make it reachable through Tailscale

Tailscale Serve puts Tonregal into the tailnet with HTTPS:

```sh
tailscale serve --bg 5100
tailscale serve status
```

If the Terminal cannot find `tailscale`, the program lives inside the app at
`/Applications/Tailscale.app/Contents/MacOS/Tailscale`. Tonregal is then reachable on all your devices in the tailnet at
`https://<mac-name>.<tailnet>.ts.net`, without a port. `tailscale serve status` shows the exact name. Check it from
another device:

```sh
curl https://<mac-name>.<tailnet>.ts.net/api/health
```

Do not put Tonregal on the open internet with `tailscale funnel`, since the interface has no login of its own. On the
iPhone you can add the page to the home screen in Safari through **Share → Add to Home Screen** and use it like an app.

## 8. Set up the nightly backup

Every night at 03:00 Tonregal mirrors the library to Nextcloud and puts copies of both databases beside it. In
Nextcloud, create a user with an app password who sees only the folder `Musik`, and give rclone the access. It stays in
`~/.config/rclone/rclone.conf` on the Mac:

```sh
rclone config create nextcloud webdav vendor=nextcloud \
  url=https://<your-nextcloud>/remote.php/dav/files/<user>/ user=<user> pass='<app-password>'
rclone lsd nextcloud:Musik    # must answer without an error
```

Start a first run at once with **Jetzt sichern** (back up now) on the overview or in the Terminal:

```sh
curl -X POST http://localhost:5100/api/backup/run
```

The overview shows the latest runs; two failures in a row turn red. A run that would delete more than 500 files in
Nextcloud stops, so an empty or wrongly mounted disk cannot empty the backup.

## 9. Switch on automatic updates

From now on the Mac should install new versions by itself. From a Terminal in which `brew`, `dotnet` and `npm` work
(the command remembers its `PATH`):

```sh
./deploy/update-tonregal.sh on
```

A background service looks for new commits on `main` every five minutes. When there are some, it waits until nothing
is being imported, analysed or backed up, copies `tonregal.db` to `Musik/backups/deploy/` and deploys with
`deploy-tonregal.sh`.

The service runs as `/bin/bash` and needs **Full Disk Access** for it once: in System Settings as in step 5, with **+**,
**Cmd+Shift+G** and `/bin/bash`. Whether it worked is shown by

```sh
./deploy/update-tonregal.sh status
cat /Volumes/T7/Musik/update/deployed    # the last deployed commit
```

If there is no log and no commit after a few minutes, access for `/bin/bash` is usually missing.

## 10. Short commands for every day

The shell functions go into `~/.zshrc`:

```sh
echo 'source ~/repos/Tonregal/deploy/shell/tonregal.zsh' >> ~/.zshrc
```

Then you have `tonregal-status`, `tonregal-log`, `tonregal-restart`, `tonregal-backup-now` and `tonregal-update`. On a
second Mac the same commands run over SSH on the Tonregal Mac; set `TONREGAL_HOST` to its name for that.

## 11. Connect the iPhone, iPad and Tonwerk-AI

- **App:** Install Tonregal through TestFlight. With Tailscale on, enter the address from step 7,
  `https://<mac-name>.<tailnet>.ts.net`, on first start. If you want to build the app yourself, the steps are in the
  [app's README](https://github.com/Marcel-B/Tonregal/blob/main/apple/README.md).
- **Tonwerk-AI:** The page **Verbindungen** (connections) in Tonregal shows the key for `tonwerk-ai` and copies the two lines that go
  into Tonwerk-AI's settings. After a restore with `tonregal.db` the old key stays valid; without it, create a new one
  there and enter it in [Tonwerk-AI](/en/projekte/tonwerk-ai/).

## Check that everything runs

- `tonregal-status` shows both services as `running` and the answer from `/api/health`.
- The interface opens at `https://<mac-name>.<tailnet>.ts.net`, and the library shows your albums.
- A track dropped into `Musik/Inbox` appears on the inbox page after about ten seconds.
- The next morning the overview shows a successful backup.

If a service does not run, its log almost always helps (`tonregal-log` or `~/Library/Logs/Tonregal/`). "Operation not
permitted" there means access to the external SSD is missing. Without the SSD mounted, the service waits until it is
back and never creates an empty library on the internal disk. More on the individual features is in
[Tonregal's README](https://github.com/Marcel-B/Tonregal#readme).
