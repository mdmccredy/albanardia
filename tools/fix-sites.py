"""Second pass (run after fix-footprints.py), statewide:
1. Every site's grounds (campuses, schools, parks, club yards/lots, port, airports,
   marinas, hospitals, venues...) becomes a superblock: local streets underneath
   are trimmed.
2. No road runs under a building: any building still crossed by a road (other
   than a tunnel or bridge) is nudged off it, shrunk a little if it must be.
3. Directions: local/access edges of the routing network that cross a site or
   building are removed, so routes go around instead of through.
Usage: python3 fix-sites.py map/data.js
"""
import json, math, re, sys, base64, array
from shapely.geometry import Polygon, LineString, Point
from shapely.strtree import STRtree
from shapely.ops import unary_union
from shapely import affinity

path = sys.argv[1]
raw = open(path).read(); end = raw.rindex('}') + 1
M = json.loads(raw[8:end])

def ispt(p): return isinstance(p, list) and len(p) == 2 and all(isinstance(t, (int, float)) for t in p)
def ispoly(o): return isinstance(o, list) and len(o) >= 3 and all(ispt(p) for p in o)
def P(o):
    try:
        g = Polygon(o); return g if g.is_valid and g.area > 0 else g.buffer(0)
    except Exception: return None
def ellipse(c, rx, ry, ang):
    return affinity.rotate(affinity.scale(Point(c).buffer(1, 24), rx, ry), ang, origin=tuple(c))

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

# ---------- 1. grounds: collect site polygons ----------
grounds = []
def g_add(o):
    if ispoly(o):
        g = P(o)
        if g is not None and not g.is_empty: grounds.append(g)
for c in M['campuses']: g_add(c['outline'])
for s in M['schools']: g_add(s['poly'])
for m in M.get('med', []): g_add(m['outline']); g_add(m.get('garage'))
for f in M.get('clubfac', []): g_add(f.get('yard')); g_add(f.get('lot')); g_add(f.get('house'))
for k in ('area', 'yard', 'wharf'): g_add(M.get('port', {}).get(k))
for k in ('grounds', 'apron', 'term', 'ga'): g_add(M.get('mck', {}).get(k))
mar = M.get('marina', {})
for k in ('yard', 'office'): g_add(mar.get(k))
for o in (mar.get('lot') or []): g_add(o)
for k in ('outline', 'parking'): g_add(M.get('pav_grounds', {}).get(k))
for p in M.get('pavilions', []): g_add(p.get('yard'))
for v in M.get('venues', []):
    grounds.append(ellipse(v['c'], v.get('rx', v.get('r', .5)), v.get('ry', v.get('r', .5)), v.get('ang', 0)))
for e in M['extras']:
    if e.get('kind') in ('label', 'marina', 'airstrip'): continue
    g_add(e.get('foot')); g_add(e.get('yard'))
BUSL = []
for grp in ('bus', 'rapid'):
    for ln in M.get('transit', {}).get(grp, []):
        if isinstance(ln, dict) and len(ln.get('path') or []) > 1: BUSL.append(LineString(ln['path']))
BUSBUF = unary_union([l.buffer(0.07) for l in BUSL]) if BUSL else None
CUT = unary_union([g.buffer(0.01) for g in grounds])
if BUSBUF is not None: CUT = CUT.difference(BUSBUF)  # streets with bus routes stay (campus roads)
CT = STRtree(list(getattr(CUT, 'geoms', [CUT])))

trimmed = 0
for t in M['street_tiles']:
    for key in ('d', 'c'):
        if not t.get(key): continue
        new = []; changed = False
        for l in parse_d(t[key]):
            L = LineString(l)
            if not CT.query(L, predicate='intersects').size: new.append(l); continue
            gdiff = L.difference(CUT)
            if gdiff.equals(L): new.append(l); continue
            changed = True; trimmed += 1
            for p in ([gdiff] if isinstance(gdiff, LineString) else list(getattr(gdiff, 'geoms', []))):
                if isinstance(p, LineString) and p.length > 0.05: new.append([(round(x, 3), round(y, 3)) for x, y in p.coords])
        if changed: t[key] = ' '.join('M' + ' L'.join(f'{x:g},{y:g}' for x, y in l) for l in new if len(l) > 1)
n0 = len(M['street_labels'])
M['street_labels'] = [lb for lb in M['street_labels'] if not CT.query(Point(lb[0], lb[1]), predicate='intersects').size]
print('street pieces trimmed under sites:', trimmed, '| street labels removed:', n0 - len(M['street_labels']))

# ---------- 2. buildings off roads ----------
segs = []
for t in M['street_tiles']:
    for key in ('d', 'c'):
        for l in parse_d(t.get(key) or ''):
            for a, b in zip(l, l[1:]):
                if a != b: segs.append(LineString([a, b]))
tun = [LineString(x['p']).buffer(0.25) for x in (M.get('tunnels') or []) if len(x.get('p', [])) > 1]
tun += [LineString(b).buffer(0.25) for b in (M.get('bridges') or []) if isinstance(b, list) and len(b) > 1 and ispt(b[0])]
TUN = unary_union(tun) if tun else None
for k in ('majors_land', 'arts_land'):
    for a in M[k]:
        if len(a['p']) > 1:
            L = LineString(a['p'])
            if TUN is not None: L = L.difference(TUN)
            for p in ([L] if isinstance(L, LineString) else list(getattr(L, 'geoms', []))):
                if isinstance(p, LineString) and p.length > 0: segs.append(p)
for r in M.get('roads', []):
    p = r.get('p')
    if isinstance(p, list) and len(p) > 1 and ispt(p[0]):
        L = LineString(p)
        if TUN is not None: L = L.difference(TUN)
        for q in ([L] if isinstance(L, LineString) else list(getattr(L, 'geoms', []))):
            if isinstance(q, LineString) and q.length > 0: segs.append(q)
TR = STRtree(segs)
def on_road(g): return TR.query(g.buffer(-0.01), predicate='intersects').size > 0

# (container, key) pairs holding one building polygon, or a list of them
bkeys = []
for c in M['campuses']:
    for i in range(len(c.get('bldg') or [])): bkeys.append((c['bldg'], i))
    for i in range(len(c.get('fields') or [])): bkeys.append((c['fields'], i))
for s in M['schools']:
    for i in range(len(s.get('bld') or [])): bkeys.append((s['bld'], i))
    if s.get('field'): bkeys.append((s, 'field'))
for m in M.get('med', []):
    for i in range(len(m.get('bldg') or [])): bkeys.append((m['bldg'], i))
    if m.get('garage'): bkeys.append((m, 'garage'))
for f in M.get('clubfac', []):
    if f.get('house'): bkeys.append((f, 'house'))
for i in range(len(M.get('port', {}).get('wh') or [])): bkeys.append((M['port']['wh'], i))
for p in M.get('pavilions', []):
    B = p.get('bldg') or []
    if B and ispt(B[0]): bkeys.append((p, 'bldg'))
    else:
        for i in range(len(B)): bkeys.append((B, i))
for i in range(len(M.get('mck', {}).get('hangars') or [])): bkeys.append((M['mck']['hangars'], i))
for k in ('term', 'ga'):
    if M.get('mck', {}).get(k): bkeys.append((M['mck'], k))
for e in M['extras']:
    for i, b in enumerate(e.get('bldgs') or []):
        if ispoly(b): bkeys.append((e['bldgs'], i))
        elif isinstance(b, list):
            for j in range(len(b)):
                if ispoly(b[j]): bkeys.append((b, j))

allb = [P(o[k]) for o, k in bkeys]
BT = STRtree([g for g in allb if g is not None])
moved = shrunk = stuck = 0
for idx, (o, k) in enumerate(bkeys):
    pts = o[k]; g = allb[idx]
    if g is None or not on_road(g): continue
    c = (g.centroid.x, g.centroid.y)
    (x1, y1), (x2, y2) = pts[0], pts[1]; a = math.atan2(y2 - y1, x2 - x1)
    ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    best = None
    near = [n for n in range(len(allb)) if n != idx and allb[n] is not None and allb[n].distance(g) < 0.7]
    for s in (1.0, 0.85, 0.7):
        gs = affinity.scale(g, s, s, origin=c)
        cand = sorted(((i * i + j * j), i, j) for i in range(-25, 26) for j in range(-25, 26))
        for d2, i, j in cand:
            if d2 > 625: break
            dx = (i * ux + j * vx) * 0.02; dy = (i * uy + j * vy) * 0.02
            q = affinity.translate(gs, dx, dy)
            if on_road(q): continue
            qb = q.buffer(-0.01)
            if any(qb.intersects(allb[n]) for n in near): continue
            best = (dx, dy, s); break
        if best: break
    if not best: stuck += 1; continue
    dx, dy, s = best
    o[k] = [[round(c[0] + (x - c[0]) * s + dx, 3), round(c[1] + (y - c[1]) * s + dy, 3)] for x, y in pts]
    allb[idx] = P(o[k]); moved += 1; shrunk += s < 1
print('buildings moved off roads:', moved, '(shrunk', shrunk, ') | could not move:', stuck)

# ---------- 3. directions: drop local edges through sites/buildings ----------
R = M['routing']
def dec(s, code): a = array.array(code); a.frombytes(base64.b64decode(s)); return a
def enc(a): return base64.b64encode(a.tobytes()).decode()
NB = dec(R['nodes'], 'H'); ecode = 'H' if R.get('w16') else 'I'
EU, EV = dec(R['eu'], ecode), dec(R['ev'], ecode); EC = array.array('B', base64.b64decode(R['ec'])); EN = dec(R['en'], 'H')
CLS = R['cls']; soft = {CLS.index(c) for c in ('local', 'access') if c in CLS}
BLD = unary_union([g for g in allb if g is not None]) if allb else None
BAN = unary_union([g.buffer(-0.04) for g in grounds] + ([BLD.buffer(-0.01)] if BLD is not None else []))
BANT = STRtree(list(getattr(BAN, 'geoms', [BAN])))
node = lambda i: (NB[2 * i] / 20, NB[2 * i + 1] / 20)
keep = []; dropped = 0
for i in range(R['m']):
    if EC[i] in soft:
        pts = [node(EU[i])] + [tuple(p) for p in R['geoms'].get(str(i), [])] + [node(EV[i])]
        L = LineString(pts) if len(set(pts)) > 1 else Point(pts[0])
        if BANT.query(L, predicate='intersects').size and L.intersects(BAN) and not (BUSBUF is not None and BUSBUF.contains(L)): dropped += 1; continue
    keep.append(i)
remap = {o: n for n, o in enumerate(keep)}
R['eu'] = enc(array.array(ecode, (EU[i] for i in keep))); R['ev'] = enc(array.array(ecode, (EV[i] for i in keep)))
R['ec'] = base64.b64encode(bytes(EC[i] for i in keep)).decode(); R['en'] = enc(array.array('H', (EN[i] for i in keep)))
R['geoms'] = {str(remap[int(k)]): v for k, v in R['geoms'].items() if int(k) in remap}
R['oneway'] = [[remap[k], d] for k, d in (R.get('oneway') or []) if k in remap]
R['m'] = len(keep)
print('direction edges removed through sites:', dropped, 'of', len(EU))

open(path, 'w').write('const M=' + json.dumps(M, ensure_ascii=False, separators=(',', ':')) + raw[end:])
