#!/usr/bin/env python3
"""Build the /docs/ pages from the markdown exports in docs/src/.

The markdown files are exported from Max's Claude Docs (World Bible, Update Log,
Stats & Comparisons, People of Silverbrooks). Re-export them, drop them in
docs/src/ with the same file names, and run:  python3 tools/build_docs.py
"""
import html, json, re, pathlib, datetime
import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "src"
OUT = ROOT / "docs"

# slug, title, one-line description, Claude Docs link
DOCS = [
    ("world-bible", "Albanardia World Bible", "The settled canon: state, counties, cities, transit, colleges, sailing and open questions.", "https://claude.ai/artifact/AK25tf6tchHyHBFsERNuUt"),
    ("update-log", "Albanardia Update Log", "Every numbered change to Albanardia, v1 onward, newest first.", "https://claude.ai/artifact/Kmnc2fGzGZmQg1pPKqkzk6"),
    ("stats", "Albanardia Stats & Comparisons", "Populations, counties, colleges, companies and transit, compared to real US places.", "https://claude.ai/artifact/4bxAgAZyNezGWWJkwfNRn4"),
    ("people", "The People of Silverbrooks", "Culture, slang, food, the year's traditions, fan culture and unwritten rules.", "https://claude.ai/artifact/KoVYXHoXLo4hzxQLtawDZo"),
]

CSS = """
:root{--bg:#f4f5f7;--card:#fff;--ink:#1b2430;--mut:#5b6573;--line:#dde1e7;--navy:#22498a;--navy2:#163566;--orange:#fd9e02;--chip:#eef1f6;--link:#1f5fbf}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f141a;--card:#18202a;--ink:#edf1f5;--mut:#9ba7b3;--line:#2a3441;--chip:#1f2935;--link:#8fb4f2}}
*{box-sizing:border-box}html{scroll-padding-top:16px}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Source Sans 3",system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--link)}
.gov{background:#0b1d3a;color:#cfd8e6;font-size:12.5px}.gov .in{max-width:1180px;margin:0 auto;padding:5px 16px;display:flex;gap:8px;align-items:center}
.gov img{width:16px;height:16px;border-radius:50%}
header.hd{background:var(--navy);color:#fff}header.hd .in{max-width:1180px;margin:0 auto;padding:14px 16px;display:flex;align-items:center;gap:12px}
header.hd a{color:#fff;text-decoration:none}.seal{width:42px;height:42px;border-radius:50%;background:#fff;padding:2px}
.ttl b{display:block;font:700 19px/1.15 "Source Sans 3",system-ui,sans-serif}.ttl small{opacity:.85;font-size:12.5px;letter-spacing:.4px;text-transform:uppercase}
.crumb{max-width:1180px;margin:0 auto;padding:14px 16px 0;font-size:14px;color:var(--mut)}.crumb a{color:var(--mut)}
.wrap{max-width:1180px;margin:0 auto;padding:12px 16px 80px;display:grid;grid-template-columns:260px minmax(0,1fr);gap:28px;align-items:start}
nav.toc{position:sticky;top:12px;max-height:calc(100vh - 24px);overflow:auto;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 6px 12px 14px;font-size:14px}
nav.toc h2{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:var(--mut);margin:0 0 8px}
nav.toc a{display:block;padding:4px 6px;border-radius:6px;color:var(--ink);text-decoration:none;line-height:1.3}nav.toc a:hover{background:var(--chip)}
article{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:28px 34px;min-width:0}
article h1{font:700 34px/1.15 "Source Serif 4",Georgia,serif;margin:0 0 6px}
article h2{font:700 24px/1.2 "Source Serif 4",Georgia,serif;margin:38px 0 10px;padding-top:12px;border-top:1px solid var(--line)}
article h3{font-size:18px;margin:24px 0 8px}
.meta{color:var(--mut);font-size:14px;margin-bottom:18px;display:flex;flex-wrap:wrap;gap:6px 14px}
.meta span{background:var(--chip);border-radius:999px;padding:2px 10px}
.tw{overflow-x:auto;margin:14px 0;border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:14.5px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--chip);font-weight:700;white-space:nowrap}tr:last-child td{border-bottom:0}
code{background:var(--chip);padding:1px 5px;border-radius:4px}
li{margin:3px 0}
.lib{max-width:1180px;margin:0 auto;padding:18px 16px 80px}
.lib h1{font:700 32px/1.15 "Source Serif 4",Georgia,serif;margin:6px 0 4px}.lib>p{color:var(--mut);margin:0 0 20px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.cards a{display:block;background:var(--card);border:1px solid var(--line);border-left:5px solid var(--navy);border-radius:10px;padding:16px 18px;text-decoration:none;color:var(--ink)}
.cards a:hover{border-left-color:var(--orange)}.cards b{display:block;font-size:18px;margin-bottom:4px}.cards span{color:var(--mut);font-size:14px}.cards small{display:block;margin-top:10px;color:var(--mut);font-size:12.5px}
@media (max-width:860px){.wrap{grid-template-columns:1fr}nav.toc{position:static;max-height:260px}article{padding:20px 18px}article h1{font-size:27px}}
"""

def shell(title, body, depth):
    up = "../" * depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)} | Albanardia.gov</title><link rel="manifest" href="{up}manifest.json"><link rel="icon" href="{up}icons/favicon.png"><link rel="apple-touch-icon" href="{up}icons/icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="theme-color" content="#22498a">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Source+Serif+4:wght@700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="gov"><div class="in"><img src="{up}icons/favicon.png" alt="">An official website of the State of Albanardia</div></div>
<header class="hd"><div class="in"><a href="{up}"><img class="seal" src="{up}icons/favicon.png" alt=""></a><a class="ttl" href="{up}"><b>Albanardia.gov</b><small>Documents &amp; Records</small></a></div></header>
{body}
<script src="{up}app/app.js" data-home="float"></script>
</body></html>"""

def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def build_doc(slug, title, desc, link):
    md = (SRC / f"{slug}.md").read_text(encoding="utf-8")
    md = md.replace("\\~", "~")
    lines = md.split("\n")
    # first line is "# Title", second non-empty is "date · @author" byline
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    byline = ""
    for i, l in enumerate(lines):
        if l.strip():
            if "·" in l and len(l) < 80:
                byline = l.strip(); lines = lines[i + 1:]
            break
    conv = markdown.Markdown(extensions=["tables", "sane_lists", "toc"], extension_configs={"toc": {"slugify": lambda v, s: slugify(v)}})
    body = conv.convert("\n".join(lines))
    body = re.sub(r"<table>", '<div class="tw"><table>', body).replace("</table>", "</table></div>")
    body = body.replace("[ ]", "☐").replace("[x]", "☑")
    toc = "".join(f'<a href="#{t["id"]}">{html.escape(t["name"])}</a>' for t in conv.toc_tokens)
    date = byline.split("·")[0].strip() if byline else ""
    meta = f'<div class="meta">{"<span>Started " + html.escape(date) + "</span>" if date else ""}<span>Synced from Claude Docs</span><span>Last synced {datetime.date.today():%b %-d, %Y}</span></div>'
    page = f"""<div class="crumb"><a href="../../">Home</a> › <a href="../">Documents</a> › {html.escape(title)}</div>
<div class="wrap"><nav class="toc" aria-label="On this page"><h2>On this page</h2>{toc}</nav>
<article><h1>{html.escape(title)}</h1>{meta}{body}</article></div>"""
    d = OUT / slug; d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(shell(title, page, 2), encoding="utf-8")

def build_index():
    cards = "".join(f'<a href="{s}/"><b>{html.escape(t)}</b><span>{html.escape(d)}</span><small>Synced from Claude Docs</small></a>' for s, t, d, _ in DOCS)
    cards += '<a href="../updates/"><b>Site Updates</b><span>Changes to this website, newest first.</span><small>Albanardia.gov</small></a>'
    page = f"""<div class="crumb"><a href="../">Home</a> › Documents</div>
<main class="lib"><h1>Documents &amp; Records</h1><p>Albanardia's reference documents. They're copied from the working docs automatically, so they stay current.</p>
<div class="cards">{cards}</div></main>"""
    (OUT / "index.html").write_text(shell("Documents & Records", page, 1), encoding="utf-8")
    (OUT / "docs.json").write_text(json.dumps([{"slug": s, "title": t, "desc": d} for s, t, d, _ in DOCS], indent=1))

if __name__ == "__main__":
    for s, t, d, l in DOCS:
        build_doc(s, t, d, l)
    build_index()
    print("built", len(DOCS), "docs")
