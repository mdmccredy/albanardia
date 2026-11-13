#!/usr/bin/env python3
"""Adds real-photo galleries (from tools/photos.py) to the hand-built pages: the transit maps, City Hall and
Visit Silverbrooks. Re-runnable: replaces the block between <!--alb-photos--> markers. Run by build_stories.py."""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import photos as P

def block(title, sub, items):
    figs = "".join(P.fig(p, cap, 1000 if i else 1400) for i, (p, cap) in enumerate(items))
    return (f'<!--alb-photos--><section class="alb-ph"><style>.alb-ph{{max-width:1180px;margin:34px auto 40px;padding:0 16px;font-family:inherit;color:inherit}}'
            f'.alb-ph h2{{margin:0 0 4px;font-size:clamp(22px,3vw,30px)}}.alb-ph p.s{{margin:0 0 16px;opacity:.75}}{P.CSS}</style>'
            f'<h2>{P.E(title)}</h2><p class="s">{P.E(sub)}</p><div class="gal">{figs}</div></section><!--/alb-photos-->')

PAGES = {
 "transit/sbtrain.html": ("Riding SBTrain", "Five lettered lines under the city and the harbor, plus the G streetcar.", "<!--app-shell-->",
     [("subway", 0, "D Line to SBX"), ("subway", 1, "Above ground on the B Line"), ("subway", 4, "Rush hour downtown"), ("subway", 2, "Every 5 minutes at peak"), ("subway", 5, "Station platforms")]),
 "transit/sbmetro.html": ("Riding SBMetro", "Gold rapid buses on the lettered lines, local routes everywhere else.", "<!--app-shell-->",
     [("bus", 0, "Lettered rapid lines"), ("bus", 1, "Level boarding at every rapid stop"), ("bus", 2, "Articulated buses on the busiest routes"), ("bus", 3, "Electric trolleybuses"), ("bus", 4, "Neighborhood routes")]),
 "transit/sbexpress.html": ("Riding ALBExpress", "Regional trains across the state from Elliot Square.", "<!--app-shell-->",
     [("rail", 0, "Commuter trains to Waterloo and Rutherford"), ("rail", 1, "Platform boarding"), ("rail", 2, "Off-peak service"), ("rail", 3, "Express runs")]),
 "transit/sbferry.html": ("Riding SBFerry", "Across the bay to New Jersey and around the harbor.", "<!--app-shell-->",
     [("ferry", 0, "Cross-bay ferries"), ("ferry", 1, "Arriving at the terminal"), ("ferry", 2, "Car decks on the big boats"), ("sunset", 1, "Evening crossings")]),
 "gov/index.html": ("Around City Hall", "Your city government at work.", r'</section>\s*<section class="pg" id="p-pay"',
     [("city hall", 0, "City Hall"), ("council", 0, "Council chambers"), ("capitol", 0, "The State House"), ("subway", 0, "Transit"), ("port", 3, "The port")]),
 "visit/index.html": ("See Silverbrooks", "On the water, on the boardwalk and around town.", r'</section>\s*<section class="pg" id="p-todo"',
     [("keelboats", 2, "Sailing on the harbor"), ("boardwalk", 0, "The boardwalk"), ("sunset", 2, "Sunset on the bay"), ("J/70", 0, "Race day"), ("ferry", 2, "Ferry rides"), ("stadium", 0, "Game day")]),
 "index.html": ("Life in Albanardia", "The Windward State: on the water, on the train and in the air.", '<section class="blk" id="services">',
     [("harbor", 0, "Racing off the Silverbrooks waterfront"), ("subway", 2, "SBTrain under the harbor"), ("delta", 1, "Delta at SBX"), ("kids", 1, "Summer sailing camp"), ("ferry", 3, "SBFerry across the bay"), ("port", 4, "The Port of Silverbrooks")]),
 "clubs/index.html": ("On the water", "Twenty-two clubs and sailing centers, from Optis to big boats.", '<h2>Yacht clubs</h2>',
     [("keelboats", 1, "Big-boat racing"), ("Optimist", 5, "Junior regattas"), ("J/70", 0, "J/70 fleets"), ("camp", 1, "Summer camp"), ("C420", 0, "High school racing"), ("sunset", 3, "Weeknight racing")]),
}

def main():
    for path, (t, sub, anchor, items) in PAGES.items():
        f = ROOT / path; s = f.read_text(encoding="utf-8")
        s = re.sub(r"<!--alb-photos-->.*?<!--/alb-photos-->", "", s, flags=re.S)
        b = block(t, sub, [(P.PH[c][i % len(P.PH[c])], cap) for c, i, cap in items])
        m = re.search(anchor if anchor.startswith("</section>") else re.escape(anchor), s)
        assert m, (path, anchor)
        s = s[:m.start()] + b + s[m.start():]
        f.write_text(s, encoding="utf-8")
    print("photos added to", len(PAGES), "pages")

if __name__ == "__main__":
    main()
