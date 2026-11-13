#!/usr/bin/env python3
"""Northeastern Sailing Foundation (nesf/) and the Albanardia Youth Racing Circuit (nesf/ayrc/).
Schedule and classes come from tools/club_data.py (AYRC, AYRC_CLASSES); clubs from tools/build_clubs.py.
News sections read stories/stories.json (sites 'nesf' and 'ayrc'). Re-run by tools/build_stories.py."""
import ast, datetime, html, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from club_data import AYRC, AYRC_CLASSES, AYRC_GUESTS, JUNIOR
import photos as PHT
XCSS = '.cdp{padding:0!important;overflow:hidden}.cdp figure{border-radius:0;aspect-ratio:16/10}.cdp .tx{padding:14px 18px 18px}.hero{position:relative}'
def gallery(items): return '<div class="gal">' + ''.join(PHT.fig(p, c, 1000 if i else 1400) for i, (p, c) in enumerate(items)) + '</div>'
HB = lambda p: f" style=\"background:linear-gradient(110deg,rgba(1,42,92,.95) 0%,rgba(2,79,170,.78) 50%,rgba(2,79,170,.25) 100%),url('{PHT.url(p[0],1800)}') center/cover\""
E = html.escape
src = (ROOT / "tools/build_clubs.py").read_text(); i = src.index("C = ["); j = src.index("\n]\n", i)
C = ast.literal_eval(src[i + 4:j + 2]); BY = {c[0]: c for c in C}
DB = json.loads((ROOT / "stories/stories.json").read_text())["stories"]
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def fdate(d): return "%s %d, %s" % (MON[int(d[5:7]) - 1], int(d[8:]), d[:4])
def latest(site, n=3): return sorted([s for s in DB if s["site"] == site], key=lambda s: s["date"], reverse=True)[:n]
def cl(code): return BY[code][2].lower()

CSS = """
:root{--o:#d1132c;--t:#024faa;--n:#012a5c;--ink:#111827;--mut:#5b6472;--line:#e1e4ea;--bg:#f5f6f8;--card:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--ink:#edf1f6;--mut:#a0a9b6;--line:#2a3340;--bg:#0c1118;--card:#151c26}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Montserrat,system-ui,sans-serif}a{color:inherit}
.in{max-width:1120px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left))}
header{background:#fff;color:#111;padding-top:env(safe-area-inset-top);position:sticky;top:0;z-index:10;border-bottom:4px solid var(--t);box-shadow:0 1px 0 var(--o)}header .in{display:flex;align-items:center;gap:14px;min-height:70px}
.lg{display:flex;align-items:center;text-decoration:none;flex:none}.lg img{height:42px;width:auto;display:block}
nav{margin-left:auto;display:flex;gap:2px;overflow-x:auto}nav a{text-decoration:none;font-weight:700;font-size:14px;padding:8px 11px;border-radius:8px;white-space:nowrap;color:#1b2330}nav a:hover{background:#eef2f8}nav a.on{background:var(--t);color:#fff}
.hero{background:linear-gradient(120deg,var(--n) 0%,var(--t) 70%);color:#fff;padding:56px 0 60px;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;left:0;right:0;bottom:0;height:8px;background:linear-gradient(90deg,var(--o) 0 33%,#fff 33% 66%,var(--t) 66%)}
.hero .in{display:grid;grid-template-columns:1.35fr .9fr;gap:30px;align-items:center}
.hero .k{color:#ffd2d8}.hero h1{font-size:clamp(34px,5.2vw,60px);line-height:1.04;margin:8px 0 14px;font-weight:800;font-style:italic;letter-spacing:-1px;max-width:15ch}.hero p{font-size:17.5px;color:#e3ebf6;max-width:56ch;margin:0 0 22px}
.mark{justify-self:center;background:#fff;border-radius:22px;padding:26px;box-shadow:0 20px 44px rgba(0,0,0,.3);width:min(380px,82vw)}.mark img{width:100%;height:auto;display:block}
.k{font-size:12px;letter-spacing:2.5px;text-transform:uppercase;font-weight:800}
.btn{display:inline-block;background:var(--o);color:#fff;font-weight:800;font-style:italic;text-decoration:none;padding:12px 20px;border-radius:10px;margin:0 8px 8px 0}.btn.o{background:#fff;color:var(--t)}
section{padding:50px 0}section.alt{background:var(--card);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
h2{font-size:clamp(26px,3.4vw,36px);line-height:1.15;margin:0 0 6px;font-weight:800;font-style:italic;letter-spacing:-.5px}h3{font-weight:800;font-style:italic}.sub{color:var(--mut);margin:0 0 22px;max-width:64ch}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.g2{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.cd{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;text-decoration:none;display:block;border-top:4px solid var(--t)}.cd b{display:block;font-size:17px;margin-bottom:4px}.cd span,.cd p{color:var(--mut);margin:0}
.cd.o{border-top-color:var(--o)}.st b{font-size:34px;font-weight:800;font-style:italic;color:var(--t);line-height:1}.st span{display:block;margin-top:4px}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card)}table{width:100%;border-collapse:collapse;min-width:560px}td,th{padding:11px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{font-size:12px;text-transform:uppercase;letter-spacing:.6px;color:var(--mut)}tr:last-child td{border-bottom:0}
td small{color:var(--mut)}tr.fin td{background:color-mix(in srgb,var(--o) 8%,var(--card))}.n{font-weight:800;font-style:italic;color:var(--o)}
.ch{display:flex;flex-wrap:wrap;gap:8px}.ch a,.ch span{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:6px 13px;font-weight:600;font-size:14px;text-decoration:none}
table.sch{min-width:820px}table.sch th{background:color-mix(in srgb,var(--mut) 22%,var(--card));color:var(--ink);text-decoration:underline;text-underline-offset:3px;font-size:13px;letter-spacing:.3px;border-right:1px solid var(--line)}table.sch td{border-right:1px solid var(--line)}table.sch td:first-child,table.sch td:last-child,table.sch th:last-child{white-space:nowrap}table.sch th:last-child,table.sch td:last-child{border-right:0}table.sch td a{font-weight:700}
.sg h3 a{text-decoration:none}.cdp.lk{position:relative;cursor:pointer}.cdl{display:block;margin-top:6px;font-weight:700;font-size:14px;color:var(--t);text-decoration:none}.cdl::after{content:"";position:absolute;inset:0;z-index:1}.cdp.lk .cr{z-index:2}.cdp.lk:hover{border-color:var(--t)}.flt{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 14px}.flt input,.flt select{font:inherit;font-size:15px;padding:9px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--ink)}.flt input{flex:1;min-width:200px}#ct{color:var(--mut);font-size:14px}
.sg{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}.sg .tw table{min-width:0}.sg h3{margin:0 0 10px}
@media (max-width:900px){.sg{grid-template-columns:1fr}}
ul.l{margin:0;padding-left:20px}ul.l li{margin:4px 0}
footer{background:#fff;color:#333;border-top:4px solid var(--o);padding:30px 0 calc(90px + env(safe-area-inset-bottom))}footer .in{display:flex;gap:18px;flex-wrap:wrap;align-items:center;font-size:14px}footer img{height:54px;width:auto}footer a{text-decoration:none;font-weight:700}footer .sp{flex:1}
@media (max-width:900px){.g3,.g2,.g4{grid-template-columns:1fr}.g4.st4{grid-template-columns:1fr 1fr}.hero .in{grid-template-columns:1fr}.mark{display:none}header .in{flex-wrap:wrap;padding-bottom:6px}.lg img{height:36px}nav{margin-left:0;width:100%}}
"""

def shell(path, title, nav, body, desc):
    depth = path.count("/") + 1; r = "../" * depth
    ay = path.startswith("nesf/ayrc")
    links = "".join(f'<a href="{r}{p}"{" class=\"on\"" if p == path + "/" else ""}>{t}</a>' for p, t in nav)
    logo = f'<img src="{r}nesf/img/{"ayrc-logo-name" if ay else "nesf-logo"}.png" alt="{"Albanardia Youth Racing Circuit" if ay else "Northeastern Sailing Foundation"}">'
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="manifest" href="{r}manifest.json"><link rel="icon" href="{r}nesf/img/{'ayrc' if ay else 'nesf'}-burgee.png"><link rel="apple-touch-icon" href="{r}icons/icon-180.png"><meta name="theme-color" content="#024faa">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,600;0,700;0,800;1,700;1,800&display=swap" rel="stylesheet"><style>{CSS}{PHT.CSS}{XCSS}</style></head><body>
<header><div class="in"><a class="lg" href="{r}{'nesf/ayrc/' if ay else 'nesf/'}">{logo}</a><nav>{links}</nav></div></header>
{body}
<footer><div class="in"><img src="{r}nesf/img/nesf-burgee.png" alt="NESF"><img src="{r}nesf/img/ayrc-burgee.png" alt="AYRC"><span>Northeastern Sailing Foundation<br>120 Spinnaker St, Silverbrooks, AB 19002 · nesf.org</span><span class="sp"></span><a href="{r}nesf/">NESF</a><a href="{r}nesf/ayrc/">AYRC</a><a href="{r}clubs/">Clubs</a><a href="{r}">Albanardia.gov</a></div></footer>
<script src="{r}app/app.js" data-home="float"></script></body></html>"""

def news(site, me):
    return "".join(f'<a class="cd o" href="{me}stories/#{s["slug"]}"><small style="color:var(--mut);font-weight:700;text-transform:uppercase;letter-spacing:.6px;font-size:12px">{E(s["cat"])} · Published {fdate(s["date"])}</small><b>{E(s["title"])}</b><span>{E(s["dek"])}</span></a>' for s in latest(site))

NAV = [("nesf/", "Home"), ("nesf/#programs", "Programs"), ("nesf/ayrc/", "AYRC"), ("nesf/#clubs", "Member clubs"), ("nesf/#events", "Events"), ("nesf/stories/", "News"), ("nesf/#give", "Give")]
ANAV = [("nesf/ayrc/", "Circuit"), ("nesf/ayrc/#schedule", "Schedule"), ("nesf/ayrc/#classes", "Classes"), ("nesf/ayrc/#rules", "Scoring"), ("nesf/ayrc/#register", "Register"), ("nesf/ayrc/standings/", "Standings"), ("nesf/ayrc/stories/", "News"), ("nesf/", "NESF")]

def host_link(a, r):
    code = a[1]
    if code in BY: return f'<a href="{r}{cl(code)}/">{E(BY[code][1])}</a>'
    return E(code)

def nesf_home():
    members = [c for c in C if c[7]]
    others = [c for c in C if not c[7]]
    prog = [("Albanardia Youth Racing Circuit", "Eleven summer regattas around the state for Optimist, ILCA, C420, Club FJ, RS Feva and 29er sailors.", "ayrc/"),
            ("Youth sailing grants", "Grants to clubs and sailing centers for boats, coaches and scholarships. 2026 grants reached 19 programs.", "#grants"),
            ("Race management training", "US Sailing club race officer and judge seminars every winter, so every club can run a good regatta.", "#events"),
            ("Coach development", "Level 1 and Level 2 instructor courses, plus a paid mentorship for first-year coaches.", "#events"),
            ("Safety at Sea", "A one-day offshore safety seminar for big-boat sailors, with hands-on liferaft and fire training.", "#events"),
            ("Boat loan pool", "Optimists, C420s and ILCAs on loan to new programs and to sailors who can't charter.", "#grants")]
    ev = [("Jan 23, 2027", "Club Race Officer seminar", "Corinthian Yacht Club, Whilliker. Two days, US Sailing certification."),
          ("Feb 6, 2027", "Coach Development Weekend", "Silverbrooks Community Sailing Center. Level 1 instructor course and safety boat training."),
          ("Feb 20, 2027", "Judges seminar", "Albanardia City Yacht Club. For new and renewing judges and umpires."),
          ("Mar 13, 2027", "Safety at Sea seminar", "Olympic Sailing Pavilion, New Brolin. In-water liferaft training at the pavilion pool."),
          ("Apr 10, 2027", "AYRC coaches meeting", "Online. Schedule, sailing instructions and charter updates for the season."),
          ("Oct 23, 2027", "NESF Awards Dinner", "Foxford Yacht Club. AYRC trophies, volunteer of the year and the Harbor Cup.")]
    hp = PHT.pick("kids", "nesf")[0]
    body = f"""<div class="hero"{HB(hp)}>{PHT.credit(hp)}<div class="in"><div><div class="k">Northeastern Sailing Foundation</div><h1>More people sailing, all over Albanardia.</h1>
<p>NESF is the state's sailing foundation. We run the Albanardia Youth Racing Circuit, fund junior programs, train race officers and coaches, and keep boats in the hands of kids who'd otherwise watch from the dock.</p>
<a class="btn" href="ayrc/">AYRC 2027</a><a class="btn o" href="#give">Support NESF</a></div><div class="mark"><img src="img/nesf-burgee.png" alt="NESF burgee"></div></div></div>
<section><div class="in g4 st4"><div class="cd o st"><b>11</b><span>AYRC regattas in 2027</span></div><div class="cd o st"><b>{len(C)}</b><span>Member clubs and sailing centers</span></div><div class="cd o st"><b>19</b><span>Programs funded in 2026</span></div><div class="cd o st"><b>64</b><span>Loan boats in the pool</span></div></div></section>
<section><div class="in"><h2>Where the money goes</h2><p class="sub">Boats, coaches and camp scholarships at clubs and sailing centers across the state.</p>{gallery([(PHT.pick("camp","nesf")[0],"Summer camp scholarships"),(PHT.pick("Optimist","nesf")[0],"Loan-pool Optimists"),(PHT.pick("coach")[0],"Coach development"),(PHT.pick("team","nesf")[0],"High school team racing"),(PHT.pick("C420","nesf")[0],"AYRC C420 fleet")])}</div></section>
<section class="alt" id="programs"><div class="in"><h2>Programs</h2><p class="sub">Everything NESF does is about getting more people on the water and keeping them there.</p><div class="g3">{''.join(f'<a class="cd" href="{h}"><b>{E(t)}</b><span>{E(d)}</span></a>' for t, d, h in prog)}</div></div></section>
<section id="grants"><div class="in g2"><div><h2>Youth sailing grants</h2><p class="sub">Clubs and community sailing centers can apply each year for up to $15,000 toward boats, coaching and scholarships. Applications open January 4 and close February 26, 2027. Decisions by April 1.</p>
<a class="btn" href="#contact">Ask about a grant</a></div><div><h2>Boat loan pool</h2><p class="sub">24 Optimists, 16 C420s, 14 ILCAs and 10 Larssen Club Radials, loaned for a season to new junior programs and to AYRC sailors who can't charter. Boats go out in April and come home in October.</p></div></div></section>
<section class="alt" id="events"><div class="in"><h2>NESF events</h2><p class="sub">Training and the awards dinner. AYRC regattas are on the <a href="ayrc/#schedule">circuit schedule</a>.</p><div class="tw"><table><tr><th>Date</th><th>Event</th><th>Where</th></tr>{''.join(f'<tr><td>{d}</td><td><b>{E(t)}</b></td><td>{E(w)}</td></tr>' for d, t, w in ev)}</table></div></div></section>
<section id="clubs"><div class="in"><h2>Member clubs</h2><p class="sub">AYRC clubs field junior teams on the circuit. Every member club gets race management support and grant eligibility.</p>
<h3>AYRC clubs</h3><div class="ch">{''.join(f'<a href="../{c[2].lower()}/">{E(c[1])}</a>' for c in members)}</div>
<h3>Member clubs</h3><div class="ch">{''.join(f'<a href="../{c[2].lower()}/">{E(c[1])}</a>' for c in others)}</div>
<p class="sub" style="margin-top:16px">NESF also partners with the Olympic Sailing Pavilion, the college sailing pavilions and the Killalea Sailing Center. They aren't clubs, but AYRC sailors train there in the off-season.</p></div></section>
<section class="alt"><div class="in"><h2>News</h2><p class="sub"><a href="stories/">All NESF stories →</a></p><div class="g3">{news('nesf', '')}</div></div></section>
<section id="give"><div class="in g2"><div><h2>Give</h2><p class="sub">$50 covers an AYRC entry. $400 sends a junior to a week of summer camp. $4,800 buys a new Optimist for the loan pool. NESF is a 501(c)(3) nonprofit; gifts are tax deductible.</p><a class="btn" href="#contact">Donate</a></div>
<div id="contact"><h2>Contact</h2><p class="sub">Northeastern Sailing Foundation<br>120 Spinnaker St, Silverbrooks, AB 19002<br>nesf.org · Office open weekdays 9 to 5</p></div></div></section>"""
    return shell("nesf", "Northeastern Sailing Foundation", NAV, body, "Albanardia's sailing foundation: the AYRC, youth grants, race officer and coach training.")

# 2026 final individual standings (best 7 of 11, Championship x1.5). (sailor or skipper / crew, club code, points)
STAND_CLUBS = [("Albanardia City Yacht Club", 1412), ("Silverbrooks Yacht Club", 1388), ("Corinthian Yacht Club of Silverbrooks", 1240), ("Foxford Yacht Club", 1196), ("New Brolin Yacht Club", 1023),
             ("Northeastern Yacht Club", 954), ("Waterloo Yacht Club", 712), ("Cape Sturgeon Yacht Club", 640), ("Silverbrooks Community Sailing Center", 588), ("Pearl's End Sailing Center", 431),
             ("Hamilton Island Sailing Club", 377), ("Willamette Boating Center", 296), ("Coven Community Sailing", 241)]
STAND_IND = {
 "Optimist Championship": [("Nora Lindqvist", "FYC", 688), ("Kai Okafor", "ACYC", 671), ("Lily Brennan", "SBYC", 655), ("Theo Park", "CYC", 640), ("Ava Delgado", "NBYC", 628)],
 "ILCA 4": [("Elise Tran", "SBYC", 712), ("Marcus Bell", "SBYC", 697), ("Jonah Weiss", "ACYC", 684), ("Sadie Ortiz", "SBYC", 668), ("Mia Castellano", "NEYC", 655)],
 "ILCA 6": [("Leo Hartmann", "SBYC", 724), ("Anya Volkova", "SBYC", 709), ("Grace Nakamura", "CYC", 691), ("Tomás Rivera", "SBYC", 678), ("Finn Gallagher", "ACYC", 662)],
 "C420": [("Ruby Sato / Henry Ames", "ACYC", 705), ("Liam O'Shea / Zoe Fontaine", "SBYC", 690), ("Isla Grant / Diego Marín", "CYC", 672), ("Ben Whitaker / Hana Kim", "NEYC", 655), ("Clara Voss / Eli Brooks", "FYC", 641)],
 "Club FJ": [("Will Tanaka / June Abara", "CYC", 680), ("Ella Fischer / Noah Reyes", "ACYC", 662), ("Jack Doyle / Maya Patel", "NEYC", 650), ("Sophie Laurent / Ty Benson", "WYC-W", 631), ("Adam Cho / Rosa Lind", "SBYC", 617)],
 "RS Feva": [("Lucy Hargrove / Sami Haddad", "HIS", 664), ("Wren Mitchell / Oscar Ng", "PESC", 650), ("Ada Novak / Felix Romero", "FYC", 637), ("Iris Cole / Jude Amari", "SBYC", 620), ("Tess Ward / Rafi Cohen", "NBYC", 604)],
 "29er": [("Hugo Bergström / Nina Alvarez", "NBYC", 711), ("Cole Jensen / Inês Duarte", "ACYC", 693), ("Luke Ferris / Amara Obi", "SBYC", 676), ("Dylan Hayes / Freya Olsen", "CYC", 659), ("Ravi Shah / Kate Morrow", "CSYC", 641)],
}

# Full 2026 fleet rosters: the top five above, then every other sailor who scored, generated once from a fixed seed
# so the lists never change between builds. Clubs are weighted by their junior fleets; SBYC dominates the ILCAs.
import random
FLEET_SLUG = {"Optimist Championship": "optimist", "ILCA 4": "ilca-4", "ILCA 6": "ilca-6", "C420": "c420", "Club FJ": "club-fj", "RS Feva": "rs-feva", "29er": "29er"}
FLEET_SIZE = {"Optimist Championship": 52, "ILCA 4": 34, "ILCA 6": 38, "C420": 26, "Club FJ": 20, "RS Feva": 18, "29er": 14}
FLEET_BOAT = {"Optimist Championship": "Optimist", "ILCA 4": "ILCA", "ILCA 6": "ILCA", "C420": "C420", "Club FJ": "Club FJ", "RS Feva": "Optimist", "29er": "29er"}
FIRST = "Aiden Alba Amir Anna Arjun Asher Bea Bodhi Brooke Calla Cam Carter Cece Chloe Dani Dev Eli Emma Esme Ezra Fatima Gabe Gia Hank Hazel Ian Ivy Jade James Jasper Joel Juno Kaia Kian Lena Levi Lila Lou Luca Mae Malik Maren Mateus Mei Milo Nadia Nico Nell Olive Omar Paige Pearl Quinn Rae Reid Remy Rhea Rory Rosa Ruth Sage Santi Sena Silas Sloane Tariq Tess Theo Uma Vera Wes Willa Yara Yusuf Zane Zara".split()
LAST = "Abbott Achebe Alvarez Andersen Baker Banerjee Barros Becker Bishop Bjork Brandt Cabrera Carver Chen Collins Costa Dahl Dawson Diaz Doherty Eaton Ellison Farrow Fernandes Fox Garza Gill Goldberg Hale Hansen Haruna Ibarra Ingram Iversen Jaramillo Kane Keller Khan Lam Larsen Lowe Lund Maddox Mendez Murphy Nakamura Nielsen Novak Okoro Olsen Ortega Pace Petrov Quinlan Reyes Rossi Sandoval Schultz Sorensen Suzuki Tate Torres Underwood Vance Varga Walsh Webb Xu Yates Young Zamora Zhou".split()
def roster(fleet):
    rng = random.Random("ayrc2026-" + fleet)
    top = STAND_IND[fleet]; dh = "/" in top[0][0]
    w = {c: n for c, js in JUNIOR.items() for b, n in js if b == FLEET_BOAT[fleet] and c in BY}
    if fleet.startswith("ILCA"): w["SBYC"] *= 4  # SBYC is the state's ILCA powerhouse
    if fleet == "RS Feva": w = {c: n for c, n in w.items() if c in ("HIS", "PESC", "FYC", "SBYC", "NBYC", "ACYC", "CYC", "SBCS", "NEYC")}
    used = {n for t in STAND_IND.values() for x in t for n in x[0].split(" / ")}
    def name():
        while True:
            n = rng.choice(FIRST) + " " + rng.choice(LAST)
            if n not in used: used.add(n); return n
    rest = []
    for _ in range(FLEET_SIZE[fleet] - len(top)):
        c = rng.choices(list(w), weights=list(w.values()))[0]
        q = rng.random() * (0.4 if fleet.startswith("ILCA") and c == "SBYC" else 1)  # lower q = better result
        rest.append([name() + (" / " + name() if dh else ""), c, q])
    rest.sort(key=lambda x: x[2])
    rows = [(n, c, p, rng.randint(9, 11)) for n, c, p in top]
    pts = top[-1][2]
    for i, (n, c, q) in enumerate(rest):
        k = len(rest); pts -= rng.randint(4, 9) + (6 if i > k * .6 else 0)
        reg = max(1, min(11, round(11 - 9 * (i / k) + rng.uniform(-1.5, 1.5))))
        rows.append((n, c, max(18, min(pts, reg * 92)), reg))
    rows.sort(key=lambda x: -x[2])
    return rows

def fleet_page(fleet):
    rows = roster(fleet); r = "../../../../"; dh = "/" in rows[0][0]
    clubs = sorted({BY[c][2] for _, c, _, _ in rows})
    sb = sum(1 for _, c, _, _ in rows[:10] if c == "SBYC")
    tr = "".join(f'<tr data-c="{E(BY[c][2])}" data-n="{E(n.lower())}"><td class="n">{i}</td><td>{E(n)}</td><td><a href="{r}{cl(c)}/">{E(BY[c][2])}</a> <small>{E(BY[c][3])}</small></td><td>{g}</td><td>{p}</td></tr>' for i, (n, c, p, g) in enumerate(rows, 1))
    others = "".join(f'<a href="../{FLEET_SLUG[f]}/">{E(f)}</a>' if f != fleet else f'<span style="background:var(--t);color:#fff;border-color:var(--t)">{E(f)}</span>' for f in FLEET_SLUG)
    note = f" SBYC sailors hold {sb} of the top 10." if fleet.startswith("ILCA") else ""
    hp = PHT.PH["sunset"][0 if fleet == "ILCA 6" else 1] if fleet.startswith("ILCA") else PHT.pick({"Optimist": "Optimist", "ILCA": "ILCA", "C420": "C420", "Club FJ": "Club FJ", "29er": "29er"}.get(FLEET_BOAT[fleet] if fleet != "RS Feva" else "x", "kids"), "ayrc")[0]
    body = f"""<div class="hero"{HB(hp)}>{PHT.credit(hp)}<div class="in"><div><div class="k">AYRC 2026 final standings</div><h1>{E(fleet)}</h1><p>All {len(rows)} {"teams" if dh else "sailors"} who scored in 2026. Best 7 of 11 regattas, Championship at 1.5 times.{note}</p><a class="btn o" href="../">All fleets</a></div><div class="mark"><img src="../../../img/ayrc-logo-full.png" alt="AYRC"></div></div></div>
<section><div class="in"><p class="ch" style="margin:0 0 18px">{others}</p>
<div class="flt"><input id="q" type="search" placeholder="Search {"teams" if dh else "sailors"}" aria-label="Search"><select id="cf" aria-label="Club"><option value="">All clubs</option>{''.join(f'<option>{E(c)}</option>' for c in clubs)}</select><span id="ct"></span></div>
<div class="tw"><table id="t"><tr><th>Place</th><th>{"Skipper / crew" if dh else "Sailor"}</th><th>Club</th><th>Regattas</th><th>Points</th></tr>{tr}</table></div></div></section>
<script>(function(){{var q=document.getElementById('q'),f=document.getElementById('cf'),ct=document.getElementById('ct'),rs=[].slice.call(document.querySelectorAll('#t tr[data-c]'));function go(){{var s=q.value.toLowerCase().trim(),c=f.value,n=0;rs.forEach(function(r){{var ok=(!c||r.dataset.c==c)&&(!s||r.dataset.n.indexOf(s)>-1);r.style.display=ok?'':'none';if(ok)n++}});ct.textContent=n+' of '+rs.length}}q.oninput=go;f.onchange=go;go()}})();</script>"""
    return shell(f"nesf/ayrc/standings/{FLEET_SLUG[fleet]}", f"{fleet} 2026 Standings | AYRC", ANAV, body, f"Every {fleet} sailor in the 2026 AYRC standings.")

def standings():
    r = "../../../"
    def club(code): return f'<a href="{r}{cl(code)}/">{E(BY[code][2])}</a>'
    ind = "".join(f'<div><h3><a href="{FLEET_SLUG[f]}/">{E(f)} →</a></h3><div class="tw"><table><tr><th>Place</th><th>Sailor{"s" if "/" in rows[0][0] else ""}</th><th>Club</th><th>Points</th></tr>' + "".join(f'<tr><td class="n">{i}</td><td>{E(n)}</td><td>{club(c)}</td><td>{p}</td></tr>' for i, (n, c, p) in enumerate(rows, 1)) + f'</table></div><p style="margin:8px 0 0"><a href="{FLEET_SLUG[f]}/"><b>All {len(roster(f))} in {E(f)} →</b></a></p></div>' for f, rows in STAND_IND.items())
    hp = PHT.PH["regatta"][1]
    body = f"""<div class="hero"{HB(hp)}>{PHT.credit(hp)}<div class="in"><div><div class="k">AYRC 2026 season</div><h1>Final standings</h1><p>Best 7 of 11 regattas, with the Championship scored at 1.5 times. Green Fleet isn't scored. 2027 standings start after the Foxford Shakedown on May 22.</p><a class="btn" href="#individual">Individual</a><a class="btn o" href="#clubs">Club team</a></div><div class="mark"><img src="../../img/ayrc-logo-full.png" alt="AYRC"></div></div></div>
<section id="individual"><div class="in"><h2>Individual standings by fleet</h2><p class="sub">Top five in each scored fleet. Tap a fleet to see every sailor in it. Doublehanded fleets list skipper / crew. Full results for each regatta are posted by the host club.</p><div class="sg">{ind}</div></div></section>
<section class="alt" id="clubs"><div class="in"><h2>Club team standings</h2><p class="sub">Final standings for the club team trophy: each club's best 12 sailor scores across all fleets.</p>
<div class="tw"><table><tr><th>Place</th><th>Club</th><th>Points</th></tr>{''.join(f'<tr><td class="n">{i}</td><td>{E(c)}</td><td>{p:,}</td></tr>' for i, (c, p) in enumerate(STAND_CLUBS, 1))}</table></div></div></section>"""
    return shell("nesf/ayrc/standings", "2026 Standings | AYRC", ANAV, body, "AYRC 2026 final standings: individual top five in every fleet and the club team trophy.")

def ayrc():
    today = datetime.date(2026, 11, 12)
    rows = ""
    for n, a in enumerate(AYRC, 1):
        d = datetime.date.fromisoformat(a[0]); d2 = d + datetime.timedelta(1); nor = d - datetime.timedelta(45)
        dt = d.strftime("%b %-d") + "–" + (d2.strftime("%-d") if d2.month == d.month else d2.strftime("%b %-d"))
        web = (f'<a href="../../{cl(a[1])}/racing/">Notice of Race</a>' if a[1] in BY else "Notice of Race") + f'<br><small>Posts {nor.strftime("%b %-d")}</small>'
        rows += f'<tr{" class=\"fin\"" if a[6] == "Championship" else ""}><td><b>{dt}</b></td><td><b>{E(a[3])}</b><br><small>{E(a[4])}</small></td><td>{host_link(a, "../../")}<br><small>{E(a[2])}</small></td><td>{E(a[5])}</td><td>{E(a[6])}</td><td>{web}</td></tr>'
    seas = {"May": "Late spring", "Jun": "Late spring", "Jul": "Summer", "Aug": "Summer", "Sep": "Early fall"}
    stand = STAND_CLUBS
    _unused = [("Albanardia City Yacht Club", 1412), ("Silverbrooks Yacht Club", 1388), ("Corinthian Yacht Club of Silverbrooks", 1240), ("Foxford Yacht Club", 1196), ("New Brolin Yacht Club", 1023),
             ("Northeastern Yacht Club", 954), ("Waterloo Yacht Club", 712), ("Cape Sturgeon Yacht Club", 640), ("Silverbrooks Community Sailing Center", 588), ("Pearl's End Sailing Center", 431),
             ("Hamilton Island Sailing Club", 377), ("Willamette Boating Center", 296), ("Coven Community Sailing", 241)]
    hp = PHT.PH["regatta"][0]
    body = f"""<div class="hero"{HB(hp)}>{PHT.credit(hp)}<div class="in"><div><div class="k">Northeastern Sailing Foundation presents</div><h1>Albanardia Youth Racing Circuit 2027</h1>
<p>Eleven regattas from late May to late September, from the Foxford Shakedown to the Hanson Bay Showdown, with one road trip down the Turnpike to Barnegat Bay. Race as many as you like; your best seven count.</p>
<a class="btn" href="#schedule">Schedule</a><a class="btn o" href="#register">Register</a></div><div class="mark"><img src="../img/ayrc-logo-full.png" alt="AYRC, Albanardia Youth Racing Circuit"></div></div></div>
<section><div class="in g4 st4"><div class="cd o st"><b>11</b><span>Regattas, one per venue</span></div><div class="cd o st"><b>8</b><span>Fleets</span></div><div class="cd o st"><b>7</b><span>Best results count</span></div><div class="cd o st"><b>May 22</b><span>Opening day in Foxford</span></div></div></section>
<section class="alt" id="schedule"><div class="in"><h2>2027 schedule</h2><p class="sub">Every regatta is two days, with racing from 11 a.m. Saturday and a 3 p.m. last warning signal Sunday. Notices of race post 45 days before each event. Each venue hosts once a season.</p>
<div class="tw"><table class="sch"><tr><th>Date</th><th>Event name</th><th>Location</th><th>Boats</th><th>Event type</th><th>Event website</th></tr>{rows}</table></div>
<p class="sub" style="margin-top:14px">{" · ".join(f"<b>{s}</b>: " + ", ".join(datetime.date.fromisoformat(a[0]).strftime("%b %-d") for a in AYRC if seas[datetime.date.fromisoformat(a[0]).strftime("%b")] == s) for s in ("Late spring", "Summer", "Early fall"))}</p></div></section>
<section id="classes"><div class="in"><h2>Fleets</h2><p class="sub">Sailors pick one fleet for the season and can move up once, before the July 10 regatta.</p><div class="g4">{''.join(f'<div class="cd cdp{" lk" if t in FLEET_SLUG else ""}">{PHT.fig(PHT.PH["ILCA"][{"ILCA 4": 2, "ILCA 6": 6}[t]] if t.startswith("ILCA") else PHT.pick({"Opt":"Optimist","C42":"C420","Clu":"Club FJ","RS ":"kids","29e":"29er"}[t[:3]], t)[0], "", 700)}<div class="tx"><b>{E(t)}</b><span>{E(d)}</span>{f'<a class="cdl" href="standings/{FLEET_SLUG[t]}/">2026 standings →</a>' if t in FLEET_SLUG else ""}</div></div>' for t, d in AYRC_CLASSES)}</div>
<h3 style="margin-top:28px">Guest classes</h3><p class="sub">Host clubs can add guest dinghy fleets when five or more boats register. Guest classes race for regatta trophies but don't score in the season standings. The circuit is dinghies only: no keelboats.</p><div class="ch">{''.join(f'<span>{E(g)}</span>' for g in AYRC_GUESTS)}</div></div></section>
<section class="alt" id="rules"><div class="in g2"><div><h2>Scoring</h2><ul class="l sub"><li>Low point scoring at each regatta, then circuit points: 100 for first, down by fleet size.</li><li>Your best 7 of 11 regattas count toward the season.</li><li>The AYRC Championship can't be dropped, and it scores 1.5 times.</li><li>Club team trophy: each club's best 12 sailor scores across all fleets.</li><li>Green Fleet isn't scored; every sailor who finishes three regattas gets a season pennant.</li></ul></div>
<div><h2>Eligibility</h2><ul class="l sub"><li>Under 19 on December 31, 2027 (Optimist and RS Feva: 15 and under).</li><li>A US Sailing youth membership and a member club, sailing center or high school team.</li><li>Sailors from outside Albanardia are welcome at every regatta, but only Albanardia sailors score in the season standings.</li><li>A swim test and a signed parent waiver, once per season.</li></ul></div></div></section>
<section id="register"><div class="in g2"><div><h2>Registration</h2><p class="sub">Season registration opens March 1, 2027: $60 per sailor, plus $55 per regatta ($35 for Green Fleet). Register by the Wednesday before each regatta; late entries pay $20 more. NESF grants cover fees for any sailor who asks, no questions.</p></div>
<div><h2>Charters</h2><p class="sub">Host clubs charter Optimists, ILCAs, C420s and Club FJs at $90 a boat per regatta. The NESF loan pool keeps season charters for sailors without boats. The Barnegat Bay stop has charter boats arranged through the host club.</p></div></div></section>
<section><div class="in"><h2>Race weekends</h2><p class="sub">Two days of racing, a cookout and a lot of trailers.</p>{gallery([(PHT.pick("youth","ayrc")[0],"29ers at a championship"),(PHT.pick("Optimist","ayrc",1,2)[0],"Optimist fleet"),(PHT.pick("ILCA","ayrc")[0],"ILCA 6"),(PHT.pick("Club FJ","ayrc")[0],"Club FJ"),(PHT.PH["crew"][0],"The crew after racing"),(PHT.pick("coach")[0],"Coach boats")])}</div></section>
<section class="alt" id="standings"><div class="in"><h2>Standings</h2><p class="sub">Final 2026 results: the top five in every fleet and the club team trophy. 2026 champions: {E(stand[0][0])} (club team), {E(STAND_IND["ILCA 6"][0][0])} (ILCA 6), {E(STAND_IND["Optimist Championship"][0][0])} (Optimist).</p><a class="btn" href="standings/">See the 2026 standings</a></div></section>
<section><div class="in"><h2>News</h2><p class="sub"><a href="stories/">All AYRC stories →</a></p><div class="g3">{news('ayrc', '')}</div></div></section>"""
    return shell("nesf/ayrc", "AYRC 2027 | Albanardia Youth Racing Circuit", ANAV, body, "The Albanardia Youth Racing Circuit: eleven summer youth regattas around the state, run by NESF.")

if __name__ == "__main__":
    for p, h in (("nesf", nesf_home()), ("nesf/ayrc", ayrc()), ("nesf/ayrc/standings", standings())) + tuple((f"nesf/ayrc/standings/{FLEET_SLUG[f]}", fleet_page(f)) for f in FLEET_SLUG):
        o = ROOT / p / "index.html"; o.parent.mkdir(parents=True, exist_ok=True); o.write_text(h, encoding="utf-8")
    print("built nesf/, nesf/ayrc/ and nesf/ayrc/standings/")
