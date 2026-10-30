---
titel: Setting up Ohmventory on a Mac
beschreibung: Step by step from a Mac with Apple Silicon to the first recognised component, with LM Studio as the local language model and Docker Desktop.
---

Ohmventory consists of a database, a web search, the server and the interface. All four run in Docker. The language
model that recognises photos and suggests projects runs alongside in LM Studio, directly on the Mac, because there it can
use the graphics memory. At the end you reach Ohmventory in the browser on the Mac and from your phone on the same Wi-Fi.

## What you need

- a Mac with Apple Silicon (M1 or later) and macOS 14 or later
- memory: 32 GB for both models; with 16 GB it works with the small model alone (see step 2)
- about 30 GB of free space for models and Docker images
- an internet connection for the downloads and the web search

## 1. Install the tools

Open Terminal. Git comes with Apple's developer tools:

```sh
xcode-select --install
```

Then download two programs and install them like any other Mac app:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) in the version for Apple Silicon. Start it once and
  wait until the menu bar says "Docker Desktop is running".
- [LM Studio](https://lmstudio.ai/). Start it once so that it creates its model folder.

LM Studio comes with the command-line tool `lms`. So that Terminal finds it:

```sh
~/.lmstudio/bin/lms bootstrap
```

Then open a new Terminal window. This shows you that everything is there:

```sh
git --version
docker version
lms version
```

## 2. Get the models

Ohmventory uses two models: a small one for the project assistant and the web search, and a larger one for photo
recognition.

```sh
lms get lmstudio-community/gemma-4-e4b-it-mlx
```

For the larger model, search LM Studio's **Discover** tab for `gemma-4-26b-a4b-it-qat` and download the MLX version
(about 16 GB). `lms ls` then shows the names of both models; Ohmventory needs exactly these names. If they differ from
`gemma-4-e4b-it-mlx` and `gemma-4-26b-a4b-it-qat-mlx`, you enter them in step 3.

**Mac with 16 GB:** leave out the large model. The small one can recognise images too, just a little less accurately.

Now start LM Studio's server and load the small model with the context Ohmventory sizes its requests for:

```sh
lms server start
lms load gemma-4-e4b-it-mlx --context-length 8192
```

You can check it like this; the answer lists the models:

```sh
curl http://localhost:1234/v1/models
```

LM Studio loads the large model by itself as soon as the first photo recognition arrives. So that it does not start with
too small a context, set the context length of both models to 8192 under **My Models** in LM Studio.

## 3. Get Ohmventory and configure it

```sh
git clone https://github.com/Marcel-B/Ohmventory.git ~/Ohmventory
cd ~/Ohmventory
cp .env.example .env
```

The file `.env` holds the settings. The following lines set random passwords, connect Ohmventory to LM Studio on the Mac
and enter the address at which your phone reaches the Mac:

```sh
sed -i '' \
  -e "s|^POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=$(openssl rand -hex 16)|" \
  -e "s|^SEARXNG_SECRET=.*|SEARXNG_SECRET=$(openssl rand -hex 32)|" \
  -e "s|^LLM_GATE_URL=.*|LLM_GATE_URL=http://host.docker.internal:1234|" \
  -e "s|^PUBLIC_BASE_URL=.*|PUBLIC_BASE_URL=http://$(ipconfig getifaddr en0):8080|" \
  .env
grep -E '^(LLM_GATE_URL|PUBLIC_BASE_URL)=' .env
```

If `PUBLIC_BASE_URL` does not show an address like `http://192.168.….:8080`, the Mac is not on the network through
Wi-Fi. Then use `ipconfig getifaddr en1` and enter the address by hand (`open -e .env`).

What the settings mean:

- `LLM_GATE_URL` is the address of the language model. Ohmventory is built to share the model with other applications
  through a queue. On your own Mac it talks to LM Studio directly; from inside Docker, `host.docker.internal` is the Mac
  itself.
- `LLM_MODEL` and `LLM_VISION_MODEL` are the model names from `lms ls`. Leave them empty if they match step 2. On a Mac
  with 16 GB, set `LLM_VISION_MODEL=gemma-4-e4b-it-mlx`.
- `PUBLIC_BASE_URL` goes into the QR labels. If the Mac's address changes, print the labels again, or give the Mac a
  fixed address in your router.

## 4. Start

```sh
docker compose up -d --build
```

The first time, Docker builds the server and the interface, which takes a few minutes. Then you can see whether
everything is running:

```sh
docker compose ps
curl http://localhost:8080/api/health
```

All four services show "running" (the database "healthy"), and the second line answers `{"status":"ok"}`. The server's
log may contain a warning that the LLM gate cannot be reached; the queue only exists in a larger installation, and on the
Mac you do not need it.

If a port is already taken, a service does not start. You can move the interface to another port with `WEB_PORT=8081` in
`.env`; the database needs port 5432 and the web search port 8888, so stop any PostgreSQL running locally.

## 5. The first component

Open <http://localhost:8080>.

1. Under **Container**, create a storage place, for example your sorting box. It gets a code like `T-001`, and you can
   print its label with the QR code straight away.
2. Under **Erfassen** (record), upload a photo of a component or breakout board. The first recognition takes longer
   because LM Studio loads the model first. You confirm the suggestion, enter the quantity and choose the container.
3. In the **Assistent**, ask for example "Can I build a thermometer?". Whatever is missing goes into the shopping list.

The interface is in German for now; more languages are on the roadmap.

If recognition does not work, look at the log under **Developer** in LM Studio to see whether the request arrives, and
compare the model names with `lms ls`. Ohmventory's own messages are shown by `docker compose logs -f api`.

## 6. From your phone

On the same Wi-Fi, open the address from `PUBLIC_BASE_URL` on your phone, that is `http://<address of the Mac>:8080`. If
macOS asks whether Docker may accept incoming connections, allow it. From then on, a QR label on a box opens its contents
directly, and under **Erfassen** the phone takes the photo with its camera.

The interface has no login of its own. So do not put it on the internet through port forwarding.

## 7. Update and stop

You get a new version like this; stock and photos live in Docker volumes and are kept:

```sh
cd ~/Ohmventory
git pull
docker compose up -d --build
```

`docker compose stop` stops Ohmventory, `docker compose start` starts it again. LM Studio has to be running for
recognition and the assistant to answer; everything else works without it. If you clean up with `docker compose down -v`,
that also deletes the database and the photos.

How Ohmventory runs on a Proxmox server with automatic updates is described in the
[project's README](https://github.com/Marcel-B/Ohmventory#installation-auf-proxmox-empfohlen).
