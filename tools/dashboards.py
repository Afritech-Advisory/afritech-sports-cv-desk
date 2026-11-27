"""The /forms dashboards keep every text in English, French, Portuguese and Kiswahili inside the page.

The build fills each Kiswahili text from the English one through i18n/sw.json (no Spanish: the CV Desk
languages are English, Français, Kiswahili and Português (BR)). Safe to re-run."""
import json, re
from bs4 import BeautifulSoup, NavigableString, Comment

START = "window.__AFRITECH__="


def _map(v, tr):
    if isinstance(v, str):
        return tr(v) if v.strip() else v
    if isinstance(v, list):
        return [_map(x, tr) for x in v]
    if isinstance(v, dict):
        return {k: _map(x, tr) for k, x in v.items()}
    return v


_TRS = None


def _walk(x, tr):
    if isinstance(x, dict):
        if "en" in x and ("fr" in x or "pt" in x):
            x.pop("es", None)
            x["sw"] = _map(x["en"], tr)
            for c in ("fr", "pt"):
                if _TRS and isinstance(x.get(c), str) and x[c] == x["en"] and _TRS[c].d.get(x["en"], x["en"]) != x["en"]:
                    x[c] = _TRS[c].d[x["en"]]
        for k, v in list(x.items()):
            if k not in ("en", "fr", "pt", "sw"):
                _walk(v, tr)
    elif isinstance(x, list):
        for v in x:
            _walk(v, tr)


NOJS_SW = ('<div class="fb-l" lang="sw"><h2>Fungua fomu hii kwenye kivinjari chako</h2><p>Onyesho hili haliwezi kuendesha fomu '
           'shirikishi. Gusa kitufe hapa chini ili uifungue kwenye Safari au Chrome.</p><a class="fb-b" href="{u}">Fungua fomu</a></div>')


LEGAL_SUM = {"en": "© Afritech Sports · Copyright and privacy", "fr": "© Afritech Sports · Droits et confidentialité",
             "pt": "© Afritech Sports · Direitos e privacidade", "sw": "© Afritech Sports · Haki na faragha"}
HL = {"en": "en", "fr": "fr", "pt": "pt", "sw": "sw"}
# The dashboard sets <html lang> when the reader picks a language; the site bar and the legal note follow it.
LANG_CSS = ('<style id="afs-dash-lang">' + "".join(
    f'html[lang^="{c}"] .L:not([data-l="{c}"]),html[lang^="{c}"] .af-legal div[lang]:not([lang^="{c}"]){{display:none!important}}'
    for c in ("fr", "pt", "sw")) +
    'html:not([lang^="fr"]):not([lang^="pt"]):not([lang^="sw"]) .L:not([data-l="en"]),'
    'html:not([lang^="fr"]):not([lang^="pt"]):not([lang^="sw"]) .af-legal div[lang]:not([lang="en"]){display:none!important}</style>')


def _bar_spans(html, trs):
    """Site bar texts in all four languages, shown by <html lang>."""
    a = html.find("<!-- afs-bar:start -->")
    b = html.find("<!-- afs-bar:end -->")
    if a < 0 or b < 0 or trs is None:
        return html
    soup = BeautifulSoup(html[a:b], "html.parser")
    for st in soup.find_all("style"):
        pass
    for t in list(soup.find_all(string=True)):
        if isinstance(t, Comment) or t.parent.name in ("style", "script") or not t.strip():
            continue
        lead = t[: len(t) - len(t.lstrip())]; trail = t[len(t.rstrip()):]
        en = " ".join(t.split())
        vals = {"en": en, **{c: trs[c](en) for c in ("fr", "pt", "sw")}}
        if len(set(vals.values())) == 1:
            continue
        parts = [NavigableString(lead)] if lead else []
        for c, v in vals.items():
            sp = soup.new_tag("span", attrs={"class": "L", "data-l": c})
            sp.string = v
            parts.append(sp)
        if trail:
            parts.append(NavigableString(trail))
        t.replace_with(*parts)
    return html[:a] + str(soup) + html[b:]


def add_kiswahili(html, tr, trs=None):
    i = html.index(START) + len(START)
    j = html.index("</script>", i)
    raw = html[i:j].rstrip()
    semi = raw.endswith(";")
    data = json.loads(raw.rstrip(";"))
    global _TRS
    _TRS = trs
    _walk(data, tr)
    new = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = html[:i] + new + (";" if semi else "") + html[j:]
    # language menu, short codes and browser-language pick
    html = html.replace('["es","Español (LATAM)"]', '["sw","Kiswahili"]')
    html = html.replace('es:"es", eslatam:"es", "es-latam":"es"', 'sw:"sw", kiswahili:"sw"')
    html = html.replace('SHORT = {en:"EN", pt:"PT-BR", fr:"FR", es:"ES"}', 'SHORT = {en:"EN", pt:"PT-BR", fr:"FR", sw:"SW"}')
    html = html.replace('return {pt:"pt", fr:"fr", es:"es"}[n] || "en"', 'return {pt:"pt", fr:"fr", sw:"sw"}[n] || "en"')
    html = html.replace('lang === "es" ? "es-419" : lang', 'lang')
    # copyright and privacy notes written once per language: the Kiswahili one replaces the Spanish one
    def sw_block(m):
        blocks = re.findall(r'<div lang="en"' + re.escape(m.group(1) or "") + r'>((?:(?!<div).)*?)</div>', html[:m.start()], flags=re.S)
        if not blocks:
            return m.group(0)
        soup = BeautifulSoup(blocks[-1], "html.parser")
        for s in list(soup.find_all(string=True)):
            if s.strip():
                lead = s[: len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
                s.replace_with(NavigableString(lead + tr(s) + trail))
        return f'<div lang="sw"{m.group(1) or ""}>' + str(soup) + "</div>"
    html = re.sub(r'<div lang="(?:es-419|sw)"( style="[^"]*")?>(?:(?!<div).)*?</div>', sw_block, html, flags=re.S)
    # legal note: one summary per language, and only the reader's language is shown
    html = re.sub(r'(<details class="af-legal"[^>]*><summary[^>]*>).*?(</summary>)',
                  lambda m: m.group(1) + "".join(f'<span class="L" data-l="{c}">{v}</span>' for c, v in LEGAL_SUM.items()) + m.group(2),
                  html, count=1, flags=re.S)
    html = re.sub(r'<style id="afs-dash-lang">.*?</style>', "", html, flags=re.S)
    html = html.replace("</head>", LANG_CSS + "</head>", 1)
    html = _bar_spans(html, trs)
    # the "open in your browser" panel shown when scripts cannot run
    m = re.search(r'<div class="fb-l" lang="(?:es|sw)">.*?</div>', html, flags=re.S)
    if m:
        u = re.search(r'href="([^"]+)"', m.group(0)).group(1)
        html = html[:m.start()] + NOJS_SW.format(u=u) + html[m.end():]
    return html
