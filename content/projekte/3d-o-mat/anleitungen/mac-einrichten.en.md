---
titel: Setting up 3d-o-mat on a Mac
beschreibung: Step by step to running the 3d-o-mat website on a Mac without Docker, for development, trying it out or running it directly on the computing Mac.
---

3d-o-mat has two parts: the website (a Python app with a React interface) and the computing side on a Mac with Apple
silicon, where TRELLIS.2, SkinTokens, Gemma and the image models run behind a shared gate. This guide gets the website
running on a Mac. At the end you reach it in the browser at `http://localhost:8090`, can upload and cut out pictures
and, as soon as the gate approves the models, also check, paint, convert to 3D and add skeletons.

Setting up the computing side itself (gate, MLX-Serve, rig service) is described in the
[project's README](https://github.com/Marcel-B/3d-o-mat#einrichten) (in German). The detailed version of this guide is
[docs/mac.md](https://github.com/Marcel-B/3d-o-mat/blob/main/docs/mac.md) in the repository.

## What you need

- a Mac with macOS and Terminal; the website alone does not need Apple silicon
- about 2 GB of space for Python packages, Node modules and the cut-out model
- for checking, painting and 3D, the address of a running gate on the same network where you can approve the models

## 1. Install the tools

Git comes with Apple's developer tools, Python 3.12 and Node 22 with [Homebrew](https://brew.sh):

```sh
xcode-select --install
brew install python@3.12 node@22
```

The Python that ships with macOS (3.9) is too old for the app, which needs at least 3.10. You only need Node to build
the interface. `python3.12 --version` and `node --version` show that both are there. If Terminal cannot find `node`,
`brew info node@22` gives you the line for `~/.zprofile`.

## 2. Fetch and build the project

```sh
git clone https://github.com/Marcel-B/3d-o-mat.git ~/repos/3d-o-mat && cd ~/repos/3d-o-mat
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-rembg.txt
(cd frontend && npm ci && npm run build)
```

The virtual environment `.venv` keeps all Python packages inside the project folder. `requirements-rembg.txt` brings
rembg for cutting out photos; without it the app only removes plain single-colour backgrounds. `npm run build` puts the
interface into `frontend/dist`, where the app serves it from. When a later `git pull` changes something in
`frontend/`, build it again.

## 3. Create the storage folder

Pictures, jobs and models go into one folder. The app only uses it when the marker file `.3d-o-mat` is inside, so
nothing ever lands on the wrong disk while an external one is missing.

```sh
mkdir -p ~/3d-o-mat-daten && touch ~/3d-o-mat-daten/.3d-o-mat
```

If the folder is on an external disk, macOS asks on first access whether Terminal may use removable volumes. Until you
click "Allow", the app waits without an error message.

## 4. Settings

```sh
cp config.example.json config.json
```

In `config.json` you change two things:

- `store` to your folder, as an absolute path: `"store": {"folder": "/Users/<you>/3d-o-mat-daten"}`
- `gate.url` to the gate's address, for example `http://<computing-mac>:1235`, or `http://127.0.0.1:1235` if the
  website runs on the computing Mac itself

`config.json` stays local and never goes into the repository. The README explains the other fields.

## 5. Start

```sh
.venv/bin/python -m omat3d
```

Open `http://localhost:8090`. Upload a picture: it appears cut out in the list, and the folder from step 3 now holds
`images/…`. With the first photo rembg downloads its model once (about 170 MB).

On start the app registers with the gate as `3d-o-mat`. If the gate cannot be reached, Terminal says so and the app
tries again every 10 seconds. After registering, approve TRELLIS.2, SkinTokens, Gemma and the image models for
3d-o-mat in the gate's interface under `/gate`; until then checking, painting and 3D are refused as not approved.
`http://localhost:8090/api/status` shows how far everything is: whether the storage is there, whether rembg is loaded
and which models are approved.

Stop it with Ctrl-C. Whatever was running or waiting goes back into the queue on the next start.

## 6. Development

```sh
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest
cd frontend && npm run dev
```

The tests need neither the computing side nor a network; gate and storage are simulated. `npm run dev` serves the
interface with live reload at `http://localhost:5173` and passes `/api` on to the running app on port 8090.

## If something goes wrong

- **`TypeError: unsupported operand type(s) for |` on start:** the virtual environment was created with macOS's own
  Python. Delete `.venv` and repeat step 2 with `python3.12`.
- **The page says the storage is not reachable:** `.3d-o-mat` is missing from the folder in `store.folder`, or the path is
  wrong. The app checks the storage again at most every 20 seconds.
- **The page stays empty:** `frontend/dist` is missing; build the interface (step 2).
- **Photos are cut out badly:** rembg is missing, and `/api/status` shows `"rembg": false`. Install the packages from
  `requirements-rembg.txt`.
- **`address already in use`:** port 8090 is taken, for example by a second instance. Change `port` in `config.json`.
