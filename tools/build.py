"""Build the CV Desk in English, Français, Português (BR) and Kiswahili.

Run from the repo root after adding or changing any page:   python3 tools/build.py
Then check every translated page in a browser at 390 px:      python3 tools/check_lang.py

1. Stamps the Afritech Sports site bar on every page (same bar as MatchIQ and the Tournament Desk).
2. Desk pages and sample layouts switch language in place: every English text gets a French, Portuguese
   and Kiswahili span, shown by the language buttons.
3. Coach, scout and analyst forms and the player, scout and coach forms in /forms: the English file is the
   source, and the build writes the -fr, -ptbr and -sw copies (the hand-made French and Portuguese forms in
   /forms are kept and only get the translated site bar and the language row).
4. The /forms dashboards carry Kiswahili alongside English, French and Portuguese, and the Kiswahili
   fillable PDFs are made from the English ones (tools/pdf_sw.py).

The build stops if any text has no translation and lists it in i18n/missing-<lang>.txt.
Never publish with missing translations and never ship English inside a translated page.
"""
import json, pathlib, re, sys
from bs4 import BeautifulSoup, NavigableString

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import sitebar, i18n, dashboards

ALL = ["en", "fr", "pt", "sw"]
# in-place pages and the languages their buttons offer
INPLACE = {
    "index.html": ALL,
    "players/index.html": ALL,
    "coaches/index.html": ALL,
    "scouts/index.html": ALL,
    "analysts/index.html": ALL,
    "coaches/sample-layout/index.html": ALL,
    "scouts/sample-layout/index.html": ALL,
    "analysts/sample-layout/index.html": ALL,
    "forms/index.html": ALL,
    # Alen Suljić's Scout CV is in English and French; its own content switches itself, the build only
    # translates the site bar around it.
    "scouts/alen-suljic/index.html": ["en", "fr"],
}
# English forms whose -fr, -ptbr and -sw copies the build writes
GENERATED = ["coaches/coach-cv.html", "coaches/coach-assessment.html",
             "scouts/scout-cv.html", "scouts/scout-assessment.html",
             "analysts/analyst-cv.html", "analysts/analyst-assessment.html"]
# English forms in /forms: the build writes the Kiswahili copy; French and Portuguese are hand-made
LEGACY = ["forms/player.html", "forms/scout.html", "forms/coach.html", "forms/coach-hire.html"]
DASHBOARDS = ["forms/player-dashboard.html", "forms/scout-dashboard.html", "forms/coach-dashboard.html"]
# pages with no translation (published English CVs and player profiles): site bar only
VARIANTS = set(GENERATED) | set(LEGACY)


def rel(p):
    return p.relative_to(ROOT).as_posix()


def write(path, html):
    p = ROOT / path
    old = p.read_text(encoding="utf-8") if p.exists() else None
    if old != html:
        p.write_text(html, encoding="utf-8")
        return 1
    return 0


def js_map(tables, code):
    return tables[code].get("__js__", {})


def translate_bar(html, tr):
    """Hand-made French and Portuguese forms: translate only the site bar."""
    a = html.find("<!-- afs-bar:start -->")
    b = html.find("<!-- afs-bar:end -->")
    if a < 0 or b < 0:
        return html
    soup = BeautifulSoup(html[a:b], "html.parser")
    for s in list(i18n.texts(soup)):
        lead = s[: len(s) - len(s.lstrip())]
        trail = s[len(s.rstrip()):]
        s.replace_with(NavigableString(lead + tr(s) + trail))
    return html[:a] + str(soup) + html[b:]


def main():
    tables, keep = i18n.load_tables()
    trs = {c: i18n.Tr(c, tables[c], keep) for c in ("fr", "pt", "sw")}
    changed = 0
    generated_out = {g.replace(".html", suf + ".html") for g in GENERATED + LEGACY for c, _, _, suf in i18n.OTHER}
    # 1. site bar on every English or hand-made page (generated copies get theirs from the English source)
    for f in sorted(ROOT.rglob("*.html")):
        r = rel(f)
        if ".git" in f.parts or (r in generated_out and r not in hand_made()) or r in INPLACE or r in GENERATED + LEGACY or r in hand_made() or r in DASHBOARDS:
            continue
        html = f.read_text(encoding="utf-8")
        new = sitebar.inject(html, "cv", "cv")
        changed += write(r, new)
    # 2. in-place pages
    for page, codes in INPLACE.items():
        html = sitebar.inject((ROOT / page).read_text(encoding="utf-8"), "cv", "cv")
        changed += write(page, i18n.expand_inplace(html, codes, trs, VARIANTS, page))
    # 3. generated forms
    for src in GENERATED + LEGACY:
        html = sitebar.inject((ROOT / src).read_text(encoding="utf-8"), "cv", "cv")
        base = pathlib.PurePosixPath(src).stem
        # the English form gets the language row too
        changed += write(src, i18n.add_lang_row(html, base, "en"))
        for c, _, _, suf in i18n.OTHER:
            out = src.replace(".html", suf + ".html")
            if out in hand_made():
                hm = sitebar.inject((ROOT / out).read_text(encoding="utf-8"), "cv", "cv")
                hm = translate_bar(hm, trs[c])
                changed += write(out, i18n.add_lang_row(hm, base, c))
                continue
            changed += write(out, i18n.translate_mono(html, c, trs[c], js_map(tables, c), base, VARIANTS, src))
    # 4. dashboards
    for d in DASHBOARDS:
        html = sitebar.inject((ROOT / d).read_text(encoding="utf-8"), "cv", "cv")
        changed += write(d, dashboards.add_kiswahili(html, trs["sw"], trs))
    report = {}
    for c, tr in trs.items():
        mf = i18n.I18N / f"missing-{c}.txt"
        if tr.missing:
            mf.write_text("\n".join(sorted(tr.missing)) + "\n", encoding="utf-8")
        elif mf.exists():
            mf.unlink()
        report[c] = len(tr.missing)
    print(f"{changed} file(s) written")
    missing = {k: v for k, v in report.items() if v}
    if missing:
        sys.exit("Missing translations (see i18n/missing-<lang>.txt): " + ", ".join(f"{k} {v}" for k, v in missing.items()))
    print("translations complete:", ", ".join(f"{k} 0 missing" for k in report))
    # Kiswahili fillable PDFs from the English ones (needs pikepdf and reportlab)
    try:
        import pdf_sw
    except ImportError as e:
        sys.exit(f"Kiswahili PDFs not built: {e}. Install with: pip install pikepdf reportlab")
    pdf_sw.main()


def hand_made():
    return {l.replace(".html", s) for l in LEGACY for s in ("-fr.html", "-ptbr.html")}


if __name__ == "__main__":
    main()
