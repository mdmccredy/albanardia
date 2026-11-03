#!/usr/bin/env python3
"""Save Claude Docs markdown exports into docs/src/.

Run this AFTER calling the Claude Docs `export` tool (format: markdown) for each doc
in the same Claude Code session. The export results land in this session's
transcript (~/.claude/projects/**.jsonl) or, when large, in a tool-results .txt file.
This script finds the newest export of each doc there, decodes it and writes it to
docs/src/<slug>.md. Then run tools/build_docs.py.
"""
import base64, glob, json, os, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAMES = {
    "Albanardia World Bible.md": "world-bible",
    "Albanardia Update Log.md": "update-log",
    "Albanardia Stats & Comparisons.md": "stats",
    "The People of Silverbrooks.md": "people",
}
PAT = re.compile(r'"name":"([^"]+\.md)".*?"bytes_b64":"([A-Za-z0-9+/=]+)"')

def candidates():
    base = os.path.expanduser("~/.claude/projects")
    files = glob.glob(base + "/**/*.jsonl", recursive=True) + glob.glob(base + "/**/tool-results/*.txt", recursive=True)
    return sorted(files, key=os.path.getmtime)  # oldest first, so newest wins

found = {}
for f in candidates():
    try:
        raw = open(f, encoding="utf-8", errors="ignore").read()
    except OSError:
        continue
    if "bytes_b64" not in raw:
        continue
    texts = [raw.replace('\\"', '"')]
    if f.endswith(".txt"):
        try:
            texts = [p.get("text", "") for p in json.loads(raw)]
        except Exception:
            pass
    for t in texts:
        for m in PAT.finditer(t):
            if m.group(1) in NAMES:
                found[m.group(1)] = base64.b64decode(m.group(2)).decode("utf-8")

for name, slug in NAMES.items():
    if name in found:
        out = ROOT / "docs" / "src" / f"{slug}.md"
        old = out.read_text(encoding="utf-8") if out.exists() else ""
        out.write_text(found[name], encoding="utf-8")
        print(f"{slug}: {'updated' if old != found[name] else 'unchanged'} ({len(found[name])} chars)")
    else:
        print(f"{slug}: NOT FOUND in this session's exports (left as is)")
