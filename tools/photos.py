"""Real photos for the Albanardia sites, from Wikimedia Commons (free licenses; every photo is credited
and links to its Commons page). Hotlinked through Special:FilePath at a set width.
PH[category] = [(file name, author, license), ...]. Add new photos the same way."""
import hashlib, html, urllib.parse
E = html.escape

PH = {
 "470": [("470 dingy.jpg", "HawaiianMama", "CC BY-SA 3.0"), ("Rio 2016 - Vela-Sailing (28946322512).jpg", "Cavalo Marinho", "Public domain"), ("470fns.jpg", "Edank", "Public domain"), ("אליפות העולם במפרשית דגם 470 4.jpg", "Ehud Halperin", "CC BY-SA 4.0")],
 "505": [("Michi Daisenberger1.jpg", "Manfred E. Fritsche", "CC BY-SA 2.0 de"), ("505er 002.jpg", "Johann-Nikolaus Andreae", "CC BY-SA 2.0")],
 "J/70": [("J70 Boote auf der Alster in Hamburg.jpg", "Lars Wehrmann", "CC BY-SA 4.0"), ("Helga Cup 2019 Bahn ActiveCity.jpg", "Hein.Mück", "CC BY-SA 4.0"), ("Helga Cup 2022-2.jpg", "Hein.Mück", "CC BY-SA 4.0"), ("Helga Cup2019 NRV.jpg", "Hein.Mück", "CC BY-SA 4.0")],
 "J/80": [("Match Race J80.jpg", "Manuel", "CC BY-SA 2.0"), ("Dans la baie du Pouliguen (2826351442).jpg", "manuel, MC from Nantes", "CC BY-SA 2.0"), ("Match Race France2008- Demi-finale (2826353356).jpg", "manuel, MC from Nantes", "CC BY-SA 2.0"), ("Match Race France 2008- Demi-finale (2826354556).jpg", "manuel, MC from Nantes", "CC BY-SA 2.0"), ("Finale (2826366040).jpg", "manuel, MC from Nantes", "CC BY-SA 2.0")],
 "J/22": [("J22 sailboat NSC Beagle III 8187.jpg", "Ahunt", "CC0"), ("J22 sailboat Great White J 4381.jpg", "Ahunt", "CC0")],
 "J/24": [("J-24 yacht racing, Sydney Harbour.jpg", "Rl", "CC BY-SA 3.0"), ("J24 002.jpg", "Johann-Nikolaus Andreae", "CC BY-SA 2.0"), ("J24 003.jpg", "Johann-Nikolaus Andreae", "CC BY-SA 2.0"), ("J24 096.jpg", "Jmulrich", "CC BY-SA 3.0"), ("J-24 sailboats racing at Europameisterschaft 2007.jpg", "Jmulrich", "CC BY-SA 3.0"), ("J24 sailboat J-Spot 0926.jpg", "Ahunt", "CC0")],
 "Etchells": [("Etchells War Kanu.jpg", "Bilby", "CC BY 3.0"), ("Etchells Melbourne 2020.jpg", "DeluxePR", "CC BY-SA 4.0")],
 "Star": [("Star 001.jpg", "Johann-Nikolaus Andreae", "CC BY-SA 2.0"), ("Starboot Regatta Wannsee DM 20100831.jpg", "Sir James", "CC BY 3.0"), ("2012 Olympic Sailing, Weymouth, Dorset.jpg", "Caroline Granycome", "CC BY-SA 2.0"), ("Brazilian and German Star-class crews racing at the 2012 Olympics.jpg", "Caroline Granycome", "CC BY-SA 2.0")],
 "Melges 15": [("Melges15 356.jpg", "Mr Swordfish3", "CC BY-SA 4.0")],
 "Melges 24": [("NavySailingteam.jpg", "Musanna", "CC BY-SA 3.0")],
 "Farr": [("Farr 40 sailboat racing off Newport Beach by Don Ramey Logan.jpg", "Don Ramey Logan", "CC BY-SA 4.0")],
 "Snipe": [("Snipe regatta gijon.JPG", "Commons", "Public domain"), ("Winnersbebum1.JPG", "Ricardo Lobato", "Public domain"), ("Snipe sailing in northern Spain 2.jpg", "Commons", "Public domain"), ("Aureliano Negrin 2011 Snipe.JPG", "Commons", "CC0"), ("Tabares and Morales 2011 Snipe.JPG", "Commons", "CC0")],
 "International 14": [("Int14 Kiel2007.jpg", "VollwertBIT", "CC BY-SA 2.5"), ("International 14 - WM 2022.jpg", "Hein.Mück", "CC BY-SA 4.0")],
 "ILCA": [("Laser dinghy pilot.jpg", "Andy Fogg", "CC BY 2.0"), ("Sailing Lake Calhoun.jpg", "Joe Bielawa", "CC BY 2.0"), ("U Wash WAC sailboats 01.jpg", "Joe Mabel", "CC BY-SA 3.0"), ("2012년 4월 해군 참모총장배 전국요트대회 (5) (7305394670).jpg", "Republic of Korea Armed Forces", "CC BY-SA 2.0")],
 "Optimist": [("- Ammersee - Sailboats -.jpg", "Nino Barbieri", "CC BY-SA 2.5"), ("2011-06 Niendorf Jollenstation - Auftakeln der Optimisten.jpg", "Hapebalf", "CC BY-SA 3.0"), ("005- Optimist (Loctudy 2012).jpg", "jakez29120", "CC BY-SA 2.0"), ("2014 Żaglówki szkółki żeglarskej w Gdyni 01.jpg", "Jacek Halicki", "CC BY-SA 4.0"), ("2010-11-21-Belek-Hotel-10.JPG", "R-E-AL", "CC BY-SA 3.0")],
 "C420": [("420 Class Dinghies with spinnakers.jpg", "Commons", "CC BY-SA 3.0"), ("420er 001.jpg", "Johann-Nikolaus Andreae", "CC BY-SA 2.0"), ("420er 003.jpg", "Johann-Nikolaus Andreae", "CC BY-SA 2.0"), ("420er 004.jpg", "Johann-Nikolaus Andreae", "CC BY-SA 2.0"), ("420er 006.jpg", "Johann-Nikolaus Andreae", "CC BY-SA 2.0"), ("420er 007.jpg", "Johann-Nikolaus Andreae", "CC BY-SA 2.0")],
 "Club FJ": [("Sail boats 5001.jpg", "Dori", "CC BY-SA 3.0 US"), ("Flying Juniors WC 2007.JPG", "Hjmdu", "Public domain"), ("Washington College dinghy team Chester River MD1.jpg", "Acroterion", "CC BY-SA 4.0")],
 "29er": [("29er going out.jpg", "Andrew Fogg", "CC BY 2.0"), ("Deriveur 29er (1).JPG", "Remi Jouan", "CC BY-SA 3.0"), ("Deriveur 29er (4).JPG", "Remi Jouan", "CC BY-SA 3.0"), ("Deriveur 29er (5).JPG", "Remi Jouan", "CC BY-SA 3.0"), ("Deriveur 29er (6).JPG", "Remi Jouan", "CC BY-SA 3.0"), ("Un dériveur 29er (1).JPG", "Jean-Pierre Bazard", "CC BY-SA 3.0")],
 "Hobie 16": [("Catamarans, Châté Lîzabé, Jèrri.jpg", "Man vyi", "Public domain"), ("Hobie 16 catamaran on the Dutch coast 3047.jpg", "Dohduhdah", "Public domain"), ("HOTEL PLAYA MAZATLANcatamaran.jpg", "Kfengler", "CC BY 3.0")],
 "49er": [("49er skiff sailing AUS nationals Geelong.jpg", "Commons", "Public domain"), ("Entrenamiento Berta Betanzos y Támara Echegoyen 49erFX.jpg", "Vanbasten 23", "CC BY-SA 3.0"), ("Berta Betanzos y Támara Echegoyen 49erFX.jpg", "Vanbasten 23", "CC BY-SA 3.0"), ("49erFX.jpg", "Mef.ellingen", "CC BY-SA 3.0")],
 "kids": [("Kids Camp 2015 Day 2 (19088073952).jpg", "Isles Yacht Club", "CC BY 2.0"), ("Kids Camp 2015 Day 2 (19088091082).jpg", "Isles Yacht Club", "CC BY 2.0"), ("Kids Camp 2015 Day 1 (18441847314).jpg", "Isles Yacht Club", "CC BY 2.0"), ("Pram sailing St. Petersburg Yacht Club basin.jpg", "Xrzt", "CC0"), ("Switzerland-02832 - Sailing Lessons (23061768880).jpg", "Dennis G. Jarvis", "CC BY-SA 2.0"), ("4586 Sailing lessons (13747605585).jpg", "crabchick", "CC BY 2.0"), ("Sailing Lesson - Priory Bay - geograph.org.uk - 2005135.jpg", "Colin Babb", "CC BY-SA 2.0")],
 "camp": [("Kids Camp 2015 Day 2 (19086130552).jpg", "Isles Yacht Club", "CC BY 2.0"), ("Kids Camp 2015 Day 2 (19091795905).jpg", "Isles Yacht Club", "CC BY 2.0"), ("Kids Camp 2015 Day 2 (19091793625).jpg", "Isles Yacht Club", "CC BY 2.0"), ("Kids Camp 2015 Day 2 (18471094323).jpg", "Isles Yacht Club", "CC BY 2.0"), ("Kids Camp 2015 Day 2 (19086120632).jpg", "Isles Yacht Club", "CC BY 2.0"), ("Kids Camp 2015 Day 2 (19091789375).jpg", "Isles Yacht Club", "CC BY 2.0")],
 "team": [("Stanford sailing team practicing on Redwood Creek 2010-10-13 10.JPG", "BrokenSphere", "CC BY 3.0"), ("Stanford sailing team practicing on Redwood Creek 2010-10-13 11.JPG", "BrokenSphere", "CC BY 3.0"), ("Stanford sailing team practicing on Redwood Creek 2010-10-13 12.JPG", "BrokenSphere", "CC BY 3.0"), ("Stanford sailing team practicing on Redwood Creek 2010-10-13 3.JPG", "BrokenSphere", "CC BY 3.0")],
 "youth": [("Julio Alonso Ortega Sailing in 29er Corpus Christi ISAF Worlds.jpg", "James Tomlinson", "CC BY-SA 4.0"), ("Julio Alonso Ortega Sailing 29er Corpus Christi ISAF Worlds.jpg", "Jen Edney", "CC BY-SA 4.0"), ("Julio Alonso Ortega Sailing at Texas during the ISAF Worlds.jpg", "Jen Edney", "CC BY-SA 4.0"), ("Julio Alonso Ortega Sailing in 29er During the ISAF worlds.jpg", "Jen Edney", "CC BY-SA 4.0")],
 "coach": [("Syc usjwdc2008 2.jpg", "Roxanne Fairbairn", "CC BY-SA 3.0")],
 "keelboats": [("Manhattan Yacht Club from the Honorable William Wall by Michael Vadon June 10th, 2015 02.jpg", "Michael Vadon", "CC BY-SA 4.0"), ("Manhattan Yacht Club from the Honorable William Wall by Michael Vadon June 10th, 2015 03.jpg", "Michael Vadon", "CC BY-SA 4.0"), ("Manhattan Yacht Club from the Honorable William Wall by Michael Vadon June 10th, 2015 01.jpg", "Michael Vadon", "CC BY-SA 4.0"), ("Manhattan Yacht Club from the Honorable William Wall by Michael Vadon June 10th, 2015 05.jpg", "Michael Vadon", "CC BY-SA 4.0"), ("Manhattan Yacht Club from the Honorable William Wall by Michael Vadon June 10th, 2015 04.jpg", "Michael Vadon", "CC BY-SA 4.0"), ("Manhattan Yacht Club from the Honorable William Wall by Michael Vadon June 10th, 2015 07.jpg", "Michael Vadon", "CC BY-SA 4.0"), ("Syc eveningsailingrace.jpg", "Roxanne Fairbairn", "CC BY-SA 3.0")],
 "sunset": [("Hunter 33 2004 sailboat at sunset in Toronto Ontario.jpg", "Commons", "CC BY-SA 2.5"), ("Red Sunset & Sailboat.JPG", "Robert Havasy", "CC BY-SA 3.0"), ("Sailboat @ Sunset (6615742233).jpg", "Daniel Ramirez", "CC BY 2.0")],
 "clubhouse": [("Watch Hill Yacht Club at dusk.jpg", "Juliancolton", "CC BY-SA 4.0"), ("Watch Hill Yacht Club in fog.jpg", "Juliancolton", "CC BY-SA 4.0"), ("Detroit Yacht Club Belle Isle.jpg", "Mikerussell", "CC BY-SA 3.0")],
 "club event": [("Isles Yacht Club Ribbon Cutting 001 (28746591812).jpg", "Isles Yacht Club", "CC BY 2.0"), ("Isles Yacht Club Ribbon Cutting 006 (28820508376).jpg", "Isles Yacht Club", "CC BY 2.0")],
 # airport
 "terminal": [("Logan Airport International Arrivals Hall.jpg", "hildgrim", "CC BY-SA 2.0"), ("2011 Logan airport Boston 5528996967.jpg", "Stephen Pierzchala", "CC BY 2.0"), ("Interior of Toronto Pearson International Airport Terminal 1 wider view.jpg", "Daniel Case", "CC BY-SA 3.0")],
 "delta": [("Delta Air Lines Airbus A321neo N511DE on final approach to Boston December 2024.jpg", "4300streetcar", "CC BY 4.0"), ("Delta Air Lines Airbus A321neo N577DN lined up at Boston December 2024.jpg", "4300streetcar", "CC BY 4.0"), ("Delta Air Lines Airbus A321neo N503DZ at San Francisco August 2022.jpg", "4300streetcar", "CC BY 4.0"), ("Boarding Delta Air Lines Airbus A321neo N503DZ August 2022.jpg", "4300streetcar", "CC BY 4.0")],
 "gate": [("Boeing 717 - Delta Gate at MSP Airport, N925AT (23228534763).jpg", "Tony Webster", "CC BY-SA 2.0"), ("Delta Air Lines A330-200 N860NW At the gate at Detroit Metro International Airport.jpg", "Steven Agre", "CC BY-SA 4.0"), ("Delta A319 pushback, Birmingham International Airport (US).JPG", "Flyfishmcd", "CC BY-SA 3.0"), ("Delta 757 GEG.JPG", "Gleby", "CC BY-SA 3.0")],
 "jetblue": [("JetBlue Airbus A321 and A320 at Boston Nov 2024.jpg", "4300streetcar", "CC BY 4.0"), ("JetBlue Airbus A320 N566JB after departing Runway 27 Boston Feb 2025 1.jpg", "4300streetcar", "CC BY 4.0"), ("JetBlue Airbus A320 N508JL on final approach to Boston April 2025.jpg", "4300streetcar", "CC BY 4.0")],
 "security": [("Portland International Airport security check.jpg", "M.O. Stevens", "CC BY 3.0"), ("Transportation Security Administration Checkpoint at John Glenn Columbus International Airport.jpg", "Michael Ball", "CC0"), ("New central security checkpoint at LAX T7 (35464412576).jpg", "Edward Russell", "CC BY 2.0")],
 "people mover": [("ATL People Mover 2.jpg", "Sanibel sun", "Public domain"), ("DIA Train 1.JPG", "Sanibel sun", "Public domain"), ("DIA Train 3.JPG", "Sanibel sun", "Public domain")],
 "garage": [("Parking garage at Pearson airport - Flickr - Stradablog.jpg", "Tino Rossini", "CC BY 2.0"), ("Ruzyně, letiště, parking C.jpg", "ŠJů", "CC BY 4.0")],
 "aerial": [("Logan Airport aerial view.jpg", "David Wilson", "CC BY 2.0"), ("Boston Logan Airport, runaways.JPG", "Luciof", "CC BY-SA 3.0"), ("20120909 030 Boston (8391469790).jpg", "David Wilson", "CC BY 2.0")],
 "dining": [("Singapore Changi Airport, Terminal 2, Restaurants, Dec 05.JPG", "Commons", "Copyrighted free use"), ("Terminal 1 Restrict Area Restaurant 201506.jpg", "Wing1990hk", "CC BY 3.0")],
 "board": [("Indicator board at Changi Airport 1.jpg", "MasterMind5991", "CC BY-SA 3.0"), ("Helsinki-Vantaa departures board 2010-04-18.jpg", "MattiPaavola", "CC BY-SA 3.0")],
 # port and transit
 "port": [("20201119-TFAA-LSC-0028 (50699880323).jpg", "US Department of Agriculture", "Public domain"), ("20201119-TFAA-LSC-0033 (50700707302).jpg", "US Department of Agriculture", "Public domain"), ("20201119-TFAA-LSC-0050 (50700627321).jpg", "US Department of Agriculture", "Public domain"), ("Aerial photograph of the Port of Miami Container Port.jpg", "James R. Tourtellotte", "Public domain"), ("Port of Oakland.jpg", "Daniel Parks", "CC BY 2.0"), ("Port of Miami container ship yard.jpg", "Chuck Kramer", "CC BY 2.0"), ("Davao International Container Terminal.jpg", "Robinson Niñal", "Public domain")],
 "subway": [("MBTA Blue Line train at State Street.jpg", "4300streetcar", "CC BY-SA 4.0"), ("MBTA Blue Line train approaching Orient Heights Oct 2024.jpg", "4300streetcar", "CC BY 4.0"), ("MBTA Blue Line train at State August 2024.jpg", "4300streetcar", "CC BY 4.0"), ("MBTA Blue Line train approaching Orient Heights Oct 2024 2.jpg", "4300streetcar", "CC BY 4.0"), ("R Train at Forest Hills-71st Avenue Station.jpg", "Apricot50", "CC BY-SA 3.0"), ("3 train arriving in Borough Hall station.jpg", "Ad Meskens", "CC BY-SA 3.0")],
 "bus": [("RapidRide -6608 in Tukwila (14644768083).jpg", "SounderBruce", "CC BY-SA 2.0"), ("RapidRide A Line to FWTC Test Coach.jpg", "Tim", "CC BY-SA 2.0"), ("MTA (2016 livery, operated by MTA Bus Company) New Flyer Xcelsior XD60 5400.jpg", "Adam Moreira", "CC BY-SA 4.0"), ("King County Metro 4506 trolleybus on route 49.jpg", "SounderBruce", "CC BY-SA 3.0"), ("CTT Xcelsior A37.jpg", "Newflyer504", "CC BY-SA 4.0")],
 "rail": [("Outbound MBTA Commuter Rail Train at West Newton Station.jpg", "4300streetcar", "CC BY 4.0"), ("MBTA Commuter Rail Train at Waltham Station Inbound Platform.jpg", "4300streetcar", "CC BY 4.0"), ("WES Commuter Rail train.jpg", "TriMet", "CC BY 2.0"), ("ACE EMD F40PH Fremont - San Jose.jpg", "David Gubler", "CC BY-SA 3.0")],
 "ferry": [("Washington State Ferry Tacoma.jpg", "Joe Mabel", "CC BY-SA 3.0"), ("Ferry Arriving in Kingston Washington.jpg", "KJRSeattle", "CC BY-SA 4.0"), ("MV Tacoma a Washington State ferry.jpg", "Ron Clausen", "CC BY-SA 4.0")],
 "campus": [("UDel Memorial and Magnolia Circle.JPG", "Cargoudel", "CC BY-SA 3.0"), ("Commons Lawn.jpg", "Northern-Virginia-Photograph", "CC BY-SA 4.0")],
 "lecture": [("Student in Class, Tulane University, September 2002.jpg", "Tulane Public Relations", "CC BY 2.0"), ("Students listen to Doug Ellin (5568274458).jpg", "Tulane Public Relations", "CC BY 2.0")],
 "stadium": [("Camp Randall Stadium crowd.jpg", "Ohsuch181", "CC BY-SA 3.0")],
 "library": [("Yale Law School Library Reading Room (L3).jpg", "PENG Yanan", "CC BY-SA 3.0"), ("Graz University-Library reading-room.jpg", "Marcus Gossler", "CC BY-SA 3.0"), ("Reading room at Chittagong University Library (02).jpg", "Moheen Reeyad", "CC BY-SA 4.0")],
 "capitol": [("Delaware Legislative Hall Dover DSC 3463 ad.JPG", "Adavyd", "CC BY-SA 3.0"), ("Delaware State Capitol.jpg", "Commons", "Public domain"), ("Delaware Legislative Hall West Side DSC 3441 ad.JPG", "Adavyd", "CC BY-SA 3.0"), ("Delaware Legislative Hall Senate chamber DSC 3442 ad.JPG", "Adavyd", "CC BY-SA 3.0")],
 "city hall": [("City Hall - Twilight.JPG", "Arundejoe", "CC BY-SA 3.0"), ("Nyc city hall jan06a.jpg", "Aude", "CC BY-SA 2.5")],
 "council": [("Glasgow City Chambers The Council Chamber.jpg", "Michael D Beckwith", "CC0")],
 "boardwalk": [("Rehoboth Beach boardwalk at Wilmington Avenue looking north.JPG", "Dough4872", "Public domain"), ("Rehoboth Beach boardwalk at Rehoboth Avenue looking south.jpg", "Dough4872", "Public domain")],
}

# which photos show a boat class: exact matches first, then close stand-ins (fictional or missing classes)
CLASS = {
 "J/70": ("J/70", 1), "J/80": ("J/80", 1), "J/22": ("J/22", 1), "J/24": ("J/24", 1), "Etchells": ("Etchells", 1), "Star": ("Star", 1),
 "Melges 24": ("Melges 24", 1), "Melges 15": ("Melges 15", 1), "Snipe": ("Snipe", 1), "International 14": ("International 14", 1), "505": ("505", 1),
 "ILCA": ("ILCA", 1), "Optimist": ("Optimist", 1), "C420": ("C420", 1), "Club FJ": ("Club FJ", 1), "29er": ("29er", 1), "Hobie 16": ("Hobie 16", 1),
 "J/105": ("keelboats", 0), "Farr 30": ("Farr", 0), "Santa Cruz 27": ("keelboats", 0), "Melges 19": ("Melges 15", 0), "Tasar": ("Snipe", 0), "RS Aero": ("ILCA", 0),
 "MC7": ("J/22", 2), "MC23": ("J/70", 2), "MC24": ("J/24", 2), "MC30": ("J/80", 2), "MC35": ("keelboats", 2),
 "Bauer": ("ILCA", 2), "JR300": ("C420", 2), "JR400": ("C420", 2), "JR500": ("470", 2), "SK400": ("49er", 2), "SK500": ("49er", 2),
 "Hobie Wave": ("Hobie 16", 0), "SailQube": ("kids", 2), "Larssen Club Radial": ("C420", 2), "Larssen Fyra": ("Optimist", 2), "Larssen Pulse XL": ("kids", 2), "Larssen Voyage": ("kids", 2), "Kayaks and SUPs": ("camp", 2),
}

def h(s): return int(hashlib.md5(s.encode()).hexdigest(), 16)
def pick(cat, seed="", n=1, skip=0):
    L = PH[cat]; s = h(cat + seed) % len(L)
    return [L[(s + skip + i) % len(L)] for i in range(min(n, len(L)))]
def url(f, w=1280): return "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(f) + f"?width={w}"
def page(f): return "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(f.replace(" ", "_"))
def credit(p): return f'<a class="cr" href="{page(p[0])}" target="_blank" rel="noopener">Photo: {E(p[1])} · {E(p[2])}</a>'
def fig(p, cap="", w=1000, cls="ph-f"):
    return f'<figure class="{cls}"><img src="{url(p[0], w)}" alt="{E(cap)}" loading="lazy">{f"<figcaption>{E(cap)}</figcaption>" if cap else ""}{credit(p)}</figure>'
def bg(p, w=1600): return f"background-image:url('{url(p[0], w)}')"
def boat(cls, seed="", n=1):
    """photos for a class: returns (photos, caption)"""
    cat, kind = CLASS.get(cls, ("keelboats", 0))
    cap = cls if kind else ("Big-boat racing" if cat in ("keelboats", "Farr") else "Dinghy racing" if cat in ("Snipe", "ILCA", "Melges 15") else "Catamaran sailing")
    return pick(cat, seed + cls, n), cap

CSS = """
figure.ph-f{position:relative;margin:0;border-radius:14px;overflow:hidden;background:#cfd8e3;aspect-ratio:3/2}
figure.ph-f img{width:100%;height:100%;object-fit:cover;display:block}
figure.ph-f figcaption{position:absolute;left:0;right:0;bottom:0;padding:26px 12px 9px;color:#fff;font-weight:700;font-size:14px;background:linear-gradient(transparent,rgba(0,0,0,.65))}
a.cr{position:absolute;right:6px;top:6px;font:600 9.5px/1.2 system-ui,sans-serif;color:#fff;background:rgba(0,0,0,.45);padding:3px 6px;border-radius:5px;text-decoration:none;max-width:70%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;opacity:.8}
.hero a.cr,.ph a.cr{top:auto;bottom:8px;right:8px}
.gal{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.gal figure:first-child{grid-column:span 2;grid-row:span 2;aspect-ratio:auto}
@media (max-width:760px){.gal{grid-template-columns:1fr 1fr}.gal figure:first-child{grid-column:span 2;aspect-ratio:3/2}}
"""
