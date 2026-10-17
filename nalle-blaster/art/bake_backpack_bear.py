"""Bakar bear_backpack.glb (spelarens 3D-modell från ChatGPT) till spriteark för spelet.
Samma animationer och radordning som pixelbjörnen: idle 4, walk 6, run 6, attack 6, hurt 3, cheer 2, faint 6.
Skriver: bear3d_sheet.png (färg), bear3d_mask.png (R=päls, G=mage/nos, B=armar/ben/öron), bear3d_sheet.json."""
import json, numpy as np
from PIL import Image
from render3d import load_glb, render, rot, project

parts = load_glb('bear_backpack.glb')
YAW, PITCH, CELL = .62, .34, 128

def group(n):
    if n.startswith(('Left_leg', 'Left_foot', 'L_toe')): return 'legL'
    if n.startswith(('Right_leg', 'Right_foot', 'R_toe')): return 'legR'
    if n.startswith(('Left_upper_arm', 'Left_paw', 'L_finger')): return 'armL'
    if n.startswith(('Right_upper_arm', 'Right_paw', 'R_finger')): return 'armR'
    if n.startswith(('Head', 'Ear', 'Muzzle', 'Nose', 'L_Eye', 'R_Eye', 'L_eyebrow', 'R_eyebrow', 'Open_smile', 'Tongue', 'Smile', 'L_freckle', 'R_freckle')): return 'head'
    return 'body'
FUR = ('Left_leg', 'Right_leg', 'Left_foot', 'Right_foot', 'Body_torso', 'Left_upper_arm', 'Right_upper_arm', 'Left_paw', 'Right_paw', 'Head', 'Ear_L', 'Ear_R', 'Head_tuft')
BELLY = ('Belly_cream_patch', 'Muzzle_base', 'Muzzle_left', 'Muzzle_right')
LIMB = ('Left_leg', 'Right_leg', 'Left_foot', 'Right_foot', 'Left_upper_arm', 'Right_upper_arm', 'Left_paw', 'Right_paw', 'Ear_L', 'Ear_R')
PIV = {'legL': (-.34, 0, 1.25), 'legR': (.34, 0, 1.25), 'armL': (-.7, 0, 2.1), 'armR': (.7, 0, 2.1), 'head': (0, 0, 2.2)}

def pose(legL=0, legR=0, armLf=0, armRf=0, armLs=0, armRs=0, head=0, headTilt=0, lean=0, bob=0, fall=0, squash=1.0):
    """vinklar i radianer. legX/armXf: svängning fram/bak (kring X), armXs: lyft åt sidan (kring Y),
    head: nick, headTilt: lutning, lean: kroppen framåt, fall: hela björnen faller bakåt."""
    out = {}
    for n, (P, C, I) in parts.items():
        g = group(n); P = P.copy()
        if g in ('legL', 'legR'):
            a = legL if g == 'legL' else legR; pv = np.array(PIV[g]); P = (P - pv) @ rot('x', a).T + pv
        if g in ('armL', 'armR'):
            f, sd = (armLf, armLs) if g == 'armL' else (armRf, armRs); pv = np.array(PIV[g])
            P = (P - pv) @ (rot('x', f) @ rot('y', sd * (1 if g == 'armL' else -1))).T + pv
        if g == 'head':
            pv = np.array(PIV['head']); P = (P - pv) @ (rot('x', head) @ rot('y', headTilt)).T + pv
        if g != 'legL' and g != 'legR':
            pv = np.array([0, 0, 1.2]); P = (P - pv) @ rot('x', lean).T + pv
            P[:, 2] = (P[:, 2] - 1.2) * squash + 1.2
        P[:, 2] += bob
        if fall:
            pv = np.array([0, -.4, .1]); P = (P - pv) @ rot('x', fall).T + pv
        out[n] = (P, C, I)
    return out

S = np.sin; TAU = 2 * np.pi
HOLD = dict(armRf=-1.05)            # höger tass håller vapnet framåt
ANIMS = {
 'idle':  [pose(squash=1 + .018 * S(k / 4 * TAU), bob=.02 * S(k / 4 * TAU), head=.03 * S(k / 4 * TAU + 1), **HOLD) for k in range(4)],
 'walk':  [pose(legL=.5 * S(k / 6 * TAU), legR=-.5 * S(k / 6 * TAU), armLf=-.35 * S(k / 6 * TAU), bob=.07 * abs(np.cos(k / 6 * TAU)), **HOLD) for k in range(6)],
 'run':   [pose(legL=.85 * S(k / 6 * TAU), legR=-.85 * S(k / 6 * TAU), armLf=-.7 * S(k / 6 * TAU), lean=-.22, bob=.12 * abs(np.cos(k / 6 * TAU)), armRf=-1.2) for k in range(6)],
 'attack':[pose(armRf=a, lean=l, armLf=.4, legL=.25, legR=-.25) for a, l in [(.5, .05), (-.4, -.05), (-1.6, -.18), (-1.75, -.2), (-1.3, -.12), (-.6, 0)]],
 'hurt':  [pose(lean=.22, head=.25, headTilt=.25, armLs=.9, armRs=.9, squash=.95), pose(lean=.3, head=.3, headTilt=-.25, armLs=1.1, armRs=1.1, squash=.93), pose(lean=.08, head=.1, **HOLD)],
 'cheer': [pose(armLs=2.5, armRs=2.5, head=-.2, squash=1.04, bob=.05), pose(armLs=1.9, armRs=1.9, head=-.1, squash=1.0)],
 'faint': [pose(lean=.25, head=.3, armLs=.8, armRs=.8), pose(fall=-.5, armLs=1.2, armRs=1.2), pose(fall=-1.0, armLs=1.4, armRs=1.4), pose(fall=-1.45, armLs=1.5, armRs=1.5, head=.2),
           pose(fall=-1.5, armLs=1.5, armRs=1.5, head=.25, bob=.06), pose(fall=-1.5, armLs=1.5, armRs=1.5, head=.3)],
}
ORDER = ['idle', 'walk', 'run', 'attack', 'hurt', 'cheer', 'faint']

# gemensam skala för alla bilder: union av alla posers gränser
R = rot('x', -PITCH) @ rot('z', YAW)
mins, maxs = [], []
for a in ORDER:
    if a == 'faint': continue
    for pz in ANIMS[a]:
        V = np.concatenate([p[0] for p in pz.values()]) @ R.T; mins.append(V.min(0)); maxs.append(V.max(0))
mn, mx = np.min(mins, 0), np.max(maxs, 0)
bounds = (mn[0], mx[0], mn[2], mx[2])
SPAN = max(bounds[1] - bounds[0], bounds[3] - bounds[2])
def frame_bounds(a, pz):
    if a != 'faint': return bounds
    V = np.concatenate([p[0] for p in pz.values()]) @ R.T
    cx = (V[:, 0].min() + V[:, 0].max()) / 2; z0 = V[:, 2].min()
    return (cx - SPAN / 2, cx + SPAN / 2, z0 - .02, z0 - .02 + SPAN)   # liggande björn vid cellens botten

def tint_mask(name, C):
    r = 1. if name.startswith(FUR) else 0.; g = 1. if name.startswith(BELLY) else 0.; b = 1. if name.startswith(LIMB) else 0.
    return np.tile(np.array([r, g, b], np.float32), (len(C), 1))

cols = max(len(ANIMS[a]) for a in ORDER)
sheet = Image.new('RGBA', (CELL * cols, CELL * len(ORDER)), (0, 0, 0, 0)); mask = Image.new('RGBA', sheet.size, (0, 0, 0, 0))
for r, a in enumerate(ORDER):
    for c, pz in enumerate(ANIMS[a]):
        fb = frame_bounds(a, pz)
        im, _ = render(pz, size=CELL, yaw=YAW, pitch=PITCH, bounds=fb, outline=2)
        mk, _ = render(pz, size=CELL, yaw=YAW, pitch=PITCH, bounds=fb, outline=2, flat=True, tint=tint_mask)
        sheet.alpha_composite(im, (c * CELL, r * CELL)); mask.alpha_composite(mk, (c * CELL, r * CELL))
        print(a, c, flush=True)

# ankare mätta i idle-bild 0: fötter, framtass (den närmast kameran), huvud
idle0 = ANIMS['idle'][0]
foot = project([[0, 0, 0.08]], bounds, CELL, YAW, PITCH)[0]
pawL = project([idle0['Left_paw'][0].mean(0)], bounds, CELL, YAW, PITCH)[0]
pawR = project([idle0['Right_paw'][0].mean(0)], bounds, CELL, YAW, PITCH)[0]
paw = pawR if pawR[0] > pawL[0] else pawL              # tassen längst åt höger (björnen tittar åt höger)
head = project([idle0['Head'][0].mean(0)], bounds, CELL, YAW, PITCH)[0]
headTop = project([[0, 0, 3.6]], bounds, CELL, YAW, PITCH)[0]
meta = {'cell': [CELL, CELL], 'anchor': [round(float(foot[0]), 1), round(float(foot[1]), 1)],
        'hand': [round(float(paw[0] - foot[0]), 1), round(float(paw[1] - foot[1]), 1)],
        'head': [round(float(head[0] - foot[0]), 1), round(float(head[1] - foot[1]), 1)], 'headTop': round(float(headTop[1] - foot[1]), 1),
        'anims': {a: {'row': i, 'frames': len(ANIMS[a])} for i, a in enumerate(ORDER)}}
sheet.save('bear3d_sheet_full.png'); mask.save('bear3d_mask_full.png'); json.dump(meta, open('bear3d_sheet.json', 'w'))
print(meta)
