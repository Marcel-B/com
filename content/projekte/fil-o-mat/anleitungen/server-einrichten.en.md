---
titel: Setting up the fil-O-mat server
beschreibung: Set up the backend with its web interface in a Proxmox container or on any Docker machine, with Tailscale for access on the road, updates from the app and a nightly backup to Nextcloud.
---

The server is the heart of fil-O-mat. It keeps filament types, spools and containers in one place for every device,
polls the printers, books what each print uses and serves the web interface. It runs as a Docker container and needs
little: one core and 1 GB of memory are enough. This guide is the first of three parts. After it come
[the apps](/en/projekte/fil-o-mat/apps-einrichten.html) and [the NFC reader at the printer](/en/projekte/fil-o-mat/nfc-leser-bauen.html).

The apps and the web interface are available in German and English, and this guide uses the English labels. You switch
the language in the settings.

## What you need

- a machine that is always on and sits in the same network as your printers, for example a
  [Proxmox](https://www.proxmox.com/) server, a NAS with Docker or a Raspberry Pi
- for the Proxmox route: access to the Proxmox host's shell as `root`
- optional: a [Tailscale](https://tailscale.com) account if you also want access on the road
- optional: a Nextcloud for the nightly backup

## 1. Create the container on Proxmox

The script `create-lxc.sh` does everything in one go. It creates an unprivileged Debian 12 container, installs Docker
in it, fetches fil-O-mat into `/opt/fil-o-mat`, builds the image and starts it. Download it in the Proxmox host's shell
and run it:

```sh
curl -fsSLO https://raw.githubusercontent.com/Marcel-B/fil-o-mat/main/deploy/proxmox/create-lxc.sh
bash create-lxc.sh
```

Without further settings the container gets the next free ID, the name `filomat` and its address by DHCP. Everything
can be set through environment variables before the call. A fixed address is sensible, because the apps and the NFC
readers will later have it entered permanently:

```sh
CTID=150 IP=192.168.1.50/24 GATEWAY=192.168.1.1 bash create-lxc.sh
```

| Variable | Default | What for |
| --- | --- | --- |
| `CTID` | next free one | the container's ID |
| `CT_HOSTNAME` | `filomat` | the container's name |
| `IP`, `GATEWAY` | DHCP | fixed address, e.g. `192.168.1.50/24` |
| `STORAGE`, `BRIDGE` | `local-lvm`, `vmbr0` | storage and network bridge |
| `DISK_GB`, `MEMORY_MB`, `CORES` | 8, 1024, 2 | size of the container |
| `PORT` | 8080 | the server's port |
| `FILOMAT_API_KEY` | empty | key that apps and readers have to send |
| `TAILSCALE`, `TS_AUTHKEY`, `TS_SERVE` | off | access through Tailscale (see step 3) |
| `NEXTCLOUD_WEBDAV_URL`, `NEXTCLOUD_USERNAME`, `NEXTCLOUD_APP_PASSWORD` | empty | nightly backup (see step 5) |

The first run takes a few minutes because the image is built. At the end the address is shown, for example
`Backend: http://192.168.1.50:8080`. The script waits until the server answers and otherwise shows the last log lines.

The API key is a simple protection: if it is set, every request has to send it in the `X-Api-Key` header. There is no
login with users. So never put the server openly on the internet; use Tailscale for access on the road.

## 1b. Without Proxmox: on a Docker machine

On any machine with Docker and Docker Compose you can do it by hand. The image builds the web interface too, so you
need the whole repository and not just the `backend` folder:

```sh
git clone https://github.com/Marcel-B/fil-o-mat.git
cd fil-o-mat/backend
docker compose up -d --build
```

Settings such as `FILOMAT_API_KEY` or the Nextcloud credentials go into the file `backend/.env` next to
`docker-compose.yml`. The database lives in the Docker volume `filomat-data` and survives every rebuild.

## 2. Check that it runs

Open `http://<address>:8080/` in your browser. You see fil-O-mat's web interface. It can do everything except NFC:
printers with their state, filament types, spools, containers, statistics, notifications, backup and update. If an API
key is set, enter it there under **Settings**. A quick test in the terminal goes like this:

```sh
curl http://192.168.1.50:8080/health
```

If an answer comes back, the server is running. It creates its database by itself on the first start.

## 3. Reach it on the road with Tailscale

In your home network the apps reach the server directly. For this to work on the road as well, Tailscale runs right
inside the container. For a new container you simply pass `TAILSCALE=1`:

```sh
TAILSCALE=1 bash create-lxc.sh
```

For a container that is already running there is a script of its own. It too runs in the Proxmox host's shell:

```sh
curl -fsSLO https://raw.githubusercontent.com/Marcel-B/fil-o-mat/main/deploy/proxmox/add-tailscale.sh
CTID=150 bash add-tailscale.sh
```

It passes the tunnel device through to the container (which restarts once for it), installs Tailscale and signs it
into your tailnet. With `TS_AUTHKEY=tskey-auth-…` this happens without a prompt, otherwise it shows a link to sign in.
At the end it lists the addresses under which the server can be reached in the tailnet, such as
`http://filomat.<your-tailnet>.ts.net:8080`. With `TS_SERVE=1` you also get HTTPS without a port; for that, MagicDNS
and HTTPS certificates must be switched on in your tailnet.

The server still reaches the printers in your home network directly; Tailscale does not reroute that traffic. The NFC
readers, on the other hand, do not join the tailnet. They always need the address in your home network.

## 4. Updates

Inside the container a schedule checks every 15 minutes whether there are new versions. The apps show this under
**Backend**, the web interface under **Settings**. Once you confirm, the server fetches the new
version, rebuilds the image and restarts. If the new image cannot be built, the previous version simply keeps running.

By hand it works in the Proxmox host's shell:

```sh
pct exec 150 -- /opt/fil-o-mat/deploy/updater/filomat-update.sh check   # only look
pct exec 150 -- /opt/fil-o-mat/deploy/updater/filomat-update.sh apply   # update
pct exec 150 -- journalctl -u filomat-update -n 50                      # log of the last update
```

If an update fails while building, the network was often briefly gone or the disk is full. Then this helps inside the
container:

```sh
df -h /
cd /opt/fil-o-mat && git pull && cd backend && docker compose build && docker compose up -d
```

If the disk is almost full, `docker system prune -af` clears out old images and the build cache. The database lives in
a volume and is kept.

## 5. Nightly backup to Nextcloud

Every night at 3 o'clock the server packs the database into a ZIP and uploads it over WebDAV into a folder of your
Nextcloud. This gives seven daily files (`filomat-mon.zip` to `filomat-sun.zip`) and one file per month
(`filomat-2026-10.zip`). Nothing is ever deleted in the Nextcloud.

1. Create an app password in Nextcloud under **Settings → Security → Devices & sessions**.
2. Create a folder such as `Backups`. The server creates the subfolder `fil-o-mat` itself.
3. Pass the three values when creating the container, or add them later to `/opt/fil-o-mat/backend/.env`.

```sh
NEXTCLOUD_WEBDAV_URL=https://cloud.example.de/remote.php/dav/files/<user>/Backups/fil-o-mat
NEXTCLOUD_USERNAME=<user>
NEXTCLOUD_APP_PASSWORD=<app-password>
```

Then restart the server inside the container and trigger a backup right away:

```sh
cd /opt/fil-o-mat/backend
docker compose up -d
curl -X POST http://localhost:8080/api/backup
curl http://localhost:8080/api/backup
```

The second request shows how the last backup went. You see the same in the app under **Backend**. With an API key,
both `curl` calls also need `-H "X-Api-Key: …"`. How to restore a backup is described in the
[backend's README](https://github.com/Marcel-B/fil-o-mat/blob/main/backend/README.md#sicherung-in-die-nextcloud)
(in German).

## 6. Notifications on your phone with ntfy

The server can let you know through [ntfy](https://ntfy.sh) when a print finishes or is cancelled, when a spool will
not last for the running print and when an unknown swatch sits in a reader. With Bambu and Klipper printers that
have a camera, a photo comes along. A topic on ntfy.sh with a name that is hard to guess is enough, such as
`https://ntfy.sh/filomat-7f3k2q`. Subscribe to it in the ntfy app and enter the address in the fil-O-mat app under
**Printers → Notifications**. There, **Send test notification** sends a test message. The ntfy app
also works without Google services.

Continue with [the apps](/en/projekte/fil-o-mat/apps-einrichten.html).
