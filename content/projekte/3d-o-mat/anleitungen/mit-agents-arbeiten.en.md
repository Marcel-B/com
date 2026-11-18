---
titel: Using 3d-o-mat with agents
beschreibung: Add 3d-o-mat to Claude Code as an MCP server, so that an agent turns a picture into a 3D model, adds a skeleton and puts the result into your project.
---

3d-o-mat is not only for the browser. Through the Model Context Protocol (MCP) an agent can work with it too, for
example Claude Code while building a game: upload a picture or have one painted, turn it into 3D, wait, add a skeleton
and fetch the model as GLB, 3MF or STL. The MCP server is part of 3d-o-mat itself and runs at the same address as the
website, under `/mcp`. Nothing needs installing on your computer apart from the entry in Claude Code.

## What you need

- a running 3d-o-mat your computer can reach, in your home network or over a private network such as Tailscale
- Claude Code on that computer

3d-o-mat asks for no login. That is why it does not belong on the open internet, and neither does its MCP server. For
the same reason agents running in the cloud cannot reach it.

## 1. Add the server

In the terminal, with your 3d-o-mat's address:

```sh
claude mcp add --transport http --scope user 3d-o-mat https://<address-of-3d-o-mat>/mcp
```

`--scope user` makes 3d-o-mat available in all your projects. To have it in one project only, and there for everyone
who checks it out, put a file `.mcp.json` into the repository instead:

```json
{ "mcpServers": { "3d-o-mat": { "type": "http", "url": "https://<address-of-3d-o-mat>/mcp" } } }
```

## 2. Check that it answers

```sh
claude mcp list
```

`3d-o-mat` should say `Connected`. If it shows an error, open the same address without `/mcp` in the browser: if the
3d-o-mat page does not load, the network is the problem, not Claude Code. Inside a running session `/mcp` lists
3d-o-mat's tools.

## 3. Use it

Just tell the agent what you want, for example:

> Turn `images/knight.png` into a 3D model with a skeleton and put the GLB under `assets/figures/`.

The agent uploads the picture, starts the job, waits and fetches the file. A job takes a few minutes depending on its
size, the skeleton about one more. Whatever it creates also shows up in the list on the website, and jobs from the
browser and from the agent wait in the same queue.

The tools at a glance:

| Tool | What it does |
| --- | --- |
| `get_status` | tells whether 3d-o-mat can work right now and how many jobs are waiting |
| `upload_image`, `list_images`, `show_image` | upload, list and look at pictures |
| `check_image` | Gemma checks whether a picture suits 3D |
| `write_image_prompts`, `paint_images`, `get_painting` | write prompts from an idea and have pictures painted |
| `create_model`, `get_job`, `list_jobs`, `cancel_job` | picture to 3D, wait for the result, look at jobs and cancel a waiting one |
| `add_skeleton` | add a skeleton with Mixamo bone names |
| `export_model` | a download address for the GLB or a print file (3MF, STL) |

Large files do not go through the conversation with the agent: it gets an address and downloads the file itself, and
it is best to let it upload a picture from disk directly as well.

## What does not work yet

Animations from the motion library, poses and the joint editor are only in the browser, because the motions are
carried over to the figure there. Importing your own model and deleting are browser-only too. The MCP server has been
tried with a simulated computing side, with Claude Code and the official MCP client; trying it with the real service
and real models is still to come.
