---
titel: Setting up Onkel Bummel
beschreibung: Set up your own notification service in a Proxmox container, with sign-in through your identity server, access through Tailscale, first messages from scripts and Grafana, and the iPhone app.
---

Onkel Bummel accepts messages from your scripts and services, keeps them along with their pictures and sends them to
your iPhone as push notifications. The server runs at home in a container on Proxmox and can only be reached in your
tailnet. This guide takes you from an empty Proxmox host to the first message on your phone. All the details are in
the [README](https://github.com/Marcel-B/onkel-bummel#readme) and the
[specification](https://github.com/Marcel-B/onkel-bummel/blob/main/docs/SPEC.md) (both in German).

## What you need

- a Proxmox host with shell access as `root`; the container needs 2 cores, 1 GB of memory and 8 GB of disk
- a Tailscale account
- an identity server with OpenID Connect that puts roles into the token, such as
  [Identity](https://github.com/Marcel-B/Identity), itself reachable in the tailnet
- for the iPhone app: a Mac with Xcode and an Apple Developer Program account
- optional: a Nextcloud for the nightly backup

It also works without Proxmox and an identity server: [Onkel Bummel on your own computer](/en/projekte/onkel-bummel/auf-dem-rechner.html)
starts the server with Docker and an access key.

## 1. Prepare the tailnet

In the Tailscale admin console, turn on MagicDNS and HTTPS certificates under **DNS**. This gives Onkel Bummel an
address like `https://onkel-bummel.<your-tailnet>.ts.net` with a valid certificate. Create an auth key under
**Settings → Keys**. Without a key, the script shows a sign-in link later on.

## 2. Prepare sign-in on the identity server

Onkel Bummel has no users of its own; it asks the identity server. Create these there once:

| What | Values |
| --- | --- |
| Scope `onkel-bummel-api` | resource or audience `onkel-bummel-api` |
| Role `onkel-bummel` | assign it to your own user |
| Client `onkel-bummel-web` | confidential, authorization code, redirect `https://onkel-bummel.<your-tailnet>.ts.net/auth/callback`, after sign-out `https://onkel-bummel.<your-tailnet>.ts.net/auth/signed-out`, scopes `profile` and `roles` |
| Client `onkel-bummel-ios` | public with PKCE, authorization code and refresh token, redirect `com.b-velop.onkel-bummel:/oauth/callback`, scope `onkel-bummel-api` |

Keep the secret of `onkel-bummel-web` to hand; it goes into the container in the next step.

## 3. Create the container

The script `create-lxc.sh` creates an unprivileged Debian container, installs Docker and Tailscale, fetches the server
and starts it. Run it in the shell of the Proxmox host:

```sh
TS_AUTHKEY=tskey-auth-... \
OIDC_ISSUER=https://identity.<your-tailnet>.ts.net \
OIDC_WEB_CLIENT_SECRET=<secret-of-onkel-bummel-web> \
bash <(curl -fsSL https://raw.githubusercontent.com/Marcel-B/onkel-bummel/main/deploy/proxmox/create-lxc.sh)
```

Without further settings, the container gets the next free ID, the name `onkel-bummel` and its address by DHCP.
Further variables such as `CTID`, `IP` and `GATEWAY` are listed in the
[Proxmox README](https://github.com/Marcel-B/onkel-bummel/blob/main/deploy/proxmox/README.md). If the script stops,
run it again with the same `CTID=…`; it carries on where it left off.

At the end, the addresses are shown. Open the app address in your browser: you land at the identity server, and after
signing in you see the timeline, still empty. The settings then live in the container in
`/etc/onkel-bummel/onkel-bummel.env`. After changing something there, apply it with

```sh
pct exec <CTID> -- docker compose -f /opt/onkel-bummel/deploy/docker-compose.yml up -d
```

## 4. Send the first message

Every sender needs a publish token. Create one in the web interface under **Verwaltung → Publish-Tokens**
(administration → publish tokens; the interface is in German so far) and enter the topics it may send to, or `*` for
all. The token starts with `ob_` and is shown only this once. A topic comes into being with its first message:

```sh
curl -H "Authorization: Bearer ob_…" -H "Content-Type: application/json" \
  -d '{"topic":"garage","title":"Door","message":"The garage door is open","priority":4,"tags":["warning"]}' \
  https://onkel-bummel.<your-tailnet>.ts.net/api/v1/messages
```

With a picture and a button, it goes as a form:

```sh
curl -H "Authorization: Bearer ob_…" -F topic=camera -F message="Motion at the driveway" -F file=@snap.jpg \
  -F 'actions=[{"label":"Lights on","url":"http://house/lights","method":"POST","clear":true}]' \
  https://onkel-bummel.<your-tailnet>.ts.net/api/v1/messages
```

The message appears in the web interface straight away. The server, not the phone, will carry out the button later.

## 5. Connect Grafana

In Grafana, create a contact point of type **Webhook** with the address
`https://onkel-bummel.<your-tailnet>.ts.net/api/v1/webhooks/grafana?topic=alarme`. Under **Authorization Header**,
enter the scheme `Bearer` and, as credentials, a token that applies to the topic `alarme`. **Test** sends a sample.

## 6. The iPhone app

The app is not in the App Store. You build it yourself with Xcode and XcodeGen:

```sh
brew install xcodegen
git clone https://github.com/Marcel-B/onkel-bummel
cd onkel-bummel/ios
xcodegen
open OnkelBummel.xcodeproj
```

The project is set up for Marcel's Apple account. For your own, change the team, bundle ID, app group and redirect
URI: in `ios/project.yml`, in the entitlements and in the app's code (a search for `b-velop` finds them all). The new
redirect URI then also goes into the client `onkel-bummel-ios`, and the bundle ID into the server setting
`Apns__BundleId`. On first launch, enter the server address or scan the QR code from **Verwaltung → App einrichten**
(set up app), sign in and subscribe to the topics you want on your phone. The app reaches the server through
Tailscale; it is best to set Tailscale on the iPhone to “On Demand”.

For pushes to arrive, the server needs an APNs key. Create it in your Apple Developer account under
**Certificates, Identifiers & Profiles → Keys** and copy the `.p8` file into the container:

```sh
pct push <CTID> AuthKey_XXXXXXXXXX.p8 /etc/onkel-bummel/secrets/apns.p8
pct exec <CTID> -- chown root:1654 /etc/onkel-bummel/secrets/apns.p8
pct exec <CTID> -- chmod 640 /etc/onkel-bummel/secrets/apns.p8
```

Then enter `Apns__KeyPath=/run/secrets/apns.p8`, `Apns__KeyId` and `Apns__TeamId` in
`/etc/onkel-bummel/onkel-bummel.env` and restart the server as in step 3. The next message arrives as a
notification, pictures with a preview.

## 7. Backup to Nextcloud

In Nextcloud, create an app password under **Settings → Security → Devices & sessions** and enter in
`/etc/onkel-bummel/onkel-bummel.env`:

```sh
Backup__NextcloudWebDavUrl=https://cloud.example.com/remote.php/dav/files/<user>/Backups/onkel-bummel
Backup__NextcloudUserName=<user>
Backup__NextcloudAppPassword=<app-password>
Backup__Passphrase=<optional, encrypts the archives>
```

The folder `Backups` must already exist. Every night at 03:30, the server uploads the database and attachments as a
ZIP, one per weekday and one per month. Keep the passphrase outside the container, for example in your password
manager. How to restore a backup is described in the
[Proxmox README](https://github.com/Marcel-B/onkel-bummel/blob/main/deploy/proxmox/README.md#sicherung-in-die-nextcloud).

## Updates

You do not need to look after updates. Every five minutes, the container checks for a new version, fetches the
finished image, backs up the database first and restarts. If the server does not answer afterwards, the previous
version and the old database run again. To see what happened last:

```sh
pct exec <CTID> -- journalctl -u onkel-bummel-update -n 30
```
