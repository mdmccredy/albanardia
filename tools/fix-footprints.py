"""Align every footprint on the Albanardia map to its local street grid and
move it so it doesn't sit on streets, roads or other footprints.
Usage: python3 fix.py <repo>/map/data.js  (rewrites the file in place)
"""
import json, math, re, sys
from shapely.geometry import Polygon, LineString, Point, MultiLineString, GeometryCollection
from shapely.strtree import STRtree
from shapely.ops import unary_union
from shapely import affinity

path = sys.argv[1]
raw = open(path).read()
assert raw.startswith('const M=')
M = json.loads(raw[8:raw.rindex('}') + 1])
log = []

# ---------- street geometry ----------
num = re.compile(r'[ML]\s*(-?[\d.]+)[ ,](-?[\d.]+)')
def parse_d(d):
    out = []; cur = []
    for m in re.finditer(r'([ML])\s*(-?[\d.]+)[ ,](-?[\d.]+)', d):
        p = (float(m.group(2)), float(m.group(3)))
        if m.group(1) == 'M':
            if len(cur) > 1: out.append(cur)
            cur = [p]
        else: cur.append(p)
    if len(cur) > 1: out.append(cur)
    return out
def fmt_d(lines, nd=1):
    return ' '.join('M' + ' L'.join(f'{x:.{nd}f},{y:.{nd}f}' for x, y in l) for l in lines if len(l) > 1)

minor = []  # LineStrings of local streets
for t in M['street_tiles']:
    for key in ('d', 'c'):
        if t.get(key):
            for l in parse_d(t[key]): minor.append(LineString(l))
major = []
for k in ('majors_land', 'arts_land', 'majors', 'arts'):
    for a in M.get(k, []):
        if len(a.get('p', [])) > 1: major.append(LineString(a['p']))
for r in M.get('roads', []):
    p = r.get('p')
    if isinstance(p, list) and len(p) > 1 and isinstance(p[0], list): major.append(LineString(p))
# split long lines into short pieces for local angle estimates
def pieces(lines):
    out = []
    for l in lines:
        c = list(l.coords)
        for a, b in zip(c, c[1:]):
            if a != b: out.append(LineString([a, b]))
    return out
road_seg = pieces(major)
transit = []
for grp in ('lines', 'bus', 'rapid'):
    for ln in M.get('transit', {}).get(grp, []):
        pth = ln.get('path') if isinstance(ln, dict) else None
        if pth and len(pth) > 1: transit.append(LineString(pth))
minor_seg = pieces(minor); major_seg = road_seg + pieces(transit)
T_minor = STRtree(minor_seg); T_major = STRtree(major_seg); T_road = STRtree(road_seg)
all_seg = minor_seg + major_seg; T_all = STRtree(all_seg)
T_all_dir = STRtree(minor_seg + road_seg); all_dir = minor_seg + road_seg

def grid_peaks(c, R=1.6):
    """street direction families near c: list of angles (deg, mod 180), strongest first"""
    box = Point(c).buffer(R)
    for segs, tree in ((minor_seg, T_minor), (all_dir, T_all_dir)):
        H = [0.0] * 180
        for i in tree.query(box):
            s = segs[i]; g = s.intersection(box)
            if g.is_empty: continue
            (x1, y1), (x2, y2) = s.coords[0], s.coords[-1]
            a = int(round(math.degrees(math.atan2(y2 - y1, x2 - x1)))) % 180
            H[a] += g.length
        if sum(H) >= 0.5: break
    if sum(H) < 0.5: return []
    Hs = [sum(H[(k + d) % 180] * (3 - abs(d)) for d in range(-2, 3)) for k in range(180)]
    peaks = []
    for k in sorted(range(180), key=lambda k: -Hs[k]):
        if Hs[k] < 0.15 * Hs[sorted(range(180), key=lambda k: -Hs[k])[0]]: break
        if all(min(abs(k - q), 180 - abs(k - q)) > 25 for q in peaks): peaks.append(k)
        if len(peaks) == 3: break
    # refine each peak with a weighted mean of its neighbourhood
    out = []
    for q in peaks:
        num = den = 0.0
        for d in range(-4, 5):
            w = H[(q + d) % 180]; num += w * (q + d); den += w
        out.append(num / den if den else q)
    return out

def best_rot(c, edge_ang, R=1.6):
    """smallest rotation that lays one of the footprint's edges along a street family"""
    pk = grid_peaks(c, R)
    if not pk: return 0.0, edge_ang
    best = None
    for rank, q in enumerate(pk[:2]):
        for e in (edge_ang, edge_ang + 90):
            d = (q - e + 90) % 180 - 90
            score = abs(d) + rank * 4  # slight preference for the dominant family
            if best is None or score < best[0]: best = (score, d, q)
    return best[1], best[2]

def grid_angle(c, R=1.6):
    pk = grid_peaks(c, R)
    return pk[0] if pk else None

def poly_angle(pts):
    (x1, y1), (x2, y2) = pts[0], pts[1]
    return math.degrees(math.atan2(y2 - y1, x2 - x1))
def wrap45(d):
    d = (d + 45) % 90 - 45
    return d


def to_frame(pts, c, g):
    a = math.radians(-g); return [((x - c[0]) * math.cos(a) - (y - c[1]) * math.sin(a), (x - c[0]) * math.sin(a) + (y - c[1]) * math.cos(a)) for x, y in pts]
def from_frame(pts, c, g):
    a = math.radians(g); return [[round(c[0] + u * math.cos(a) - v * math.sin(a), 3), round(c[1] + u * math.sin(a) + v * math.cos(a), 3)] for u, v in pts]
def rectify(pts, c, g):
    """replace a skewed quad with its bounding rectangle in the street-grid frame"""
    F = to_frame(pts, c, g); us = [p[0] for p in F]; vs = [p[1] for p in F]
    return from_frame([(min(us), min(vs)), (max(us), min(vs)), (max(us), max(vs)), (min(us), max(vs))], c, g)
def snap_shift(pts, c, g, m=0.035, lim=0.35):
    """shift so the footprint's edges sit just inside the nearest parallel streets"""
    F = to_frame(pts, c, g); us = [p[0] for p in F]; vs = [p[1] for p in F]
    box = Polygon(pts).buffer(0.8)
    Lu, Lv = [], []
    for i in T_minor.query(box):
        sg = minor_seg[i]; (x1, y1), (x2, y2) = sg.coords[0], sg.coords[-1]
        if sg.length < 0.05: continue
        a = math.degrees(math.atan2(y2 - y1, x2 - x1)) - g
        a = (a + 90) % 180 - 90
        mid = to_frame([((x1 + x2) / 2, (y1 + y2) / 2)], c, g)[0]
        if abs(a) < 4: Lv.append(mid[1])
        elif abs(abs(a) - 90) < 4: Lu.append(mid[0])
    def best(L, lo, hi):
        opts = [(L0 + m) - lo for L0 in L] + [(L0 - m) - hi for L0 in L]
        opts = [o for o in opts if abs(o) <= lim]
        return min(opts, key=abs) if opts else 0.0
    du, dv = best(Lu, min(us), max(us)), best(Lv, min(vs), max(vs))
    a = math.radians(g)
    return du * math.cos(a) - dv * math.sin(a), du * math.sin(a) + dv * math.cos(a)

# ---------- generic rigid transform of nested data ----------
def is_pt(v): return isinstance(v, list) and len(v) == 2 and all(isinstance(t, (int, float)) for t in v)
def xf_point(p, c, ang, dx, dy, s=1.0):
    a = math.radians(ang); x, y = p[0] - c[0], p[1] - c[1]
    x, y = x * s, y * s
    return [round(c[0] + x * math.cos(a) - y * math.sin(a) + dx, 3), round(c[1] + x * math.sin(a) + y * math.cos(a) + dy, 3)]
def xf(v, c, ang, dx, dy, s=1.0, key=None):
    if is_pt(v): return xf_point(v, c, ang, dx, dy, s)
    if isinstance(v, list): return [xf(t, c, ang, dx, dy, s) for t in v]
    if isinstance(v, dict):
        o = {}
        for k, t in v.items():
            if k in ('ang',) and isinstance(t, (int, float)): o[k] = round(t + ang, 2)
            elif k in ('rx', 'ry', 'r', 'w', 'h') and isinstance(t, (int, float)): o[k] = round(t * s, 3)
            else: o[k] = xf(t, c, ang, dx, dy, s, k)
        return o
    return v

# point features that should ride along with whatever footprint they sit in
riders = []
for e in M['extras']:
    if e.get('kind') == 'label': riders.append(e)
for p in M.get('pois', []):
    if isinstance(p, dict) and is_pt(p.get('p')): riders.append(p)
for p in M.get('townpois', []):
    if is_pt(p.get('p')): riders.append(p)

placed = []  # polygons already settled (for footprint-footprint overlap)
cuts = []    # polygons whose interior streets get removed (superblocks)

def search(P, c, gang, obst_minor=True, rmax=1.2, step=0.04, others=True, scales=(1.0,), tree=None):
    """find the smallest grid-aligned shift (and scale) so P clears obstacles"""
    a = math.radians(gang); ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
    n = int(rmax / step)
    cand = sorted(((i * step) ** 2 + (j * step) ** 2, i, j) for i in range(-n, n + 1) for j in range(-n, n + 1))
    others_tree = STRtree(placed) if (others and placed) else None
    for s in scales:
        Ps = affinity.scale(P, s, s, origin=c) if s != 1 else P
        for d2, i, j in cand:
            if d2 > rmax * rmax: break
            dx = (i * ux + j * vx) * step; dy = (i * uy + j * vy) * step
            Q = affinity.translate(Ps, dx, dy).buffer(-0.015)
            tr = tree or (T_all if obst_minor else T_major)
            if tr.query(Q, predicate='intersects').size: continue
            if others_tree is not None and others_tree.query(Q, predicate='intersects').size: continue
            return dx, dy, s
    return None

def settle(obj, keys, outline_key, label, cut_ok=True, rmax=1.2, scales=(1.0, 0.9, 0.8, 0.7), anchor=None, ref=None):
    out = obj[outline_key] if outline_key else None
    if out is None or len(out) < 3: return
    P0 = Polygon(out)
    if not P0.is_valid or P0.area <= 0: return
    c = anchor or [P0.centroid.x, P0.centroid.y]
    fa = poly_angle(ref) if ref else poly_angle(out)
    dang, gang = best_rot(c, fa)
    P = affinity.rotate(P0, dang, origin=tuple(c))
    if len(out) == 4: P = Polygon(rectify(list(P.exterior.coords)[:-1], c, gang))
    r = search(P, tuple(c), gang, rmax=rmax, scales=scales)
    mode = 'fit'
    if r is None:
        # superblock: stay put (aligned), only dodge major roads, cut minor streets underneath
        r = search(P, tuple(c), gang, obst_minor=False, rmax=max(rmax, 2.2), step=0.05, scales=(1.0, 0.85)) or (0.0, 0.0, 1.0)
        mode = 'superblock'
    dx, dy, s = r
    inside = [rd for rd in riders if P0.contains(Point(rd['p']))]
    for k in keys:
        if k in obj and obj[k] is not None: obj[k] = xf(obj[k], c, dang, dx, dy, s)
    for rd in inside: rd['p'] = xf_point(rd['p'], c, dang, dx, dy, s)
    nc = [c[0] + dx, c[1] + dy]
    if len(obj[outline_key]) == 4: obj[outline_key] = rectify(obj[outline_key], nc, gang)
    if mode == 'superblock':
        sx, sy = snap_shift(obj[outline_key], nc, gang)
        Ps = affinity.translate(Polygon(obj[outline_key]), sx, sy).buffer(-0.015)
        if any(Ps.intersects(q) for q in placed) or T_major.query(Ps, predicate='intersects').size: sx = sy = 0.0
        for k in keys:
            if k in obj and obj[k] is not None: obj[k] = xf(obj[k], nc, 0, sx, sy)
        for rd in inside: rd['p'] = xf_point(rd['p'], nc, 0, sx, sy)
    Pn = Polygon(obj[outline_key])
    placed.append(Pn)
    if mode == 'superblock' and cut_ok: cuts.append(Pn.buffer(0.01))
    log.append((label, round(dang, 1), round(math.hypot(dx, dy), 2), s, mode))

# ---------- run ----------
# big things first so smaller things settle around them
for cp in M['campuses']:
    # campuses are superblocks by design: align to grid, dodge major roads, cut local streets
    out = cp['outline']; P0 = Polygon(out); c = [P0.centroid.x, P0.centroid.y]
    fa = poly_angle(out); dang, g = best_rot(c, fa, R=3.0)
    P = affinity.rotate(P0, dang, origin=tuple(c))
    r = search(P, tuple(c), g, obst_minor=False, rmax=1.5, step=0.1, others=False, tree=T_road) or (0, 0, 1)
    inside = [rd for rd in riders if P0.contains(Point(rd['p']))]
    for k in ('outline', 'quads', 'bldg', 'fields', 'stadium', 'arena', 'docks', 'c'):
        if cp.get(k) is not None: cp[k] = xf(cp[k], c, dang, r[0], r[1])
    for rd in inside: rd['p'] = xf_point(rd['p'], c, dang, r[0], r[1])
    nc = [c[0] + r[0], c[1] + r[1]]
    cp['outline'] = rectify(cp['outline'], nc, g)
    sx, sy = snap_shift(cp['outline'], nc, g, lim=0.5)
    for k in ('outline', 'quads', 'bldg', 'fields', 'stadium', 'arena', 'docks', 'c'):
        if cp.get(k) is not None: cp[k] = xf(cp[k], nc, 0, sx, sy)
    for rd in inside: rd['p'] = xf_point(rd['p'], nc, 0, sx, sy)
    Pn = Polygon(cp['outline']); placed.append(Pn); cuts.append(Pn.buffer(0.01))
    log.append((cp['name'], round(dang, 1), round(math.hypot(r[0], r[1]), 2), 1, 'campus'))

for m in M.get('med', []):
    settle(m, ('outline', 'bldg', 'c'), 'outline', m['name'], rmax=1.0, scales=(1.0,), ref=(m['bldg'][0] if m.get('bldg') else None))

for v in M.get('venues', []):
    rx = v.get('rx', v.get('r', 0.5)); ry = v.get('ry', v.get('r', 0.5))
    e = affinity.rotate(affinity.scale(Point(v['c']).buffer(1, 32), rx, ry), v.get('ang', 0), origin=tuple(v['c']))
    v['_o'] = [list(p) for p in e.exterior.coords][:-1]
    dang, g = best_rot(v['c'], v.get('ang', 0))
    P = affinity.rotate(e, dang, origin=tuple(v['c']))
    r = search(P, tuple(v['c']), g, obst_minor=False, rmax=0.8) or (0, 0, 1)
    v['ang'] = round(v.get('ang', 0) + dang, 2); v['c'] = [round(v['c'][0] + r[0], 3), round(v['c'][1] + r[1], 3)]
    placed.append(affinity.translate(P, r[0], r[1])); cuts.append(affinity.translate(P, r[0], r[1]).buffer(0.01))
    del v['_o']; log.append(('venue ' + v['t'], round(dang, 1), round(math.hypot(r[0], r[1]), 2), 1, 'venue'))

for s in M['schools']:
    settle(s, ('poly', 'bld', 'field', 'track', 'play', 'c'), 'poly', s['n'], anchor=s['c'], ref=(max(s['bld'], key=lambda b: Polygon(b).area) if s.get('bld') else None))

ROT_KINDS = {'bldg', 'office', 'museum', 'boathouse', 'urbcorp', 'school', 'warehouse', 'corp', 'hub', 'stadium', 'arena'}
for e in M['extras']:
    if e.get('kind') in ROT_KINDS and len(e.get('foot') or []) >= 3:
        if e.get('kind') in ('boathouse',): continue  # waterfront, sits on purpose by the water
        settle(e, ('foot', 'p'), 'foot', e['n'], rmax=0.8, scales=(1.0, 0.85, 0.7), anchor=e['p'])
        if 'ang' in e and log and log[-1][0] == e['n']: e['ang'] = round(e['ang'] + log[-1][1], 2)

# chain stores: small rectangles, rotate to grid and nudge off streets
B = M['brands']
for q in M['chains']:
    b = B[q[0]]; w, h = b[4], b[5]; x, y, a = q[1], q[2], q[3]
    R = affinity.rotate(Polygon([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)]), a, origin=(x, y))
    dang, g = best_rot((x, y), a, R=0.8)
    P = affinity.rotate(R, dang, origin=(x, y))
    r = search(P, (x, y), g, rmax=0.45, step=0.02, scales=(1.0, 0.8)) or search(P, (x, y), g, rmax=1.0, step=0.04, scales=(0.8,)) or (0, 0, 1)
    q[1] = round(x + r[0], 3); q[2] = round(y + r[1], 3); q[3] = round(a + dang, 2)
    placed.append(affinity.translate(P, r[0], r[1]))

# ---------- cut local streets inside superblocks ----------
if cuts:
    CU = unary_union(cuts); CT = STRtree(list(getattr(CU, 'geoms', [CU])))
    removed = 0
    for t in M['street_tiles']:
        for key in ('d', 'c'):
            if not t.get(key): continue
            new = []; changed = False
            for l in parse_d(t[key]):
                L = LineString(l)
                if not CT.query(L, predicate='intersects').size: new.append(l); continue
                changed = True
                g = L.difference(CU)
                parts = [g] if isinstance(g, LineString) else list(getattr(g, 'geoms', []))
                for p in parts:
                    if isinstance(p, LineString) and p.length > 0.05: new.append([(round(x, 3), round(y, 3)) for x, y in p.coords])
                removed += 1
            if changed: t[key] = ' '.join('M' + ' L'.join(f'{x:g},{y:g}' for x, y in l) for l in new if len(l) > 1)
    keep = []
    for lb in M['street_labels']:
        if not CT.query(Point(lb[0], lb[1]), predicate='intersects').size: keep.append(lb)
    log.append(('street lines trimmed', removed, len(M['street_labels']) - len(keep), 0, 'cut'))
    M['street_labels'] = keep

open(path, 'w').write('const M=' + json.dumps(M, ensure_ascii=False, separators=(',', ':')) + raw[raw.rindex('}') + 1:])
import collections
print(collections.Counter(m for *_, m in log))
json.dump(log, open(sys.argv[2] if len(sys.argv) > 2 else '/dev/null', 'w'), ensure_ascii=False)
