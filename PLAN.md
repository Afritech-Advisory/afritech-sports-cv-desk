# afritech-sports-cv-desk: version 1 plan

_Written 2026-11-03 from a question-and-answer session with Andrew Rukidi. No code has been written yet._

## 1. Goal
cv-desk is the single public home for Afritech player CVs. It takes over from
the `players/` folder in Player-Scouting-Forms. In order, it is:
1. a publishing site (version 1),
2. a place `/dashboard` output is committed to without hand-assembly (version 1, in Claude Code only),
3. later steps that follow from these. Nothing beyond 1 and 2 is in version 1.

## 2. Who uses it
- Club scouts and recruiters, mostly on a phone.
- Agents.
- Players and their families.
- Andrew, who publishes.

## 3. What each player gets
One folder per player, named with a slug: lowercase first and last name joined by a hyphen, ASCII only
(`seb-fisher`, `mohammed-bajaber`).

| File | What it is |
|---|---|
| `<slug>/index.html` | v3 tabbed public profile (club, agent and player-and-family views) |
| `<slug>/share.png` | 1200×630 share card, used as the link preview (og:image) |
| `<slug>/card.png` | 1080×1350 player card |
| `<slug>/cv.html` | Player CV as a web page, opening on the CV cover |
| `<slug>/cv.pdf` | Same CV as a PDF, built from `Afritech_Dossier_Front_Page_and_CV_Cover_Template.docx` |

At the repo root, `index.html` lists every player and links to each profile.

All of these files are public: anyone with the address may read any of them.

## 4. Hosting
- The repo is made **public** (it is private today) and served with GitHub Pages from `main`, root folder.
- Address: `https://afritech-advisory.github.io/afritech-sports-cv-desk/`
- No custom domain.

## 5. Contact details (every page)
Allowed, and nothing else:
- Email: Advisory@afritechsports.com
- LinkedIn, Afritech: https://www.linkedin.com/company/afritech-sports-technology-and-innovation-group-limited/
- LinkedIn, Andrew: https://www.linkedin.com/in/andrew-r-b1b514 (tracking parameters removed from the link Andrew supplied)

Banned: phone numbers, WhatsApp links or QR codes, and `tel:` links.

## 6. Publishing a player
- **From Claude Code:** at the end of `/dashboard`, Claude shows the files and, once Andrew approves, commits them to `<slug>/`, updates `index.html`, and pushes.
- **From Claude chat (phone):** Andrew uploads by hand using `PUBLISHING.md`, a checklist to be written as part of version 1: the folder name, the five exact file names, updating the index, and the checks in section 9.
- File names never contain spaces or browser-added suffixes such as `(1)`.

## 7. Rules on content
- Customer-safe material only. Internal decision files, risk notes, price limits and internal method names never go in this repo.
- English only.
- Pages work fully with JavaScript turned off. A small optional script is allowed only if the page works without it (as on the Seb Fisher pilot).
- Phone-first: check at 390px wide.

## 8. Edge cases
- **Player signs elsewhere or stops working with Afritech:** the profile stays up, showing the new club, as Afritech track record. If the player or family asks for removal, delete the player's folder and their index entry; the address then returns "not found".
- **Players under 18:** decided case by case by Andrew. No rule applies when the player's details are already public.
- **Links already sent out:** none exist for the current `players/` pages, so no redirects are needed.

## 9. Definition of done (version 1)
1. `seb-fisher/` and `mohammed-bajaber/` each contain all five files in section 3. Bajaber is rebuilt to the v3 tabbed template first.
2. The root `index.html` lists both players and carries only the section 5 contacts.
3. Every page loads at the GitHub Pages address on a phone at 390px wide, with JavaScript off.
4. A search of the repo finds no phone numbers, `wa.me`, `whatsapp` or `tel:`, and no file names with spaces or `(1)`.
5. `players/` (including `index (1).html`) is deleted from Player-Scouting-Forms.
6. `PUBLISHING.md` exists, and `/dashboard` can commit to cv-desk from Claude Code.

## 10. Not in version 1
- Intake or submission forms, and stage tracking (those stay in Player-Scouting-Forms).
- Internal decision files.
- Logins, passwords or private links.
- A custom domain.
- Visitor analytics or tracking.
- Languages other than English.
- Building pages automatically from a dossier. `/dashboard` builds them; cv-desk only stores and serves them.
- Phone numbers and WhatsApp.

## 11. Open flags
_Correction (2026-11-03): an earlier draft listed a separate `public.html`. The v3 skill makes the tabbed profile itself the public page, with a separate 1200×630 share card, so the five files are now index, share card, player card, CV page and CV PDF._

1. **Phone numbers are public now.** Two numbers and a WhatsApp link are live in Player-Scouting-Forms `players/` today. They disappear at done-item 5. Andrew may want them removed sooner.
2. **The `/dashboard` skill:** v3.1 was written on 2026-11-03 with the commit step, the cv-desk layout and email/LinkedIn-only contacts. It goes live once Andrew uploads it on claude.ai (Customize > Skills).
3. **Missing files:** Seb Fisher has only the profile today, and needs the public page, card, CV page and CV PDF. Bajaber needs all five. Each needs the Afritech logo and a verified player photo supplied before building.
4. **Photo and image rights:** player photos become public. Confirm Afritech may publish each one.
5. **How "signed" looks is not yet confirmed:** the skill (v3.1) uses one line, "Signed with <club>, <month year>", under the name and in the same index list. Andrew to confirm.
8. **"Book a call" with no phone:** the skill (v3.1) makes these buttons email links to Advisory@afritechsports.com. Andrew to confirm, or name a booking page.
9. **CTA orange:** the dashboard skill uses #E8701A, while the other skills use #F97316. Unresolved; v3.1 leaves it as it was.
6. **Under-18 risk:** the case-by-case rule leaves no written record of consent. That is Andrew's decision; noted here only so it is visible.
7. **Making the repo public** exposes its history too. It currently holds only the initial commit, so nothing is at risk today.
