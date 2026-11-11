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

CSS = """
:root{--c:@C;--ink:#14202c;--mut:#5c6672;--line:#e3e1da;--bg:#faf8f4;--card:#fff;--navy:#0f2340}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--ink:#eef1f4;--mut:#9ca6b2;--line:#2a323d;--bg:#0f141a;--card:#171e27}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Source Sans 3",system-ui,sans-serif}a{color:inherit}
.in{max-width:1120px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left))}
.tb{background:var(--navy);color:#cdd6e2;font-size:13px;padding-top:env(safe-area-inset-top)}.tb .in{display:flex;gap:16px;min-height:34px;align-items:center;white-space:nowrap;overflow-x:auto}.tb a{text-decoration:none}.tb .sp{flex:1}
header{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10}header .in{display:flex;align-items:center;gap:14px;min-height:72px}
.bg{width:58px;height:35px;flex:none;filter:drop-shadow(0 1px 1px rgba(0,0,0,.2))}
.nm b{display:block;font:700 19px/1.15 "Cormorant Garamond",Georgia,serif;letter-spacing:.2px}.nm small{color:var(--mut);font-size:12px;letter-spacing:1.5px;text-transform:uppercase}
nav{margin-left:auto;display:flex;gap:2px}nav a{text-decoration:none;font-weight:600;padding:9px 11px;border-radius:8px;font-size:15px}nav a:hover{background:rgba(0,0,0,.05)}
.hero{background:var(--navy);color:#fff;position:relative;overflow:hidden}.hero::after{content:"";position:absolute;inset:auto 0 0 0;height:8px;background:var(--c)}
.hero .in{display:grid;grid-template-columns:1.2fr 1fr;gap:30px;align-items:center;padding-top:60px;padding-bottom:64px}
.hero h1{font:600 clamp(38px,5.6vw,64px)/1.02 "Cormorant Garamond",Georgia,serif;margin:8px 0 12px}.hero p{font-size:18px;color:#d7dee8;max-width:46ch;margin:0 0 22px}
.k{font-size:12.5px;letter-spacing:2.5px;text-transform:uppercase;color:#aebbd0}
.flag{justify-self:center;width:min(380px,80vw);filter:drop-shadow(0 18px 30px rgba(0,0,0,.45));transform:rotate(-4deg)}
.btn{display:inline-block;background:#fff;color:var(--navy);font-weight:700;text-decoration:none;padding:12px 20px;border-radius:999px;margin:0 8px 8px 0}.btn.o{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.6)}
section{padding:56px 0}section.alt{background:var(--card);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
h2{font:600 clamp(30px,3.8vw,42px)/1.1 "Cormorant Garamond",Georgia,serif;margin:0 0 6px}.sub{color:var(--mut);margin:0 0 22px;max-width:60ch}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.cd{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px;border-top:4px solid var(--c)}
.cd b{display:block;font-size:18px;margin-bottom:4px}.cd span{color:var(--mut)}
.cal{display:grid;gap:10px}.ev{display:grid;grid-template-columns:76px 1fr auto;gap:14px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px}
.dt{background:var(--navy);color:#fff;border-radius:10px;text-align:center;padding:6px 0;line-height:1.1}.dt b{display:block;font-size:24px}.dt span{font-size:11px;letter-spacing:1px;text-transform:uppercase}
.ev h3{margin:0;font-size:17px}.ev p{margin:2px 0 0;color:var(--mut);font-size:14px}.tag{font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px;background:var(--c);color:#fff;white-space:nowrap}
.ch{display:flex;flex-wrap:wrap;gap:8px}.ch span{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:6px 12px;font-weight:600;font-size:14px}
.ct{display:grid;grid-template-columns:1fr 1fr;gap:24px}.ct div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px}
footer{background:var(--navy);color:#c3ccd8;padding:36px 0 calc(90px + env(safe-area-inset-bottom))}footer .in{display:flex;gap:16px;align-items:center;flex-wrap:wrap}footer a{text-decoration:none}footer .sp{flex:1}
@media (max-width:820px){nav{display:none}.hero .in,.ct{grid-template-columns:1fr}.g3{grid-template-columns:1fr}.flag{width:min(260px,70vw)}.ev{grid-template-columns:64px 1fr}.ev .tag{grid-column:2;justify-self:start}}
"""

def page(c, svg):
    cid, name, short, town, addr, web, kind, ayrc, blurb = c
    col = color(svg)
    flag = f'<svg viewBox="0 0 631 377" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'
    yc = kind == "yc"
    progs = ([("Junior racing team", f"Year-round coaching for the AYRC and high school regattas in {AYRC.split(', ')[0]}s, C420s and Optis."),
              ("Adult racing", "Wednesday night series, weekend regattas and a winter frostbite fleet."),
              ("Cruising and social", "Raft-ups, the commodore's ball and the summer cruise to Hamilton Island.")] if yc else
             [("Learn to sail", "Weekend classes for adults and summer camps for kids, no experience needed."),
              ("Youth programs", "Opti, Club Radial and Larssen Fyra programs that grow into racing teams."),
              ("Rentals and memberships", "Take a boat out by the hour once you've passed a checkout sail.")])
    events = [("Jan","11","Frostbite Series opens","Every Sunday through March","Racing"),
              ("Apr","18","First Water","Boat blessing and the first race of the season","Club"),
              ("Jun","20","Midsummer Regatta","One-design racing and a dock party","Racing"),
              ("Jul","8","AYRC stop" if ayrc else "Junior Regatta",("Albanardia Youth Racing Circuit, classes: "+AYRC) if ayrc else "Youth one-design racing","Youth"),
              ("Aug","14","Harbor Week","Tall ships, the tug race and the Harbor Week regatta","Club")]
    cal = "".join(f'<div class="ev"><div class="dt"><b>{d}</b><span>{m} 2027</span></div><div><h3>{E(t)}</h3><p>{E(p)}</p></div><span class="tag">{E(tg)}</span></div>' for m,d,t,p,tg in events)
    fleet = (["ILCA","C420","Optimist","Club FJ","RS Feva","29er","J/24"] if yc else ["Larssen Club Radial","Larssen Fyra","Larssen Pulse XL","Optimist","Larssen Voyage","Kayaks and SUPs"])
    body = f"""
<div class="tb"><div class="in"><a href="../../">Albanardia.gov</a><a href="../">All clubs</a><span class="sp"></span><a href="#calendar">Calendar</a><a href="#join">Join</a><a href="#contact">Contact</a></div></div>
<header><div class="in"><div class="bg">{flag}</div><div class="nm"><b>{E(name)}</b><small>{E(short)} · {E(town)}</small></div>
<nav><a href="#programs">Programs</a><a href="#news">News</a><a href="#calendar">Calendar</a><a href="#fleet">Fleet</a><a href="#join">Membership</a><a href="#contact">Contact</a></nav></div></header>
<div class="hero"><div class="in"><div><div class="k">{'Yacht club' if yc else 'Community sailing'} · {E(town)}, Albanardia</div><h1>{E(name)}</h1><p>{E(blurb)}{' An AYRC member club.' if ayrc else ''}</p>
<a class="btn" href="#join">{'Become a member' if yc else 'Sign up for a class'}</a><a class="btn o" href="#calendar">Racing calendar</a></div><div class="flag">{flag}</div></div></div>
<section id="programs"><div class="in"><h2>Programs</h2><p class="sub">{'Racing, juniors and the social side of the club.' if yc else 'Sailing for everyone, whatever your age or experience.'}</p><div class="g3">{''.join(f'<div class="cd"><b>{E(a)}</b><span>{E(b)}</span></div>' for a,b in progs)}</div></div></section>
<section class="alt" id="calendar"><div class="in"><h2>2027 calendar</h2><p class="sub">Highlights of the season. Full notices of race and sailing instructions go out before each event.</p><div class="cal">{cal}</div></div></section>
<section id="news"><div class="in"><h2>News</h2><p class="sub">From the club. <a href="stories/">All stories →</a></p><div class="g3">{''.join(f'<a class="cd" href="stories/#{n["slug"]}" style="color:inherit;text-decoration:none"><small style="color:var(--mut);font-weight:700;text-transform:uppercase;letter-spacing:.6px;font-size:12px">{E(n["cat"])} · {fdate(n["date"])}</small><b>{E(n["title"])}</b><span>{E(n["dek"])}</span></a>' for n in latest("club:" + slug(c), 3))}</div></div></section>
<section id="fleet"><div class="in"><h2>{'Fleets' if yc else 'Our boats'}</h2><p class="sub">{'One-design fleets that race at the club.' if yc else 'Boats available for classes and members.'}</p><div class="ch">{''.join(f'<span>{E(f)}</span>' for f in fleet)}</div></div></section>
<section class="alt" id="join"><div class="in"><h2>{'Membership' if yc else 'Join'}</h2><div class="g3">{''.join(f'<div class="cd"><b>{E(a)}</b><span>{E(b)}</span></div>' for a,b in ([("Junior","Ages 8 to 18, includes the junior program."),("Young adult","Ages 19 to 30, full racing privileges."),("Family","Everyone in the household, plus a guest slip.")] if yc else [("Class pass","Pay per class or camp week."),("Sailor membership","Unlimited rentals after a checkout sail."),("Family membership","Rentals and member pricing for the household.")]))}</div></div></section>
<section id="contact"><div class="in ct"><div><h2>Visit</h2><p>{E(addr)}</p><p><a href="../../map/">Open in the Albanardia map →</a></p></div><div><h2>Contact</h2><p>{E(web)}</p><p>Office hours: Tue to Sun, 9 to 5.</p></div></div></section>
<footer><div class="in"><span class="bg">{flag}</span><span>{E(name)}</span><span class="sp"></span><a href="../">All Albanardia clubs</a><a href="../../">Albanardia.gov</a></div></footer>"""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(name)}</title><link rel="manifest" href="../../manifest.json"><link rel="apple-touch-icon" href="../../icons/icon-180.png"><meta name="theme-color" content="#0f2340">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS.replace('@C', col)}</style></head><body>{body}<script src="../../app/app.js" data-home="float"></script></body></html>"""

def slug(c): return c[2].lower() if c[0] not in ("WYC-W", "WYC-Wil") else ("waterloo-yc" if c[0] == "WYC-W" else "willamette-bc")

def index(F):
    cards = "".join(f'<a class="cl" href="{slug(c)}/"><span class="bg"><svg viewBox="0 0 631 377">{F[c[0]]}</svg></span><span><b>{E(c[1])}</b><small>{E(c[3])}{" · AYRC" if c[7] else ""}</small></span></a>' for c in C)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Yacht Clubs & Sailing Centers | Albanardia.gov</title><link rel="manifest" href="../manifest.json"><link rel="icon" href="../icons/favicon.png"><meta name="theme-color" content="#22498a">
<style>:root{{--bg:#f4f5f7;--card:#fff;--ink:#1b2430;--mut:#5b6573;--line:#dde1e7;--navy:#22498a}}@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#0f141a;--card:#18202a;--ink:#edf1f5;--mut:#9ba7b3;--line:#2a3441}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,sans-serif}}.gov{{background:#0b1d3a;color:#cfd8e6;font-size:12.5px;padding:6px 16px}}
header{{background:var(--navy);color:#fff;padding:26px 16px}}header .in,main{{max-width:1120px;margin:0 auto}}header a{{color:#cfd8e6;font-size:14px}}header h1{{font:700 34px/1.1 Georgia,serif;margin:8px 0 4px}}main{{padding:20px 16px 90px}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}}.cl{{display:flex;gap:14px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;text-decoration:none;color:var(--ink)}}
.bg{{width:62px;height:37px;flex:none}}.bg svg{{width:100%;height:100%}}.cl b{{display:block}}.cl small{{color:var(--mut)}}p.n{{color:var(--mut)}}</style></head><body>
<div class="gov">An official website of the State of Albanardia</div><header><div class="in"><a href="../">← Albanardia.gov</a><h1>Yacht Clubs &amp; Sailing Centers</h1><div>{len(C)} clubs and centers across the Windward State. AYRC clubs host the Albanardia Youth Racing Circuit, run by the Northeastern Sailing Foundation.</div></div></header>
<main><div class="g">{cards}</div><p class="n">Also on the water: the Killalea Sailing Center on Hanson Bay, the Maldonado Boathouse, the Olympic Sailing Pavilion and the James L. Gore Sailing Pavilion in New Brolin.</p></main>
<script src="../app/app.js" data-home="float"></script></body></html>"""

if __name__ == "__main__":
    F = flags()
    for c in C:
        d = OUT / slug(c); d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(c, F[c[0]]), encoding="utf-8")
    (OUT / "index.html").write_text(index(F), encoding="utf-8")
    print("built", len(C), "club sites")
