"""Kiswahili fillable PDFs for /forms, made from the English fillable PDFs.

Every printed text and every field tooltip is looked up in i18n/sw.json (the same Kiswahili the browser
forms use). Lines of a paragraph are joined, translated and wrapped again into the same lines; a text that
is longer in Kiswahili is set a little smaller so nothing overlaps. All fields stay as they are.
Missing texts are listed in i18n/missing-sw-pdf.txt and stop the run.

Run from the repo root:  python3 tools/pdf_sw.py
"""
import pathlib, re, sys
import pikepdf
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import i18n

FORMS = ["player", "scout", "coach", "coach-hire"]
TITLES = {"player": "Fomu ya Uskauti na Wasifu wa Kazi ya Mchezaji", "scout": "Fomu ya Usajili wa Mchezaji na Taarifa za Soko",
          "coach": "Fomu ya Tathmini na Maendeleo ya Mchezaji", "coach-hire": "Fomu ya Taarifa na Tathmini ya Kocha"}
RIGHT = 576.0


def dec(b):
    return bytes(b).decode("cp1252", errors="replace")


def enc(s):
    return s.encode("cp1252", errors="replace")


def font_name(pdf_font):
    base = str(pdf_font.get("/BaseFont", "/Helvetica"))[1:]
    return base if base in ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique", "Times-Roman", "Courier") else "Helvetica"


def runs(ops):
    """Text runs: (op index of Tj, font, size, leading, x, y, text)."""
    out, font, size, lead, x, y, tm = [], None, 10, 12, 0, 0, None
    for i, (operands, op) in enumerate(ops):
        o = str(op)
        if o == "Tf":
            font, size = str(operands[0]), float(operands[1])
        elif o == "TL":
            lead = float(operands[0])
        elif o == "Tm":
            x, y, tm = float(operands[4]), float(operands[5]), i
        elif o == "Tj":
            out.append([i, font, size, lead, x, y, dec(operands[0]), tm])
    return out


def paragraphs(rs):
    """Consecutive lines with the same font, size and x, one leading apart, form one paragraph."""
    groups = []
    for r in rs:
        g = groups[-1] if groups else None
        if g and r[1] == g[-1][1] and r[2] == g[-1][2] and abs(r[4] - g[-1][4]) < .01 and 0 < g[-1][5] - r[5] <= max(r[3] * 1.05, r[2] * 1.6) + .01:
            g.append(r)
        else:
            groups.append([r])
    return groups


def wrap(text, fname, size, width):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if stringWidth(t, fname, size) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


ENTRY = re.compile(r"^(.*) \(Entry (\d+)\)$")
DASH = re.compile(r"^(.*?) - (.*)$")


def sw_text(tr, en):
    """Kiswahili for a PDF text or tooltip, including the PDF's own patterns."""
    k = i18n.norm(en)
    m = ENTRY.match(k)
    if m:
        return f"{sw_text(tr, m.group(1))} (Ingizo {m.group(2)})"
    if k not in tr.d and " — " in k:
        return " — ".join(sw_text(tr, part) for part in k.split(" — "))
    if k not in tr.d and DASH.match(k):
        a, b = DASH.match(k).groups()
        if (a in tr.d or " — " in a) and b in tr.d:
            return f"{tr(a)} - {tr(b)}"
    if k not in tr.d and len(k) >= 80:
        full = [key for key in tr.d if key.startswith(k)]
        if len(full) == 1:
            return tr.d[full[0]]
    return tr(k)


def main():
    tables, keep = i18n.load_tables()
    tr = i18n.Tr("sw", tables["sw"], keep)
    extra = {}
    page_re = re.compile(r"^Page (\d+)$")
    for base in FORMS:
        src = ROOT / "forms" / f"{base}-fillable-en.pdf"
        pdf = pikepdf.open(src)
        for pno, page in enumerate(pdf.pages):
            fonts = {str(k): font_name(v) for k, v in page.Resources.get("/Font", {}).items()}
            ops = list(pikepdf.parse_content_stream(page))
            rs = runs(ops)
            for g in paragraphs(rs):
                fname = fonts.get(g[0][1], "Helvetica")
                size = g[0][2]
                en = " ".join(r[6].strip() for r in g)
                m = page_re.match(en)
                if m:
                    sw = f"Ukurasa {m.group(1)}"
                elif base.upper() in en and en.endswith("FORM"):
                    sw = {"PLAYER FORM": "FOMU YA MCHEZAJI", "SCOUT FORM": "FOMU YA SKAUTI", "COACH FORM": "FOMU YA KOCHA",
                          "COACH-HIRE FORM": "FOMU YA KUAJIRI KOCHA"}.get(en, en)
                else:
                    sw = sw_text(tr, en)
                if sw == i18n.norm(en):
                    continue
                # room on the right: the page margin or the next text on the same line
                x, y = g[0][4], g[0][5]
                nxt = [r[4] for r in rs if abs(r[5] - y) < .6 and r[4] > x + 1]
                width = (min(nxt) - 8 if nxt else RIGHT) - x
                width = max(width, max(stringWidth(r[6], fname, size) for r in g))
                ow = stringWidth(g[0][6], fname, size)
                if len(g) == 1 and x + ow > 540 and abs(x + ow - round(x + ow)) < 1 and not nxt:
                    # right-aligned header or page number: keep the right edge, start further left
                    nw = stringWidth(sw, fname, size)
                    tm = g[0][7]
                    if tm is not None:
                        o = list(ops[tm].operands)
                        o[4] = float(o[4]) + ow - nw
                        ops[tm] = pikepdf.ContentStreamInstruction(o, pikepdf.Operator("Tm"))
                    ops[g[0][0]] = pikepdf.ContentStreamInstruction([pikepdf.String(enc(sw))], pikepdf.Operator("Tj"))
                    continue
                s = size
                lines = wrap(sw, fname, s, width)
                while len(lines) > len(g) and s > size * .72:
                    s -= .25
                    lines = wrap(sw, fname, s, width)
                scale = 100.0
                if len(lines) > len(g):
                    lines = lines[: len(g) - 1] + [" ".join(lines[len(g) - 1:])]
                longest = max(stringWidth(l, fname, s) for l in lines)
                if longest > width:
                    scale = max(60.0, 100.0 * width / longest)
                for k, r in enumerate(g):
                    text = lines[k] if k < len(lines) else ""
                    i = r[0]
                    ops[i] = pikepdf.ContentStreamInstruction([pikepdf.String(enc(text))], pikepdf.Operator("Tj"))
                    if s != size or scale != 100.0:
                        # set the smaller size and squeeze just for this run
                        ops[i] = pikepdf.ContentStreamInstruction([pikepdf.String(enc(text))], pikepdf.Operator("Tj"))
                        r.append(None)
                        r[8] = (s, scale)
            # apply size and squeeze changes: insert Tf / Tz right before each changed Tj
            new_ops = []
            changed = {r[0]: r[8] for r in rs if len(r) > 8}
            for i, ins in enumerate(ops):
                if i in changed:
                    s, scale = changed[i]
                    fkey = next(r[1] for r in rs if r[0] == i)
                    new_ops.append(pikepdf.ContentStreamInstruction([pikepdf.Name(fkey), s], pikepdf.Operator("Tf")))
                    new_ops.append(pikepdf.ContentStreamInstruction([scale], pikepdf.Operator("Tz")))
                new_ops.append(ins)
            page.Contents = pdf.make_stream(pikepdf.unparse_content_stream(new_ops))
            # field tooltips
            for a in page.get("/Annots", []):
                if "/TU" in a:
                    a.TU = pikepdf.String(sw_text(tr, str(a.TU)))
        pdf.docinfo["/Title"] = TITLES[base]
        pdf.docinfo["/Subject"] = ("© 2026 Afritech Sports Technology and Innovation Group Limited. Haki zote zimehifadhiwa. Hairuhusiwi "
                                   "kunakiliwa, kurekebishwa, kuchapishwa upya au kutumika kufundisha mifumo ya AI bila ruhusa ya maandishi.")
        pdf.docinfo["/Copyright"] = "© 2026 Afritech Sports Technology and Innovation Group Limited. Haki zote zimehifadhiwa."
        if "/Lang" in pdf.Root or True:
            pdf.Root.Lang = pikepdf.String("sw")
        out = ROOT / "forms" / f"{base}-fillable-sw.pdf"
        pdf.save(out)
        print(out.relative_to(ROOT), len(pdf.pages), "pages")
    mf = i18n.I18N / "missing-sw-pdf.txt"
    if tr.missing:
        mf.write_text("\n".join(sorted(tr.missing)) + "\n", encoding="utf-8")
        sys.exit(f"Kiswahili PDFs: {len(tr.missing)} texts have no translation (see i18n/missing-sw-pdf.txt)")
    elif mf.exists():
        mf.unlink()
    print("Kiswahili PDFs complete")


if __name__ == "__main__":
    main()
