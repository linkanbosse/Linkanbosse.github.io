"""Mäter var huvud, ögon, hals och rygg hamnar i varje bild av 3D-björnens spriteark.
Används för att utstyrseln (hattar, glasögon, flugor, mantlar) ska följa animationen exakt.
Skriver bear3d_anchors.json: per animation en lista med [huvudmitt x,y, hjässa x,y, ögon x,y, hals x,y, rygg x,y, lutning]
(pixlar i cellen, räknat från fotankaret)."""
import json, numpy as np
src = open('bake_backpack_bear.py').read().split('cols = max')[0]
exec(src)

names = list(parts.keys())
def find(prefix):
    for n in names:
        if n.startswith(prefix): return n
    raise KeyError(prefix)
HEAD, LE, RE, TORSO = find('Head'), find('L_Eye'), find('R_Eye'), find('Body_torso')
AX, AY = json.load(open('bear3d_sheet.json'))['anchor']

def P(pz, n): return pz[n][0]
def proj(fb, pts): return project(np.asarray(pts), fb, CELL, YAW, PITCH)

out = {}
for a in ORDER:
    rows = []
    for pz in ANIMS[a]:
        fb = frame_bounds(a, pz)
        H = P(pz, HEAD); hc = H.mean(0)
        z = H[:, 2]; top = H[z >= np.quantile(z, .93)].mean(0)
        eyes = (P(pz, LE).mean(0) + P(pz, RE).mean(0)) / 2
        T = P(pz, TORSO); tz = T[:, 2]; cap = T[tz >= np.quantile(tz, .9)]
        med = np.median(cap[:, 1])
        neck = cap[cap[:, 1] <= med].mean(0); back = cap[cap[:, 1] > med].mean(0)
        s = proj(fb, [hc, top, eyes, neck, back])
        ang = float(np.arctan2(s[1, 0] - s[0, 0], -(s[1, 1] - s[0, 1])))
        row = []
        for p in s: row += [round(float(p[0] - AX), 1), round(float(p[1] - AY), 1)]
        row.append(round(ang, 3)); rows.append(row)
    out[a] = rows
idle0 = ANIMS['idle'][0]
hs = proj(bounds, P(idle0, HEAD))
headR = float((hs[:, 0].max() - hs[:, 0].min()) / 2)
json.dump({'headR': round(headR, 1), 'frames': out}, open('bear3d_anchors.json', 'w'))
print('headR', headR); print(out['idle'][0]); print(out['cheer'])
