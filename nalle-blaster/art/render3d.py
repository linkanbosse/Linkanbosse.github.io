"""Liten mjukvarurenderare för hd_bear_character.glb (bara numpy + Pillow).
Läser GLB, delar upp i namngivna delar, kan rotera delar runt leder (för animation),
ritar med z-buffert, mjuk ljussättning (cel-skuggning) och mörk kontur."""
import struct, json, numpy as np
from PIL import Image

COMP = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
NCOMP = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}

def load_glb(path):
    d = open(path, 'rb').read()
    clen, = struct.unpack('<I', d[12:16]); j = json.loads(d[20:20+clen])
    off = 20 + clen; blen, = struct.unpack('<I', d[off:off+4]); buf = d[off+8:off+8+blen]
    def acc(i):
        a = j['accessors'][i]; bv = j['bufferViews'][a['bufferView']]
        start = bv.get('byteOffset', 0) + a.get('byteOffset', 0); dt = COMP[a['componentType']]; n = NCOMP[a['type']]
        arr = np.frombuffer(buf, dtype=dt, count=a['count'] * n, offset=start).reshape(a['count'], n)
        if a.get('normalized'): arr = arr.astype(np.float32) / np.iinfo(dt).max
        return arr.astype(np.float32) if dt != np.float32 else arr
    parts = {}
    for node in j['nodes']:
        if 'mesh' not in node: continue
        m = j['meshes'][node['mesh']]
        for pr in m['primitives']:
            P = acc(pr['attributes']['POSITION']).copy()
            if 'COLOR_0' in pr['attributes']:
                C = acc(pr['attributes']['COLOR_0'])[:, :3].copy()
            else:
                mat = j.get('materials', [{}])[pr['material']] if 'material' in pr else {}
                bc = mat.get('pbrMetallicRoughness', {}).get('baseColorFactor', [.7, .7, .7, 1])
                C = np.tile(np.array(bc[:3], np.float32), (len(P), 1))
            if C.max() > 1.01: C = C / 255.0
            I = acc(pr['indices']).reshape(-1, 3).astype(np.int64)
            if 'translation' in node: P += np.array(node['translation'], np.float32)
            if 'scale' in node: P *= np.array(node['scale'], np.float32)
            parts[node.get('name', m.get('name'))] = (P, C, I)
    return parts

def rot(axis, ang):
    c, s = np.cos(ang), np.sin(ang)
    if axis == 'x': return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], np.float32)
    if axis == 'y': return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], np.float32)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], np.float32)

def vertex_normals(P, I):
    N = np.zeros_like(P); f = np.cross(P[I[:, 1]] - P[I[:, 0]], P[I[:, 2]] - P[I[:, 0]])
    for k in range(3): np.add.at(N, I[:, k], f)
    return N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)

def render(parts, size=256, yaw=0.0, pitch=0.35, pad=0.06, bounds=None, light=(-.45, -.75, .55), tint=None, outline=2, flat=False):
    """yaw: rotation kring Z (0 = framifrån, positiv = vrid mot höger), pitch: kamerans lutning ovanifrån.
    tint: funktion (färger) -> färger för att byta päls. Returnerar RGBA-bild."""
    allP, allC, allN, allI, allID = [], [], [], [], []
    base = 0
    for pid, (name, (P, C, I)) in enumerate(parts.items()):
        allP.append(P); allC.append(tint(name, C) if tint else C); allN.append(vertex_normals(P, I)); allI.append(I + base)
        allID.append(np.full(len(I), pid)); base += len(P)
    P = np.concatenate(allP); C = np.concatenate(allC); N = np.concatenate(allN); I = np.concatenate(allI); ID = np.concatenate(allID)
    R = rot('x', -pitch) @ rot('z', yaw)        # modell: Z upp, -Y framåt
    V = P @ R.T; NV = N @ R.T
    # skärm: x = V.x, y = -V.z (upp), djup = V.y (mindre = närmare kameran som tittar mot +Y)
    if bounds is None:
        bounds = (V[:, 0].min(), V[:, 0].max(), V[:, 2].min(), V[:, 2].max())
    x0, x1, z0, z1 = bounds; span = max(x1 - x0, z1 - z0) * (1 + 2 * pad)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    sx = (V[:, 0] - cx) / span * size + size / 2; sy = (cz - V[:, 2]) / span * size + size / 2; dep = V[:, 1]
    L = np.array(light, np.float32); L /= np.linalg.norm(L)
    lam = np.clip(NV @ L, 0, 1)
    # cel-skuggning: tre ljusnivåer + lite mjukhet
    shade = np.where(lam > .55, 1.0, np.where(lam > .18, .82, .64)) * .78 + lam * .22
    rim = np.clip(1 - np.abs(NV[:, 1]), 0, 1) ** 3 * .12
    col = C.copy() if flat else np.clip(C * shade[:, None] + rim[:, None], 0, 1)
    zbuf = np.full((size, size), np.inf, np.float32); img = np.zeros((size, size, 3), np.float32); idb = np.full((size, size), -1, np.int32)
    tri = np.stack([sx[I], sy[I]], -1); dz = dep[I]; tc = col[I]
    area = (tri[:, 1, 0] - tri[:, 0, 0]) * (tri[:, 2, 1] - tri[:, 0, 1]) - (tri[:, 2, 0] - tri[:, 0, 0]) * (tri[:, 1, 1] - tri[:, 0, 1])
    for t in np.where(np.abs(area) > 1e-9)[0]:
        a, b, c = tri[t]; xs = (a[0], b[0], c[0]); ys = (a[1], b[1], c[1])
        xa, xb = max(int(min(xs)), 0), min(int(max(xs)) + 1, size - 1); ya, yb = max(int(min(ys)), 0), min(int(max(ys)) + 1, size - 1)
        if xa > xb or ya > yb: continue
        gx, gy = np.meshgrid(np.arange(xa, xb + 1) + .5, np.arange(ya, yb + 1) + .5)
        w0 = ((b[0] - gx) * (c[1] - gy) - (c[0] - gx) * (b[1] - gy)) / area[t]
        w1 = ((c[0] - gx) * (a[1] - gy) - (a[0] - gx) * (c[1] - gy)) / area[t]
        w2 = 1 - w0 - w1
        m = (w0 >= -1e-4) & (w1 >= -1e-4) & (w2 >= -1e-4)
        if not m.any(): continue
        z = w0 * dz[t, 0] + w1 * dz[t, 1] + w2 * dz[t, 2]
        zb = zbuf[ya:yb + 1, xa:xb + 1]; upd = m & (z < zb)
        if not upd.any(): continue
        zb[upd] = z[upd]
        cc = w0[..., None] * tc[t, 0] + w1[..., None] * tc[t, 1] + w2[..., None] * tc[t, 2]
        img[ya:yb + 1, xa:xb + 1][upd] = cc[upd]; idb[ya:yb + 1, xa:xb + 1][upd] = ID[t]
    alpha = np.isfinite(zbuf)
    if outline:
        # kontur runt hela figuren och tunnare linjer där djupet hoppar mellan delar
        from scipy import ndimage
        out = ndimage.binary_dilation(alpha, iterations=outline) & ~alpha
        zz = np.where(alpha, zbuf, 9); edge = np.zeros_like(alpha)
        for dy, dx in ((0, 1), (1, 0)):
            d = np.abs(zz - np.roll(np.roll(zz, dy, 0), dx, 1)); edge |= (d > span * .045) & alpha
        ink = np.zeros(3) if flat else np.array([.17, .1, .06])
        if not flat: img[edge] = img[edge] * .35 + ink * .65
        img[out] = ink; alpha = alpha | out
    rgba = np.dstack([np.clip(img, 0, 1) * 255, alpha * 255]).astype(np.uint8)
    return Image.fromarray(rgba, 'RGBA'), bounds

def project(pts, bounds, size, yaw, pitch, pad=0.06):
    R = rot('x', -pitch) @ rot('z', yaw); V = np.asarray(pts, np.float32) @ R.T
    x0, x1, z0, z1 = bounds; span = max(x1 - x0, z1 - z0) * (1 + 2 * pad); cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    return np.stack([(V[:, 0] - cx) / span * size + size / 2, (cz - V[:, 2]) / span * size + size / 2, V[:, 1]], 1)
