# Passungstest für den Magnet-Einschub von unten: fünf Einschübe nebeneinander, von links (1) nach rechts (5) strammer.
# Die Kerben oben zählen die Nummer. Wandstärken wie beim Halter (0,6 mm Haut, 0,8 mm innen).
import sys
from manifold3d import Manifold
import numpy as np

MAG_D, MAG_H = 12.0, 2.66
SKIN, INNER = 0.6, 0.8
# (Spiel Durchmesser, Spiel Dicke); der jetzige Halter hat 0,3 / 0,15
FITS = [(0.20, 0.10), (0.15, 0.05), (0.10, 0.00), (0.05, -0.05), (0.00, -0.10)]
CELL, HEIGHT = 17.0, 18.0

def box(x0, y0, z0, x1, y1, z1):
    return Manifold.cube([x1-x0, y1-y0, z1-z0]).translate([x0, y0, z0])

T = SKIN + MAG_H + 0.15 + INNER      # gleiche Gesamtdicke wie die Rückwand des Halters
body = box(0, 0, 0, CELL*len(FITS), T, HEIGHT)
for i, (fd, fh) in enumerate(FITS):
    md, mh = MAG_D + fd, MAG_H + fh
    x = CELL*(i + 0.5)
    y0 = INNER
    body -= Manifold.cylinder(mh, md/2, md/2, 128).rotate([-90, 0, 0]).translate([x, y0, md/2])
    body -= box(x - md/2, y0, -1, x + md/2, y0 + mh, md/2)
    for k in range(i + 1):           # Kerben oben = Nummer
        kx = x - (i*2.0)/2 + k*2.0
        body -= box(kx - 0.5, -1, HEIGHT - 1.5, kx + 0.5, T + 1, HEIGHT + 1)

mesh = body.to_mesh()
v = np.asarray(mesh.vert_properties)[:, :3]; t = np.asarray(mesh.tri_verts)
print("Maße", np.round(v.max(0)-v.min(0), 2), "Volumen cm3", round(body.volume()/1000, 2), "Genus", body.genus())

def write_3mf(path, v, t, title):
    import zipfile
    vs = "\n".join(f'<vertex x="{a:.4f}" y="{b:.4f}" z="{c:.4f}"/>' for a, b, c in v)
    ts = "\n".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in t)
    model = f'''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="de-DE" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">
<metadata name="Title">{title}</metadata>
<resources><object id="1" name="{title}" type="model"><mesh><vertices>
{vs}
</vertices><triangles>
{ts}
</triangles></mesh></object></resources>
<build><item objectid="1"/></build></model>'''
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model', model)

# Druck stehend, Unterkante (Einschuböffnungen) aufs Bett
write_3mf('Magnet-Passungstest.3mf', v - v.min(0), t, 'Magnet-Passungstest')
