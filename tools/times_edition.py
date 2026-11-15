#!/usr/bin/env python3
"""The Silverbrooks Times: weekly Sunday edition helper.

  python3 tools/times_edition.py archive   # copy the current front page into media/times/editions/<date>/
  python3 tools/times_edition.py index     # rebuild media/times/editions/index.html and the "Past editions" link
  python3 tools/times_edition.py next      # print the folio line (date, volume, number) for the coming Sunday

Run `archive` BEFORE rewriting media/times/index.html, then `index` after. See media/times/EDITION.md.
"""
import datetime as dt, html, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'media/times/index.html'
ED = ROOT / 'media/times/editions'
MONL = ['January','February','March','April','May','June','July','August','September','October','November','December']
DAYN = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
FOLIO = re.compile(r'Silverbrooks, Albanardia · (\w+), (\w+) (\d+), (\d{4})')
NUM = re.compile(r'Vol\. ([IVXLC]+) · No\. ([\d,]+)')
LINK = re.compile(r'<!--times-editions-->.*?<!--/times-editions-->', re.S)
LINK_HTML = ('<!--times-editions--><p style="max-width:1200px;margin:6px auto 0;padding:0 16px;text-align:right;'
             'font:600 12px/1.4 \'Libre Franklin\',system-ui,sans-serif"><a href="editions/" style="color:inherit">'
             'Past editions →</a></p><!--/times-editions-->')


def edition_date(s):
    m = FOLIO.search(s)
    if not m: sys.exit('No folio date found in media/times/index.html')
    return dt.date(int(m.group(4)), MONL.index(m.group(2)) + 1, int(m.group(3)))


def long(d): return '%s, %s %d, %d' % (DAYN[d.weekday()], MONL[d.month - 1], d.day, d.year)


def archive():
    s = PAGE.read_text()
    d = edition_date(s)
    if d >= dt.date.today():
        sys.exit(f'STOP: the paper is already the edition of {long(d)}. Nothing to do.')
    out = ED / d.isoformat() / 'index.html'
    if out.exists():
        print('Already archived:', out.relative_to(ROOT)); return
    a = re.sub(r'<!--alb-stories-->.*?<!--/alb-stories-->', '', s, flags=re.S)   # live boxes don't belong in a back issue
    a = a.replace('"../../', '"../../../../')
    a = a.replace('src="img/', 'src="../../img/').replace("url(img/", "url(../../img/").replace("url('img/", "url('../../img/")
    a = a.replace('<title>The Silverbrooks Times</title>', f'<title>The Silverbrooks Times · {long(d)}</title>')
    banner = ('<p style="max-width:1200px;margin:10px auto 0;padding:8px 16px;background:#f3efe6;border:1px solid #d8d2c4;'
              'font:600 13px/1.4 \'Libre Franklin\',system-ui,sans-serif;color:#1d1d1f">Back issue: the edition of '
              f'{long(d)}. <a href="../../" style="color:inherit">Today\'s paper</a> · '
              '<a href="../" style="color:inherit">All editions</a></p>')
    a = LINK.sub(banner, a) if LINK.search(a) else a.replace('</nav>', '</nav>' + banner, 1)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(a)
    print('Archived', out.relative_to(ROOT))


def index():
    rows = []
    for p in sorted(ED.glob('*/index.html'), reverse=True):
        s = p.read_text(); d = dt.date.fromisoformat(p.parent.name)
        m = NUM.search(s); lead = re.search(r'<article class="col lead">.*?<h1>(.*?)</h1>', s, re.S)
        rows.append(f'<li><a href="{p.parent.name}/"><b>{long(d)}</b><span>{"Vol. %s · No. %s" % m.groups() if m else ""}</span>'
                    f'<i>{lead.group(1) if lead else ""}</i></a></li>')
    cur = PAGE.read_text(); cd = edition_date(cur)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Past editions · The Silverbrooks Times</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Display&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Libre+Franklin:wght@400;600;800&display=swap">
<style>
:root{{--ink:#1d1d1f;--muted:#6b6b70;--hair:#d8d2c4;--paper:#fbfaf6}}
@media (prefers-color-scheme:dark){{:root{{--ink:#ecebe6;--muted:#a3a29c;--hair:#3a3934;--paper:#16161a}}}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:'Libre Caslon Text',Georgia,serif}}
.w{{max-width:820px;margin:0 auto;padding:28px 16px 60px}}
.mast{{width:100%;max-width:520px;display:block;margin:0 auto}}
@media (prefers-color-scheme:dark){{.mast{{filter:invert(1)}}}}
h1{{font:400 34px/1.15 'Libre Caslon Display',Georgia,serif;margin:22px 0 4px;border-top:3px double var(--ink);padding-top:14px}}
p.s{{font:400 14px/1.5 'Libre Franklin',system-ui,sans-serif;color:var(--muted);margin:0 0 18px}}
a{{color:inherit}} ul{{list-style:none;margin:0;padding:0}}
li a{{display:grid;gap:2px;padding:14px 0;border-bottom:1px solid var(--hair);text-decoration:none}}
li b{{font:700 18px/1.3 'Libre Caslon Text',Georgia,serif}} li span{{font:600 11.5px/1.4 'Libre Franklin',sans-serif;letter-spacing:.6px;text-transform:uppercase;color:var(--muted)}}
li i{{font-size:15px}} li a:hover b{{text-decoration:underline}}
</style></head><body><div class="w">
<a href="../"><img class="mast" src="../img/masthead.png" alt="The Silverbrooks Times"></a>
<h1>Past editions</h1>
<p class="s">A new edition comes out every Sunday. Today's paper is the edition of {long(cd)}: <a href="../">read it here</a>.</p>
<ul>
{chr(10).join(rows) if rows else '<li>No back issues yet.</li>'}
</ul></div>
<!--app-shell--><script src="../../../app/app.js" data-home="float"></script><!--/app-shell-->
</body></html>
'''
    ED.mkdir(parents=True, exist_ok=True)
    (ED / 'index.html').write_text(page)
    if not LINK.search(cur):
        cur = cur.replace('</nav>', '</nav>\n  ' + LINK_HTML, 1); PAGE.write_text(cur)
    print(f'Editions index: {len(rows)} back issues')


def nxt():
    s = PAGE.read_text(); d = edition_date(s); m = NUM.search(s)
    today = dt.date.today()
    sun = today + dt.timedelta(days=(6 - today.weekday()) % 7)
    n = int(m.group(2).replace(',', '')) + (sun - d).days   # the Times prints every day, so the number goes up by one a day
    print(f'Vol. {m.group(1)} · No. {n:,}')
    print(f'Silverbrooks, Albanardia · {long(sun)}')


if __name__ == '__main__':
    {'archive': archive, 'index': index, 'next': nxt}.get((sys.argv[1:] or [''])[0], lambda: print(__doc__))()
