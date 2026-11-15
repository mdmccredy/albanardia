#!/usr/bin/env python3
"""Silverbrooks Sailing Foundation (sbsf/, "sbsf.org"): the nonprofit behind Silverbrooks Yacht Club and the
Silverbrooks Community Sailing Center. Logo files in sbsf/img/ (Max's branding); burgees from brand/burgees/.
Photos come from tools/photos.py. Run: python3 tools/build_sbsf.py"""
import html, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import photos as PHT
E = html.escape

def PF(name): return next(x for L in PHT.PH.values() for x in L if x[0] == name)

NAV = [("", "Home"), ("our-work/", "Our Work"), ("impact/", "Impact"), ("about/", "About"), ("give/", "Give")]

CSS = """
:root{--navy:#0a2747;--blue:#0451ab;--red:#c40000;--gold:#ffc200;--ivory:#faf7f0;--ink:#16202c;--mut:#5b6573;--line:#e4ddcc;--card:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--ivory);color:var(--ink);font:400 17px/1.65 'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--blue)}img{max-width:100%}
h1,h2,h3,.serif{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;letter-spacing:.2px;line-height:1.1;color:var(--navy)}
h1{font-size:clamp(40px,6vw,74px);margin:0 0 18px}h2{font-size:clamp(32px,4vw,48px);margin:0 0 12px}h3{font-size:26px;margin:0 0 8px}
.in{max-width:1180px;margin:0 auto;padding:0 24px}
.eyebrow{font:600 12px/1 'Inter',sans-serif;letter-spacing:3px;text-transform:uppercase;color:var(--red);margin:0 0 16px}
.rule{width:64px;height:2px;background:var(--gold);margin:18px 0 22px;border:0}
.lede{font-size:20px;color:var(--mut);max-width:680px}
header.top{position:sticky;top:0;z-index:20;background:rgba(250,247,240,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
header.top .in{display:flex;align-items:center;gap:22px;height:78px}
.brand{display:flex;align-items:center;gap:14px;text-decoration:none;margin-right:auto}
.brand img.m{height:40px;width:auto}.brand img.w{height:30px;width:auto}
nav.main a{font:500 14px/1 'Inter',sans-serif;letter-spacing:.6px;color:var(--ink);text-decoration:none;padding:10px 12px;border-radius:6px}
nav.main a:hover,nav.main a.on{color:var(--blue)}nav.main a.on{box-shadow:inset 0 -2px 0 var(--gold);border-radius:0}
.btn{display:inline-block;font:600 14px/1 'Inter',sans-serif;letter-spacing:1.2px;text-transform:uppercase;text-decoration:none;padding:16px 26px;border-radius:2px;border:1px solid transparent;transition:.2s}
.btn.gold{background:var(--gold);color:var(--navy)}.btn.gold:hover{background:#ffd447}
.btn.line{border-color:rgba(255,255,255,.7);color:#fff}.btn.line:hover{background:#fff;color:var(--navy)}
.btn.navy{background:var(--navy);color:#fff}.btn.navy:hover{background:var(--blue)}
nav.main a.give{background:var(--navy);color:#fff;padding:12px 18px;border-radius:2px;margin-left:6px;box-shadow:none}
nav.main a.give:hover{background:var(--red);color:#fff}
#mt{display:none;background:none;border:0;font-size:26px;color:var(--navy);cursor:pointer}
.hero{position:relative;min-height:min(88vh,760px);display:flex;align-items:flex-end;color:#fff;background-size:cover;background-position:center}
.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,39,71,.15) 0%,rgba(10,39,71,.55) 55%,rgba(10,39,71,.92) 100%)}
.hero .in{position:relative;padding-bottom:84px;padding-top:120px;width:100%}
.hero h1{color:#fff;max-width:900px}.hero .eyebrow{color:var(--gold)}.hero p{font-size:21px;max-width:640px;color:#e8eef7;margin:0 0 30px}
.hero .btn{margin:0 10px 10px 0}
.hero a.cr,.ph a.cr,.hero span.cr{top:auto;bottom:12px;right:14px;position:absolute}
.page-hero{min-height:440px}
section{padding:96px 0}section.tight{padding:64px 0}
.alt{background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.dark{background:var(--navy);color:#dbe4f0}.dark h2,.dark h3{color:#fff}.dark .eyebrow{color:var(--gold)}.dark a{color:var(--gold)}
.split{display:grid;grid-template-columns:1.05fr 1fr;gap:64px;align-items:center}
.quote{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:clamp(26px,3vw,38px);line-height:1.3;color:var(--navy);margin:0;max-width:900px}
.quote cite{display:block;margin-top:18px;font:600 12px/1 'Inter',sans-serif;letter-spacing:2.5px;text-transform:uppercase;font-style:normal;color:var(--red)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-top:1px solid rgba(255,255,255,.18)}
.stats div{padding:34px 26px 6px;border-right:1px solid rgba(255,255,255,.18)}.stats div:last-child{border-right:0}
.stats b{display:block;font:600 clamp(40px,5vw,62px)/1 'Cormorant Garamond',serif;color:#fff}.stats span{display:block;margin-top:10px;font-size:14px;letter-spacing:.4px;color:#b9c7da}
.stats.light{border-color:var(--line)}.stats.light div{border-color:var(--line)}.stats.light b{color:var(--navy)}.stats.light span{color:var(--mut)}
.clubs{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.club{background:var(--card);border:1px solid var(--line);padding:40px;text-decoration:none;color:inherit;transition:.25s;display:flex;flex-direction:column}
.club:hover{transform:translateY(-3px);box-shadow:0 18px 40px rgba(10,39,71,.12);border-color:var(--gold)}
.club img.b{height:96px;width:auto;margin-bottom:26px;align-self:flex-start;filter:drop-shadow(0 4px 6px rgba(0,0,0,.12))}
.club p{color:var(--mut);margin:0 0 22px}.club .more{margin-top:auto;font:600 13px/1 'Inter',sans-serif;letter-spacing:1.5px;text-transform:uppercase;color:var(--blue)}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.prog{background:var(--card);border:1px solid var(--line);display:flex;flex-direction:column}
.prog .ph{position:relative;aspect-ratio:4/3;overflow:hidden;background:#d8dde4}.prog .ph img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s}
.prog:hover .ph img{transform:scale(1.04)}
.prog .tx{padding:26px 28px 30px}.prog p{color:var(--mut);margin:0;font-size:16px}
.prog .tag{font:600 11px/1 'Inter',sans-serif;letter-spacing:2px;text-transform:uppercase;color:var(--red);margin-bottom:12px;display:block}
.photo{position:relative;overflow:hidden;aspect-ratio:4/5;background:#d8dde4}.photo img{width:100%;height:100%;object-fit:cover;display:block}
.photo.wide{aspect-ratio:3/2}
.cta{text-align:center}.cta img{width:min(420px,80%);margin:0 auto 26px;display:block}.cta p{max-width:620px;margin:0 auto 30px;font-size:19px}
.tiers{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.tier{background:var(--card);border:1px solid var(--line);border-top:3px solid var(--gold);padding:30px 26px}
.tier .amt{font:600 38px/1 'Cormorant Garamond',serif;color:var(--navy);margin:8px 0 12px}.tier p{color:var(--mut);font-size:15px;margin:0}
.tier.top{background:var(--navy);color:#cfdbea;border-top-color:var(--red)}.tier.top h3,.tier.top .amt{color:#fff}.tier.top p{color:#cfdbea}
.ways{display:grid;grid-template-columns:repeat(2,1fr);gap:28px}
.way{border-left:2px solid var(--gold);padding:4px 0 4px 24px}.way p{color:var(--mut);margin:6px 0 0}
.bars .row{display:grid;grid-template-columns:200px 1fr 70px;gap:16px;align-items:center;margin:14px 0;font-size:15px}
.bars .track{height:12px;background:#ece6d6}.bars .fill{height:12px;background:var(--blue)}.bars .fill.r{background:var(--red)}.bars .fill.g{background:var(--gold)}
.people{display:grid;grid-template-columns:repeat(3,1fr);gap:22px 40px}
.person b{display:block;font:600 22px/1.2 'Cormorant Garamond',serif;color:var(--navy)}.person span{color:var(--mut);font-size:15px}
.timeline{border-left:1px solid var(--line);margin-left:8px}
.ev{position:relative;padding:0 0 34px 34px}.ev::before{content:"";position:absolute;left:-6px;top:8px;width:11px;height:11px;background:var(--gold);transform:rotate(45deg)}
.ev .yr{font:600 30px/1 'Cormorant Garamond',serif;color:var(--red)}.ev p{margin:6px 0 0;color:var(--mut)}
footer{background:#071c34;color:#9fb0c6;padding:72px 0 40px;font-size:15px}
footer .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:40px}
footer img.lg{width:260px;margin-bottom:18px}footer h4{font:600 12px/1 'Inter',sans-serif;letter-spacing:2.5px;text-transform:uppercase;color:var(--gold);margin:6px 0 16px}
footer a{color:#dbe4f0;text-decoration:none;display:block;margin:0 0 10px}footer a:hover{color:#fff}
footer .burgees{display:flex;gap:14px;margin-top:6px}footer .burgees img{height:38px;width:auto}
footer .base{border-top:1px solid rgba(255,255,255,.12);margin-top:48px;padding-top:24px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;font-size:13px}
.reveal{opacity:0;transform:translateY(18px);transition:opacity .8s ease,transform .8s ease}.reveal.vis{opacity:1;transform:none}
@media (max-width:980px){.split,.clubs,.ways{grid-template-columns:1fr;gap:36px}.grid3,.tiers,.people{grid-template-columns:1fr 1fr}.stats{grid-template-columns:1fr 1fr}.stats div:nth-child(2){border-right:0}
 footer .cols{grid-template-columns:1fr 1fr}.bars .row{grid-template-columns:130px 1fr 54px}}
@media (max-width:760px){#mt{display:block}nav.main{display:none;position:absolute;top:78px;left:0;right:0;background:var(--ivory);border-bottom:1px solid var(--line);padding:10px 16px 18px;flex-direction:column}
 nav.main.open{display:flex}nav.main a{padding:14px 8px}nav.main a.give{margin:8px 0 0;text-align:center}.brand img.w{display:none}
 .grid3,.tiers,.people{grid-template-columns:1fr}section{padding:68px 0}.hero .in{padding-bottom:56px}}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}*{scroll-behavior:auto}}
"""

JS = """<script>(function(){var b=document.getElementById('mt'),n=document.querySelector('nav.main');if(b)b.onclick=function(){n.classList.toggle('open')};
var els=document.querySelectorAll('.reveal');if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('vis')});return}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}})},{threshold:.12});els.forEach(function(e){io.observe(e)})})();</script>"""

def shell(path, title, desc, body):
    depth = path.count("/") + 1 if path else 1
    r = "../" * depth          # to the repo root
    s = "../" * (depth - 1)    # to sbsf/
    here = path[5:] + "/" if path != "sbsf" else ""
    nav = "".join(f'<a href="{s}{h}"{' class="give"' if h == "give/" else (' class="on"' if h == here else "")}>{E(t)}</a>' for h, t in NAV)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#0a2747">
<link rel="manifest" href="{r}manifest.json"><link rel="icon" href="{s}img/sbsf-icon.png"><link rel="apple-touch-icon" href="{r}icons/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}{PHT.CSS}</style></head><body>
<header class="top"><div class="in"><a class="brand" href="{s}"><img class="m" src="{s}img/sbsf-mark.png" alt=""><img class="w" src="{s}img/sbsf-wordmark.png" alt="Silverbrooks Sailing Foundation"></a>
<button id="mt" aria-label="Menu">&#9776;</button><nav class="main">{nav}</nav></div></header>
{body.replace("@S@", s).replace("@R@", r)}
<footer><div class="in"><div class="cols">
<div><img class="lg" src="{s}img/sbsf-logo-white.png" alt="Silverbrooks Sailing Foundation"><p>Keeping Silverbrooks on the water since 1958. A 501(c)(3) nonprofit; gifts are tax-deductible as allowed by law.</p>
<div class="burgees"><a href="{r}sbyc/" title="Silverbrooks Yacht Club"><img src="{r}brand/burgees/sbyc.svg" alt="SBYC burgee"></a><a href="{r}sbcs/" title="Silverbrooks Community Sailing Center"><img src="{r}brand/burgees/sbcs.svg" alt="SBCS burgee"></a></div></div>
<div><h4>Foundation</h4><a href="{s}our-work/">Our work</a><a href="{s}impact/">2026 impact</a><a href="{s}about/">About &amp; leadership</a><a href="{s}give/">Ways to give</a></div>
<div><h4>Our clubs</h4><a href="{r}sbyc/">Silverbrooks Yacht Club</a><a href="{r}sbcs/">Community Sailing Center</a><a href="{r}nesf/ayrc/">Youth Racing Circuit</a><a href="{r}clubs/">All Albanardia clubs</a></div>
<div><h4>Visit</h4><p style="margin:0 0 10px">231 NE Belwether St, 2nd floor<br>Silverbrooks, AB 19001</p><p style="margin:0">info@sbsf.org<br>Office open weekdays 9 to 5</p></div>
</div><div class="base"><span>&copy; 2026 Silverbrooks Sailing Foundation · sbsf.org</span><span>A fictional organization in the world of Albanardia</span></div></div></footer>
{JS}<script src="{r}app/app.js" data-home="float"></script></body></html>"""

def img(p, w=1100, alt=""):
    return f'<img src="{PHT.url(p[0], w)}" alt="{E(alt)}" loading="lazy">{PHT.credit(p)}'

def hero_bg(p, w=2000): return f"background-image:url('{PHT.url(p[0], w)}')"

PROGRAMS = [
 ("Scholarships", "Junior Sailing Scholarships", "Need-based awards that cover camp, team dues and regatta travel. No sailor at SBYC or SBCS is turned away for cost.", "max/wind-dsc-2189.jpg"),
 ("Fleet", "Boat & Equipment Fund", "New Optimists, C420s, ILCAs and Larssen trainers for both clubs, plus sails, life jackets and coach boats.", "max/tb-20251122-202857818-ios.jpg"),
 ("Community", "Free Sail Saturdays", "Every summer Saturday the Community Sailing Center opens its docks: free rides and first lessons for anyone in the city.", "max/br-cyc-fj-downwind-1.jpg"),
 ("Access", "Adaptive Sailing", "Keel-equipped Larssen Alegria XS boats, lift-assisted docks and trained volunteers so sailors of every ability can take the helm.", "max/cd-20250330-190347449-ios.jpg"),
 ("Coaching", "Coach & Instructor Pathway", "Paid US Sailing Level 1 and 2 courses for teenage instructors, who then teach the next summer's campers.", "max/wind-dsc-0958.jpg"),
 ("Racing", "Racing Team Travel", "Travel grants for the SBYC and SBCS racing teams on the AYRC and beyond, and hosting support for the Hanson Bay Showdown.", "max/wind-dsc-1196.jpg"),
]

def home():
    hp = PF("max/br-cyc-fj-downwind-1.jpg")
    progs = "".join(f'<a class="prog reveal" href="@S@our-work/#p{i}" style="text-decoration:none;color:inherit"><div class="ph">{img(PF(f), 900, t)}</div><div class="tx"><span class="tag">{E(tag)}</span><h3>{E(t)}</h3><p>{E(d)}</p></div></a>' for i, (tag, t, d, f) in enumerate(PROGRAMS[:3]))
    body = f"""<div class="hero" style="{hero_bg(hp)}">{PHT.credit(hp)}<div class="in"><p class="eyebrow">The Silverbrooks Sailing Foundation</p>
<h1>Keeping Silverbrooks on the water since 1958.</h1><p>We fund the boats, the coaches and the scholarships behind Silverbrooks Yacht Club and the Silverbrooks Community Sailing Center, so every kid in the city can learn to sail.</p>
<a class="btn gold" href="@S@give/">Make a gift</a><a class="btn line" href="@S@our-work/">See our work</a></div></div>
<section><div class="in split"><div class="reveal"><p class="eyebrow">Our mission</p><h2>Sailing belongs to the whole city.</h2><hr class="rule">
<p class="lede">The Foundation began in 1958, when a few Silverbrooks Yacht Club members passed a hat to buy six Optimists for the junior program. Today it is the nonprofit home of two clubs: one at the end of Hanson Bay Marina, one open to everyone on Foundland Street.</p>
<p><a class="btn navy" href="@S@about/">Our story</a></p></div>
<div class="photo reveal">{img(PF("max/wind-dsc-1298.jpg"), 1100, "ILCA fleet at the start")}</div></div></section>
<section class="dark tight"><div class="in"><p class="eyebrow">2026 at a glance</p><div class="stats">
<div><b>2,400</b><span>sailors on the water</span></div><div><b>$612K</b><span>in scholarships awarded</span></div><div><b>41%</b><span>of SBCS juniors sailed on scholarship</span></div><div><b>38</b><span>boats bought or rebuilt</span></div></div>
<p style="margin:30px 0 0"><a href="@S@impact/">Read the 2026 impact report →</a></p></div></section>
<section><div class="in"><p class="eyebrow">Two clubs, one foundation</p><h2>Where your gift goes sailing</h2><hr class="rule"><div class="clubs">
<a class="club reveal" href="@R@sbyc/"><img class="b" src="@R@brand/burgees/sbyc.svg" alt="SBYC burgee"><h3>Silverbrooks Yacht Club</h3><p>At the outer end of Hanson Bay Marina on the north shore. Junior racing, summer camps and the home of the Hanson Bay Showdown, the AYRC Championship.</p><span class="more">Visit SBYC →</span></a>
<a class="club reveal" href="@R@sbcs/"><img class="b" src="@R@brand/burgees/sbcs.svg" alt="SBCS burgee"><h3>Silverbrooks Community Sailing Center</h3><p>Public sailing for the whole city on Foundland Street, from first sails and adaptive programs to a racing team. Opened by the Foundation in 1994.</p><span class="more">Visit SBCS →</span></a>
</div></div></section>
<section class="alt"><div class="in"><p class="eyebrow">What we fund</p><h2>Programs</h2><hr class="rule"><div class="grid3">{progs}</div>
<p style="margin:34px 0 0"><a class="btn navy" href="@S@our-work/">All six programs</a></p></div></section>
<section><div class="in"><blockquote class="quote reveal">"I learned to sail on a Foundation scholarship at the Community Sailing Center. Ten years later I coach there."<cite>Priya Natarajan · SBCS head coach</cite></blockquote></div></section>
<section class="dark cta"><div class="in"><img src="@S@img/sbsf-logo-white.png" alt=""><h2>Put a kid in a boat this summer.</h2><p>$450 sends one sailor to a week of camp. Every gift stays in Silverbrooks.</p><a class="btn gold" href="@S@give/">Give today</a></div></section>"""
    return shell("sbsf", "Silverbrooks Sailing Foundation", "The Silverbrooks Sailing Foundation funds Silverbrooks Yacht Club and the Silverbrooks Community Sailing Center: scholarships, boats, coaching and free community sailing.", body)

def our_work():
    hp = PF("max/wind-dsc-1196.jpg")
    rows = ""
    for i, (tag, t, d, f) in enumerate(PROGRAMS):
        ph = f'<div class="photo wide reveal">{img(PF(f), 1200, t)}</div>'
        tx = f'<div class="reveal"><p class="eyebrow">{E(tag)}</p><h2>{E(t)}</h2><hr class="rule"><p class="lede">{E(d)}</p></div>'
        rows += f'<section id="p{i}" class="{"alt" if i % 2 else ""}"><div class="in split">{(ph + tx) if i % 2 == 0 else (tx + ph)}</div></section>'
    body = f"""<div class="hero page-hero" style="{hero_bg(hp)}">{PHT.credit(hp)}<div class="in"><p class="eyebrow">Our work</p><h1>Six programs, one goal.</h1><p>Every dollar the Foundation raises goes to sailors at Silverbrooks Yacht Club and the Silverbrooks Community Sailing Center.</p></div></div>{rows}
<section class="dark cta"><div class="in"><h2>Fund a program</h2><p>Gifts can go to the Annual Fund or straight to any one of these programs.</p><a class="btn gold" href="@S@give/">Ways to give</a></div></section>"""
    return shell("sbsf/our-work", "Our Work | Silverbrooks Sailing Foundation", "Scholarships, boats, free community sailing, adaptive sailing, coach training and racing team travel.", body)

def impact():
    hp = PF("max/wind-dsc-1844.jpg")
    uses = [("Scholarships", 41, ""), ("Boats & equipment", 24, "r"), ("Coaching & instruction", 12, "g"), ("Community & adaptive", 7, ""), ("Racing travel", 5, "r"), ("Fundraising", 7, "g"), ("Administration", 4, "")]
    bars = "".join(f'<div class="row"><span>{E(n)}</span><div class="track"><div class="fill {c}" style="width:{p*2.2}%"></div></div><b>{p}%</b></div>' for n, p, c in uses)
    body = f"""<div class="hero page-hero" style="{hero_bg(hp)}">{PHT.credit(hp)}<div class="in"><p class="eyebrow">2026 impact report</p><h1>A record summer on the water.</h1><p>The 2026 season, by the numbers.</p></div></div>
<section><div class="in"><div class="stats light">
<div><b>2,400</b><span>sailors on the water across both clubs</span></div><div><b>$612K</b><span>in scholarships to 389 sailors</span></div><div><b>1,150</b><span>free seats at Free Sail Saturdays</span></div><div><b>26</b><span>teen instructors certified</span></div></div></div></section>
<section class="alt"><div class="in split"><div class="reveal"><p class="eyebrow">Where the money went</p><h2>89 cents of every dollar goes to sailing.</h2><hr class="rule"><p class="lede">Total 2026 spending: $1.48 million. Fundraising and administration together stayed under 11 percent.</p></div>
<div class="bars reveal">{bars}</div></div></section>
<section><div class="in split"><div class="photo reveal">{img(PF("max/tb-20251122-202903964-ios.jpg"), 1100, "ILCA sailor hiking")}</div>
<div class="reveal"><p class="eyebrow">Highlights</p><h2>The season in brief</h2><hr class="rule">
<div class="timeline"><div class="ev"><div class="yr">Spring</div><p>12 new C420s and 8 ILCAs delivered to SBYC; 10 Larssen Fyras to the Community Sailing Center.</p></div>
<div class="ev"><div class="yr">Summer</div><p>Free Sail Saturdays sold out 11 of 12 weeks. The adaptive program doubled to two Alegria XS boats.</p></div>
<div class="ev"><div class="yr">Fall</div><p>SBYC sailors swept the top two places in both ILCA fleets on the AYRC, and SBYC hosted the Hanson Bay Showdown.</p></div></div></div></div></section>"""
    return shell("sbsf/impact", "2026 Impact | Silverbrooks Sailing Foundation", "The Silverbrooks Sailing Foundation's 2026 impact report: sailors, scholarships and where the money went.", body)

def about():
    hp = PF("max/cd-20250330-190347449-ios.jpg")
    board = [("Eleanor Whitcombe", "Chair"), ("Marcus Okafor", "Vice Chair"), ("Diane Ferreira", "Treasurer"), ("Thomas Hale", "Secretary"), ("Commodore, SBYC", "Ex officio"), ("Director, SBCS", "Ex officio")]
    staff = [("Margaret Holloway", "Executive Director"), ("Sam Whitaker", "Director of Development"), ("Lena Brandt", "Programs & Scholarships Manager")]
    pp = lambda L: "".join(f'<div class="person"><b>{E(n)}</b><span>{E(r)}</span></div>' for n, r in L)
    body = f"""<div class="hero page-hero" style="{hero_bg(hp)}">{PHT.credit(hp)}<div class="in"><p class="eyebrow">About the Foundation</p><h1>Since 1958.</h1><p>Two clubs, one nonprofit, and nearly seventy years of getting Silverbrooks out on the bay.</p></div></div>
<section><div class="in split"><div class="reveal"><p class="eyebrow">Our story</p><h2>From six Optimists to two clubs</h2><hr class="rule">
<div class="timeline"><div class="ev"><div class="yr">1958</div><p>Silverbrooks Yacht Club members found the SBYC Junior Fund and buy six Optimists.</p></div>
<div class="ev"><div class="yr">1976</div><p>The fund becomes an independent nonprofit and takes the name Silverbrooks Sailing Foundation.</p></div>
<div class="ev"><div class="yr">1994</div><p>The Foundation opens the Silverbrooks Community Sailing Center on Foundland Street, open to everyone.</p></div>
<div class="ev"><div class="yr">2011</div><p>Adaptive sailing launches with the first keel-equipped trainer and a lift dock.</p></div>
<div class="ev"><div class="yr">2026</div><p>A record 2,400 sailors across both clubs, and $612,000 in scholarships.</p></div></div></div>
<div class="photo reveal">{img(PF("max/fleet-lake.jpg"), 1100, "Dinghy fleet on the lake")}</div></div></section>
<section class="alt"><div class="in"><p class="eyebrow">Leadership</p><h2>Board of Trustees</h2><hr class="rule"><div class="people">{pp(board)}</div>
<h2 style="margin-top:64px">Staff</h2><hr class="rule"><div class="people">{pp(staff)}</div></div></section>
<section><div class="in split"><div><p class="eyebrow">Our clubs</p><h2>The Foundation family</h2><hr class="rule"><p class="lede">Silverbrooks Yacht Club and the Silverbrooks Community Sailing Center run their own programs and keep their own burgees. The Foundation owns the boats, funds the scholarships and raises the money for both.</p></div>
<div class="clubs"><a class="club" href="@R@sbyc/"><img class="b" src="@R@brand/burgees/sbyc.svg" alt="SBYC burgee"><h3>SBYC</h3><span class="more">silverbrooksyc.org →</span></a>
<a class="club" href="@R@sbcs/"><img class="b" src="@R@brand/burgees/sbcs.svg" alt="SBCS burgee"><h3>SBCS</h3><span class="more">sbcommunitysailing.org →</span></a></div></div></section>"""
    return shell("sbsf/about", "About | Silverbrooks Sailing Foundation", "History, trustees and staff of the Silverbrooks Sailing Foundation, the nonprofit behind SBYC and SBCS.", body)

def give():
    hp = PF("max/wind-dsc-2508.jpg")
    tiers = [("Pennant", "$250", "Sends a beginner to two weeks of Free Sail lessons and first-sail gear.", ""),
             ("Burgee", "$1,000", "A full summer of camp for one scholarship sailor.", ""),
             ("Ensign", "$5,000", "A new Optimist or Larssen Fyra, with a plaque on the transom.", ""),
             ("Commodore's Circle", "$25,000+", "Underwrites a program for a season and an invitation to the Commodore's Dinner.", "top")]
    tt = "".join(f'<div class="tier {c} reveal"><h3>{E(n)}</h3><div class="amt">{E(a)}</div><p>{E(d)}</p></div>' for n, a, d, c in tiers)
    ways = [("Annual Fund", "Unrestricted gifts go where the need is greatest each season."), ("Name a boat", "Fund a new C420, ILCA or trainer and choose the name on its transom."),
            ("Scholarship endowment", "Endow a named scholarship that sends a sailor to camp every year, forever."), ("Planned giving", "Leave a legacy through your will, a trust or a retirement account."),
            ("Gear drive", "Donate gently used boats, sails, wetsuits and life jackets to either club."), ("Volunteer", "Free Sail Saturdays, regatta race committee and the adaptive program all run on volunteers.")]
    ww = "".join(f'<div class="way reveal"><h3>{E(n)}</h3><p>{E(d)}</p></div>' for n, d in ways)
    body = f"""<div class="hero page-hero" style="{hero_bg(hp)}">{PHT.credit(hp)}<div class="in"><p class="eyebrow">Give</p><h1>Every gift stays in Silverbrooks.</h1><p>Join the Burgee Society and keep two clubs on the water.</p><a class="btn gold" href="#ways">Ways to give</a></div></div>
<section><div class="in"><p class="eyebrow">The Burgee Society</p><h2>Annual giving levels</h2><hr class="rule"><div class="tiers">{tt}</div></div></section>
<section class="alt" id="ways"><div class="in"><p class="eyebrow">Ways to give</p><h2>More than one way to help</h2><hr class="rule"><div class="ways">{ww}</div></div></section>
<section class="dark cta"><div class="in"><img src="@S@img/sbsf-logo-white.png" alt=""><h2>Make your gift</h2><p>Mail a check to the Silverbrooks Sailing Foundation, 231 NE Belwether St, Silverbrooks, AB 19001, or email gifts@sbsf.org and the development team will be in touch.</p></div></section>"""
    return shell("sbsf/give", "Give | Silverbrooks Sailing Foundation", "Join the Burgee Society: annual giving levels, naming a boat, scholarship endowments and planned giving.", body)

if __name__ == "__main__":
    for p, h in (("sbsf", home()), ("sbsf/our-work", our_work()), ("sbsf/impact", impact()), ("sbsf/about", about()), ("sbsf/give", give())):
        d = ROOT / p; d.mkdir(parents=True, exist_ok=True); (d / "index.html").write_text(h)
    print("built sbsf/ (5 pages)")
