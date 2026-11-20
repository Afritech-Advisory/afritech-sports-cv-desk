"""Stamp the Afritech Sports site bar (Home button, menu, desks, Talk to us) onto every CV Desk page.
Same bar as MatchIQ and the Tournament Desk. Safe to re-run: it replaces the old bar, never adds a second.
Run from the repo root after adding or changing any page:  python3 tools/apply_sitebar.py"""
import pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "tools"))
import sitebar
n = 0
for f in sorted(root.rglob("*.html")):
    if ".git" in f.parts:
        continue
    old = f.read_text(encoding="utf-8")
    new = sitebar.inject(old, "cv", "cv")
    if new != old:
        f.write_text(new, encoding="utf-8"); n += 1
print(f"site bar on {n} page(s) updated")
