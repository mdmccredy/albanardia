#!/usr/bin/env python3
"""Which websites are due for new stories today, from stories/cadence.json.
Prints one line per due site: site key, how many stories to write, and the latest titles
(so new stories continue the thread instead of repeating). Use --date YYYY-MM-DD to test."""
import json, pathlib, sys, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
cad = json.loads((ROOT/'stories/cadence.json').read_text())
db = json.loads((ROOT/'stories/stories.json').read_text())['stories']
sites = __import__('re').search(r'window.ALB_STORIES=(\{.*\});', (ROOT/'stories/data.js').read_text()).group(1)
sites = json.loads(sites)['sites']
today = datetime.date.fromisoformat(sys.argv[sys.argv.index('--date') + 1]) if '--date' in sys.argv else datetime.date.today()
def rule(k):
    if k in cad: return cad[k]
    if k.startswith('college:'): return cad.get('colleges')
    if k.startswith('club:'): return cad.get('clubs')
due = []
for k, si in sites.items():
    r = rule(k)
    if not r: continue
    mine = sorted([s for s in db if s['site'] == k], key=lambda s: s['date'])
    last = datetime.date.fromisoformat(mine[-1]['date']) if mine else datetime.date(2000, 1, 1)
    if (today - last).days >= r['every_days']:
        due.append((k, si['name'], r['per_run'], (today - last).days, [s['title'] for s in mine[-4:]]))
print(f'{today}: {len(due)} sites due')
for k, n, per, age, recent in due:
    print(f'- {k} ({n}): write {per}; last story {age} days ago; recent: ' + ' | '.join(recent))
