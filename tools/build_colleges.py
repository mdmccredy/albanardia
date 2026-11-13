#!/usr/bin/env python3
"""Generate colleges/<slug>/index.html for each Albanardia school, plus the colleges/ directory page.
Facts come from the World Bible and Stats doc; logos are Max's (colleges/img)."""
import sys as _sys
_sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import photos as PHT
import html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "colleges"
E = html.escape

import json as _json
_DB = _json.loads((ROOT/"stories/stories.json").read_text())["stories"]
_MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
def latest(site, n=3):
    """Newest stories for a site from the shared database (tools/build_stories.py)."""
    return sorted([x for x in _DB if x["site"] == site], key=lambda x: x["date"], reverse=True)[:n]
def fdate(d): return "%s %d, %s" % (_MON[int(d[5:7]) - 1], int(d[8:]), d[:4])

S = [
 dict(slug="ua-silverbrooks", name="University of Albanardia: Silverbrooks", short="UA Silverbrooks", c1="#0b7a3e", c2="#0d1f17", acc="#f2c230",
      logo="w_ua_silverbrooks.png", ath="a_ua_silverbrooks.png", seal=None, town="Silverbrooks (Lindgren Heights)", kind="Flagship urban public university",
      students="32,000", acres="300", mascot="Mets", domain="silverbrooks.albanardia.edu",
      tagline="The flagship of the University of Albanardia, in the heart of the capital.",
      programs=["Engineering","Business","Nursing & Health Sciences","Public Policy","Arts & Sciences","Education"],
      venues=[("Lindgren Stadium","Football","2035 143rd St"),("Hallström Arena","Basketball, hockey","1442 154th St")],
      rival="Aldense Bruins", system=True),
 dict(slug="ua-albanardia-city", name="University of Albanardia: Albanardia City", short="UA Albanardia City", c1="#c8202b", c2="#2a0b0d", acc="#ffffff",
      logo="w_ua_albcity.png", ath="a_ua_albcity.png", seal=None, town="Albanardia City", kind="Public university",
      students="22,000", acres="220", mascot="Ravens", domain="albcity.albanardia.edu",
      tagline="A University of Albanardia campus for the state's second city.",
      programs=["Business","Engineering Technology","Criminal Justice","Health Sciences","Arts & Sciences"],
      venues=[("Raven Stadium","Football","1600 Marlow Pike"),("Raven Center","Basketball","45 Gull Point Rd")], system=True),
 dict(slug="ua-waterloo", name="University of Albanardia: Waterloo", short="UA Waterloo", c1="#2563c9", c2="#0b1a36", acc="#ffffff",
      logo="w_ua_waterloo.png", ath="a_ua_waterloo.png", seal=None, town="Waterloo", kind="Public university",
      students="19,000", acres="250", mascot="Sharks", domain="waterloo.albanardia.edu",
      tagline="Hands-on learning on the Rochester County riverfront.",
      programs=["Engineering","Agriculture & Environment","Business","Education","Arts & Sciences"],
      venues=[("Riverside Stadium","Football","400 Riverbend Pkwy"),("The Tank","Basketball, hockey","55 Penns Ferry Rd")], system=True),
 dict(slug="ua-foxford", name="University of Albanardia: Foxford", short="UA Foxford", c1="#e8742a", c2="#2b1406", acc="#ffffff",
      logo="w_ua_foxford.png", ath="a_ua_foxford.png", seal=None, town="Foxford", kind="Regional public university",
      students="9,000", acres="120", mascot="Eagles", domain="foxford.albanardia.edu",
      tagline="Small classes on Albanardia Sound.",
      programs=["Marine Science","Education","Nursing","Business","Arts & Sciences"],
      venues=[("Foxford Field","Football, soccer","700 Sound View Dr"),("Beaver Lodge","Basketball","18 Lodgepole Ln")], system=True),
 dict(slug="ua-moiyane", name="University of Albanardia: Moïyane", short="UA Moïyane", c1="#d6249f", c2="#2a0820", acc="#ffffff",
      logo="w_ua_moiyane.png", ath="a_ua_moiyane.png", seal=None, town="Moïyane", kind="Community college",
      students="—", acres="—", mascot="Royals", domain="moiyane.albanardia.edu",
      tagline="Two-year degrees, transfer paths and career training for Moïyane County.",
      programs=["Transfer Associate Degrees","Nursing","Skilled Trades","Agriculture","Business"],
      venues=[], system=True),
 dict(slug="sbu", name="Silverbrooks University", short="SBU", c1="#c8102e", c2="#1a1a1a", acc="#ffffff",
      logo="f_sbu.png", ath="a_sbu.png", seal="seal_sbu.png", town="Silverbrooks, north bank of the Wellington River", kind="Private research university",
      students="18,000", acres="140", mascot="SBU", domain="sbu.edu", founded="1799",
      tagline="Research, medicine and engineering on the Wellington River since 1799.",
      programs=["Medicine","Engineering","Artificial Intelligence","Law & Policy","Arts & Sciences","Business"],
      venues=[("Nyberg Field","Football, soccer","248 North Taylor Ave"),("SBU Fieldhouse","Basketball, volleyball","5005 148th St"),("SBU Sailing Pavilion","Sailing","12 Boathouse Ln")]),
 dict(slug="albtech", name="Albanardia Institute of Technology", short="AlbTech", c1="#1b9e5a", c2="#0c1a14", acc="#f5c518",
      logo="w_albtech.png", ath="a_albtech.png", seal=None, town="Silverbrooks, south bank, 4012 Commerce St", kind="Institute of technology",
      students="12,000", acres="170", mascot="Beavers", domain="albtech.edu",
      tagline="Engineering, design, startups and AI, facing SBU across the river.",
      programs=["Mechanical Engineering","Computer Science & AI","Product Design","Electrical Engineering","Architecture","Entrepreneurship"],
      venues=[("Tech Field","Football, lacrosse","3842 Lincoln Ave"),("Beaver Center","Basketball, hockey, esports","6334 Rochelle Ave"),("AlbTech Sailing Center","Sailing","3 Ferry Slip Rd")]),
 dict(slug="aldense", name="Aldense University", short="Aldense", c1="#4b2a8f", c2="#170c2c", acc="#fbb514",
      logo="w_aldense.png", ath="a_aldense.png", seal="seal_aldense.png", mark="m_aldense_bear.png", town="New Brolin, on the headland south of downtown", kind="Private university",
      students="14,000", acres="210", mascot="Bruins", domain="aldense.edu", motto="Amicitia et Sapientia",
      tagline="An elite small university on the New Brolin headland.",
      programs=["Specter School of Law","Mirano School of Engineering","Humanities","Philosophy","Business"],
      venues=[("Brady Field","Football","1 Bruin Way"),("Bruin Arena","Basketball, hockey","300 Headland Rd"),("James L. Gore Sailing Pavilion","Sailing","New Brolin")],
      rival="UA Silverbrooks Mets"),
 dict(slug="mckay", name="McKay University", short="McKay U", c1="#1d3a6e", c2="#0b1426", acc="#e7b53b",
      logo="w_mckay.png", ath=None, seal="seal_mckay.png", town="Silverbrooks (East Harbor / Farsgod), 1732 15th St", kind="Private university",
      students="7,000", acres="75", mascot="McKay", domain="mckay.edu",
      tagline="Physics, space and the sciences beside the harbor.",
      programs=["Physics","Space Science","Mathematics","Biology & Medicine","Education"],
      venues=[("McKay Fieldhouse","Basketball, rec center","5735 Garfield Ave")]),
 dict(slug="smithsonian", name="Smithsonian College", short="Smithsonian", c1="#0f7a4a", c2="#0a1f15", acc="#ffffff",
      logo="w_smithsonian.png", ath=None, seal="seal_smithsonian.png", town="Belwether", kind="Private liberal arts college",
      students="2,600", acres="150", mascot="Stingers", domain="smithsonian.edu",
      tagline="A liberal arts college in Albanardia's college town.",
      programs=["English & Writing","History","Environmental Studies","Mathematics","Fine Arts"], venues=[]),
 dict(slug="saint-marse", name="Université Saint-Marsé", short="Saint-Marsé", c1="#1c2b4a", c2="#0b1222", acc="#c9a54b",
      logo="w_saintmarse.png", ath=None, seal=None, town="Not yet placed on the map", kind="French-language university",
      students="—", acres="—", mascot=None, domain="saintmarse.edu", motto="Lux in Flumine",
      tagline="Albanardia's French-language university.",
      programs=["French","European Studies","Education","Arts"], venues=[]),
]
OTHERS = [("Albanardia State University (ASU)","Belwether · \"the Alzoo\" · 41,500 students"),("Albanardia Maritime Academy","Coven · Mariners"),("Coven College","Saint-Sturgeon"),("Aboraxas College","Moïyane")]

CSS = """
:root{--c1:@C1;--c2:@C2;--acc:@ACC;--bg:#fff;--ink:#16181d;--mut:#5e6570;--line:#e3e5e9;--soft:#f4f5f7;--card:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0e1116;--ink:#eef0f3;--mut:#9aa3ae;--line:#272e38;--soft:#161b22;--card:#161b22}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Source Sans 3",system-ui,sans-serif}a{color:inherit}
.in{max-width:1180px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left))}
.ut{background:var(--c2);color:#d9dde3;font-size:13px;padding-top:env(safe-area-inset-top)}.ut .in{display:flex;gap:16px;min-height:34px;align-items:center;overflow-x:auto;white-space:nowrap}.ut a{text-decoration:none}.ut .sp{flex:1}
header{background:#fff;border-bottom:4px solid var(--c1);position:sticky;top:0;z-index:20}header .in{display:flex;align-items:center;gap:20px;min-height:76px}
.lg img{height:52px;width:auto;display:block}
nav{display:flex;gap:4px;margin-left:auto}nav a{text-decoration:none;font-weight:700;color:#16181d;padding:10px 12px;border-radius:8px;font-size:15px}nav a:hover{background:#f1f2f4}
.mb{display:none;margin-left:auto;width:44px;height:44px;border:1px solid #ddd;border-radius:10px;background:#fff;font-size:22px}
.hero{background:linear-gradient(120deg,var(--c1),var(--c2));color:#fff;position:relative;overflow:hidden}
.hero .in{display:grid;grid-template-columns:1.3fr 1fr;gap:30px;align-items:center;padding-top:64px;padding-bottom:64px}
.hero h1{font:700 clamp(36px,5.4vw,62px)/1.05 "Source Serif 4",Georgia,serif;margin:10px 0 14px}.hero p{font-size:19px;opacity:.92;max-width:48ch;margin:0 0 24px}
.kick{font-weight:700;letter-spacing:2px;text-transform:uppercase;font-size:13px;color:var(--acc)}
.seal{justify-self:center;width:min(320px,70vw);aspect-ratio:1;border-radius:50%;background:#fff;display:grid;place-items:center;box-shadow:0 20px 50px rgba(0,0,0,.3);padding:18px}.seal img{max-width:100%;max-height:100%}
.btn{display:inline-block;background:var(--acc);color:var(--c2);font-weight:700;text-decoration:none;padding:13px 22px;border-radius:6px;margin:0 8px 8px 0}.btn.o{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.7)}
.ql{background:var(--soft);border-bottom:1px solid var(--line)}.ql .in{display:grid;grid-template-columns:repeat(5,1fr)}
.ql a{padding:18px 12px;text-decoration:none;font-weight:700;border-left:1px solid var(--line);text-align:center}.ql a:first-child{border-left:0}.ql a:hover{color:var(--c1)}
section{padding:60px 0}section.alt{background:var(--soft)}
h2{font:700 clamp(28px,3.6vw,40px)/1.1 "Source Serif 4",Georgia,serif;margin:0 0 8px}.sub{color:var(--mut);margin:0 0 24px;max-width:62ch}
.stats{display:grid;grid-template-columns:repeat(4,1fr);background:var(--c1);color:#fff}.stats div{padding:26px 20px;border-left:1px solid rgba(255,255,255,.2)}.stats div:first-child{border-left:0}
.stats b{display:block;font:700 34px "Source Serif 4",Georgia,serif}.stats span{opacity:.88;font-size:14px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--c1);border-radius:8px;padding:18px}
.card b{display:block;font-size:18px;margin-bottom:4px}.card span{color:var(--mut);font-size:14.5px}
.ath{display:grid;grid-template-columns:260px 1fr;gap:30px;align-items:center}.ath .mk{background:var(--c2);border-radius:12px;padding:28px;display:grid;place-items:center;min-height:200px}.ath .mk img{max-width:100%;max-height:150px}
table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:10px 8px;border-bottom:1px solid var(--line)}th{font-size:13px;text-transform:uppercase;letter-spacing:1px;color:var(--mut)}
.news{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.nw{border:1px solid var(--line);border-radius:10px;padding:18px;background:var(--card)}.nw small{color:var(--c1);font-weight:700;text-transform:uppercase;letter-spacing:1px;font-size:12px}.nw h3{font:700 21px/1.25 "Source Serif 4",Georgia,serif;margin:6px 0}.nw p{margin:0;color:var(--mut)}
.visit{background:var(--c2);color:#fff;border-radius:14px;padding:30px;display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap}.visit p{margin:4px 0 0;opacity:.85}
footer{background:var(--c2);color:#cfd4db;padding:40px 0 calc(90px + env(safe-area-inset-bottom))}footer .g{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:24px}footer a{display:block;text-decoration:none;padding:3px 0}footer h5{color:#fff;margin:0 0 8px;font-size:15px}
footer .wm{background:#fff;display:inline-block;padding:10px 14px;border-radius:8px}footer .wm img{height:40px;display:block}
@media (max-width:860px){nav{display:none}nav.on{display:flex;flex-direction:column;position:absolute;left:0;right:0;top:100%;background:#fff;padding:10px 16px;border-bottom:1px solid #ddd}.mb{display:block}
 .hero .in,.ath{grid-template-columns:1fr}.ql .in{display:flex;overflow-x:auto}.ql a{flex:none;padding:14px 16px}.stats{grid-template-columns:1fr 1fr}.grid,.news{grid-template-columns:1fr}footer .g{grid-template-columns:1fr}.lg img{height:40px}}
"""

def page(s):
    news = latest("college:" + s["slug"], 3)
    seal = s.get("seal") or s.get("ath") or s["logo"]
    mark = s.get("mark") or s.get("ath")
    stats = [(s.get("founded") or s["students"], "Founded" if s.get("founded") else "Students"),
             (s["students"] if s.get("founded") else s["acres"]+(" acres" if s["acres"]!="—" else ""), "Students" if s.get("founded") else "Campus"),
             (s["mascot"] or "—", "Athletics"), (s["kind"].split(" ")[0].capitalize() if False else ("UA System" if s.get("system") else "Independent"), "Governance")]
    venues = "".join(f"<tr><td><b>{E(v[0])}</b></td><td>{E(v[1])}</td><td>{E(v[2])}</td></tr>" for v in s["venues"]) or '<tr><td colspan="3">Venues not on the map yet.</td></tr>'
    body = f"""
<div class="ut"><div class="in"><a href="../../">Albanardia.gov</a><a href="../">All colleges</a><span class="sp"></span><a href="#visit">Visit</a><a href="#apply">Apply</a><a href="#news">News</a></div></div>
<header><div class="in"><a class="lg" href="./"><img src="../img/{s['logo']}" alt="{E(s['name'])}"></a>
<nav id="nv"><a href="#about">About</a><a href="#academics">Academics</a><a href="#apply">Admissions</a><a href="#athletics">Athletics</a><a href="#news">News</a></nav>
<button class="mb" onclick="document.getElementById('nv').classList.toggle('on')" aria-label="Menu">☰</button></div></header>
<div class="hero" style="position:relative;background:linear-gradient(110deg,{s['c1']}f2 0%,{s['c1']}c8 50%,{s['c1']}55 100%),url('{PHT.url(PHT.pick("campus", s["slug"])[0][0], 1800)}') center/cover">{PHT.credit(PHT.pick("campus", s["slug"])[0])}<div class="in"><div><div class="kick">{E(s['town'].split(',')[0])}, Albanardia</div><h1>{E(s['name'])}</h1><p>{E(s['tagline'])}</p>
<a class="btn" href="#apply">Apply</a><a class="btn o" href="#visit">Visit campus</a></div>
<div class="seal"><img src="../img/{seal}" alt=""></div></div></div>
<div class="ql"><div class="in"><a href="#academics">Academics</a><a href="#apply">Admissions</a><a href="#athletics">Athletics</a><a href="#visit">Visit</a><a href="#news">News</a></div></div>
<div class="stats">{''.join(f'<div><b>{E(a)}</b><span>{E(b)}</span></div>' for a,b in stats)}</div>
<section id="about"><div class="in"><h2>About {E(s['short'])}</h2><p class="sub">{E(s['name'])} is a {E(s['kind'].lower())} in {E(s['town'])}{', on about '+s['acres']+' acres' if s['acres']!='—' else ''}.{' Part of the University of Albanardia system (albanardia.edu).' if s.get('system') else ''}{' Motto: '+E(s['motto'])+'.' if s.get('motto') else ''}</p></div></section>
<section class="alt" id="academics"><div class="in"><h2>Academics</h2><p class="sub">Schools and areas of study.</p><div class="grid">{''.join(f'<div class="card"><b>{E(p)}</b><span>Undergraduate and graduate programs</span></div>' for p in s['programs'])}</div></div></section>
<section><div class="in"><h2>Campus life</h2><p class="sub">Classes, late nights in the library and Saturdays in the stands.</p><style>{PHT.CSS}</style><div class="gal">{''.join(PHT.fig(p, c, 1000 if i else 1400) for i, (p, c) in enumerate([(PHT.pick("lecture", s["slug"])[0], "In class"), (PHT.pick("library", s["slug"])[0], "The library"), (PHT.pick("stadium")[0], "Game day"), (PHT.pick("team", s["slug"])[0], "Club and varsity sailing"), (PHT.pick("campus", s["slug"], 1, 1)[0], "On the quad")]))}</div></div></section>
<section id="athletics"><div class="in ath"><div class="mk"><img src="../img/{mark or s['logo']}" alt=""></div><div><h2>{E(s['short'])} {E(s['mascot'] or 'Athletics')}</h2><p class="sub">{'Rivalry: '+E(s['rival'])+'.' if s.get('rival') else 'Home venues and teams.'}</p>
<table><tr><th>Venue</th><th>Sports</th><th>Address</th></tr>{venues}</table></div></div></section>
<section class="alt" id="news"><div class="in"><h2>News</h2><p class="sub">From around campus. <a href="stories/">All stories →</a> · <a href="../../media/university-news/">University News →</a></p><div class="news">{''.join(f'<a class="nw" href="stories/#{n["slug"]}" style="display:block;color:inherit;text-decoration:none"><small>{E(n["cat"])} · Published {fdate(n["date"])}</small><h3>{E(n["title"])}</h3><p>{E(n["dek"])}</p></a>' for n in news)}</div></div></section>
<section id="apply"><div class="in"><div class="visit" id="visit"><div><h2 style="color:#fff">Apply or visit</h2><p>Tours every weekday. Applications for fall 2027 are open at {E(s['domain'])}.</p></div><a class="btn" href="../../map/">Find us on the map</a></div></div></section>
<footer><div class="in g"><div><span class="wm"><img src="../img/{s['logo']}" alt=""></span><p>{E(s['town'])}, Albanardia</p></div>
<div><h5>Explore</h5><a href="#academics">Academics</a><a href="#athletics">Athletics</a><a href="#news">News</a><a href="stories/">All stories</a></div><div><h5>Albanardia</h5><a href="../">All colleges</a><a href="../../">Albanardia.gov</a><a href="../../map/">State map</a></div></div></footer>"""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(s['name'])}</title><link rel="manifest" href="../../manifest.json"><link rel="icon" href="../img/{s.get('ath') or s['logo']}"><link rel="apple-touch-icon" href="../../icons/icon-180.png">
<meta name="theme-color" content="{s['c1']}"><link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Source+Serif+4:wght@700&display=swap" rel="stylesheet">
<style>{CSS.replace("@C1",s["c1"]).replace("@C2",s["c2"]).replace("@ACC",s["acc"])}</style></head><body>{body}<script src="../../app/app.js" data-home="float"></script></body></html>"""

def index():
    cards = "".join(f'<a class="cc" href="{s["slug"]}/" style="--c1:{s["c1"]}"><span class="lg"><img src="img/{s["logo"]}" alt=""></span><b>{E(s["name"])}</b><span>{E(s["town"].split(",")[0])} · {E(s["kind"])}{" · "+E(s["mascot"]) if s["mascot"] else ""}</span></a>' for s in S)
    others = "".join(f'<div class="cc o"><b>{E(a)}</b><span>{E(b)} · site coming</span></div>' for a,b in OTHERS)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Colleges & Universities | Albanardia.gov</title><link rel="manifest" href="../manifest.json"><link rel="icon" href="../icons/favicon.png"><meta name="theme-color" content="#22498a">
<style>
:root{{--bg:#f4f5f7;--card:#fff;--ink:#1b2430;--mut:#5b6573;--line:#dde1e7;--navy:#22498a}}@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#0f141a;--card:#18202a;--ink:#edf1f5;--mut:#9ba7b3;--line:#2a3441}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,sans-serif}}
.gov{{background:#0b1d3a;color:#cfd8e6;font-size:12.5px;padding:6px 16px}}header{{background:var(--navy);color:#fff;padding:26px 16px}}header .in,main{{max-width:1180px;margin:0 auto}}header a{{color:#cfd8e6;font-size:14px}}
header h1{{font:700 34px/1.1 Georgia,serif;margin:8px 0 4px}}main{{padding:20px 16px 90px}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:12px}}.cc{{display:block;background:var(--card);border:1px solid var(--line);border-top:5px solid var(--c1,#888);border-radius:10px;padding:16px;text-decoration:none;color:var(--ink)}}
.cc .lg{{display:flex;align-items:center;height:64px;background:#fff;border-radius:6px;padding:6px 10px;margin-bottom:10px}}.cc .lg img{{max-height:52px;max-width:100%}}.cc b{{display:block}}.cc span{{color:var(--mut);font-size:14px}}.cc.o{{border-top-color:#9aa3ae}}
h2{{margin:30px 0 12px}}
</style></head><body><div class="gov">An official website of the State of Albanardia</div>
<header><div class="in"><a href="../">← Albanardia.gov</a><h1>Colleges &amp; Universities</h1><div>Higher education in the Windward State: the University of Albanardia system and independent colleges.</div></div></header>
<main><div class="g">{cards}</div><h2>More schools</h2><div class="g">{others}</div></main><script src="../app/app.js" data-home="float"></script></body></html>"""

if __name__ == "__main__":
    for s in S:
        d = OUT / s["slug"]; d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(s), encoding="utf-8")
    (OUT / "index.html").write_text(index(), encoding="utf-8")
    print("built", len(S), "college sites")
