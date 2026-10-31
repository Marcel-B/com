---
untertitel: A 3D model from a picture
vision: A photo or an idea should turn into a 3D model you can spin around, put into a game or print. 3d-o-mat does this
  with AI models on your own Mac, without a cloud and without any 3D skills.
kurz: Upload a picture or have one painted, cut it out, turn it into a textured 3D model with TRELLIS.2, view it, give it
  a skeleton and download it as GLB.
links:
- text: Source on GitHub
  url: https://github.com/Marcel-B/3d-o-mat
features:
- titel: Upload and cut out a picture
  wozu: An ordinary photo is enough as a template, background and all.
  verhalten:
  - PNG, JPEG and WebP are accepted.
  - If the picture already has transparency, it is kept; otherwise rembg removes the background.
  - The picture is then cropped to a square around the object.
- titel: Have a picture checked
  wozu: Know whether the template is any good before a model computes for minutes.
  verhalten:
  - Gemma judges whether a single object is fully and sharply in frame, and gives tips.
- titel: Have pictures painted
  wozu: Get a model even when there is no suitable photo.
  verhalten:
  - From an idea, Gemma writes image prompts for a good template.
  - img-o-mat paints one to four pictures with FLUX.2 Klein 4B, Z-Image Turbo or Krea 2 Turbo.
  - Every painted picture is cut out like an uploaded one and keeps the note that it is AI-generated.
- titel: Convert to 3D
  wozu: The picture becomes a textured model without any modelling of your own.
  verhalten:
  - TRELLIS.2 creates a GLB with PBR textures; texture size, faces, resolution and seed can be chosen.
  - Jobs run one after another, and the list shows their progress.
  - Music from Tonwerk takes priority on the machine; a job then waits and says what it is waiting for.
- titel: View and download
  wozu: Check the result and carry on in Blender, Godot or Unity.
  verhalten:
  - The model can be turned in the browser and downloaded as GLB.
- titel: Add a skeleton
  wozu: Move a figure instead of having just a statue.
  verhalten:
  - SkinTokens adds bones and weights, with Mixamo names for humans, so Mixamo animations fit directly.
  - Six test moves (walk, punch, kick, raise arms, squat, fall over) show in the browser whether the skeleton fits.
  - The test moves can be taken along as animations in the GLB, for example into Godot's AnimationPlayer.
- titel: Everything on your own machine
  wozu: Pictures and models never leave the house.
  verhalten:
  - All models run locally on a Mac; the files are kept on a drive of its own.
  - If the drive is not there, the site accepts nothing.
- titel: German or English, light or dark
  wozu: Use the site in your own language and the colour scheme you are used to.
  verhalten:
  - The interface is available in German and English; without a choice it follows the browser's language.
  - Gemma checks pictures and answers in the chosen language.
  - The colour scheme is light, dark or follows the system; the browser remembers both choices.
roadmap:
  als_naechstes:
  - 'Localisation: server messages and error texts in English too'
steckbrief:
- name: Platform
  wert: Web; Docker in a Proxmox container or directly on a Mac, computing on a Mac with Apple silicon
- name: Licence
  wert: MIT
---

## Technology

The website is a Python app with FastAPI and a React interface, running in a Docker container and holding no data of its
own. The computing happens on a Mac with Apple silicon: TRELLIS.2 in MLX for picture to 3D, SkinTokens for the skeleton,
Gemma 4 in LM Studio for checking and prompting, img-o-mat for painting. A shared gate divides the models on the Mac
between 3d-o-mat and Tonwerk, loads them when needed and unloads them again after a short pause.
