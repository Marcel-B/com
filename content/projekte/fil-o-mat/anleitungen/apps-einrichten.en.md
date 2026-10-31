---
titel: Setting up fil-O-mat on Android and iPhone
beschreibung: Install the apps, connect them to the server, add printers and give the first sample tiles their NFC tags.
---

The apps are the part of fil-O-mat you hold in your hand every day. With them you read and write the NFC tags on the
sample tiles, put spools into storage and load them into printers. This guide assumes a running server, see
[Setting up the fil-O-mat server](/en/projekte/fil-o-mat/server-einrichten.html).

The apps are in German so far; this guide gives the German labels in bold with their meaning alongside.

## What you need

- an Android phone with NFC (Android 7 or later) or an iPhone with iOS 17 or later; NFC only works on real devices, not
  in the emulator or simulator
- for Android: a computer with [Android Studio](https://developer.android.com/studio)
- for the iPhone: a Mac with Xcode 16 or newer and an Apple developer account, because without one Apple gives an app
  no NFC access
- NFC tags of type NTAG213, NTAG215 or NTAG216 as stickers, one for each sample tile
- your server's address, such as `http://192.168.1.50:8080`, and the API key if you set one

The apps are not in the stores. You build them from the source code, which you fetch like this:

```sh
git clone https://github.com/Marcel-B/fil-o-mat.git
```

## 1. Install the Android app

1. In Android Studio choose **File → Open** and open the folder `fil-o-mat/android-app`. Android Studio downloads the
   dependencies by itself.
2. On the phone, switch on the developer options and USB debugging, and connect it by cable.
3. Select the phone as the target at the top and press **Run** (▶). The app then starts on the phone.

You install an update the same way; the data on the phone is kept. Do not uninstall the app as long as it has not been
synchronised with the server, or its local data is gone.

On GrapheneOS the app needs the **Network** permission. Without it, synchronising fails with the message
“socket failed: EPERM”. You switch it on in the app's settings under **Permissions**.

## 2. Install the iPhone app

1. Open `fil-o-mat/ios-app/Filomat.xcodeproj` in Xcode.
2. For the target **Filomat**, choose your team under **Signing & Capabilities**. If the bundle ID `com.filomat.app`
   is already taken, enter one of your own, such as `de.<yourname>.filomat`. The NFC entitlement is already in place.
3. Connect the iPhone, select it as the target and start with ⌘R.

Without a cable it works through TestFlight: GitHub Actions builds the app signed and uploads it. How to set that up
for your own account is described in
[TESTFLIGHT.md](https://github.com/Marcel-B/fil-o-mat/blob/main/ios-app/TESTFLIGHT.md).

On the first connection iOS asks whether the app may access devices on the local network. Allow it, or the app will
not reach the server in your home network.

## 3. Connect to the server

This works the same in both apps:

1. In the **Container** tab, tap the cloud symbol at the top.
2. Enter the server address, for example `http://192.168.1.50:8080`, and the API key if one is set.
3. Tap **Verbinden und abgleichen** (connect and synchronise).

When connecting, the app uploads what is already on the device and then takes over the shared state. Nothing is
deleted in the process. After that every change goes to the server at once, and the app reloads every two minutes
while it is open. If you have already worked with both apps, connect one first and then the other; afterwards both
show the same.

On the road you use the Tailscale address, such as `http://filomat.<your-tailnet>.ts.net:8080`. For this the Tailscale
app on the phone has to be connected. It works the same way in your home network.

If app and server do not match, the app tells you: “Backend veraltet” (backend outdated) means you should update the
server (under **Backend**), “App veraltet” (app outdated) means the app needs an update.

## 4. Add printers

In the **Drucker** (printers) tab you add each printer with **+**. Every printer gets a container of its own that holds
the loaded spools.

| Printer | Type in the app | Address | Key |
| --- | --- | --- | --- |
| Klipper, e.g. Voron | Klipper / Moonraker | `http://<printer>:7125` | only with Moonraker login |
| Snapmaker U1 with paxx12 firmware | Snapmaker U1 (paxx12) | `http://<printer>` | none |
| Prusa MK4, Core One, Mini, XL | Prusa (PrusaLink) | `http://<printer>` | API key from Settings → Network → PrusaLink on the printer |
| Anycubic Kobra X, S1, 3, 4 | Anycubic Kobra (LAN-Modus) | `http://<printer>` | none; switch on LAN mode on the printer |
| Bambu Lab P1S, P1P, X1, A1 | Bambu Lab (LAN) | `http://<printer>` | access code from the printer's Wi-Fi settings |

After saving, the server polls the printer at once. If that works, the app shows its state with the running print,
temperatures and occupied slots. With Bambu printers on newer firmware it may be necessary to switch on LAN mode with
developer mode on the printer; if the app shows an MQTT error, look there.

## 5. Filament types and sample tiles

fil-O-mat thinks in filament types. A type is, for example, “eSun PLA+ very peri”, with a stock of full spools. The NFC
tag is not stuck on the spool but on a sample tile of the type, so it stays when a spool is empty. Every opened spool
gets a short number that you write on the spool with a pen, and has its own remaining weight and its place: in a
printer or in storage.

1. Stick the tag sticker onto the sample tile.
2. In the **Filamente** (filaments) tab, create a new type: manufacturer, material, colour, temperatures, full and
   empty weight and how many full spools you have. The templates fill in much of it already.
3. Tap **Auf Tag schreiben** (write to tag) and hold the phone to the tile. The app writes the type's data onto the
   tag in the open OpenSpool format and remembers the tag's ID. Printers such as the Snapmaker U1 read this format
   directly.

A type may have several tiles, for example one on the box and one at the printer. All point to the same entry. You add
more tiles when editing the type with **Plättchen hinzufügen** (add tile). Whether a tile is written correctly you can
see in the **Scannen** (scan) tab under **Filament-Tag lesen** (read filament tag). It shows everything on the tag and
what fil-O-mat knows about it.

## 6. Store spools and load them into the printer

In the **Scannen** (scan) tab you find the everyday workflows:

- **Einlagern** (store): scan the tile, choose whether the type's full spools or an opened spool go into storage, then
  scan the container or pick it from the list. Containers get a tag of their own for this.
- **In Drucker einlegen** (load into printer): scan the tile, choose an opened spool or open a new one, then tap the
  printer and slot. Whatever was there before goes back into storage.
- **Vorrat** (stock): full and opened spools per type with total weight and a shopping list.
- **Lichtdurchlässigkeit erfassen** (record translucency): enter a type's TD value, from a TD-1 for example.

From here on, the server books what each print uses onto the spool that is loaded in the printer. So that this happens
by itself, without tapping “In Drucker einlegen” after every spool change, there is the
[NFC reader at the printer](/en/projekte/fil-o-mat/nfc-leser-bauen.html).
