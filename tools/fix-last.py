"""Third pass (after fix-footprints.py and fix-sites.py): port warehouses off the
roads through the port, and chain stores off any street, road or footprint.
Usage: python3 fix-last.py map/data.js
"""
import json, re, math, sys
from shapely.geometry import Polygon, LineString
from shapely.strtree import STRtree
from shapely import affinity

path = sys.argv[1]; s = open(path).read(); end = s.rindex('}') + 1; M = json.loads(s[8:end])
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
segs = []
for t in M['street_tiles']:
    for k in ('d', 'c'):
        for l in parse_d(t.get(k) or ''):
            for a, b in zip(l, l[1:]):
                if a != b: segs.append(LineString([a, b]))
roads = [LineString(a['p']) for k in ('majors_land', 'arts_land') for a in M[k] if len(a['p']) > 1]
roads += [LineString(r['p']) for r in M.get('roads', []) if isinstance(r.get('p'), list) and len(r['p']) > 1 and isinstance(r['p'][0], list)]
T = STRtree(segs + roads)

# port warehouses
port = M.get('port') or {}
if port.get('area') and port.get('wh'):
    area = Polygon(port['area']); WH = port['wh']
    blocks = [Polygon(b) for b in (port.get('blocks') or []) if isinstance(b, list) and len(b) >= 3 and isinstance(b[0], list)]
    for i, w in enumerate(WH):
        g = Polygon(w)
        if not T.query(g.buffer(-0.01), predicate='intersects').size: continue
        others = [Polygon(x) for j, x in enumerate(WH) if j != i] + blocks
        best = None
        for sc in (1.0, 0.85, 0.7, 0.55):
            gs = affinity.scale(g, sc, sc)
            for d2, a, b in sorted((a * a + b * b, a, b) for a in range(-50, 51) for b in range(-50, 51)):
                q = affinity.translate(gs, a * 0.05, b * 0.05)
                if not area.buffer(0.01).contains(q): continue
                if T.query(q.buffer(-0.01), predicate='intersects').size: continue
                if any(q.buffer(-0.01).intersects(o) for o in others): continue
                best = (a * 0.05, b * 0.05, sc); break
            if best: break
        if best:
            c = g.centroid; dx, dy, sc = best
            WH[i] = [[round(c.x + (x - c.x) * sc + dx, 3), round(c.y + (y - c.y) * sc + dy, 3)] for x, y in w]
            print('warehouse', i, 'moved')

# schools still crossed by a street that has to stay (bus routes): slide them clear
def xpt(p, c, dx, dy, sc): return [round(c[0] + (p[0] - c[0]) * sc + dx, 3), round(c[1] + (p[1] - c[1]) * sc + dy, 3)]
def xall(v, c, dx, dy, sc):
    if isinstance(v, list) and len(v) == 2 and all(isinstance(t, (int, float)) for t in v): return xpt(v, c, dx, dy, sc)
    if isinstance(v, list): return [xall(t, c, dx, dy, sc) for t in v]
    if isinstance(v, dict): return {k: (round(t * sc, 3) if k in ('rx', 'ry', 'r') and isinstance(t, (int, float)) else xall(t, c, dx, dy, sc)) for k, t in v.items()}
    return v
allfp = [Polygon(c['outline']) for c in M['campuses']] + [Polygon(x['poly']) for x in M['schools']]
for si, sc_ in enumerate(M['schools']):
    g = Polygon(sc_['poly'])
    if not T.query(g.buffer(-0.015), predicate='intersects').size: continue
    c = (g.centroid.x, g.centroid.y); (x1, y1), (x2, y2) = sc_['poly'][0], sc_['poly'][1]
    a = math.atan2(y2 - y1, x2 - x1); ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    others = [o for j, o in enumerate(allfp) if j != len(M['campuses']) + si and o.distance(g) < 3]
    best = None
    for sc in (1.0, 0.85, 0.7, 0.6):
        gs = affinity.scale(g, sc, sc, origin=c)
        for d2, i, j in sorted((i * i + j * j, i, j) for i in range(-50, 51) for j in range(-50, 51)):
            if d2 > 2500: break
            dx = (i * ux + j * vx) * 0.05; dy = (i * uy + j * vy) * 0.05; q = affinity.translate(gs, dx, dy).buffer(-0.015)
            if T.query(q, predicate='intersects').size or any(q.intersects(o) for o in others): continue
            best = (dx, dy, sc); break
        if best: break
    if not best: print('school stuck:', sc_['n']); continue
    for k in ('poly', 'bld', 'field', 'track', 'play', 'c'):
        if sc_.get(k) is not None: sc_[k] = xall(sc_[k], c, *best)
    allfp[len(M['campuses']) + si] = Polygon(sc_['poly']); print('school moved:', sc_['n'], [round(v, 2) for v in best])

# chain stores
fp = [Polygon(x['poly']) for x in M['schools']] + [Polygon(c['outline']) for c in M['campuses']]
fp += [Polygon(e['foot']) for e in M['extras'] if len(e.get('foot') or []) >= 3 and e['kind'] != 'label']
B = M['brands']
def rect(q):
    b = B[q[0]]; w, h = b[4], b[5]; x, y = q[1], q[2]
    return affinity.rotate(Polygon([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)]), q[3], origin=(x, y))
shops = [rect(q) for q in M['chains']]; fixed = 0
for i, q in enumerate(M['chains']):
    g = shops[i]
    others = [o for j, o in enumerate(shops) if j != i and o.distance(g) < 2] + [o for o in fp if o.distance(g) < 2]
    bad = lambda r: T.query(r.buffer(-0.01), predicate='intersects').size or any(r.buffer(-0.01).intersects(o) for o in others)
    if not bad(g): continue
    a = math.radians(q[3]); ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    for d2, ii, jj in sorted((ii * ii + jj * jj, ii, jj) for ii in range(-40, 41) for jj in range(-40, 41)):
        dx = (ii * ux + jj * vx) * 0.04; dy = (ii * uy + jj * vy) * 0.04; r = affinity.translate(g, dx, dy)
        if not bad(r): q[1] = round(q[1] + dx, 3); q[2] = round(q[2] + dy, 3); shops[i] = r; fixed += 1; break
print('stores moved:', fixed)
open(path, 'w').write('const M=' + json.dumps(M, ensure_ascii=False, separators=(',', ':')) + s[end:])
