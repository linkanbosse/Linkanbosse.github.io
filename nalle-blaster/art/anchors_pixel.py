"""Hittar huvudet i varje bild av pixelbjörnens spriteark (bear_sheet.png) med avståndstransform:
huvudet är den tjockaste runda delen i övre halvan av figuren. Skriver bear_anchors.json i samma format som 3D-björnen."""
import json, numpy as np
from PIL import Image
from scipy import ndimage

CW, CH, AX, AY = 102, 73, 35, 68
ANIMS = [('idle', 4), ('walk', 6), ('run', 6), ('attack', 6), ('hurt', 3), ('cheer', 2), ('faint', 6)]
im = np.array(Image.open('bear_sheet.png').convert('RGBA'))
out = {}; radii = []
for r, (a, n) in enumerate(ANIMS):
    rows = []
    for f in range(n):
        cell = im[r * CH:(r + 1) * CH, f * CW:(f + 1) * CW]
        m = cell[:, :, 3] > 100
        # bara björnen (största sammanhängande området), inte stjärnor eller slageffekter
        lab, k = ndimage.label(m)
        if k > 1:
            sizes = ndimage.sum(m, lab, range(1, k + 1)); m = lab == (1 + int(np.argmax(sizes)))
        # slageffekten är ljus och halvgenomskinlig; ta bort ljusa pixlar till höger om björnen
        ys, xs = np.nonzero(m); top, bot = ys.min(), ys.max()
        dt = ndimage.distance_transform_edt(m)
        lim = top + int((bot - top) * .5)
        dt2 = dt.copy(); dt2[lim:] = 0
        hy, hx = np.unravel_index(np.argmax(dt2), dt2.shape); rad = float(dt2[hy, hx])
        # hjässan: översta pixeln i huvudets kolumn
        col = np.nonzero(m[:, max(0, hx - 2):hx + 3].any(1))[0]; ty = col.min() if len(col) else hy - rad
        radii.append(rad)
        pts = [(hx, hy), (hx, ty + 1), (hx + rad * .30, hy - rad * .45), (hx + rad * .10, hy + rad * .85), (hx - rad * .50, hy + rad * 1.10)]
        row = []
        for x, y in pts: row += [round(float(x - AX), 1), round(float(y - AY), 1)]
        row.append(0.0); rows.append(row)
    out[a] = rows
headR = float(np.median(radii[:4])) * 1.15
json.dump({'headR': round(headR, 1), 'frames': out}, open('bear_anchors.json', 'w'))
print('headR', headR)
for a, _ in ANIMS: print(a, [r[:4] for r in out[a]])
