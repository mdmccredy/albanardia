#!/usr/bin/env python3
"""flysbx.com: the website of Silverbrooks Thompson International Airport (SBX), at flysbx/.
Facts follow the World Bible and the SBX airport map (flysbx/map/, the old airport/ redirects there): concourses, gates, lounges, checkpoints,
Garages A to D, AirLink stations, Transit Center. The flight board is generated in the browser from ROUTES
(a realistic daily schedule) and shows live-looking statuses for the current Eastern time.
News reads stories/stories.json (site 'sbx'). Re-run by tools/build_stories.py."""
import html, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import photos as PHT
def gallery(items): return '<div class="gal">' + ''.join(PHT.fig(p, c, 1000 if i else 1400) for i, (p, c) in enumerate(items)) + '</div>'
def HB(p): return f"background:linear-gradient(110deg,rgba(2,30,72,.94) 0%,rgba(2,79,170,.78) 50%,rgba(0,120,74,.35) 100%),url('{PHT.url(p[0],1800)}') center/cover"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "flysbx"
E = html.escape
DB = json.loads((ROOT / "stories/stories.json").read_text())["stories"]
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def fdate(d): return "%s %d, %s" % (MON[int(d[5:7]) - 1], int(d[8:]), d[:4])

# airline code: name, color, concourse, gates, flight number base
AIR = {
 "DL": ("Delta", "#9b1c2c", "C", ["C%d" % i for i in list(range(1, 14)) + list(range(20, 30))], 300),
 "DLC": ("Delta Connection", "#9b1c2c", "B", ["B%d" % i for i in range(1, 13)], 5100),
 "AA": ("American", "#0078d2", "B", ["B%d" % i for i in range(13, 23)], 1400),
 "B6": ("JetBlue", "#0033a0", "A", ["A%d" % i for i in range(1, 9)], 900),
 "WN": ("Southwest", "#304cb2", "A", ["A%d" % i for i in range(9, 15)], 2200),
 "UA": ("United", "#005daa", "D", ["D%d" % i for i in range(1, 11)], 1700),
 "AC": ("Air Canada", "#d22630", "D", ["D11", "D12"], 8600),
 "PD": ("Porter", "#1b365d", "D", ["D13"], 430),
 "AS": ("Alaska", "#01426a", "D", ["D14", "D15"], 760),
 "F9": ("Frontier", "#00843d", "D", ["D16"], 1300),
 "NK": ("Spirit", "#c8a400", "D", ["D17A"], 2900),
 "MX": ("Breeze", "#1e5ba8", "D", ["D17B"], 410),
 "SY": ("Sun Country", "#f58025", "D", ["D17C"], 390),
 "DLI": ("Delta", "#9b1c2c", "X", ["X1", "X2", "X3", "X4"], 100),
 "AF": ("Air France", "#002157", "X", ["X5", "X6"], 320), "KL": ("KLM", "#00a1de", "X", ["X6", "X7"], 640), "VS": ("Virgin Atlantic", "#da0530", "X", ["X5", "X7"], 150),
 "BA": ("British Airways", "#075aaa", "X", ["X8", "X9"], 230), "EI": ("Aer Lingus", "#006272", "X", ["X10"], 130), "LH": ("Lufthansa", "#05164d", "X", ["X11", "X12"], 440),
 "TP": ("TAP Air Portugal", "#ed1c24", "X", ["X13"], 220), "EK": ("Emirates", "#d71921", "X", ["X16"], 230), "TK": ("Turkish Airlines", "#c70a0c", "X", ["X17"], 12),
 "FI": ("Icelandair", "#1c4a8f", "X", ["X14"], 620), "QR": ("Qatar Airways", "#5c0632", "X", ["X18"], 750), "IB": ("Iberia", "#d7192d", "X", ["X15"], 6250),
 "LX": ("Swiss", "#e2001a", "X", ["X19"], 18), "SK": ("SAS", "#000f9f", "X", ["X20"], 930), "AM": ("Aeroméxico", "#0b2343", "X", ["X15"], 470), "LY": ("El Al", "#002b72", "X", ["X19"], 16),
 "KE": ("Korean Air", "#00256c", "X", ["X21", "X22"], 92), "AZ": ("ITA Airways", "#1b2f6e", "X", ["X23"], 610), "AI": ("Air India", "#d81e05", "X", ["X24"], 144), "ET": ("Ethiopian", "#078930", "X", ["X25"], 518),
}
CITY = {"ATL": "Atlanta", "MSP": "Minneapolis", "DTW": "Detroit", "SLC": "Salt Lake City", "LAX": "Los Angeles", "SFO": "San Francisco", "SEA": "Seattle", "JFK": "New York-JFK", "LGA": "New York-LaGuardia",
 "BOS": "Boston", "MCO": "Orlando", "FLL": "Fort Lauderdale", "TPA": "Tampa", "MIA": "Miami", "RSW": "Fort Myers", "DEN": "Denver", "LAS": "Las Vegas", "PHX": "Phoenix", "AUS": "Austin", "BNA": "Nashville",
 "RDU": "Raleigh-Durham", "CHS": "Charleston", "SAN": "San Diego", "SJU": "San Juan", "CUN": "Cancún", "PDX": "Portland, OR", "MSY": "New Orleans", "DCA": "Washington-National", "ORD": "Chicago-O'Hare",
 "MCI": "Kansas City", "IND": "Indianapolis", "PWM": "Portland, ME", "BTV": "Burlington", "ALB": "Albany", "ROC": "Rochester", "BUF": "Buffalo", "SYR": "Syracuse", "PIT": "Pittsburgh", "CMH": "Columbus",
 "CVG": "Cincinnati", "RIC": "Richmond", "ORF": "Norfolk", "BDL": "Hartford", "PVD": "Providence", "BGR": "Bangor", "MHT": "Manchester", "CLE": "Cleveland", "GSO": "Greensboro", "SAV": "Savannah",
 "MYR": "Myrtle Beach", "ILM": "Wilmington, NC", "CLT": "Charlotte", "DFW": "Dallas-Fort Worth", "PHL": "Philadelphia", "PBI": "West Palm Beach", "BWI": "Baltimore", "MDW": "Chicago-Midway", "HOU": "Houston-Hobby",
 "STL": "St. Louis", "EWR": "Newark", "IAD": "Washington-Dulles", "IAH": "Houston", "YYZ": "Toronto", "YUL": "Montréal", "YTZ": "Toronto-Billy Bishop", "SRQ": "Sarasota", "CDG": "Paris", "AMS": "Amsterdam",
 "LHR": "London-Heathrow", "FCO": "Rome", "DUB": "Dublin", "MXP": "Milan", "BCN": "Barcelona", "SNN": "Shannon", "FRA": "Frankfurt", "MUC": "Munich", "LIS": "Lisbon", "DXB": "Dubai", "IST": "Istanbul",
 "KEF": "Reykjavík", "DOH": "Doha", "MAD": "Madrid", "ZRH": "Zurich", "CPH": "Copenhagen", "MEX": "Mexico City", "TLV": "Tel Aviv", "ICN": "Seoul-Incheon", "DEL": "Delhi", "ADD": "Addis Ababa", "ATH": "Athens"}
ROUTES = {
 "DL": "ATL8 MSP5 DTW5 SLC3 LAX4 SFO3 SEA3 JFK4 LGA6 BOS5 MCO5 FLL4 TPA3 MIA2 RSW2 DEN3 LAS3 PHX2 AUS2 BNA2 RDU2 CHS2 SAN1 SJU1 CUN2 PDX1 MSY2 DCA4 ORD3 MCI1 IND1",
 "DLC": "PWM3 BTV2 ALB2 ROC2 BUF3 SYR2 PIT3 CMH3 CVG2 RIC3 ORF2 BDL2 PVD2 BGR1 MHT2 CLE2 GSO1 SAV2 MYR2 ILM1",
 "AA": "CLT5 DFW4 MIA3 ORD3 PHL3 DCA3", "B6": "BOS4 FLL3 MCO3 SJU2 TPA2 LAX1 PBI2 CUN1", "WN": "BWI3 MDW3 BNA2 ATL2 DEN2 MCO2 HOU1 STL2",
 "UA": "ORD4 EWR5 IAD4 DEN3 IAH3 SFO2", "AC": "YYZ4 YUL3", "PD": "YTZ3", "AS": "SEA2", "F9": "DEN1 MCO2 ATL1", "NK": "FLL2 MCO1", "MX": "CHS1 PVD1 SRQ1", "SY": "MSP1",
 "DLI": "CDG1 AMS1 LHR2 FCO1 DUB1 MXP1 BCN1 ATH1", "AF": "CDG2", "KL": "AMS1", "VS": "LHR2", "BA": "LHR2", "EI": "DUB1 SNN1", "LH": "FRA1 MUC1", "TP": "LIS1", "EK": "DXB1", "TK": "IST1",
 "FI": "KEF1", "QR": "DOH1", "IB": "MAD1", "LX": "ZRH1", "SK": "CPH1", "AM": "MEX1", "LY": "TLV1", "KE": "ICN1", "AZ": "FCO1", "AI": "DEL1", "ET": "ADD1",
}
CLAIM = {"A": "1–2", "B": "3–4", "C": "5–7", "D": "8–9", "X": "10–12"}

CSS = """
:root{--n:#02336e;--n2:#024faa;--sky:#024faa;--g:#009951;--y:#ffc72c;--ink:#121a26;--mut:#5d6878;--line:#e0e4ea;--bg:#f4f6f9;--card:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--ink:#edf1f6;--mut:#9fa9b7;--line:#28323f;--bg:#0b1017;--card:#141b25}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Montserrat,system-ui,sans-serif}a{color:inherit}
.in{max-width:1180px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left))}
.tb{background:#f1f4f8;color:#33415a;border-bottom:1px solid #e0e4ea;font-size:12.5px;padding-top:env(safe-area-inset-top)}.tb .in{display:flex;gap:16px;min-height:32px;align-items:center;white-space:nowrap;overflow-x:auto}.tb a{text-decoration:none}.tb .sp{flex:1}.tb .port{display:inline-flex;align-items:center;gap:6px;font-weight:800;color:#024faa}.tb .port img{width:16px;height:16px}
header{background:#fff;color:#121a26;position:sticky;top:0;z-index:10;border-bottom:4px solid var(--g);box-shadow:0 2px 0 var(--n2)}header .in{display:flex;align-items:center;gap:16px;min-height:68px}
.lg{display:flex;align-items:center;gap:12px;text-decoration:none}.lg img{height:40px;width:auto;display:block}.lg small{color:#4a5568!important}.lg .w{font-weight:800;font-size:30px;letter-spacing:-1px;line-height:1}.lg .w i{color:var(--y);font-style:normal}.lg small{display:block;font-size:11px;letter-spacing:.4px;color:#b7c4d6;line-height:1.25;max-width:150px}
nav.mn{margin-left:auto;display:flex;gap:2px}nav.mn a{text-decoration:none;font-weight:700;font-size:14px;padding:9px 11px;border-radius:8px;white-space:nowrap;color:#1b2330}nav.mn a:hover{background:#eef2f8}nav.mn a.on{background:var(--n2);color:#fff}
.sub2{display:none;overflow-x:auto;gap:6px;padding:8px 16px;background:#fff;border-top:1px solid #e0e4ea}.sub2 a{text-decoration:none;font-weight:700;font-size:13.5px;padding:6px 12px;border-radius:999px;white-space:nowrap;color:#1b2330;border:1px solid #d5dbe4}.sub2 a.on{background:var(--n2);color:#fff;border-color:var(--n2)}
.hero{background:linear-gradient(150deg,var(--n) 0%,var(--n2) 65%,#00784a 100%);color:#fff;padding:46px 0 54px;position:relative;overflow:hidden}
.hero h1{font-size:clamp(32px,5vw,56px);line-height:1.05;margin:6px 0 10px;font-weight:800;letter-spacing:-1px}.hero p{color:#d6e1ef;font-size:17px;max-width:58ch;margin:0 0 20px}.k{font-size:12px;letter-spacing:2.5px;text-transform:uppercase;font-weight:800;color:#7ee2ae}
.hero svg.pl{position:absolute;right:-40px;top:20px;width:min(520px,60vw);opacity:.12}
.fs{display:flex;gap:8px;flex-wrap:wrap;background:#fff;border-radius:14px;padding:8px;max-width:640px}.fs input{flex:1;min-width:180px;border:0;font:inherit;font-size:16px;padding:10px 12px;color:#121a26;background:transparent;outline:none}.fs button,.btn{background:var(--g);color:#fff;border:0;font:inherit;font-weight:800;padding:11px 18px;border-radius:10px;cursor:pointer;text-decoration:none;display:inline-block}
.ql{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-top:-28px;position:relative}.ql a{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;text-decoration:none;font-weight:700;font-size:14.5px;box-shadow:0 6px 16px rgba(10,30,60,.08)}.ql a span{display:block;font-size:22px;margin-bottom:4px}
section{padding:46px 0}section.alt{background:var(--card);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
h2{font-size:clamp(24px,3.2vw,34px);line-height:1.15;margin:0 0 6px;font-weight:800;letter-spacing:-.5px}h3{margin:0 0 6px}.sub{color:var(--mut);margin:0 0 20px;max-width:66ch}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.g2{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.cd{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;text-decoration:none;display:block}.cd b{display:block;font-size:17px;margin-bottom:3px}.cd p,.cd span{color:var(--mut);margin:0}.cd .pr{color:var(--ink);font-weight:800;font-size:22px;display:block;margin:6px 0 2px}
.board{background:#0a1a33;color:#f2f2f2;border-radius:14px;overflow:hidden;border:1px solid #20262f}.bh{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:12px 14px;background:#024faa;border-bottom:1px solid #2a313b}
.tabs button{background:transparent;color:#c9d1d9;border:1px solid #39424e;border-radius:8px;font:inherit;font-weight:700;padding:7px 14px;cursor:pointer}.tabs button.on{background:var(--g);color:#fff;border-color:var(--g)}
.bh input,.bh select{background:#0d1117;color:#f2f2f2;border:1px solid #39424e;border-radius:8px;font:inherit;padding:7px 10px;min-width:0}.bh .sp{flex:1}.clock{font-variant-numeric:tabular-nums;font-weight:800;color:#3ddc84}
.bt{overflow-x:auto}.bt table{width:100%;border-collapse:collapse;min-width:640px;font-variant-numeric:tabular-nums}.bt th{font-size:11.5px;letter-spacing:1px;text-transform:uppercase;color:#8b949e;text-align:left;padding:9px 14px;border-bottom:1px solid #2a313b}
.bt td{padding:10px 14px;border-bottom:1px solid #1d232c;white-space:nowrap}.bt td.c{font-weight:700;color:#fff;white-space:normal}.bt .al{display:inline-flex;align-items:center;gap:8px}.bt .dot{width:10px;height:10px;border-radius:3px;flex:none}
.st{font-weight:800}.st.ok{color:#3fb950}.st.bd{color:#58a6ff}.st.dl{color:#f0883e}.st.cx{color:#f85149}.st.gn{color:#8b949e}.bt tr.gone td{opacity:.55}.more{display:block;text-align:center;padding:12px;color:#3ddc84;font-weight:800;text-decoration:none}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card)}table.t{width:100%;border-collapse:collapse;min-width:560px}table.t td,table.t th{padding:11px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}table.t th{font-size:12px;text-transform:uppercase;letter-spacing:.6px;color:var(--mut)}table.t tr:last-child td{border-bottom:0}
.cc{display:inline-grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--n2);color:#fff;font-weight:800;font-size:18px}
.ch{display:flex;flex-wrap:wrap;gap:7px}.ch span,.ch a{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:5px 12px;font-weight:600;font-size:13.5px;text-decoration:none}
.note{background:color-mix(in srgb,var(--g) 10%,var(--card));border:1px solid color-mix(in srgb,var(--g) 45%,var(--line));border-radius:12px;padding:12px 16px;margin:0 0 18px}
footer{background:var(--n);color:#c5d2e4;padding:34px 0 calc(90px + env(safe-area-inset-bottom));font-size:14px}footer .in{display:grid;grid-template-columns:1.4fr repeat(3,1fr);gap:20px}footer a{display:block;text-decoration:none;margin:3px 0}footer b{color:#fff;display:block;margin-bottom:6px}
@media (max-width:960px){nav.mn{display:none}.sub2{display:flex}.g3,.g2,.g4{grid-template-columns:1fr}.ql{grid-template-columns:repeat(3,1fr)}footer .in{grid-template-columns:1fr 1fr}}
"""
NAV = [("", "Home"), ("flights/", "Flights"), ("parking/", "Parking"), ("getting-here/", "Getting here"), ("airlines/", "Airlines & gates"), ("dining/", "Shop & dine"), ("map/", "Airport map"), ("travel-info/", "Travel info"), ("stories/", "News")]
PLANE = '<svg class="pl" viewBox="0 0 24 24" fill="#fff"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"/></svg>'

def shell(path, title, body, board=False):
    depth = path.count("/") + 1; r = "../" * depth; me = "../" * (depth - 1) if depth > 1 else "./"
    links = "".join(f'<a href="{me}{p}"{" class=\"on\"" if p == path else ""}>{t}</a>' for p, t in NAV)
    js = f'<script>{BOARD_JS}</script>' if board else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title + " | " if title else "")}SBX · Silverbrooks Thompson International Airport</title><meta name="description" content="Flights, parking, transit, dining and travel information for Silverbrooks Thompson International Airport (SBX).">
<link rel="manifest" href="{r}manifest.json"><link rel="apple-touch-icon" href="{r}icons/icon-180.png"><meta name="theme-color" content="#024faa"><link rel="icon" href="{r}brand/logos/sbx-logo-sm.png">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap" rel="stylesheet"><style>{CSS}{PHT.CSS}{XCSS}</style></head><body>
<div class="tb"><div class="in"><a class="port" href="{r}portofsilverbrooks/"><img src="{r}brand/logos/port-mark-64.png" alt="">Port of Silverbrooks</a><a href="{r}">Albanardia.gov</a><a href="{r}transit/sbtrain.html">SBTrain</a><a href="{r}transit/sbmetro.html">SBMetro</a><span class="sp"></span><a href="{me}map/">Airport map</a><a href="{me}travel-info/#contact">Contact</a></div></div>
<header><div class="in"><a class="lg" href="{me}"><img src="{r}brand/logos/sbx-logo-sm.png" alt="SBX"><small>Silverbrooks Thompson International Airport</small></a><nav class="mn">{links}</nav></div><div class="sub2">{links}</div></header>
{body}
<footer><div class="in"><div><a href="{r}portofsilverbrooks/" style="display:inline-block;background:#fff;border-radius:10px;padding:10px 14px;margin-bottom:10px"><img src="{r}brand/logos/port-aviation.png" alt="Port of Silverbrooks" style="height:56px;width:auto;display:block"></a><p>Silverbrooks Thompson International Airport<br>1 Thompson Road, Silverbrooks, AB 19010<br>Run by the Silverbrooks Airport Authority, part of the <a href="{r}portofsilverbrooks/" style="display:inline;color:#fff;font-weight:700">Port of Silverbrooks</a></p></div>
<div><b>Flights</b><a href="{me}flights/">Departures</a><a href="{me}flights/#arr">Arrivals</a><a href="{me}airlines/">Airlines & gates</a></div>
<div><b>At the airport</b><a href="{me}parking/">Parking</a><a href="{me}getting-here/">Getting here</a><a href="{me}dining/">Shop & dine</a><a href="{me}map/">Airport map</a></div>
<div><b>About</b><a href="{r}portofsilverbrooks/">Port of Silverbrooks</a><a href="{me}travel-info/">Travel info</a><a href="{me}stories/">News</a><a href="{r}">Albanardia.gov</a></div></div></footer>
{js}<script src="{r}app/app.js" data-home="float"></script></body></html>"""

# ---------- flight board (client side) ----------
BOARD_JS = "const AIR=" + json.dumps({k: [v[0], v[1], v[2], v[3], v[4]] for k, v in AIR.items()}, ensure_ascii=False) + ";const CITY=" + json.dumps(CITY, ensure_ascii=False) + ";const ROUTES=" + json.dumps(ROUTES) + ";const CLAIM=" + json.dumps(CLAIM, ensure_ascii=False) + r""";
(function(){
let seed=7;const rnd=()=>{seed=(seed*16807)%2147483647;return (seed-1)/2147483646};
const F=[];const used={};
for(const [al,s] of Object.entries(ROUTES)){const a=AIR[al];const intl=a[2]==='X';for(const tok of s.split(' ')){const ap=tok.slice(0,3),n=+tok.slice(3);
 for(let i=0;i<n;i++){
  const span=intl?[[17*60,22*60+40],[6*60+20,14*60]]:[[6*60,22*60],[7*60,23*60+30]];
  for(const dir of ['dep','arr']){const [lo,hi]=dir==='dep'?span[0]:span[1];let t=Math.round((lo+(hi-lo)*((i+.15+rnd()*.7)/n))/5)*5;
   let num;do{num=a[4]+Math.floor(rnd()*(al==='DLC'?800:al==='DL'?1900:300))}while(used[al+num]);used[al+num]=1;
   const r=rnd(),delay=r<.06?0:r<.17?15+Math.round(rnd()*12)*5:0,cx=rnd()<.012;
   F.push({dir,al,num:(al==='DLI'||al==='DLC'?'DL':al)+' '+num,ap,city:CITY[ap]||ap,t,delay,cx,gate:a[3][Math.floor(rnd()*a[3].length)],conc:a[2]});}
 }}}
F.sort((x,y)=>x.t-y.t);
const ny=()=>{const d=new Date(new Date().toLocaleString('en-US',{timeZone:'America/New_York'}));return d.getHours()*60+d.getMinutes()};
const hm=m=>{m=((m%1440)+1440)%1440;let h=Math.floor(m/60),mi=m%60,ap=h<12?'AM':'PM';h=h%12||12;return h+':'+String(mi).padStart(2,'0')+' '+ap};
function status(f,now){const est=f.t+f.delay,d=est-now;
 if(f.cx)return['Cancelled','cx',0];
 if(f.dir==='dep'){if(d<=-5)return['Departed '+hm(est),'gn',1];if(d<=15)return['Final call','bd',0];if(d<=40)return['Boarding','bd',0];return f.delay?['Delayed to '+hm(est),'dl',0]:['On time','ok',0]}
 if(d<=-20)return['Arrived · Claim '+CLAIM[f.conc],'gn',1];if(d<=0)return['Landed '+hm(est),'ok',0];if(d<=25)return['Arriving '+hm(est),'bd',0];return f.delay?['Delayed to '+hm(est),'dl',0]:['On time','ok',0]}
function row(f,now){const a=AIR[f.al],s=status(f,now);return `<tr class="${s[2]?'gone':''}"><td>${hm(f.t)}</td><td class="c">${f.city} <span style="color:#8b949e;font-weight:600">${f.ap}</span></td><td><span class="al"><span class="dot" style="background:${a[1]}"></span>${a[0]} ${f.num.split(' ')[1]}</span></td><td>${f.gate}</td><td><span class="st ${s[1]}">${s[0]}</span></td></tr>`}
document.querySelectorAll('[data-board]').forEach(el=>{
 const full=el.dataset.board==='full';let dir=location.hash==='#arr'?'arr':'dep',q='',air='';
 const names=[...new Set(Object.values(AIR).map(a=>a[0]))].sort();
 el.innerHTML=`<div class="board"><div class="bh"><span class="tabs"><button data-d="dep">Departures</button> <button data-d="arr">Arrivals</button></span>${full?`<input type="search" placeholder="City, airport code or flight" aria-label="Search flights"><select aria-label="Airline"><option value="">All airlines</option>${names.map(n=>`<option>${n}</option>`).join('')}</select>`:''}<span class="sp"></span><span class="clock"></span></div><div class="bt"><table><thead><tr><th>Time</th><th class="h2">Destination</th><th>Flight</th><th>Gate</th><th>Status</th></tr></thead><tbody></tbody></table></div>${full?'':'<a class="more" href="flights/">All flights →</a>'}</div>`;
 const tb=el.querySelector('tbody'),h2=el.querySelector('.h2'),ck=el.querySelector('.clock');
 function draw(){const now=ny();ck.textContent=hm(now)+' ET';h2.textContent=dir==='dep'?'Destination':'From';
  el.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('on',b.dataset.d===dir));
  let r=F.filter(f=>f.dir===dir&&(!air||AIR[f.al][0]===air)&&(!q||(f.city+' '+f.ap+' '+f.num+' '+AIR[f.al][0]).toLowerCase().includes(q)));
  if(!full)r=r.filter(f=>status(f,now)[2]===0).slice(0,8);
  tb.innerHTML=r.map(f=>row(f,now)).join('')||'<tr><td colspan="5" style="padding:18px">No flights match.</td></tr>'}
 el.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{dir=b.dataset.d;draw()});
 const i=el.querySelector('input');if(i)i.oninput=()=>{q=i.value.toLowerCase().trim();draw()};const s=el.querySelector('select');if(s)s.onchange=()=>{air=s.value;draw()};
 draw();setInterval(draw,30000);
});
})();"""

def news(n=3):
    st = sorted([s for s in DB if s["site"] == "sbx"], key=lambda s: s["date"], reverse=True)[:n]
    return "".join(f'<a class="cd" href="stories/#{s["slug"]}"><small style="color:var(--mut);font-weight:700;text-transform:uppercase;letter-spacing:.6px;font-size:12px">{E(s["cat"])} · Published {fdate(s["date"])}</small><b>{E(s["title"])}</b><span>{E(s["dek"])}</span></a>' for s in st)

XCSS = '.hero{position:relative}.hero.ph2 svg.pl{display:none}.cdp{padding:0!important;overflow:hidden}.cdp figure{border-radius:0;aspect-ratio:16/9}.cdp .tx{padding:14px 18px 18px}'
def ph(k, t, p, cat='terminal'):
    hp = PHT.pick(cat, t)[0]
    return f'<div class="hero ph2" style="padding:70px 0 44px;{HB(hp)}">{PHT.credit(hp)}<div class="in"><div class="k">{E(k)}</div><h1>{E(t)}</h1><p>{E(p)}</p></div></div>'

def home():
    ND = len({t[:3] for v in ROUTES.values() for t in v.split()})
    hp = PHT.pick("delta", "home")[0]
    return "", "", f"""<div class="hero ph2" style="{HB(hp)}">{PHT.credit(hp)}<div class="in"><div class="k">Silverbrooks Thompson International Airport</div><h1>Fly SBX.</h1><p>More than 70 million travelers a year, more than 100 gates across five concourses, and nonstops to {ND} cities on four continents. Delta's East Coast hub, on the water at the edge of the city.</p>
<form class="fs" action="flights/" onsubmit="location.href='flights/#q='+encodeURIComponent(this.q.value);return false"><input name="q" placeholder="Track a flight: city, airline or flight number" aria-label="Track a flight"><button>Track</button></form></div></div>
<div class="in ql"><a href="flights/"><span>✈</span>Flight status</a><a href="parking/"><span>🅿</span>Parking</a><a href="getting-here/"><span>🚆</span>Transit</a><a href="airlines/"><span>🧭</span>Airlines & gates</a><a href="dining/"><span>☕</span>Shop & dine</a><a href="map/"><span>🗺</span>Airport map</a></div>
<section><div class="in"><h2>Right now at SBX</h2><p class="sub">Times are scheduled times, Eastern. Check with your airline before you leave home.</p><div data-board="mini"></div></div></section>
<section><div class="in"><h2>Your trip through SBX</h2><p class="sub">From the curb to the gate, and home again.</p>{gallery([(PHT.pick("gate","h")[0],"Delta's East Coast hub"),(PHT.pick("terminal","h")[0],"International arrivals, Concourse X"),(PHT.pick("jetblue","h")[0],"JetBlue in Concourse A"),(PHT.pick("people mover","h")[0],"AirLink people mover"),(PHT.pick("dining","h")[0],"Shop and dine"),(PHT.pick("aerial","h")[0],"Four runways on the bay")])}</div></section>
<section class="alt"><div class="in"><h2>Getting to SBX</h2><p class="sub">The airport is on its own peninsula in the bay. Airport Parkway is the only road in, so give yourself time at rush hour, or skip the traffic on the train.</p><div class="g4">
<a class="cd" href="getting-here/#train"><b>SBTrain D Line</b><span>Downtown to the SBX Transit Center in 18 minutes, under the harbor. Every 6 minutes.</span></a>
<a class="cd" href="getting-here/#bus"><b>110 SBX Flyer</b><span>Express bus from Elliot Square through the I-95 Harbor Tunnel, all day.</span></a>
<a class="cd" href="getting-here/#rail"><b>ALBExpress X4</b><span>Trains from Elliot Square, Marisfield, Rutherford and New Brolin every 20 minutes.</span></a>
<a class="cd" href="parking/"><b>Park</b><span>Garages A to D next to the terminals, and the Economy Lot on the AirLink.</span></a></div></div></section>
<section><div class="in"><h2>News from SBX</h2><p class="sub"><a href="stories/">All airport news →</a></p><div class="g3">{news()}</div></div></section>"""

def flights():
    return "flights/", "Flights", ph("Flight status", "Departures and arrivals", "Every flight at SBX today. Statuses update every 30 seconds.", "board") + """<section><div class="in"><div class="note">Flight times change. Check with your airline for the latest gate and status, and sign up for alerts in your airline's app.</div><div data-board="full"></div></div></section>
<section class="alt"><div class="in"><h2>Watch them go</h2><p class="sub">The best plane spotting is from the Concourse X windows and Pearl's End Point.</p>""" + gallery([(PHT.pick("delta","f1")[0],"Departing runway 22"),(PHT.pick("aerial","f2")[0],"Final approach over the bay"),(PHT.pick("jetblue","f3")[0],"JetBlue to Boston"),(PHT.pick("intl","f4")[0],"Evening flights to Europe"),(PHT.pick("tower","f5")[0],"SBX tower"),(PHT.pick("gate","f6")[0],"At the gate")]) + """</div></section>
<script>addEventListener('DOMContentLoaded',()=>{const m=location.hash.match(/q=([^&]*)/);if(m){const i=document.querySelector('[data-board] input');if(i){i.value=decodeURIComponent(m[1]);i.dispatchEvent(new Event('input'))}}})</script>"""

def parking():
    G = [("Garage A", "Short-term", "$6 per half hour, $54 per day", "Closest to Concourses A and X. Best for pickups and short trips."),
         ("Garage B", "Hourly", "$5 per half hour, $48 per day", "Across from Concourse B. Covered walkway on the departures level."),
         ("Garage C", "Daily", "$38 per day", "Next to Concourse C and the Delta check-in hall."),
         ("Garage D", "Daily and long-term", "$32 per day, $160 per week", "Beside Concourse D. Ten floors, EV chargers on floor 2."),
         ("Economy Lot", "Long-term", "$19 per day, $95 per week", "Off Thompson Blvd, with free AirLink trains to every terminal every 4 minutes."),
         ("Cell Phone Lot", "Waiting", "Free, up to 60 minutes", "On Airport Pkwy inbound. Wait here until your traveler is at the curb.")]
    cards = "".join(f'<div class="cd"><b>{a}</b><span>{b}</span><span class="pr">{c}</span><p>{d}</p></div>' for a, b, c, d in G)
    return "parking/", "Parking", ph("Parking", "Park at SBX", "Six places to park, from the garages next to the concourses to the Economy Lot on the AirLink.", "garage") + f"""
<section><div class="in"><div class="g3">{cards}</div></div></section>
<section><div class="in"><h2>Steps from the terminals</h2><p class="sub">Garages A to D connect to every concourse by covered walkways on the departures level.</p>{gallery([(PHT.pick("garage","p1")[0],"Garages A to D"),(PHT.pick("aerial","p2")[0],"SBX from the air"),(PHT.pick("people mover","p3")[0],"The AirLink to the Economy Lot"),(PHT.pick("terminal","p4")[0],"Departures level"),(PHT.pick("delta","p5")[0],"Delta at the gate"),(PHT.pick("checkin","p6")[0],"Straight to check-in")])}</div></section>
<section class="alt"><div class="in g2"><div><h2>Good to know</h2><ul class="sub"><li>Pay with a card or your phone at the exit. Garages A to D take E-ZPass.</li><li>Live space counts show on the signs along Terminal Drive.</li><li>EV charging in Garages C and D and the Economy Lot, at the regular parking rate.</li><li>Accessible spaces on the first floor of every garage, near the elevators.</li><li>Motorcycles park free in the marked areas of Garage D.</li></ul></div>
<div><h2>Picking someone up?</h2><p class="sub">Wait free in the Cell Phone Lot. Terminal Drive is one-way, counterclockwise, around the garages and terminals, so if you miss your door, you'll need to circle. Arrivals pickups are on the lower level; rideshare and taxis are on the Ground Transportation level of each garage.</p></div></div></section>"""

def getting_here():
    return "getting-here/", "Getting here", ph("Getting here", "Getting to and from SBX", "Train, bus, regional rail, rideshare, rental cars or your own car. Everything meets at the SBX Transit Center.", "subway") + f"""
<section><div class="in g2">
<div class="cd cdp" id="train">{PHT.fig(PHT.pick("subway","gh")[0],"",900)}<div class="tx"><b>SBTrain D Line</b><p>From Nygård through downtown, under Silverbrooks Harbor to East Harbor, then under Elliott Bay to the port and SBX. About 18 minutes from downtown, every 6 minutes at rush hour. One SBCard fare plus the $3 airport station surcharge.</p></div></div>
<div class="cd cdp" id="bus">{PHT.fig(PHT.pick("bus","gh")[0],"",900)}<div class="tx"><b>SBMetro buses</b><p><b style="display:inline;font-size:inherit">R Line</b> rapid bus, <b style="display:inline;font-size:inherit">81</b> Airport–Rutherford local through Marisfield, and the <b style="display:inline;font-size:inherit">110 SBX Flyer</b> express from Elliot Square through the I-95 Harbor Tunnel, all day. At night the <b style="display:inline;font-size:inherit">N110</b> follows the D Line.</p></div></div>
<div class="cd cdp" id="rail">{PHT.fig(PHT.pick("rail","gh")[0],"",900)}<div class="tx"><b>ALBExpress X4 and NETA Regional Rail</b><p>The X4 runs Elliot Square, Marisfield, SBX, Rutherford and New Brolin every 20 minutes. NETA Regional Rail trains to Waterloo and Rutherford stop here too.</p></div></div>
<div class="cd"><b>AirLink people mover</b><p>Free, every 4 minutes, 24 hours. Seven stations: Terminal D, Terminal C, Terminal B, Terminals A & X, Central Garages, the Economy Lot and the Rental Car Center.</p></div>
<div class="cd"><b>Free terminal shuttle</b><p>Run by the airport, every 5 minutes, 24 hours. Leaves the Transit Center and circles counterclockwise to Concourse X (International), A, B, C and D.</p></div>
<div class="cd"><b>Rideshare and taxis</b><p>Uber, Lyft and taxis pick up on the Ground Transportation level of each garage. Follow the green signs from baggage claim.</p></div>
<div class="cd"><b>Rental cars</b><p>Every rental company is in the Rental Car Center, one stop on the AirLink: Alamo, Avis, Budget, Dollar, Enterprise, Hertz, National, Sixt and Thrifty.</p></div>
<div class="cd"><b>Driving</b><p>Follow the airport signs to Exit 4 for Airport Pkwy, the only road onto the airport. It meets Terminal Drive, a one-way loop around the garages and terminals.</p></div>
</div></section>
<section class="alt"><div class="in"><h2>See it on the map</h2><p class="sub">Every road, garage, station and gate is on the <a href="../map/">SBX airport map</a>.</p></div></section>"""

def airlines():
    C = [("A", "14", "JetBlue (A1–A8), Southwest (A9–A14)", "Checkpoint 1 · X/A, 6 lanes · TSA PreCheck · CLEAR", "Chase Sapphire Lounge"),
         ("B", "24", "Delta Connection (B1–B12), American (B13–B22)", "Checkpoint 2, 8 lanes · TSA PreCheck", "Delta Sky Club, Admirals Club"),
         ("C", "24", "Delta (C1–C13, C20–C29)", "Checkpoint 3, 10 lanes · TSA PreCheck · CLEAR · Delta Digital ID", "Delta Sky Club (flagship), The Centurion Lounge"),
         ("D", "19", "United (D1–D10), Air Canada, Porter, Alaska, Frontier, Spirit, Breeze, Sun Country", "Checkpoint 4, 8 lanes · TSA PreCheck", "United Club, Air Canada Maple Leaf Lounge, Alaska Lounge"),
         ("X", "28", "Delta, Air France, KLM, Virgin Atlantic and common-use international gates (X1–X28)", "Checkpoint 1 · X/A, 8 lanes · TSA PreCheck · CLEAR", "Delta One Lounge, Air France–KLM Lounge, British Airways Galleries, Lufthansa Lounge")]
    rows = "".join(f'<tr><td><span class="cc">{c}</span></td><td>{g}</td><td>{E(a)}</td><td>{E(s)}</td><td>{E(l)}</td></tr>' for c, g, a, s, l in C)
    byc = {}
    for k, v in AIR.items(): byc.setdefault(v[2], set()).add(v[0])
    dest = {}
    for al, s in ROUTES.items():
        for tok in s.split(): dest.setdefault(tok[:3], set()).add(AIR[al][0])
    dl = "".join(f'<span>{E(CITY[a])} <b style="color:var(--mut);font-weight:600">{a}</b></span>' for a in sorted(dest, key=lambda a: CITY[a]))
    return "airlines/", "Airlines & gates", ph("Airlines & gates", "Airlines, concourses and lounges", f"{len(set(v[0] for v in AIR.values()))} airlines fly from SBX. Check which concourse your airline uses before you go through security.", "gate") + f"""
<section><div class="in"><div class="tw"><table class="t"><tr><th>Concourse</th><th>Gates</th><th>Airlines</th><th>Security</th><th>Lounges</th></tr>{rows}</table></div>
<p class="sub" style="margin-top:14px">Concourses A, B, C and D are connected airside, so you can walk between them after security. Concourse X connects to A. International arrivals clear US Customs in Concourse X and collect bags at Claims 10 to 12.</p></div></section>
<section><div class="in"><h2>On the ramp</h2><p class="sub">Delta mainline in Concourse C, Delta Connection and American in B, JetBlue and Southwest in A, and the world in X.</p>{gallery([(PHT.pick("gate","a1")[0],"Delta's hub in Concourse C"),(PHT.pick("delta","a2")[0],"Delta A321neo"),(PHT.pick("jetblue","a3")[0],"JetBlue in Concourse A"),(PHT.pick("intl","a4")[0],"Air France to Paris"),(PHT.pick("intl","a5")[0],"Concourse X"),(PHT.pick("aerial","a6")[0],"Four runways on the bay")])}</div></section>
<section class="alt"><div class="in"><h2>Airlines</h2><div class="g4">{''.join(f'<div class="cd"><b>Concourse {c}</b><span>{", ".join(sorted(n))}</span></div>' for c, n in sorted(byc.items()))}</div></div></section>
<section><div class="in"><h2>Nonstop destinations</h2><p class="sub">{len(dest)} cities nonstop from SBX this winter.</p><div class="ch">{dl}</div></div></section>"""

def dining():
    D = {"A": ["Dunkin'", "Wawa", "Chick-fil-A", "Sam Adams Tap Room", "Hudson", "InMotion"],
         "B": ["Starbucks", "Potbelly", "Auntie Anne's", "Bar Symon", "Hudson News", "Brookstone"],
         "C": ["Shake Shack", "Starbucks Reserve", "Legal Sea Foods", "Sound Side Crab House", "Vino Volo", "Ben & Jerry's", "Hudson", "MAC Cosmetics", "Tumi", "Kiehl's"],
         "D": ["Dunkin'", "Chipotle", "Jamba", "Sbarro", "Hudson News", "Be Relax Spa"],
         "X": ["Starbucks", "Pret A Manger", "Wolfgang Puck Bistro", "Champagne Bar", "Dufry Duty Free", "Hermès", "Pandora"]}
    cards = "".join(f'<div class="cd"><b><span class="cc" style="width:28px;height:28px;font-size:15px;margin-right:8px">{c}</span>Concourse {c}</b><div class="ch" style="margin-top:10px">{"".join(f"<span>{E(x)}</span>" for x in xs)}</div></div>' for c, xs in D.items())
    return "dining/", "Shop & dine", ph("Shop & dine", "Shop and dine", "Coffee before the gate, a lobster roll at the Crab House, or duty free on the way to Europe.", "dining") + f"""
<section><div class="in"><div class="g2">{cards}</div><p class="sub" style="margin-top:16px">Most places open at 4:30 a.m. and close after the last departure from that concourse. Mobile ordering with gate delivery is available in Concourses B, C and D.</p></div></section>
<section class="alt"><div class="in"><h2>Take a break</h2>{gallery([(PHT.pick("dining","d1")[0],"Restaurants after security"),(PHT.pick("terminal","d2")[0],"Gate-side seating"),(PHT.pick("sunset","d3")[0],"Sunset over the bay from Concourse X"),(PHT.pick("terminal","d4")[0],"International arrivals"),(PHT.pick("dining","d5")[0],"Coffee before the gate"),(PHT.pick("gate","d6")[0],"Gate views")])}</div></section>"""

def info():
    return "travel-info/", "Travel info", ph("Travel info", "Before you fly", "Security, accessibility, Wi-Fi, lost and found, and everything else.", "security") + """
<section><div class="in g3">
<div class="cd"><b>When to arrive</b><p>Two hours before domestic flights and three hours before international flights. Add 20 minutes Monday mornings, Thursday and Friday afternoons, and holiday weekends.</p></div>
<div class="cd"><b>Security</b><p>Four TSA checkpoints. TSA PreCheck at all of them, CLEAR at Checkpoints 1 and 3, and Delta Digital ID at Checkpoint 3. Wait times are on the screens at every check-in hall.</p></div>
<div class="cd"><b>Free Wi-Fi</b><p>Connect to "SBX Free WiFi". No ads, no time limit, and streaming fast enough for a movie at the gate.</p></div>
<div class="cd"><b>Accessibility</b><p>Wheelchair help through your airline, quiet rooms in Concourses C and X, Hidden Disabilities Sunflower lanyards at every information desk, and hearing loops at every gate.</p></div>
<div class="cd"><b>Families</b><p>Nursing rooms and family restrooms in every concourse, and play areas near gates B10, C22 and D4.</p></div>
<div class="cd"><b>Pets</b><p>Pet relief areas after security in Concourses B, C, D and X, and outdoors at each garage.</p></div>
<div class="cd"><b>Lost and found</b><p>Left it on the plane? Contact your airline. Left it in the terminal or a garage? The airport's lost and found is at Baggage Claim 6, open daily 6 a.m. to 10 p.m.</p></div>
<div class="cd"><b>Customs and immigration</b><p>International arrivals clear US Customs and Border Protection in Concourse X. Global Entry and Mobile Passport Control lanes are open for every arrival.</p></div>
<div class="cd" id="contact"><b>Contact</b><p>Silverbrooks Airport Authority<br>1 Thompson Road, Silverbrooks, AB 19010<br>Information desks at every baggage claim, open 24 hours.</p></div>
</div></section>
<section><div class="in"><h2>From the curb to the gate</h2>""" + gallery([(PHT.pick("checkin","t1")[0],"Check-in halls"),(PHT.pick("security","t2")[0],"TSA checkpoints"),(PHT.pick("terminal","t3")[0],"Concourse walkways"),(PHT.pick("board","t4")[0],"Departure boards"),(PHT.pick("baggage","t5")[0],"Baggage claim"),(PHT.pick("people mover","t6")[0],"AirLink to the garages")]) + """</div></section>
<section class="alt"><div class="in"><h2>About SBX</h2><p class="sub">Built on fill in the bay from 1968 to 1974, along with the D Line under the harbor. Today SBX has four runways (12/30, 8/26, 3L/21R and 3R/21L), five concourses, a Delta hub of about 40 gates, a cargo complex for FedEx, UPS and DHL, and Delta TechOps and JetBlue maintenance hangars. It is run by the Silverbrooks Airport Authority, part of the <a href="../../portofsilverbrooks/">Port of Silverbrooks</a>, which also runs McKay Field and the Samolette Container Terminal.</p></div></section>"""

if __name__ == "__main__":
    for fn in (home, flights, parking, getting_here, airlines, dining, info):
        path, title, body = fn()
        o = OUT / path / "index.html"; o.parent.mkdir(parents=True, exist_ok=True)
        o.write_text(shell(path, title, body, board=fn in (home, flights)), encoding="utf-8")
    print("built flysbx/")
