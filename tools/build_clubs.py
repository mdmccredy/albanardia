#!/usr/bin/env python3
"""Generate clubs/<slug>/index.html for every Albanardia yacht club and sailing center, plus clubs/index.html.
Burgees come from the map (FLAGS in map/app.js); club facts from the World Bible."""
import html, json, pathlib, re, subprocess
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "clubs"
E = html.escape

import json as _json
_DB = _json.loads((ROOT/"stories/stories.json").read_text())["stories"]
_MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
def latest(site, n=3):
    """Newest stories for a site from the shared database (tools/build_stories.py)."""
    return sorted([x for x in _DB if x["site"] == site], key=lambda x: x["date"], reverse=True)[:n]
def fdate(d): return "%s %d, %s" % (_MON[int(d[5:7]) - 1], int(d[8:]), d[:4])

def flags():
    s = (ROOT / "map/app.js").read_text(encoding="utf-8")
    i = s.index("FLAGS="); j = s.index("{", i); d = 0
    for k in range(j, len(s)):
        if s[k] == "{": d += 1
        elif s[k] == "}":
            d -= 1
            if not d: break
    js = "process.stdout.write(JSON.stringify(" + s[j:k+1] + "))"
    return json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout)

# id, name, short, town, address, website, kind, ayrc
C = [
 ("SBYC","Silverbrooks Yacht Club","SBYC","Silverbrooks","231 NE Belwether St, Silverbrooks, AB 19001","silverbrooksyc.org","yc",True,"At the outer end of Hanson Bay Marina on Silverbrooks' north shore."),
 ("SBCS","Silverbrooks Community Sailing Center","SBCS","Silverbrooks","312 SE Foundland St, Silverbrooks, AB 19002","sbcommunitysailing.org","cs",True,"Public sailing for the whole city, from first sails to racing teams."),
 ("PESC","Pearl's End Sailing Center","PESC","Silverbrooks","17 W Harborshore Dr, Silverbrooks, AB 19003","pearlsendsailing.org","cs",True,"On the oyster-boat waterfront at Pearl's End."),
 ("NEYC","Northeastern Yacht Club","NEYC","Rutherford","123 Krugen Blvd, Rutherford, AB 19110","neyc.org","yc",True,"Rutherford's big-boat and junior racing club."),
 ("CYC","Corinthian Yacht Club of Silverbrooks","CYC","Whilliker","731 N Olweicz St, Whilliker, AB 19120","cycsb.org","yc",True,"A racing club on the north shore of the bay, home of a strong junior team."),
 ("WYC-W","Waterloo Yacht Club","WYC","Waterloo","182 Anderssen St, Waterloo, AB 19201","waterlooyc.org","yc",True,"River and bay sailing in Rochester County."),
 ("FYC","Foxford Yacht Club","FYC","Foxford","865 Richards Rd, Foxford, AB 19301","fyc.org","yc",True,"Sound sailing a short walk from the Larssen boat works."),
 ("HIS","Hamilton Island Sailing","HIS","Hamilton Island","12 Wilson St, Hamilton Island, AB 19350","sailhamilton.org","cs",True,"A community sailing club on the island, reached by ferry."),
 ("ACYC","Albanardia City Yacht Club","ACYC","Albanardia City","17 W Marlow St, Albanardia City, AB 19401","acyc.org","yc",True,"The state's second city's home club."),
 ("NBYC","New Brolin Yacht Club","NBYC","New Brolin","28 S Atlantic Dr, New Brolin, AB 19601","nbyc.org","yc",True,"Ocean-side sailing near the Olympic Sailing Pavilion."),
 ("WYC-Wil","Willamette Boating Center","WBC","Willamette","419 Ashton Rd, Willamette, AB 19701","wboating.org","cs",True,"Boating and sailing lessons for Coven County."),
 ("CCS","Coven Community Sailing","CCS","Coven","10 Appleton Dr, Coven, AB 19750","covencommsail.org","cs",True,"Community sailing on Coven Bay, next to the Maritime Academy."),
 ("CSYC","Cape Sturgeon Yacht Club","CSYC","Arlington","117 Cape Rd, Arlington, AB 19901","csyc.org","yc",True,"Open-water sailing at the tip of Cape Sturgeon."),
 ("BWYC","Belwether Yacht Club","BWYC","Belwether","Beside the Alex Bennett Marina, Belwether, AB 19540","belwetheryc.org","yc",False,"The college town's club, beside the Alex Bennett Marina."),
 ("EYC","Everett Yacht Club","EYC","Silverbrooks","350 Garfield Ct, Silverbrooks, AB 19006","everettyc.org","yc",False,"A neighborhood club in Silverbrooks."),
 ("EBYC","Elliott Bay Yacht Club","EBYC","Marisfield","178 10th St, Marisfield, AB 19105","elliottbayyc.org","yc",False,"Marisfield's club on Elliott Bay."),
 ("NSC","Notrhabite Sailing Club","NSC","Silverbrooks","20 Riverfront Ln, Silverbrooks, AB 19005","notrhabite.org","yc",False,"A river sailing club on the Wellington."),
 ("SYC","Sjagette Yacht Club","SYC","Silverbrooks","1 Farsgod Point Rd, Silverbrooks, AB 19009","sjagetteyc.org","yc",False,"On Farsgod Point at the harbor mouth."),
 ("NMYC","Northmark Yacht Club","NMYC","Victoria","On the river, Victoria, AB 19260","northmarkyc.org","yc",False,"Farm-country river sailing in Northmark County."),
 ("STYC","Stepford Yacht Club","STYC","Stepford","Stepford, AB 19280","stepfordyc.org","yc",False,"Archila County's yacht club."),
 ("ACSC","Archila Community Sailing Center","ACSC","Stepford","Stepford, AB 19280","archilasailing.org","cs",False,"Public sailing for Archila County."),
 ("MYC","Marianoe Yacht Club","MYC","Marianoe","Marianoe, AB 19320","marianoeyc.org","yc",False,"A small island-town club on the Sound."),
]
AYRC = "ILCA, C420, Optimist, CFJ, RS Feva, 29er"

def color(svg):
    cs = [c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", svg) if c.lower() not in ("#ffffff", "#fff")]
    return cs[0] if cs else "#123a6b"


# ===================== club websites =====================
# Each club is its own multi-page website at /<code>/ (sbyc/, cyc/, ...). Yacht clubs and sailing
# centers have different designs and pages. Old /clubs/<slug>/ addresses redirect to the new ones.
import datetime, sys
sys.path.insert(0, str(ROOT / "tools"))
from club_data import FLEETS, EVENTS, KEELBOAT, JUNIOR, AYRC as AYRC_STOPS, AYRC_CLASSES
JR_ONLY = {"Optimist", "C420", "Club FJ", "29er", "RS Feva"}
DINGHY = {"Optimist", "C420", "Club FJ", "29er", "ILCA", "RS Aero", "RS Feva", "Snipe", "Tasar", "International 14", "505", "Melges 15", "Bauer", "JR300", "JR400", "JR500", "SK400", "SK500",
          "Larssen Club Radial", "Larssen Fyra", "Larssen Pulse XL", "Hobie Wave", "Larssen Voyage"}
CLASSDESC = {
 "J/70": "The world's most popular sportboat, raced by four.", "J/105": "A 34-foot keelboat with an asymmetric kite, raced by five.", "J/80": "A 26-foot sportboat for four.",
 "J/22": "A tough 22-foot keelboat for three, the classic club and match-racing boat.", "J/24": "The classic 24-foot one-design for five.", "Etchells": "A 30-foot three-person keelboat with a deep fleet of serious racers.",
 "Star": "The classic two-person keelboat, Olympic from 1932 to 2012.", "Melges 24": "A 24-foot sportboat for five with a big asymmetric kite.", "Melges 19": "A new 19-foot sportboat for two or three.",
 "Melges 15": "A new doublehanded dinghy for all ages.", "Farr 30": "A 30-foot grand-prix keelboat raced by seven.", "Santa Cruz 27": "The classic ultralight downwind sled for four or five.",
 "Snipe": "Serious sailing, serious fun: a 15-foot doublehander raced around the world.", "Tasar": "A 15-foot doublehander built for couples and mixed crews.", "International 14": "The original development skiff, with twin trapezes.",
 "505": "A 16-foot trapeze dinghy, one of the fastest two-person boats around.", "ILCA": "The Olympic singlehander, in 4, 6 and 7 rigs.", "RS Aero": "A light, modern singlehander in 5, 6, 7 and 9 rigs.",
 "MC7": "McCredy Yachts' 7-meter club keelboat, like a J/22: classic sailing for all programs.", "MC23": "McCredy Yachts' sportboat, like a J/70.", "MC24": "McCredy Yachts' 24-footer, like a J/24 or Moore 24: a new type of classic racing.",
 "MC30": "McCredy Yachts' 30-foot keelboat, like a J/105.", "MC35": "McCredy Yachts' flagship big boat for full crews.",
 "Bauer": "Larssen's light singlehander in four rigs, built in Foxford.", "JR300": "Larssen's gennaker dinghy with one trapeze.", "JR400": "Larssen's doublehander with a gennaker and no trapeze.",
 "JR500": "Larssen's take on the 470: traditional racing brought into the 21st century.", "SK400": "Larssen's premier skiff, like a 49er.", "SK500": "Larssen's triplehanded skiff, like an 18-footer.",
 "Optimist": "The first racing boat for most junior sailors.", "C420": "The doublehanded trainer for high school and youth racing.", "Club FJ": "The high school and college team-racing boat.", "29er": "The youth skiff, with a trapeze and a big gennaker.",
 "Larssen Club Radial": "Larssen's simple doublehander for classes and teams.", "Larssen Fyra": "Larssen's youth singlehander for learners and racers.", "Larssen Pulse XL": "A stable trainer for two to four.",
 "SailQube": "A tough, simple trainer that's almost impossible to break. Perfect for first sails.", "Hobie 16": "The classic beach catamaran, fast and wet for teens and coaches.",
 "Larssen Voyage": "Larssen's family explorer.", "Hobie Wave": "An easy, boomless beach catamaran.", "Kayaks and SUPs": "Paddle craft for members.",
}
TAGC = {"Weeknight": "#2f6f9f", "Frostbite": "#4f7a99", "Regatta": None, "Championship": "#b8860b", "Youth": "#2e8b57", "Social": "#8b4c7a", "Cruising": "#2a7d7a", "Clinic": "#6a6a2a", "Club": "#5a6470", "AYRC": "#c4552f"}
MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def code(c): return c[2].lower()
def old_slug(c): return c[2].lower() if c[0] not in ("WYC-W", "WYC-Wil") else ("waterloo-yc" if c[0] == "WYC-W" else "willamette-bc")
slug = old_slug  # site keys in stories/stories.json stay "club:<old slug>"
def juniors(c): return c[6] == "yc" and c[0] not in KEELBOAT
def ayrc_stop(c): return next((a for a in AYRC_STOPS if a[1] == c[0]), None)

def events(c):
    ev = []
    for m, d, t, p, g in EVENTS[c[0]]:
        ev.append((datetime.date(2027, MON.index(m) + 1, int(d)), t, p, g))
    a = ayrc_stop(c)
    if a:
        x = datetime.date.fromisoformat(a[0])
        ev.append((x, "AYRC: " + a[3], f"Albanardia Youth Racing Circuit, two days of junior racing. {a[4]}", "AYRC"))
    return sorted(ev)

def chips(lst):
    return "".join(f'<span>{E(k)}{f" <b>{n}</b>" if n else ""}</span>' for k, n in lst)
def adult_fleets(c): return [(k, n) for k, n in FLEETS[c[0]] if k not in JR_ONLY or c[6] != "yc"]
def fleet_chips(c): return chips(adult_fleets(c))

def evrow(x, t, p, g):
    col = TAGC.get(g) or "var(--c)"
    return f'<div class="ev"><div class="dt"><b>{x.day}</b><span>{MON[x.month-1]} {x.year}</span></div><div><h3>{E(t)}</h3><p>{E(p)}</p></div><span class="tag" style="background:{col}">{E(g)}</span></div>'

# ---------- shared shell ----------
FONTS_YC = '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">'
FONTS_CS = '<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">'
CSS_BASE = """
:root{--c:@C;--ink:#14202c;--mut:#5c6672;--line:#e3e1da;--bg:#faf8f4;--card:#fff;--navy:#0f2340}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--ink:#eef1f4;--mut:#9ca6b2;--line:#2a323d;--bg:#0f141a;--card:#171e27}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--f,system-ui),sans-serif}a{color:inherit}img,svg{max-width:100%}
.in{max-width:1120px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left))}
.tb{background:var(--navy);color:#cdd6e2;font-size:13px;padding-top:env(safe-area-inset-top)}.tb .in{display:flex;gap:16px;min-height:34px;align-items:center;white-space:nowrap;overflow-x:auto}.tb a{text-decoration:none}.tb .sp{flex:1}
header{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10}header .in{display:flex;align-items:center;gap:14px;min-height:70px}
.bg{width:58px;height:35px;flex:none;filter:drop-shadow(0 1px 1px rgba(0,0,0,.2))}.bg svg{width:100%;height:100%}
.nm{text-decoration:none}.nm b{display:block;line-height:1.15}.nm small{color:var(--mut);font-size:12px;letter-spacing:1.5px;text-transform:uppercase}
nav.mn{margin-left:auto;display:flex;gap:2px}nav.mn a{text-decoration:none;font-weight:600;padding:9px 11px;border-radius:8px;font-size:15px;white-space:nowrap}nav.mn a:hover,nav.mn a.on{background:rgba(0,0,0,.06)}
.sub2{display:none;overflow-x:auto;gap:6px;padding:8px 16px;border-top:1px solid var(--line);background:var(--card)}.sub2 a{text-decoration:none;font-weight:700;font-size:14px;padding:6px 12px;border-radius:999px;border:1px solid var(--line);white-space:nowrap}.sub2 a.on{background:var(--c);color:#fff;border-color:var(--c)}
section{padding:52px 0}section.alt{background:var(--card);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.sub{color:var(--mut);margin:0 0 22px;max-width:62ch}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.g2{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.cd{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px;text-decoration:none;display:block}.cd b{display:block;font-size:18px;margin-bottom:4px}.cd span,.cd p{color:var(--mut);margin:0}
.cal{display:grid;gap:10px}.ev{display:grid;grid-template-columns:76px 1fr auto;gap:14px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px}
.dt{background:var(--navy);color:#fff;border-radius:10px;text-align:center;padding:6px 0;line-height:1.1}.dt b{display:block;font-size:24px}.dt span{font-size:11px;letter-spacing:1px;text-transform:uppercase}
.ev h3{margin:0;font-size:17px}.ev p{margin:2px 0 0;color:var(--mut);font-size:14px}.tag{font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px;color:#fff;white-space:nowrap}
.ch{display:flex;flex-wrap:wrap;gap:8px}.ch span{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:6px 12px;font-weight:600;font-size:14px}.ch span b{color:var(--c);margin-left:4px}
.fl{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}.fl div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;border-left:4px solid var(--c)}.fl b{font-size:18px}.fl small{display:block;color:var(--c);font-weight:700}.fl p{margin:4px 0 0;color:var(--mut);font-size:14.5px}
table.t{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}table.t td,table.t th{padding:10px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}table.t th{font-size:13px;text-transform:uppercase;letter-spacing:.6px;color:var(--mut)}
.ct{display:grid;grid-template-columns:1fr 1fr;gap:24px}.ct>div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px}
.ph{padding:44px 0 34px;background:var(--navy);color:#fff}.ph .k{color:#aebbd0}.ph p{color:#d7dee8;max-width:62ch;margin:8px 0 0;font-size:17px}
.k{font-size:12.5px;letter-spacing:2.5px;text-transform:uppercase}
.btn{display:inline-block;background:var(--c);color:#fff;font-weight:700;text-decoration:none;padding:12px 20px;border-radius:999px;margin:0 8px 8px 0}.btn.w{background:#fff;color:var(--navy)}.btn.o{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.6)}
.hi{background:color-mix(in srgb,var(--c) 10%,var(--card));border:1px solid color-mix(in srgb,var(--c) 40%,var(--line))}
footer{background:var(--navy);color:#c3ccd8;padding:36px 0 calc(90px + env(safe-area-inset-bottom))}footer .in{display:flex;gap:16px;align-items:center;flex-wrap:wrap}footer a{text-decoration:none}footer .sp{flex:1}
@media (max-width:900px){nav.mn{display:none}.sub2{display:flex}.g3,.g2,.ct{grid-template-columns:1fr}.ev{grid-template-columns:64px 1fr}.ev .tag{grid-column:2;justify-self:start}}
"""
CSS_YC = """
body{--f:"Source Sans 3"}h1,h2,.nm b{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600}.nm b{font-size:20px;font-weight:700}
h2{font-size:clamp(30px,3.8vw,42px);line-height:1.1;margin:0 0 6px}.ph h1{font-size:clamp(38px,5vw,56px);line-height:1.05;margin:6px 0 0}
.hero{background:var(--navy);color:#fff;position:relative;overflow:hidden}.hero::after{content:"";position:absolute;inset:auto 0 0 0;height:8px;background:var(--c)}
.hero .in{display:grid;grid-template-columns:1.2fr 1fr;gap:30px;align-items:center;padding-top:56px;padding-bottom:60px}
.hero h1{font-size:clamp(40px,5.6vw,66px);line-height:1.02;margin:8px 0 12px}.hero p{font-size:18px;color:#d7dee8;max-width:46ch;margin:0 0 22px}.hero .k{color:#aebbd0}
.flag{justify-self:center;width:min(380px,80vw);filter:drop-shadow(0 18px 30px rgba(0,0,0,.45));transform:rotate(-4deg)}
.cd{border-top:4px solid var(--c)}.ph{border-bottom:6px solid var(--c)}
@media (max-width:900px){.hero .in{grid-template-columns:1fr}.flag{width:min(240px,64vw)}}
"""
CSS_CS = """
body{--f:Nunito;--navy:#12354f}h1,h2,.nm b{font-family:Nunito,system-ui,sans-serif;font-weight:800;letter-spacing:-.3px}.nm b{font-size:19px}
h2{font-size:clamp(28px,3.6vw,38px);line-height:1.15;margin:0 0 6px}.ph{background:linear-gradient(135deg,var(--c),var(--navy))}.ph h1{font-size:clamp(34px,5vw,52px);line-height:1.08;margin:6px 0 0}
.hero{background:linear-gradient(160deg,var(--c) 0%,var(--navy) 85%);color:#fff;position:relative;overflow:hidden}
.hero .in{display:grid;grid-template-columns:1.3fr .9fr;gap:24px;align-items:center;padding-top:46px;padding-bottom:84px}
.hero h1{font-size:clamp(36px,5.4vw,60px);line-height:1.05;margin:6px 0 12px}.hero p{font-size:19px;color:#eef4f8;max-width:44ch;margin:0 0 20px}.hero .k{color:#d9e7f0}
.hero svg.wave{position:absolute;left:0;right:0;bottom:-1px;width:100%;height:60px}
.flag{justify-self:center;width:min(300px,70vw);background:#fff;border-radius:22px;padding:18px;box-shadow:0 18px 40px rgba(0,0,0,.25)}
.cd,.ev,.fl div,.ct>div{border-radius:18px}.btn{border-radius:14px}.btn.w{color:var(--c)}
.cd .pill,.pill{display:inline-block;background:var(--c);color:#fff;border-radius:999px;padding:3px 10px;font-weight:800;font-size:12.5px;margin-bottom:6px}
@media (max-width:900px){.hero .in{grid-template-columns:1fr}.flag{width:min(220px,60vw)}}
"""

def shell(c, svg, path, title, body, nav):
    depth = path.count("/") + 1 if path else 1
    r = "../" * depth
    me = "../" * (depth - 1) if depth > 1 else "./"
    yc = c[6] == "yc"
    col = color(svg)
    flag = f'<svg viewBox="0 0 631 377" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'
    links = "".join(f'<a href="{me}{p}"{" class=on" if p == path else ""}>{E(t)}</a>'.replace(" class=on", ' class="on"') for p, t in nav)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title + " | " if title else "")}{E(c[1])}</title><meta name="description" content="{E(c[8])}"><link rel="manifest" href="{r}manifest.json"><link rel="apple-touch-icon" href="{r}icons/icon-180.png"><meta name="theme-color" content="{'#0f2340' if yc else '#12354f'}">
{FONTS_YC if yc else FONTS_CS}<style>{(CSS_BASE + (CSS_YC if yc else CSS_CS)).replace('@C', col)}</style></head><body>
<div class="tb"><div class="in"><a href="{r}">Albanardia.gov</a><a href="{r}clubs/">All clubs</a><a href="{r}nesf/">NESF</a><span class="sp"></span>{f'<a href="{r}nesf/ayrc/">AYRC</a>' if c[7] else ''}<a href="{me}#contact">Contact</a></div></div>
<header><div class="in"><span class="bg">{flag}</span><a class="nm" href="{me}"><b>{E(c[1])}</b><small>{E(c[2])} · {E(c[3])}</small></a><nav class="mn">{links}</nav></div><div class="sub2">{links}</div></header>
{body}
<footer><div class="in"><span class="bg">{flag}</span><span>{E(c[1])} · {E(c[4])}</span><span class="sp"></span><a href="{me}stories/">News</a><a href="{r}clubs/">All Albanardia clubs</a><a href="{r}nesf/">NESF</a><a href="{r}">Albanardia.gov</a></div></footer>
<script src="{r}app/app.js" data-home="float"></script></body></html>"""

def news_cards(c, me):
    ns = latest("club:" + old_slug(c), 3)
    return "".join(f'<a class="cd" href="{me}stories/#{n["slug"]}"><small style="color:var(--mut);font-weight:700;text-transform:uppercase;letter-spacing:.6px;font-size:12px">{E(n["cat"])} · Published {fdate(n["date"])}</small><b>{E(n["title"])}</b><span>{E(n["dek"])}</span></a>' for n in ns)

def ph(kick, title, text):
    return f'<div class="ph"><div class="in"><div class="k">{E(kick)}</div><h1>{E(title)}</h1><p>{E(text)}</p></div></div>'

def tier(c):
    boats = sum(n or 0 for _, n in FLEETS[c[0]])
    return 3 if boats >= 150 else 2 if boats >= 80 else 1

# ---------- yacht clubs ----------
def yc_nav(c):
    n = [("", "Home"), ("racing/", "Racing")]
    if juniors(c): n.append(("juniors/", "Juniors"))
    return n + [("calendar/", "Calendar"), ("club/", "The Club"), ("membership/", "Membership"), ("stories/", "News")]

def yc_pages(c, svg):
    flag = f'<svg viewBox="0 0 631 377" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'
    ev = events(c); nav = yc_nav(c); kb = c[0] in KEELBOAT
    adult = [(k, n) for k, n in adult_fleets(c) if n]
    big = sorted(adult, key=lambda x: -x[1])[:3]
    up = ev[:4]
    pages = {}
    # home
    pages[""] = ("", f"""
<div class="hero"><div class="in"><div><div class="k">{'Keelboat club' if kb else 'Yacht club'} · {E(c[3])}, Albanardia</div><h1>{E(c[1])}</h1><p>{E(c[8])} Home to {", ".join(f"{n} {k}s" for k, n in big)}.</p>
<a class="btn w" href="membership/">Become a member</a><a class="btn o" href="racing/">Racing at {E(c[2])}</a></div><div class="flag">{flag}</div></div></div>
<section><div class="in"><div class="g3">
<a class="cd" href="racing/"><b>Racing</b><span>{len(adult)} one-design fleets, {sum(1 for x in ev if x[3] == 'Weeknight')} weeknight series and {sum(1 for x in ev if x[3] in ('Regatta','Championship'))} regattas in 2027.</span></a>
{f'<a class="cd" href="juniors/"><b>Juniors</b><span>Green Fleet to high school and AYRC racing, plus summer camps.</span></a>' if juniors(c) else '<a class="cd" href="club/"><b>Big-boat sailing</b><span>A keelboat club: crew boards, distance races and evenings on the water.</span></a>'}
<a class="cd" href="club/"><b>The Club</b><span>Dining, moorage and {sum(1 for x in ev if x[3] in ('Social','Club','Cruising'))} club events on the calendar.</span></a>
</div></div></section>
<section class="alt"><div class="in"><h2>Coming up</h2><p class="sub">Highlights from the 2027 season. <a href="calendar/">Full calendar →</a></p><div class="cal">{''.join(evrow(*x) for x in up)}</div></div></section>
<section><div class="in"><h2>News</h2><p class="sub">From the club. <a href="stories/">All stories →</a></p><div class="g3">{news_cards(c, '')}</div></div></section>
<section class="alt"><div class="in"><h2>Fleets</h2><p class="sub">Boats racing at {E(c[2])}, with active boats in each fleet.</p><div class="ch">{fleet_chips(c)}</div></div></section>
<section id="contact"><div class="in ct"><div><h2>Visit</h2><p>{E(c[4])}</p><p><a href="../map/">Open in the Albanardia map →</a></p></div><div><h2>Contact</h2><p>{E(c[5])}</p><p>Club office: Tuesday to Sunday, 9 to 5. Dining room hours on <a href="club/">The Club</a> page.</p></div></div></section>""")
    # racing
    series = [x for x in ev if x[3] in ("Weeknight", "Frostbite")]
    regs = [x for x in ev if x[3] in ("Regatta", "Championship", "AYRC")]
    pages["racing/"] = ("Racing", ph("Racing at " + c[2], "Racing", f"{len(adult)} one-design fleets race at {c[1]}. Notices of race and sailing instructions are posted 30 days before each regatta.") + f"""
<section><div class="in"><h2>Fleets</h2><p class="sub">Active boats in each fleet for 2027.</p><div class="fl">{''.join(f'<div><small>{n} boats</small><b>{E(k)}</b><p>{E(CLASSDESC.get(k, ""))}</p></div>' for k, n in adult)}</div></div></section>
<section class="alt"><div class="in"><h2>Series</h2><p class="sub">Weeknight and winter racing. Check in on the race committee channel before the first start.</p><div class="cal">{''.join(evrow(*x) for x in series) or '<p class="sub">No weeknight series this year.</p>'}</div></div></section>
<section><div class="in"><h2>Regattas and championships</h2><div class="cal">{''.join(evrow(*x) for x in regs)}</div></div></section>
<section class="alt"><div class="in g2"><div class="cd"><b>Race committee</b><span>Every member races better after a day on the committee boat. Sign up for one race day a season; training is in April.</span></div><div class="cd"><b>Visiting boats</b><span>Guest moorage and dry storage are free for registered regatta entries. Charter boats can sometimes be arranged through the fleet captains.</span></div></div></section>""")
    # juniors
    if juniors(c):
        jf = [k for k, _ in JUNIOR.get(c[0], [])]
        lv = [("Green Fleet", "Ages 7 to 11 in Optimists. First races on short courses, lots of games and swimming.", "Optimist" in jf),
              ("Opti Race Team", "Ages 9 to 15 racing the full AYRC circuit and regional Opti regattas.", "Optimist" in jf),
              ("High School Team", "Ages 14 to 18 in C420s and Club FJs, with team racing for high school sailors.", "C420" in jf or "Club FJ" in jf),
              ("ILCA Team", "Singlehanded racing in ILCA 4 and 6 rigs for teens moving up from Optis.", "ILCA" in jf),
              ("29er Skiff Squad", "Trapeze and gennaker racing for older juniors on the Olympic pathway.", "29er" in jf),
              ("Larssen Club Radial", "Doublehanded sailing for juniors who want to sail with a friend.", "Larssen Club Radial" in jf),
              ("Learn to Sail", "Ages 6 to 10 in SailQubes, the boat you can't break. Splashing encouraged.", "SailQube" in jf),
              ("Catamaran Week", "Teens in Hobie " + ("16s" if "Hobie 16" in jf else "Waves") + ": speed, flying a hull and beach launches.", "Hobie 16" in jf or "Hobie Wave" in jf)]
        a = ayrc_stop(c)
        stops = "".join(f'<tr{" class=hi" if s[1] == c[0] else ""}><td>{datetime.date.fromisoformat(s[0]).strftime("%b %-d")}–{(datetime.date.fromisoformat(s[0]) + datetime.timedelta(1)).strftime("%-d")}</td><td><b>{E(s[3])}</b><br><small>{E(s[2])}</small></td></tr>' for s in AYRC_STOPS).replace("class=hi", 'class="hi"')
        pages["juniors/"] = ("Juniors", ph("Junior sailing at " + c[2], "Juniors", f"From a first sail in an Optimist to high school and AYRC racing. Junior members sail every day of summer camp and train year-round.") + f"""
<section><div class="in"><h2>Programs</h2><div class="g3">{''.join(f'<div class="cd"><b>{E(t)}</b><span>{E(d)}</span></div>' for t, d, ok in lv if ok)}</div></div></section>
<section class="alt"><div class="in"><h2>Junior boats</h2><p class="sub">Club-owned boats for the junior program. Juniors with their own boats are welcome in every group.</p><div class="fl">{''.join(f'<div><small>{n} boats</small><b>{E(k)}</b><p>{E(CLASSDESC.get(k, ""))}</p></div>' for k, n in JUNIOR.get(c[0], []))}</div></div></section>
<section class="alt"><div class="in g2"><div><h2>Summer camps</h2><p class="sub">Weekly camps from June 21 to August 20, 9 a.m. to 3 p.m. Beginners welcome; every camper swims a short test on the first day.</p>
<table class="t"><tr><th>Camp</th><th>Ages</th><th>Week</th></tr><tr><td>Learn to Sail{' (SailQubes)' if 'SailQube' in jf else ''}</td><td>6 to 10</td><td>$395</td></tr><tr><td>Opti Intermediate</td><td>9 to 13</td><td>$425</td></tr>{'<tr><td>Doublehanded Racing</td><td>12 to 18</td><td>$450</td></tr>' if ('C420' in jf or 'Club FJ' in jf) else ''}{'<tr><td>Skiff Week (29ers)</td><td>13 to 18</td><td>$495</td></tr>' if '29er' in jf else ''}{'<tr><td>Catamaran Week</td><td>12 to 18</td><td>$450</td></tr>' if ('Hobie 16' in jf or 'Hobie Wave' in jf) else ''}{'<tr><td>ILCA Week</td><td>13 to 18</td><td>$425</td></tr>' if 'ILCA' in jf else ''}</table></div>
<div><h2>Year-round training</h2><p class="sub">Spring and fall practices on weekends, winter rules and video nights in the clubhouse{', and frostbite racing for older juniors' if any(x[3] == 'Frostbite' for x in ev) else ''}. Coaches are US Sailing certified, and every practice has a safety boat.</p>
<div class="cd"><b>Scholarships</b><span>No one misses out for money. NESF youth grants and the {E(c[2])} junior fund cover camp, charter boats and travel.</span></div></div></div></section>
<section><div class="in"><h2>AYRC 2027</h2><p class="sub">{E(c[2])} juniors race the Albanardia Youth Racing Circuit, run by the <a href="../nesf/">Northeastern Sailing Foundation</a>.{f" {c[2]} hosts the {a[3]} on " + datetime.date.fromisoformat(a[0]).strftime('%B %-d') + "." if a else ""} <a href="../nesf/ayrc/">Circuit details →</a></p><table class="t"><tr><th>Dates</th><th>Regatta</th></tr>{stops}</table></div></section>""")
    # calendar
    pages["calendar/"] = ("Calendar", ph(c[2] + " · 2027", "Calendar", "Racing, juniors, clinics and club events for the 2027 season.") + f"""
<section><div class="in"><div class="cal">{''.join(evrow(*x) for x in ev)}</div></div></section>""")
    # club
    t = tier(c)
    soc = [x for x in ev if x[3] in ("Social", "Club", "Cruising")]
    fac = [("Dining room and bar", ["Bar Thursday to Sunday, dinner Friday and Saturday.", "Bar and grill Wednesday to Sunday, member dinners on race nights.", "Full dining room and bar, lunch and dinner Tuesday to Sunday."][t-1]),
           ("Moorage", ["About 60 slips and moorings for members.", "About 140 slips and a guest dock.", "Over 300 slips, a guest dock and a fuel dock."][t-1]),
           ("Dry sail and hoist", "Dry storage for trailered keelboats" + ("" if kb else " and a dinghy park") + ", with a member-run hoist."),
           ("Reciprocal privileges", "Members are welcome at the other Albanardia clubs and at hundreds of yacht clubs around the country.")]
    pages["club/"] = ("The Club", ph("The Club", "The Club", f"{c[1]} is a members' club on the water in {c[3]}. " + c[8]) + f"""
<section><div class="in g2">{''.join(f'<div class="cd"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in fac)}</div></section>
<section class="alt"><div class="in"><h2>Club events</h2><p class="sub">Parties, cruises and the work days that keep the club running.</p><div class="cal">{''.join(evrow(*x) for x in soc)}</div></div></section>""")
    # membership
    fee = [(1500, 95), (3500, 160), (8000, 260)][t-1]
    rows = [("Family", f"${fee[0]:,}", f"${fee[1]*2:,}", "Two adults and children under 19.")] + ([("Junior", "None", "$45", "Ages 8 to 18, includes the junior program.")] if juniors(c) else []) + \
           [("Young adult", f"${fee[0]//4:,}", f"${fee[1]:,}", "Ages 19 to 32, full racing privileges."), ("Senior", f"${fee[0]:,}", f"${int(fee[1]*1.6):,}", "Voting member with moorage priority."), ("Crew", "None", "$30", "For sailors who race on members' boats.")]
    pages["membership/"] = ("Membership", ph("Join " + c[2], "Membership", "Members race, cruise and help run the club. Two members sponsor each new application, and the membership committee meets monthly.") + f"""
<section><div class="in"><table class="t"><tr><th>Membership</th><th>Initiation</th><th>Monthly dues</th><th>Who it's for</th></tr>{''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{d}</td><td>{e}</td></tr>' for a, b, d, e in rows)}</table>
<p class="sub" style="margin-top:16px">Not sure? Come to a Wednesday or Thursday night race as crew; the crew board in the clubhouse matches new sailors with boats every week.</p></div></section>""")
    return pages, nav

# ---------- sailing centers ----------
def cs_nav(c):
    return [("", "Home"), ("classes/", "Adult classes"), ("youth/", "Youth"), ("rentals/", "Rentals"), ("calendar/", "Calendar"), ("volunteer/", "Volunteer"), ("stories/", "News")]

def cs_pages(c, svg):
    flag = f'<svg viewBox="0 0 631 377" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'
    ev = events(c); nav = cs_nav(c); fl = FLEETS[c[0]]; names = [k for k, _ in fl]
    keel = [k for k in names if k in ("MC7", "J/22")]
    wave = '<svg class="wave" viewBox="0 0 1440 60" preserveAspectRatio="none"><path d="M0 30 C 240 0 480 60 720 30 S 1200 0 1440 30 V60 H0Z" fill="var(--bg)"/></svg>'
    pages = {}
    pages[""] = ("", f"""
<div class="hero"><div class="in"><div><div class="k">Community sailing · {E(c[3])}</div><h1>{E(c[1])}</h1><p>{E(c[8])} Classes for every age, boats to rent and a crew of volunteers who'll get you on the water.</p>
<a class="btn w" href="classes/">Learn to sail</a><a class="btn o" href="youth/">Kids and teens</a></div><div class="flag">{flag}</div></div>{wave}</div>
<section><div class="in"><div class="g3">
<a class="cd" href="classes/"><span class="pill">Adults</span><b>Learn to sail</b><span>Four-week courses in {E(names[0])}s{(' and ' + keel[0] + ' keelboats') if keel else ''}. No experience needed.</span></a>
<a class="cd" href="youth/"><span class="pill">Ages 7 to 17</span><b>Camps and youth racing</b><span>Summer camps every week, then a racing team for kids who catch the bug.</span></a>
<a class="cd" href="rentals/"><span class="pill">Members</span><b>Rent a boat</b><span>{sum(n or 0 for _, n in fl)} boats on the dock once you've passed a checkout sail.</span></a>
</div></div></section>
<section class="alt"><div class="in"><h2>What's happening</h2><p class="sub"><a href="calendar/">Full 2027 calendar →</a></p><div class="cal">{''.join(evrow(*x) for x in ev[:4])}</div></div></section>
<section><div class="in"><h2>News</h2><p class="sub"><a href="stories/">All stories →</a></p><div class="g3">{news_cards(c, '')}</div></div></section>
<section id="contact" class="alt"><div class="in ct"><div><h2>Find us</h2><p>{E(c[4])}</p><p><a href="../map/">Open in the Albanardia map →</a></p></div><div><h2>Questions?</h2><p>{E(c[5])}</p><p>Front desk: daily 9 to 6 in season, weekends in winter.</p></div></div></section>""")
    adult = [("Learn to Sail 1", f"Four evenings or two weekends in {names[0]}s: rigging, tacking, jibing and getting back to the dock.", "$295"),
             ("Learn to Sail 2", "Sailing in more wind, crew overboard drills and your checkout sail for rentals.", "$275")] + \
            ([(f"Keelboat Basics", f"Two weekends in the {keel[0]}s, toward US Sailing Basic Keelboat certification.", "$395")] if keel else []) + \
            [("Intro to Racing", "Starts, mark roundings and the basic rules, then the Wednesday or Friday fun races.", "$195")]
    pages["classes/"] = ("Adult classes", ph("Adults", "Adult classes", "No experience needed. Classes are small, instructors are US Sailing certified, and life jackets are included.") + f"""
<section><div class="in"><div class="g2">{''.join(f'<div class="cd"><span class="pill">{p}</span><b>{E(t)}</b><span>{E(d)}</span></div>' for t, d, p in adult)}</div></div></section>
<section class="alt"><div class="in"><h2>Dates</h2><div class="cal">{''.join(evrow(*x) for x in ev if x[3] == 'Clinic')}</div></div></section>""")
    a = ayrc_stop(c)
    jb = [k for k, _ in JUNIOR.get(c[0], [])]
    yp = [("Little Sailors", "Ages 6 to 9, half days in " + ("SailQubes" if "SailQube" in jb else "Optis") + " and on the dock: knots, swimming and first sails.", "$245 / week")]
    if "Optimist" in jb: yp.append(("Opti Camp", "Ages 8 to 12 sailing Optimists solo, with games and short races.", "$295 / week"))
    if "C420" in jb or "Club FJ" in jb: yp.append(("Teen Racing", "Ages 13 to 17 in " + ("C420s" if "C420" in jb else "Club FJs") + ", for high school sailors and beginners alike.", "$325 / week"))
    if "Hobie 16" in jb or "Hobie Wave" in jb: yp.append(("Catamaran Camp", "Ages 12 to 17 in Hobie " + ("16s and Waves" if "Hobie 16" in jb else "Waves") + ".", "$345 / week"))
    if "Larssen Fyra" in names: yp.append(("Fyra Camp", "Ages 9 to 13 in Larssen Fyras, sailing solo by the end of the week.", "$325 / week"))
    if "Larssen Club Radial" in names: yp.append(("Teen Doublehanded", "Ages 12 to 17 in Club Radials with a friend.", "$325 / week"))
    if "Larssen Pulse XL" in names or "Hobie Wave" in names: yp.append(("Adventure Week", "Ages 10 to 15, island trips and beach landings in the bigger boats.", "$345 / week"))
    if c[7]: yp.append(("Youth Racing Team", "Ages 10 to 17. Spring and fall practices and the AYRC circuit, with center boats to charter.", "$650 / season"))
    pages["youth/"] = ("Youth", ph("Kids and teens", "Youth sailing", "Summer camps from mid-June to late August, and a racing team for the kids who want more. Scholarships cover anyone who needs one.") + f"""
<section><div class="in"><div class="g3">{''.join(f'<div class="cd"><span class="pill">{p}</span><b>{E(t)}</b><span>{E(d)}</span></div>' for t, d, p in yp)}</div></div></section>
<section class="alt"><div class="in"><h2>Youth boats</h2><div class="fl">{''.join(f'<div><small>{n} boats</small><b>{E(k)}</b><p>{E(CLASSDESC.get(k, ""))}</p></div>' for k, n in JUNIOR.get(c[0], []))}</div></div></section>
<section><div class="in"><h2>Youth dates</h2><div class="cal">{''.join(evrow(*x) for x in ev if x[3] in ('Youth', 'AYRC'))}</div>
{f'<p class="sub" style="margin-top:16px">Our racing team sails the <a href="../nesf/ayrc/">Albanardia Youth Racing Circuit</a>, run by the <a href="../nesf/">Northeastern Sailing Foundation</a>.' + (f' We host the {a[3]} on {datetime.date.fromisoformat(a[0]).strftime("%B %-d")}.' if a else '') + '</p>' if c[7] else ''}</div></section>""")
    pages["rentals/"] = ("Rentals", ph("Members", "Rentals and memberships", "Pass a checkout sail, then take a boat out whenever the dock is open.") + f"""
<section><div class="in"><h2>Our boats</h2><div class="fl">{''.join(f'<div><small>{n if n else ""}{" boats" if n else "On the dock"}</small><b>{E(k)}</b><p>{E(CLASSDESC.get(k, ""))}</p></div>' for k, n in fl)}</div></div></section>
<section class="alt"><div class="in"><table class="t"><tr><th>Membership</th><th>Price</th><th>Includes</th></tr><tr><td><b>Individual</b></td><td>$425 / year</td><td>Unlimited small-boat sailing after checkout</td></tr><tr><td><b>Family</b></td><td>$650 / year</td><td>Two adults and kids, plus member pricing on camps</td></tr>{'<tr><td><b>Keelboat add-on</b></td><td>$200 / year</td><td>' + keel[0] + ' rentals after a keelboat checkout</td></tr>' if keel else ''}<tr><td><b>Day pass</b></td><td>$45</td><td>One day of sailing for checked-out sailors</td></tr></table></div></section>""")
    pages["calendar/"] = ("Calendar", ph(c[2] + " · 2027", "Calendar", "Classes, camps, fun races and the events that bring the waterfront together.") + f"""
<section><div class="in"><div class="cal">{''.join(evrow(*x) for x in ev)}</div></div></section>""")
    pages["volunteer/"] = ("Volunteer", ph("Join the crew", "Volunteer", f"{c[1]} runs on volunteers. No sailing experience needed for most jobs, and volunteers sail free on open days.") + f"""
<section><div class="in"><div class="g3">{''.join(f'<div class="cd"><b>{t}</b><span>{d}</span></div>' for t, d in [("Dock hand", "Help sailors launch and land, and keep the dock tidy."), ("Safety boat driver", "Drive a chase boat during classes. Training and a boating license course provided."), ("Assistant instructor", "Help with camps and classes, a great first step toward US Sailing instructor certification."), ("Front desk", "Welcome visitors, check out boats and answer the phone."), ("Boat maintenance", "Winter work nights fixing boats, sails and trailers."), ("Events", "Open houses, fun races and fundraisers.")])}</div></div></section>
<section class="alt"><div class="in"><div class="cal">{''.join(evrow(*x) for x in ev if x[0].month <= 4 and x[3] in ('Clinic', 'Club'))}</div></div></section>""")
    return pages, nav

def club_site(c, svg):
    pages, nav = (yc_pages if c[6] == "yc" else cs_pages)(c, svg)
    base = ROOT / code(c)
    for path, (title, body) in pages.items():
        out = base / path / "index.html"; out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(shell(c, svg, path, title, body, nav), encoding="utf-8")
    # old address redirects
    old = OUT / old_slug(c)
    for sub in ("", "stories/"):
        d = old / sub; d.mkdir(parents=True, exist_ok=True)
        up = "../" * (2 + sub.count("/"))
        (d / "index.html").write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{E(c[1])}</title><script>location.replace("{up}{code(c)}/{sub}"+location.hash)</script><meta http-equiv="refresh" content="0;url={up}{code(c)}/{sub}"></head><body><a href="{up}{code(c)}/{sub}">{E(c[1])} has moved</a></body></html>', encoding="utf-8")
    return len(pages)

def index(F):
    def card(c): return f'<a class="cl" href="../{code(c)}/"><span class="bg"><svg viewBox="0 0 631 377">{F[c[0]]}</svg></span><span><b>{E(c[1])}</b><small>{E(c[3])} · {"Keelboat club" if c[0] in KEELBOAT else "Yacht club" if c[6] == "yc" else "Sailing center"}{" · AYRC" if c[7] else ""}</small></span></a>'
    yc = "".join(card(c) for c in C if c[6] == "yc"); cs = "".join(card(c) for c in C if c[6] != "yc")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Yacht Clubs & Sailing Centers | Albanardia.gov</title><link rel="manifest" href="../manifest.json"><link rel="icon" href="../icons/favicon.png"><meta name="theme-color" content="#22498a">
<style>:root{{--bg:#f4f5f7;--card:#fff;--ink:#1b2430;--mut:#5b6573;--line:#dde1e7;--navy:#22498a}}@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#0f141a;--card:#18202a;--ink:#edf1f5;--mut:#9ba7b3;--line:#2a3441}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,sans-serif}}.gov{{background:#0b1d3a;color:#cfd8e6;font-size:12.5px;padding:6px 16px}}
header{{background:var(--navy);color:#fff;padding:26px 16px}}header .in,main{{max-width:1120px;margin:0 auto}}header a{{color:#cfd8e6;font-size:14px}}header h1{{font:700 34px/1.1 Georgia,serif;margin:8px 0 4px}}main{{padding:20px 16px 90px}}
h2{{font:700 22px Georgia,serif;margin:26px 0 10px}}.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}}.cl{{display:flex;gap:14px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;text-decoration:none;color:var(--ink)}}
.bg{{width:62px;height:37px;flex:none}}.bg svg{{width:100%;height:100%}}.cl b{{display:block}}.cl small{{color:var(--mut)}}p.n{{color:var(--mut)}}ul{{color:var(--mut);padding-left:20px}}</style></head><body>
<div class="gov">An official website of the State of Albanardia</div><header><div class="in"><a href="../">← Albanardia.gov</a><h1>Yacht Clubs &amp; Sailing Centers</h1><div>{len(C)} clubs and centers across the Windward State. AYRC clubs race the <a href="../nesf/ayrc/" style="color:#fff">Albanardia Youth Racing Circuit</a>, run by the <a href="../nesf/" style="color:#fff">Northeastern Sailing Foundation</a>.</div></div></header>
<main><h2>Yacht clubs</h2><div class="g">{yc}</div><h2>Community sailing centers</h2><div class="g">{cs}</div>
<h2>Other sailing venues</h2><p class="n">These aren't clubs, but they're on the water too:</p><ul><li><b>Olympic Sailing Pavilion</b>, New Brolin: the national Olympic training base</li><li><b>James L. Gore Sailing Pavilion</b>, New Brolin: Aldense University's college sailing center</li><li><b>SBU Sailing Pavilion</b> and <b>AlbTech Sailing Center</b>: college boathouses on the Wellington River</li><li><b>Killalea Sailing Center</b> on Hanson Bay and the <b>Maldonado Boathouse</b></li></ul></main>
<script src="../app/app.js" data-home="float"></script></body></html>"""

if __name__ == "__main__":
    F = flags(); n = 0
    for c in C: n += club_site(c, F[c[0]])
    (OUT / "index.html").write_text(index(F), encoding="utf-8")
    print("built", len(C), "club websites,", n, "pages")
