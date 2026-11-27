# Afritech Sports CV Desk

Football CVs for players, coaches, scouts and analysts, built and reviewed by Afritech Sports Technology and Innovation Group Limited.

Live: https://afritech-advisory.github.io/afritech-sports-cv-desk/

© 2026 Afritech Sports Technology and Innovation Group Limited. All rights reserved. The forms, questions, layouts and pages in this repository may not be copied, adapted, republished or used to train AI systems without written permission. Contact: Advisory@afritechsports.com

## Languages

Every page is in English, Français, Kiswahili and Português (BR). Names (people, clubs, Afritech Sports, MatchIQ, WhatsApp, LinkedIn), the email address and the phone number stay as written.

- Desk pages and sample layouts switch language in place with the language buttons (or `?lang=fr|pt|sw`).
- Coach, scout and analyst forms, and the player, scout and coach forms in `/forms`, have `-fr`, `-ptbr` and `-sw` copies made by the build from the English form. The Kiswahili fillable PDFs are made from the English PDFs.
- Translations live in `i18n/fr.json`, `i18n/pt.json` and `i18n/sw.json`, keyed by the exact English text. Names kept as written are in `i18n/keep.txt`.

After adding or changing any page, from the repo root:

```
python3 tools/build.py        # site bar + all four languages; stops and lists i18n/missing-<lang>.txt if any text has no translation
python3 tools/check_lang.py   # opens every translated page at 390 px; stops if any English shows or a page is wider than the phone
```

The same two steps run on every pull request (`.github/workflows/languages.yml`). Never publish with missing translations and never ship English inside a translated page.
