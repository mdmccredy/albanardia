#!/usr/bin/env python3
"""Northeastern Sailing Foundation (nesf/) and the Albanardia Youth Racing Circuit (nesf/ayrc/).
Schedule and classes come from tools/club_data.py (AYRC, AYRC_CLASSES); clubs from tools/build_clubs.py.
News sections read stories/stories.json (sites 'nesf' and 'ayrc'). Re-run by tools/build_stories.py."""
import ast, datetime, html, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from club_data import AYRC, AYRC_CLASSES, AYRC_GUESTS
E = html.escape
src = (ROOT / "tools/build_clubs.py").read_text(); i = src.index("C = ["); j = src.index("\n]\n", i)
C = ast.literal_eval(src[i + 4:j + 2]); BY = {c[0]: c for c in C}
DB = json.loads((ROOT / "stories/stories.json").read_text())["stories"]
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def fdate(d): return "%s %d, %s" % (MON[int(d[5:7]) - 1], int(d[8:]), d[:4])
def latest(site, n=3): return sorted([s for s in DB if s["site"] == site], key=lambda s: s["date"], reverse=True)[:n]
def cl(code): return BY[code][2].lower()

CSS = """
:root{--o:#c4552f;--t:#0b4f6c;--n:#0a2233;--ink:#14202c;--mut:#5c6672;--line:#dfe3e6;--bg:#f6f7f5;--card:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--ink:#edf1f4;--mut:#9ca6b2;--line:#28323c;--bg:#0d1318;--card:#151d24}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Inter",system-ui,sans-serif}a{color:inherit}
.in{max-width:1120px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left))}
header{background:var(--n);color:#fff;padding-top:env(safe-area-inset-top);position:sticky;top:0;z-index:10}header .in{display:flex;align-items:center;gap:14px;min-height:66px}
.lg{display:flex;align-items:center;gap:10px;text-decoration:none}.lg svg{width:38px;height:38px;flex:none}.lg b{font-weight:800;letter-spacing:.3px;line-height:1.1}.lg small{display:block;color:#9fb4c4;font-size:11.5px;letter-spacing:1.5px;text-transform:uppercase}
nav{margin-left:auto;display:flex;gap:2px;overflow-x:auto}nav a{text-decoration:none;font-weight:600;font-size:14.5px;padding:8px 11px;border-radius:8px;white-space:nowrap;color:#d6e0e8}nav a:hover,nav a.on{background:rgba(255,255,255,.1);color:#fff}
.hero{background:linear-gradient(135deg,var(--n) 30%,var(--t));color:#fff;padding:60px 0 64px;position:relative;overflow:hidden}
.hero .k{color:#f3b49b}.hero h1{font-size:clamp(36px,5.4vw,62px);line-height:1.04;margin:8px 0 14px;font-weight:800;letter-spacing:-1px;max-width:15ch}.hero p{font-size:18px;color:#d8e3ea;max-width:56ch;margin:0 0 22px}
.k{font-size:12.5px;letter-spacing:2.5px;text-transform:uppercase;font-weight:700}
.btn{display:inline-block;background:var(--o);color:#fff;font-weight:700;text-decoration:none;padding:12px 20px;border-radius:10px;margin:0 8px 8px 0}.btn.o{background:transparent;border:1.5px solid rgba(255,255,255,.6)}
section{padding:50px 0}section.alt{background:var(--card);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
h2{font-size:clamp(26px,3.4vw,36px);line-height:1.15;margin:0 0 6px;font-weight:800;letter-spacing:-.5px}.sub{color:var(--mut);margin:0 0 22px;max-width:64ch}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.g2{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.cd{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;text-decoration:none;display:block;border-top:4px solid var(--t)}.cd b{display:block;font-size:18px;margin-bottom:4px}.cd span,.cd p{color:var(--mut);margin:0}
.cd.o{border-top-color:var(--o)}.st b{font-size:34px;font-weight:800;color:var(--o);line-height:1}.st span{display:block;margin-top:4px}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card)}table{width:100%;border-collapse:collapse;min-width:560px}td,th{padding:11px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{font-size:12.5px;text-transform:uppercase;letter-spacing:.6px;color:var(--mut)}tr:last-child td{border-bottom:0}
td small{color:var(--mut)}tr.fin td{background:color-mix(in srgb,var(--o) 9%,var(--card))}tr.past td{opacity:.6}.n{font-weight:800;color:var(--o)}
.ch{display:flex;flex-wrap:wrap;gap:8px}.ch a,.ch span{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:6px 13px;font-weight:600;font-size:14px;text-decoration:none}
ul.l{margin:0;padding-left:20px}ul.l li{margin:4px 0}
footer{background:var(--n);color:#b9c7d2;padding:34px 0 calc(90px + env(safe-area-inset-bottom))}footer .in{display:flex;gap:16px;flex-wrap:wrap;align-items:center}footer a{text-decoration:none}footer .sp{flex:1}
@media (max-width:900px){.g3,.g2,.g4{grid-template-columns:1fr}.g4.st4{grid-template-columns:1fr 1fr}header .in{flex-wrap:wrap;padding-bottom:6px}nav{margin-left:0;width:100%}}
"""
LOGO = '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#0b4f6c" stroke="#fff" stroke-width="1.5"/><path d="M20 7 L20 30 L9 30 Z" fill="#fff"/><path d="M22 11 L22 30 L31 30 Z" fill="#c4552f"/><path d="M7 32 Q13 29 20 32 T33 32" stroke="#fff" stroke-width="2" fill="none"/></svg>'

def shell(path, title, nav, body, desc):
    depth = path.count("/") + 1; r = "../" * depth
    links = "".join(f'<a href="{r}{p}"{" class=\"on\"" if p == path + "/" else ""}>{t}</a>' for p, t in nav)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="manifest" href="{r}manifest.json"><link rel="apple-touch-icon" href="{r}icons/icon-180.png"><meta name="theme-color" content="#0a2233">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>
<header><div class="in"><a class="lg" href="{r}nesf/">{LOGO}<span><b>{'AYRC' if path.startswith('nesf/ayrc') else 'NESF'}</b><small>{'Albanardia Youth Racing Circuit' if path.startswith('nesf/ayrc') else 'Northeastern Sailing Foundation'}</small></span></a><nav>{links}</nav></div></header>
{body}
<footer><div class="in"><span>{LOGO}</span><span>Northeastern Sailing Foundation · 120 Spinnaker St, Silverbrooks, AB 19002 · nesf.org</span><span class="sp"></span><a href="{r}clubs/">Clubs</a><a href="{r}">Albanardia.gov</a></div></footer>
<script src="{r}app/app.js" data-home="float"></script></body></html>"""

def news(site, me):
    return "".join(f'<a class="cd o" href="{me}stories/#{s["slug"]}"><small style="color:var(--mut);font-weight:700;text-transform:uppercase;letter-spacing:.6px;font-size:12px">{E(s["cat"])} · Published {fdate(s["date"])}</small><b>{E(s["title"])}</b><span>{E(s["dek"])}</span></a>' for s in latest(site))

NAV = [("nesf/", "Home"), ("nesf/#programs", "Programs"), ("nesf/ayrc/", "AYRC"), ("nesf/#clubs", "Member clubs"), ("nesf/#events", "Events"), ("nesf/stories/", "News"), ("nesf/#give", "Give")]
ANAV = [("nesf/ayrc/", "Circuit"), ("nesf/ayrc/#schedule", "Schedule"), ("nesf/ayrc/#classes", "Classes"), ("nesf/ayrc/#rules", "Scoring"), ("nesf/ayrc/#register", "Register"), ("nesf/ayrc/#standings", "Standings"), ("nesf/ayrc/stories/", "News"), ("nesf/", "NESF")]

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
    body = f"""<div class="hero"><div class="in"><div class="k">Northeastern Sailing Foundation</div><h1>More people sailing, all over Albanardia.</h1>
<p>NESF is the state's sailing foundation. We run the Albanardia Youth Racing Circuit, fund junior programs, train race officers and coaches, and keep boats in the hands of kids who'd otherwise watch from the dock.</p>
<a class="btn" href="ayrc/">AYRC 2027</a><a class="btn o" href="#give">Support NESF</a></div></div>
<section><div class="in g4 st4"><div class="cd o st"><b>11</b><span>AYRC regattas in 2027</span></div><div class="cd o st"><b>{len(C)}</b><span>Member clubs and sailing centers</span></div><div class="cd o st"><b>19</b><span>Programs funded in 2026</span></div><div class="cd o st"><b>64</b><span>Loan boats in the pool</span></div></div></section>
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

def ayrc():
    today = datetime.date(2026, 11, 12)
    rows = ""
    for n, a in enumerate(AYRC, 1):
        d = datetime.date.fromisoformat(a[0]); d2 = d + datetime.timedelta(1)
        fin = n == len(AYRC)
        rows += f'<tr{" class=\"fin\"" if fin else ""}><td class="n">{n}</td><td>{d.strftime("%a %b %-d")} to {d2.strftime("%a %b %-d")}</td><td><b>{E(a[3])}</b><br><small>{E(a[4])}</small></td><td>{host_link(a, "../../")}<br><small>{E(a[2])}</small></td></tr>'
    seas = {"May": "Late spring", "Jun": "Late spring", "Jul": "Summer", "Aug": "Summer", "Sep": "Early fall"}
    stand = [("Albanardia City Yacht Club", 1412), ("Silverbrooks Yacht Club", 1388), ("Corinthian Yacht Club of Silverbrooks", 1240), ("Foxford Yacht Club", 1196), ("New Brolin Yacht Club", 1023),
             ("Northeastern Yacht Club", 954), ("Waterloo Yacht Club", 712), ("Cape Sturgeon Yacht Club", 640), ("Silverbrooks Community Sailing Center", 588), ("Pearl's End Sailing Center", 431),
             ("Hamilton Island Sailing", 377), ("Willamette Boating Center", 296), ("Coven Community Sailing", 241)]
    body = f"""<div class="hero"><div class="in"><div class="k">Northeastern Sailing Foundation presents</div><h1>Albanardia Youth Racing Circuit 2027</h1>
<p>Eleven regattas from late May to late September, from the Sound to the cape, with one road trip to Barnegat Bay. Race as many as you like; your best seven count. The Championship on Hanson Bay closes the season.</p>
<a class="btn" href="#schedule">Schedule</a><a class="btn o" href="#register">Register</a></div></div>
<section><div class="in g4 st4"><div class="cd o st"><b>11</b><span>Regattas, one per venue</span></div><div class="cd o st"><b>8</b><span>Fleets</span></div><div class="cd o st"><b>7</b><span>Best results count</span></div><div class="cd o st"><b>May 22</b><span>Opening day in Foxford</span></div></div></section>
<section class="alt" id="schedule"><div class="in"><h2>2027 schedule</h2><p class="sub">Every regatta is two days, with racing from 11 a.m. Saturday and a 3 p.m. last warning signal Sunday. Notices of race post 45 days before each event. Each venue hosts once a season.</p>
<div class="tw"><table><tr><th>#</th><th>Dates</th><th>Regatta</th><th>Host</th></tr>{rows}</table></div>
<p class="sub" style="margin-top:14px">{" · ".join(f"<b>{s}</b>: " + ", ".join(datetime.date.fromisoformat(a[0]).strftime("%b %-d") for a in AYRC if seas[datetime.date.fromisoformat(a[0]).strftime("%b")] == s) for s in ("Late spring", "Summer", "Early fall"))}</p></div></section>
<section id="classes"><div class="in"><h2>Fleets</h2><p class="sub">Sailors pick one fleet for the season and can move up once, before the July 10 regatta.</p><div class="g4">{''.join(f'<div class="cd"><b>{E(t)}</b><span>{E(d)}</span></div>' for t, d in AYRC_CLASSES)}</div>
<h3 style="margin-top:28px">Guest classes</h3><p class="sub">Host clubs can add guest fleets when five or more boats register. Guest classes race for regatta trophies but don't score in the season standings.</p><div class="ch">{''.join(f'<span>{E(g)}</span>' for g in AYRC_GUESTS)}</div></div></section>
<section class="alt" id="rules"><div class="in g2"><div><h2>Scoring</h2><ul class="l sub"><li>Low point scoring at each regatta, then circuit points: 100 for first, down by fleet size.</li><li>Your best 7 of 11 regattas count toward the season.</li><li>The AYRC Championship can't be dropped, and it scores 1.5 times.</li><li>Club team trophy: each club's best 12 sailor scores across all fleets.</li><li>Green Fleet isn't scored; every sailor who finishes three regattas gets a season pennant.</li></ul></div>
<div><h2>Eligibility</h2><ul class="l sub"><li>Under 19 on December 31, 2027 (Optimist and RS Feva: 15 and under).</li><li>A US Sailing youth membership and a member club, sailing center or high school team.</li><li>Sailors from outside Albanardia are welcome at every regatta, but only Albanardia sailors score in the season standings.</li><li>A swim test and a signed parent waiver, once per season.</li></ul></div></div></section>
<section id="register"><div class="in g2"><div><h2>Registration</h2><p class="sub">Season registration opens March 1, 2027: $60 per sailor, plus $55 per regatta ($35 for Green Fleet). Register by the Wednesday before each regatta; late entries pay $20 more. NESF grants cover fees for any sailor who asks, no questions.</p></div>
<div><h2>Charters</h2><p class="sub">Host clubs charter Optimists, ILCAs, C420s and Club FJs at $90 a boat per regatta. The NESF loan pool keeps season charters for sailors without boats. The Barnegat Bay stop has charter boats arranged through the host club.</p></div></div></section>
<section class="alt" id="standings"><div class="in"><h2>2026 club team standings</h2><p class="sub">Final standings for the club team trophy. Individual results are posted for each regatta by the host club.</p>
<div class="tw"><table><tr><th>Place</th><th>Club</th><th>Points</th></tr>{''.join(f'<tr><td class="n">{i}</td><td>{E(c)}</td><td>{p:,}</td></tr>' for i, (c, p) in enumerate(stand, 1))}</table></div></div></section>
<section><div class="in"><h2>News</h2><p class="sub"><a href="stories/">All AYRC stories →</a></p><div class="g3">{news('ayrc', '')}</div></div></section>"""
    return shell("nesf/ayrc", "AYRC 2027 | Albanardia Youth Racing Circuit", ANAV, body, "The Albanardia Youth Racing Circuit: eleven summer youth regattas around the state, run by NESF.")

if __name__ == "__main__":
    for p, h in (("nesf", nesf_home()), ("nesf/ayrc", ayrc())):
        o = ROOT / p / "index.html"; o.parent.mkdir(parents=True, exist_ok=True); o.write_text(h, encoding="utf-8")
    print("built nesf/ and nesf/ayrc/")
