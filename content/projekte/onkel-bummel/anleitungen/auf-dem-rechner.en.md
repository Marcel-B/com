---
titel: Onkel Bummel on your own computer
beschreibung: Start the notification service with Docker and without an identity server, sign in with the access key and send the first message from a script.
---

You need neither Proxmox nor an identity server of your own for Onkel Bummel. On any computer with Docker the server
starts with a single command, and you sign in with an access key the server creates itself. That is enough to collect
messages from scripts and services and to read and search them in the browser. How it runs with an identity server,
Tailscale and the iPhone app is shown in [Setting up Onkel Bummel](/en/projekte/onkel-bummel/einrichten.html).

## What you need

- a computer with Docker, on macOS or Windows for example Docker Desktop
- a terminal

## 1. Start the server

Create a folder, fetch the Compose file into it and start the server:

```sh
mkdir onkel-bummel && cd onkel-bummel
curl -fsSLO https://raw.githubusercontent.com/Marcel-B/onkel-bummel/main/deploy/eigener-server/docker-compose.yml
docker compose up -d
```

Docker pulls the finished image and starts the server. Database and pictures live in a Docker volume and survive
restarts and updates.

## 2. Sign in with the access key

On the first start the server creates an access key and writes it to the log once (the log line is in German):

```sh
docker compose logs onkel-bummel | grep Zugangsschlüssel
```

The key starts with `obk_`. Keep it in your password manager. The server stores only a checksum of it and cannot show
it to you again. Then open http://localhost:8080 in your browser, enter the key, and you see the still empty timeline.

If the key is lost, create a new one. The old one stops working, and every browser has to sign in again:

```sh
docker compose exec onkel-bummel dotnet OnkelBummel.Api.dll --new-access-key
```

## 3. Send the first message

Scripts do not send with the access key but each with a publish token of its own. Create it in the web interface under
**Verwaltung → Publish-Tokens** (administration, publish tokens) and give the topics it may send to, or `*` for all. The
token starts with `ob_` and is shown only once.

```sh
curl -H "Authorization: Bearer ob_…" -H "Content-Type: application/json" \
  -d '{"topic":"test","title":"Hello","message":"The first message","tags":["tada"]}' \
  http://localhost:8080/api/v1/messages
```

The message shows up in the browser right away. Pictures, buttons and the webhook for Grafana are described in
[Setting up Onkel Bummel](/en/projekte/onkel-bummel/einrichten.html) from step 4 on; replace the tailnet address with
`http://localhost:8080` there.

## 4. Reach it from other devices

As the Compose file is set up, the server answers only on your own computer. If other devices should send or read,
change the line under `ports` to `"8080:8080"` and restart with `docker compose up -d`. The access key then travels
through the network unencrypted, though. So put HTTPS in front, for example with Tailscale or a reverse proxy, before
you make the server reachable from outside your computer.

## What does not work yet

The iPhone app signs in only through an identity server so far, and pushes to the iPhone need an APNs key from the Apple
account the app belongs to. Without an identity server you therefore read your messages in the browser, on your phone
too.

## Updates

Fetch a new version in the same folder with:

```sh
docker compose pull
docker compose up -d
```
