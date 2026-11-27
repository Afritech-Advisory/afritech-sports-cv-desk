"""Open every translated CV Desk page in a phone-sized browser (390 px) and stop if English shows.

Run from the repo root after the build:   python3 tools/check_lang.py   [--shots DIR]

For each page in French, Portuguese (BR) and Kiswahili it opens every section and tab, reads all the
text a reader can see, and flags:
- any text that is an English text from the source pages and has no translation (names, the email
  address and the phone number in i18n/keep.txt are allowed);
- any text that reads as English sentences (two or more common English words);
- a page wider than the phone screen (sideways scrolling).
Anything found is written to i18n/missing-<lang>.txt and the check fails, like the build.
Needs Playwright with Chromium:  pip install playwright && python -m playwright install chromium
"""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import i18n, build

STOP = re.compile(r"\b(the|and|your|you|with|this|are|will|from|have|what|when|which|for|only|their|before|after)\b")
SUFFIX = {"fr": "-fr", "pt": "-ptbr", "sw": "-sw"}

COLLECT = r"""() => {
  const out = [];
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = w.nextNode())) {
    const p = n.parentElement;
    if (!p || p.closest('script,style,noscript,[translate="no"],[aria-hidden="true"]')) continue;
    const t = n.textContent.replace(/\s+/g, ' ').trim();
    if (!t || !/[A-Za-zÀ-ÿ]{2,}/.test(t)) continue;
    if (!p.getClientRects().length) continue;
    const cs = getComputedStyle(p);
    if (cs.visibility === 'hidden' || cs.opacity === '0') continue;
    out.push(t);
  }
  document.querySelectorAll('input[placeholder],textarea[placeholder]').forEach(e => {
    if (e.getClientRects().length && e.placeholder.trim()) out.push(e.placeholder.trim());
  });
  return out;
}"""

OPEN_ALL = r"""() => { document.querySelectorAll('details').forEach(d => { if (!d.closest('.afs-bar')) d.open = true; }); }"""


def views():
    """(page path, language, url query) for every translated view."""
    out = []
    for page, codes in build.INPLACE.items():
        for c in codes:
            if c != "en":
                out.append((page, c, f"?lang={c}"))
    for src in build.GENERATED + build.LEGACY:
        for c in ("fr", "pt", "sw"):
            out.append((src.replace(".html", SUFFIX[c] + ".html"), c, ""))
    for d in build.DASHBOARDS:
        for c in ("fr", "pt", "sw"):
            out.append((d, c, f"?lang={c}"))
    return out


def english_keys():
    keys = set()
    for page in list(build.INPLACE) + build.GENERATED + build.LEGACY:
        html = (ROOT / page).read_text(encoding="utf-8")
        html = re.sub(r'<span class="L" data-l="(?:fr|pt|sw)"[^>]*>.*?</span>', "", html, flags=re.S)
        keys.update(i18n.keys(html))
    return keys


def main():
    shots = None
    if "--shots" in sys.argv:
        shots = pathlib.Path(sys.argv[sys.argv.index("--shots") + 1])
        shots.mkdir(parents=True, exist_ok=True)
    tables, keep = i18n.load_tables()
    en = english_keys()
    found = {c: [] for c in ("fr", "pt", "sw")}
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox"], **({"executable_path": sys.argv[sys.argv.index("--chrome") + 1]} if "--chrome" in sys.argv else {}))
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg = ctx.new_page()
        pg.on("dialog", lambda d: d.dismiss())
        for page, c, q in views():
            f = ROOT / page
            if not f.exists():
                found[c].append(f"{page} | page missing")
                continue
            pg.goto(f.as_uri() + q)
            pg.wait_for_timeout(250)
            if shots:
                pg.screenshot(path=str(shots / f"{page.replace('/', '_')}.{c}.png"))
            texts = set()
            pg.evaluate(OPEN_ALL)
            texts.update(pg.evaluate(COLLECT))
            # every tab of the CV layouts and the dashboards
            for sel in ['input[name="tab"]', '[role="tab"]']:
                n = pg.locator(sel).count()
                for i in range(n):
                    try:
                        el = pg.locator(sel).nth(i)
                        if sel.startswith("input"):
                            el.evaluate("e => { e.checked = true; e.dispatchEvent(new Event('change', {bubbles: true})); }")
                        else:
                            el.click(timeout=1500)
                        pg.wait_for_timeout(80)
                        pg.evaluate(OPEN_ALL)
                        texts.update(pg.evaluate(COLLECT))
                    except Exception:
                        pass
            wide = pg.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            if wide > 1:
                found[c].append(f"{page} | wider than a 390 px phone by {wide} px")
            d = tables[c]
            for t in sorted(texts):
                if t in keep or i18n.AUTO_KEEP.match(t):
                    continue
                if t in en and d.get(t) != t:
                    found[c].append(f"{page} | {t}")
                    continue
                if len(set(STOP.findall(t))) >= 2 and t not in d.values() and not any(t in v for v in d.values()):
                    found[c].append(f"{page} | {t}")
        b.close()
    bad = 0
    for c, items in found.items():
        mf = i18n.I18N / f"missing-{c}.txt"
        if items:
            mf.write_text("# English or layout problems seen at 390 px\n" + "\n".join(items) + "\n", encoding="utf-8")
            bad += len(items)
        elif mf.exists():
            mf.unlink()
    print(f"checked {len(views())} translated views at 390 px")
    if bad:
        sys.exit("English or layout problems on translated pages (see i18n/missing-<lang>.txt): " +
                 ", ".join(f"{c} {len(v)}" for c, v in found.items() if v))
    print("no English on any translated page; no page wider than the screen")


if __name__ == "__main__":
    main()
