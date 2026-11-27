"""Afritech Sports CV Desk translations: English, Français, Português (BR) and Kiswahili.

Every visible text on a translated page is looked up by its exact English text in i18n/<lang>.json.
A missing translation stops the build and is listed in i18n/missing-<lang>.txt, so no English slips
onto a translated page. Names (people, clubs, Afritech Sports, MatchIQ, WhatsApp, LinkedIn), the email
address and the phone number stay as written (i18n/keep.txt).

Two kinds of page:
- In-place pages (the desk pages and sample layouts): the language buttons switch the page where it is.
  Each English text gets a span per language; the checked language radio shows its span.
- Form pages: the English form is the source; the build writes -fr, -ptbr and -sw copies next to it,
  with a language row under the site bar that opens the same form in another language.
"""
import json, re, pathlib
from bs4 import BeautifulSoup, NavigableString, Comment
from bs4.element import PreformattedString

ROOT = pathlib.Path(__file__).resolve().parent.parent
I18N = ROOT / "i18n"
# code, button label, html lang, file suffix
LANGS = [("en", "English", "en", ""), ("fr", "Français", "fr", "-fr"),
         ("pt", "Português (BR)", "pt-BR", "-ptbr"), ("sw", "Kiswahili", "sw", "-sw")]
OTHER = [l for l in LANGS if l[0] != "en"]
HOME = "https://afritechsports.github.io/"
LETTER = re.compile(r"[A-Za-zÀ-ÿ]{2,}")
AUTO_KEEP = re.compile(r"^(\S+@\S+\.\S+|https?://\S+|\+?[\d\s()./:–-]+|v\d[\d.]*|[A-Z]{2,4}\d*)$")
MONO_ATTRS = ("alt", "title", "aria-label", "placeholder", "data-label")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def needs(s):
    return bool(LETTER.search(s))


def load_tables():
    keep = set()
    kf = I18N / "keep.txt"
    if kf.exists():
        keep = {l.strip() for l in kf.read_text().splitlines() if l.strip() and not l.startswith("#")}
    tables = {}
    for code, *_ in OTHER:
        f = I18N / f"{code}.json"
        tables[code] = json.loads(f.read_text()) if f.exists() else {}
    return tables, keep


class Tr:
    """Looks a text up in one language's table and records what is missing."""

    def __init__(self, code, table, keep):
        self.code, self.d, self.keep, self.missing = code, table, keep, set()

    def __call__(self, text):
        k = norm(text)
        if not k or not needs(k) or k in self.keep or AUTO_KEEP.match(k):
            return k
        v = self.d.get(k)
        if v is None and " — " in k:
            # "Field — evidence", "Analysis role — From": each part is translated on its own
            parts = k.split(" — ")
            got = [self(p) if (p in self.d or p in self.keep or not needs(p) or AUTO_KEEP.match(p)) else None for p in parts]
            if all(g is not None for g in got):
                return " — ".join(got)
            for p, g in zip(parts, got):
                if g is None:
                    self.missing.add(p)
            return k
        if v is None:
            self.missing.add(k)
            return k
        return v


def skip(node):
    for p in node.parents:
        if p is None or p.name is None:
            continue
        if p.name in ("script", "style", "title"):
            return True
        if p.get("translate") == "no":
            return True
        if p.get("data-i18n") == "skip":
            return True
        if "afs-langs" in (p.get("class") or []):
            return True
    return False


def is_ref(node):
    p = node.parent
    return p is not None and p.name == "span" and p.get("aria-hidden") == "true" and "reference" in (p.string or "")


def texts(soup):
    for s in soup.find_all(string=True):
        if isinstance(s, (PreformattedString, Comment)) or skip(s) or is_ref(s):
            continue
        if norm(s) and needs(norm(s)):
            yield s


def keys(html):
    soup = BeautifulSoup(html, "html.parser")
    return [norm(s) for s in texts(soup)]


# ---------------------------------------------------------------- form pages (one file per language)

def lang_row(base, code, rel_prefix=""):
    """The language row under the site bar on form pages."""
    links = []
    for c, label, hl, suf in LANGS:
        href = f"{base}{suf}.html"
        links.append(f'<a href="{href}" hreflang="{hl}" lang="{hl}"{" class=on aria-current=true" if c == code else ""}>{label}</a>')
    nav_label = {"en": "Language", "fr": "Langue", "pt": "Idioma", "sw": "Lugha"}[code]
    return ('<!-- afs-lang:start --><style id="afs-lang-css">.afs-lang{background:#0B1C33;font:600 14px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;'
            'text-align:center;padding:6px 8px;display:flex;flex-wrap:wrap;justify-content:center;gap:4px}.afs-lang a{color:#C9D6E6;text-decoration:none;padding:9px 10px;'
            'border-radius:8px;display:inline-flex;align-items:center;min-height:40px}.afs-lang a.on{background:#14B8A6;color:#06221F}@media print{.afs-lang{display:none}}</style>'
            f'<nav class="afs-lang" translate="no" aria-label="{nav_label}">' + "".join(links) + "</nav><!-- afs-lang:end -->")


def add_lang_row(html, base, code):
    html = re.sub(r"<!-- afs-lang:start -->.*?<!-- afs-lang:end -->", "", html, flags=re.S)
    i = html.find("<!-- afs-bar:end -->")
    i = (i + len("<!-- afs-bar:end -->")) if i >= 0 else html.index(">", html.index("<body")) + 1
    return html[:i] + lang_row(base, code) + html[i:]


def has_variant(page, href, variants):
    """True when href (as written on page, a repo-relative path) points at an English form with language copies."""
    h = href.split("#")[0].split("?")[0]
    if not h or re.match(r"^(https?:|mailto:|tel:|#|data:|javascript:)", h):
        return False
    import posixpath
    return posixpath.normpath(posixpath.join(posixpath.dirname(page), h)) in variants


def translate_mono(html, code, tr, js_map, base, variants, page):
    """English form -> one language. variants: repo-relative paths of English forms that have language copies."""
    hl = dict((c, h) for c, _, h, _ in LANGS)[code]
    suf = dict((c, s) for c, _, _, s in LANGS)[code]
    soup = BeautifulSoup(html, "html.parser")
    for s in list(texts(soup)):
        lead = s[: len(s) - len(s.lstrip())]
        trail = s[len(s.rstrip()):]
        s.replace_with(NavigableString(lead + tr(s) + trail))
    for el in soup.find_all(True):
        if el.get("translate") == "no" or any(p.get("translate") == "no" for p in el.parents if p.name):
            continue
        for a in MONO_ATTRS:
            if el.has_attr(a) and needs(el[a]):
                el[a] = tr(el[a])
        if el.name == "input" and el.get("type") in ("radio", "checkbox", "button", "submit") and el.has_attr("value") and needs(el["value"]):
            el["value"] = tr(el["value"])
        if el.name == "meta" and el.get("content") and (el.get("name") in ("description", "twitter:title", "twitter:description")
                                                       or el.get("property") in ("og:title", "og:description")):
            el["content"] = tr(el["content"])
        if el.name == "a" and el.has_attr("href"):
            h = el["href"]
            if h.startswith(HOME):
                el["href"] = re.sub(r"([?&])lang=[a-z]+&?", r"\1", h)
                el["href"] = add_param(el["href"], "lang", code)
            elif has_variant(page, h, variants):
                p, _, frag = h.partition("#")
                el["href"] = p.replace(".html", suf + ".html") + ("#" + frag if frag else "")
            elif not re.match(r"^(https?:|mailto:|tel:|#|data:|javascript:)", h) and (h.endswith("/") or "/#" in h or h.startswith("../")):
                el["href"] = add_param(h, "lang", code)
    if soup.title and soup.title.string:
        soup.title.string = tr(soup.title.string)
    for sc in soup.find_all("script"):
        t = sc.string
        if t and "afs-bar" not in t:
            t = translate_js(t, tr, js_map)
            sc.string = t
    out = str(soup)
    out = re.sub(r'<html lang="[^"]*"', f'<html lang="{hl}"', out, count=1)
    out = add_lang_row(out, base, code)
    return out


JS_LIT = re.compile(r"""(["'])((?:\\.|(?!\1)[^\\\n])*)\1""")


def translate_js(t, tr, js_map):
    """Script texts the reader sees: exact snippets from __js__ first, then any quoted string that is a
    visible text of the form (field names the script looks up must match the translated page)."""
    for en_s, v in sorted(js_map.items(), key=lambda kv: -len(kv[0])):
        t = t.replace(en_s, v)

    def lit(m):
        body = m.group(2)
        k = norm(body)
        if k != body or not needs(k):
            return m.group(0)
        v = tr.d.get(k)
        if v is None and " — " in k and all(p in tr.d for p in k.split(" — ")):
            v = " — ".join(tr.d[p] for p in k.split(" — "))
        if v is None:
            return m.group(0)
        if m.group(1) in v:
            v = v.replace(m.group(1), "\\" + m.group(1))
        return m.group(1) + v + m.group(1)
    return JS_LIT.sub(lit, t)


def add_param(h, k, v):
    p, hs, frag = h.partition("#")
    p = re.sub(rf"([?&]){k}=[^&]*&?", r"\1", p).rstrip("?&")
    return p + ("&" if "?" in p else "?") + f"{k}={v}" + (hs + frag)


# ---------------------------------------------------------------- in-place pages (switch where you are)

IP_JS = """<script id="afs-i18n-js">(function(){var L=%s,T=%s,H=%s,HOME="%s";
function pick(){var m=/[?&]lang=([a-z-]+)/i.exec(location.search),q=m&&m[1].toLowerCase(),a={ptbr:"pt","pt-br":"pt"};q=a[q]||q;if(q&&L.indexOf(q)>=0)return q;try{var s=localStorage.getItem("afs-lang");if(s&&L.indexOf(s)>=0)return s}catch(e){}var n=(navigator.language||"").slice(0,2).toLowerCase();return L.indexOf(n)>=0?n:"en"}
function withLang(h,c){var p=h.split("#"),u=p[0].replace(/([?&])lang=[^&#]*&?/,"$1").replace(/[?&]$/,"");if(c!=="en"||u.indexOf(HOME)===0)u+=(u.indexOf("?")<0?"?":"&")+"lang="+c;return u+(p.length>1?"#"+p.slice(1).join("#"):"")}
function apply(c){window.__afsLang=c;document.documentElement.lang=H[c];if(T[c])document.title=T[c];var a=document.querySelectorAll("a[href]");for(var i=0;i<a.length;i++){var el=a[i],d=el.getAttribute("data-href-"+c),h=el.getAttribute("href");if(d){el.setAttribute("href",d);continue}if(!h||/^(mailto:|tel:|#|data:|javascript:)/i.test(h))continue;if(/^https?:/i.test(h)&&h.indexOf(HOME)!==0)continue;el.setAttribute("href",withLang(h,c))}}
var c=pick(),r=document.getElementById("l-"+c);if(r)r.checked=true;apply(c);
for(var i=0;i<L.length;i++){var x=document.getElementById("l-"+L[i]);if(x)x.addEventListener("change",(function(k){return function(){try{localStorage.setItem("afs-lang",k)}catch(e){}apply(k)}})(L[i]))}})();</script>"""


def ip_css(codes):
    hide = ",".join(f"#l-{c}:checked~* .L:not([data-l={c}])" for c in codes)
    lab = ",".join(f"#l-{c}:checked~* .afs-langs label[for=l-{c}]" for c in codes)
    focus = ",".join(f"#l-{c}:focus-visible~* .afs-langs label[for=l-{c}]" for c in codes)
    return ('<!-- afs-i18n:start --><style id="afs-i18n-css">.lr{position:absolute;opacity:0;pointer-events:none;width:1px;height:1px}'
            f"{hide}{{display:none!important}}"
            '.afs-langs{display:flex;flex-wrap:wrap;gap:8px;margin:4px 0 18px}.afs-langs label{border:1px solid #D6DEE8;background:#fff;color:#1A365D;'
            'border-radius:999px;padding:8px 14px;font-weight:600;cursor:pointer;min-height:44px;display:inline-flex;align-items:center;font-family:inherit}'
            f"{lab}{{background:#0D9488;color:#fff;border-color:#0D9488}}{focus}{{outline:2px solid #0D9488;outline-offset:3px}}"
            '@media (prefers-color-scheme:dark){.afs-langs label{background:#16223A;color:#E6EEF7;border-color:#2A3A55}}'
            "</style><!-- afs-i18n:end -->")


def ip_radios(codes):
    return "<!-- afs-radios:start -->" + "".join(
        f'<input type="radio" name="lang" id="l-{c}" class="lr"{" checked" if c == "en" else ""} aria-label="{lab}">'
        for c, lab, _, _ in LANGS if c in codes) + "<!-- afs-radios:end -->"


def ip_nav(codes):
    return ('<nav class="afs-langs" aria-label="Language" translate="no">' + "".join(
        f'<label for="l-{c}" lang="{hl}">{lab}</label>' for c, lab, hl, _ in LANGS if c in codes) + "</nav>")


def collapse(soup):
    """Undo a previous build: every group of language spans goes back to its English text."""
    for sp in soup.select('span.L[data-l="en"]'):
        nxt = sp.next_sibling
        while nxt is not None and getattr(nxt, "name", None) == "span" and "L" in (nxt.get("class") or []) and nxt.get("data-l") != "en":
            after = nxt.next_sibling
            nxt.decompose()
            nxt = after
        sp.replace_with(NavigableString(sp.get_text()))


def expand_inplace(html, codes, trs, variants, page):
    """English in-place page -> page with a span per language for every visible text."""
    html = re.sub(r"<!-- afs-(?:i18n|radios):start -->.*?<!-- afs-(?:i18n|radios):end -->", "", html, flags=re.S)
    html = re.sub(r'<script id="afs-i18n-js">.*?</script>', "", html, flags=re.S)
    soup = BeautifulSoup(html, "html.parser")
    collapse(soup)
    # old per-page language radios and buttons are replaced by the shared ones
    for el in soup.select('input[name="lang"].lr'):
        el.decompose()
    titles = {}
    t_en = norm(soup.title.string) if soup.title and soup.title.string else ""
    for w in soup.select("span.Lw > span.Lw"):
        w.unwrap()
    # text broken by <br> inside a grid or flex box stays one item when it gets language spans
    for br in soup.find_all("br"):
        par = br.parent
        if par is None or "Lw" in (par.get("class") or []) or par.name in ("body", "main", "section", "div") and par.get("class") is None:
            continue
        if any(isinstance(c, NavigableString) and needs(norm(c)) for c in par.children):
            w = soup.new_tag("span", attrs={"class": "Lw"})
            for c in list(par.children):
                w.append(c.extract())
            par.append(w)
    for s in list(texts(soup)):
        lead = s[: len(s) - len(s.lstrip())]
        trail = s[len(s.rstrip()):]
        en = norm(s)
        if all(trs[c](en) == en for c in codes if c != "en"):
            continue  # names, the email address, the phone number: the same in every language
        frag = BeautifulSoup("", "html.parser")
        parts = [NavigableString(lead)] if lead else []
        for c in codes:
            sp = frag.new_tag("span", attrs={"class": "L", "data-l": c})
            sp.string = en if c == "en" else trs[c](en)
            if c != "en":
                sp["lang"] = dict((x, h) for x, _, h, _ in LANGS)[c]
            parts.append(sp)
        if trail:
            parts.append(NavigableString(trail))
        s.replace_with(*parts)
    for a in soup.find_all("a", href=True):
        if any(x.get("translate") == "no" for x in [a] + [q for q in a.parents if q.name]):
            continue
        if has_variant(page, a["href"], variants):
            a["data-href-en"] = a["href"]
            for c, _, _, suf in OTHER:
                if c in codes:
                    a[f"data-href-{c}"] = a["href"].replace(".html", suf + ".html")
    js_d = {c: {} for c in codes if c != "en"}
    for sc in soup.find_all("script"):
        t = sc.string
        if not t or "afs-bar" in t or sc.get("id") in ("afs-i18n-js", "af-source"):
            continue
        t = re.sub(r"__afsT\((\"[^\"]*\")\)", lambda m: "'" + json.loads(m.group(1)).replace("'", "\\'") + "'", t)

        def lit(m):
            body = m.group(2)
            k = norm(body)
            if k != body or not needs(k) or not all(k in trs[c].d for c in js_d):
                return m.group(0)
            for c in js_d:
                js_d[c][k] = trs[c].d[k]
            return "__afsT(" + json.dumps(k) + ")"
        sc.string = JS_LIT.sub(lit, t)
    for c in codes:
        titles[c] = t_en if c == "en" else (trs[c](t_en) if t_en else "")
    out = str(soup)
    out = re.sub(r"<!-- afs-langs:start -->.*?<!-- afs-langs:end -->", "<!-- afs-langs:start -->" + ip_nav(codes) + "<!-- afs-langs:end -->", out, flags=re.S)
    i = out.find("</head>")
    out = out[:i] + ip_css(codes).replace("<!-- afs-i18n:end -->", "<script>window.__afsT=function(k){var c=window.__afsLang||\"en\",m=window.__afsD&&window.__afsD[c];return m&&m[k]||k};</script><!-- afs-i18n:end -->") + out[i:]
    b = out.index(">", out.index("<body")) + 1
    out = out[:b] + ip_radios(codes) + out[b:]
    hl = {c: h for c, _, h, _ in LANGS}
    js = IP_JS % (json.dumps(codes), json.dumps(titles, ensure_ascii=False), json.dumps({c: hl[c] for c in codes}), HOME)
    js = js.replace("<script id=\"afs-i18n-js\">", "<script id=\"afs-i18n-js\">window.__afsD=" + json.dumps(js_d, ensure_ascii=False) + ";", 1)
    j = out.rfind("</body>")
    out = out[:j] + js + out[j:]
    return out
