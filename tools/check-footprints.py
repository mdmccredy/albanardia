import json,re,sys,math
from shapely.geometry import Polygon,LineString,Point
from shapely.strtree import STRtree
from shapely import affinity
def load(p):
    s=open(p).read();return json.loads(s[8:s.rindex('}')+1])
def parse_d(d):
    out=[];cur=[]
    for m in re.finditer(r'([ML])\s*(-?[\d.]+)[ ,](-?[\d.]+)',d):
        p=(float(m.group(2)),float(m.group(3)))
        if m.group(1)=='M':
            if len(cur)>1: out.append(cur)
            cur=[p]
        else: cur.append(p)
    if len(cur)>1: out.append(cur)
    return out
for fn in sys.argv[1:]:
    M=load(fn);segs=[]
    for t in M['street_tiles']:
        for k in ('d','c'):
            for l in parse_d(t.get(k) or ''):
                for a,b in zip(l,l[1:]):
                    if a!=b: segs.append(LineString([a,b]))
    for k in ('majors_land','arts_land'):
        for a in M[k]:
            if len(a['p'])>1: segs.append(LineString(a['p']))
    T=STRtree(segs)
    fps=[]
    for c in M['campuses']: fps.append(('campus',c['name'],Polygon(c['outline'])))
    for s in M['schools']: fps.append(('school',s['n'],Polygon(s['poly'])))
    for m in M['med']: fps.append(('med',m['name'],Polygon(m['outline'])))
    for e in M['extras']:
        if e['kind'] in {'bldg','office','museum','urbcorp','school','warehouse','corp','hub','stadium','arena'} and len(e.get('foot') or [])>=3: fps.append(('extra',e['n'],Polygon(e['foot'])))
    B=M['brands']
    for q in M['chains']:
        b=B[q[0]];w,h=b[4],b[5];x,y=q[1],q[2]
        fps.append(('shop',b[0],affinity.rotate(Polygon([(x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2),(x-w/2,y+h/2)]),q[3],origin=(x,y))))
    street=[f for f in fps if T.query(f[2].buffer(-0.015),predicate='intersects').size]
    PT=STRtree([f[2] for f in fps]);ov=set()
    for i,f in enumerate(fps):
        for j in PT.query(f[2].buffer(-0.015),predicate='intersects'):
            if j>i and not (f[0]=='campus' or fps[j][0]=='campus'): ov.add((i,j))
    import collections
    print([ (x[0],x[1]) for x in street if x[0]!='shop'])
    print(fn.split('/')[-2], 'on streets:',collections.Counter(x[0] for x in street),' overlaps:',len(ov),[ (fps[i][1],fps[j][1]) for i,j in list(ov)[:6]])
