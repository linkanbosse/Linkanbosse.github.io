"""Renderar appikonens björn (../logo.png, 1024×1024) ur bear_backpack.glb med spelets egen renderare.
Körs med `python3 render_logo.py` (numpy, Pillow, scipy). Android-bygget gör ikoner och startbild av logo.png."""
import os
import sys
import numpy as np
from PIL import Image

ART = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ART, "..", "logo.png")
SIZE = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
sys.path.insert(0, ART)
from render3d import load_glb, render, rot  # noqa: E402

parts = load_glb(ART + '/bear_backpack.glb')
PIV = {'legL': (-.34, 0, 1.25), 'legR': (.34, 0, 1.25), 'armL': (-.7, 0, 2.1), 'armR': (.7, 0, 2.1), 'head': (0, 0, 2.2)}


def group(n):
    if n.startswith(('Left_leg', 'Left_foot', 'L_toe')): return 'legL'
    if n.startswith(('Right_leg', 'Right_foot', 'R_toe')): return 'legR'
    if n.startswith(('Left_upper_arm', 'Left_paw', 'L_finger')): return 'armL'
    if n.startswith(('Right_upper_arm', 'Right_paw', 'R_finger')): return 'armR'
    if n.startswith(('Head', 'Ear', 'Muzzle', 'Nose', 'L_Eye', 'R_Eye', 'L_eyebrow', 'R_eyebrow', 'Open_smile', 'Tongue', 'Smile', 'L_freckle', 'R_freckle')): return 'head'
    return 'body'


def pose(armLf=0, armRf=0, armLs=0, armRs=0, head=0, headTilt=0):
    out = {}
    for n, (P, C, I) in parts.items():
        g = group(n); P = P.copy()
        if g in ('armL', 'armR'):
            f, sd = (armLf, armLs) if g == 'armL' else (armRf, armRs); pv = np.array(PIV[g])
            P = (P - pv) @ (rot('x', f) @ rot('y', sd * (1 if g == 'armL' else -1))).T + pv
        if g == 'head':
            pv = np.array(PIV['head']); P = (P - pv) @ (rot('x', head) @ rot('y', headTilt)).T + pv
        out[n] = (P, C, I)
    return out


# glad björn som vinkar med ena tassen, lätt vriden mot betraktaren
pz = pose(armLs=2.35, armRs=.35, head=-.12, headTilt=.12)
im, _ = render(pz, size=SIZE, yaw=.32, pitch=.3, pad=.04, outline=max(2, SIZE // 110))
im.save(OUT)
print('saved', OUT, im.size)
