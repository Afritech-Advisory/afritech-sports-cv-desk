# Afritech Sports Player CV Desk: version 1 plan

_Rewritten 2026-11-03. Replaces the earlier draft, which covered only publishing and missed the intake desk._

## 1. What the CV Desk is
One path from "here is a player" to "here is a live Player CV":

1. **Intake.** A player, parent, scout, coach or agent opens the CV Desk link, picks a language and their role, and fills in the full Afritech form.
2. **Send.** They save the form as a PDF and email it to Advisory@afritechsports.com.
3. **Review.** Afritech Sports reviews every form. Nothing is shared with a club, agent or family until Afritech approves it.
4. **Build.** Afritech runs `/dashboard` (afritech-scouting-dashboard v3.1) on the dossier to make the profile, share card, player card and CV.
5. **Publish.** The files go live in this repo on GitHub Pages.

## 2. Who uses it
| Person | Uses | Form |
|---|---|---|
| Player, or parent/guardian for under-18s | Intake | Player Scouting & Career Profile Form (20 sections) |
| Scout, coach, recruitment analyst, FIFA-licensed agent | Intake | Player Recruitment & Market Intelligence Form (19 sections). Scouts and coaches use the same form |
| Afritech Sports | Review, build, publish | — |
| Clubs, agents, families | Read the published CV, mostly on a phone | — |

No one filling in a form needs a claude.ai account or any sign-in.

## 3. Intake (live since 2026-11-03)
- **Front door:** the root page of this repo, https://afritech-advisory.github.io/afritech-sports-cv-desk/ (moved here 2026-11-10 so people can open it without a Claude account). The CV Desk sits at the top and the published players are listed underneath. This is the link to share, including on WhatsApp. It has no database or sign-in features.
- **Old front door:** the claude.ai artifact "Afritech Sports Player CV Desk", https://claude.ai/artifact/K5uuVkDWXfTQ5P6xEoiEtd. Keep it up for links already sent, but do not share it again.
- **Languages:** English, Français, Português (BR), Español (LATAM). The page picks the phone's language and has a switch at the top. It works with scripts off (English shown).
- **Forms:** the two buttons open the existing v5.0 forms from Player-Scouting-Forms on GitHub Pages:

| Language | Player / parent | Scout / coach / agent |
|---|---|---|
| English | `player.html` | `scout.html` |
| Français | `player-fr.html` | `scout-fr.html` |
| Português (BR) | `player-ptbr.html` | `scout-ptbr.html` |
| Español (LATAM) | `player-eslatam.html` | `scout-eslatam.html` |

  Base address: `https://afritech-advisory.github.io/Player-Scouting-Forms/`
- **Drafts:** the forms save answers on the phone as people type and restore them on reopening, with a "Clear saved answers" button (restored and live 2026-11-03).
- **Sending:** in the form, Review, then Save as PDF, then email the PDF to Advisory@afritechsports.com.
- **Standard:** the forms must keep everything in the v4.2 Player / Parent form Andrew supplied: all sections, repeatable entries, a progress percentage, Review, Copy text, Save as PDF, and readable without scripts.
- **Approval wording:** pages say Afritech Sports reviews and approves, never a named person.

## 4. Publishing (this repo)
- The repo becomes **public** and is served by GitHub Pages from `main`, root folder, at `https://afritech-advisory.github.io/afritech-sports-cv-desk/`. No custom domain.
- One folder per player, named with a slug: lowercase first and last name, hyphenated, ASCII only (`seb-fisher`, `mohammed-bajaber`).

| File | What it is |
|---|---|
| `<slug>/index.html` | Tabbed public profile (club, agent and player-and-family views) |
| `<slug>/share.png` | 1200×630 share card, used as the link preview |
| `<slug>/card.png` | 1080×1350 player card |
| `<slug>/cv.html` | Player CV as a web page, opening on the CV cover |
| `<slug>/cv.pdf` | Same CV as PDF, built on `Afritech_Dossier_Front_Page_and_CV_Cover_Template.docx` |

- The root `index.html` is the CV Desk front door (section 3) followed by every live player, each linking to their profile. When a player is added, add their card under "Players" and leave the front door above it unchanged.
- Everything here is public. Customer-safe material only: internal decision files, risk notes, price limits and internal method names never go in this repo.
- English only for published CVs.
- Pages work fully with scripts off. A small optional script is allowed only if the page works without it.
- **Publishing route:** from Claude Code, `/dashboard` commits after Afritech approves. From Claude chat on a phone, upload by hand using the checklist in the dashboard skill. File names never contain spaces or "(1)".

## 5. Contact details (every page, form front door and CV)
- The contact block names Afritech Sports Technology and Innovation Group Limited, Advisory Services, Nairobi, Kenya. No personal name (ruling 2026-11-03).
- Email: Advisory@afritechsports.com
- Phone: Kenya +254 715 551 506 only. The US number is never used (ruling 2026-11-03).
- WhatsApp: "Chat with Afritech on WhatsApp" button (stays, ruling 2026-11-03).
- LinkedIn, Afritech: https://www.linkedin.com/company/afritech-sports-technology-and-innovation-group-limited/
- LinkedIn, Andrew Rukidi: https://www.linkedin.com/in/andrew-r-b1b514 (stays, ruling 2026-11-03), as a link only.
- Never: any other phone number or `tel:` links.

## 6. Edge cases
- **Player signs elsewhere or stops working with Afritech:** the profile stays up as track record, with "Signed with <club>, <month year>". If the player or family asks for removal, delete the folder and the index entry in one commit.
- **Under-18s:** Afritech decides case by case before building. No rule applies where the details are already public.
- **The person forgets to attach the PDF:** Afritech receives nothing usable and replies asking for it.
- **The person closes the form before saving:** once the draft-saving change is live, their answers come back when they reopen the form on the same phone. A different phone or a cleared browser starts empty.
- **Links already sent:** the claude.ai CV Desk link has been shared and stays up; new shares use the GitHub address in section 3. No links to `player-scouting-forms/players/` were sent, so those pages can simply be deleted.

## 7. Definition of done (version 1)
1. The CV Desk opens both forms in all four languages on a phone, with no sign-in. **Done 2026-11-03**, except a live tap-test of the links on a phone.
2. `seb-fisher/` and `mohammed-bajaber/` each hold all five files in section 4. Bajaber is rebuilt to the v3 tabbed template first.
   - **First player published 2026-11-05:** `jackson-dwanga/` (all five files), from his CV Desk form of 2026-11-04. The root `index.html` lists him.
   - **Done 2026-11-05:** `seb-fisher/` and `mohammed-bajaber/` published with all five files. Bajaber's profile rebuilt into five tabs from his 2 Nov 2026 Player CV; Afritech-only contact, Kenyan number only.
3. The root `index.html` lists both players with only the section 5 contacts.
4. Every published page loads on the GitHub Pages address at 390px wide with scripts off.
5. A search of this repo finds no phone number other than +254 715 551 506, no `tel:` and no personal name in a contact block, and no file names with spaces or `(1)`.
6. `players/` is deleted from Player-Scouting-Forms.
7. `/dashboard` v3.1 is uploaded on claude.ai and can commit to this repo from Claude Code.

## 8. Not in version 1
- Any sign-in, database, inbox or progress tracking on the CV Desk.
- A service that stores form submissions (Formspree, Google Forms or similar).
- Building CVs automatically from a submitted PDF. Afritech runs `/dashboard`.
- Changes to the form questions.
- Visitor analytics, a custom domain, or published CVs in languages other than English.

## 9. Open flags
_Resolved 2026-11-03: draft saving restored in all 8 forms (on the working branch); phone tap-test passed; CV Desk translations accepted for now; contact blocks are Afritech-only; only the Kenyan number remains._

1. ~~**Merge to `main`.**~~ Done 2026-11-03 (Player-Scouting-Forms PR #1); CV Desk step 1 updated. Original note: Draft saving and the Afritech-only profile contacts are on branch `claude/dreaming-pass-projects-rxyirh` of Player-Scouting-Forms. The live forms the CV Desk links to update only once that branch is merged into `main`. After the merge, change the CV Desk's step 1 from "finish in one sitting" to "your answers are saved on this phone".
2. ~~**WhatsApp button:**~~ Stays (ruling 2026-11-03). Original note: the Seb Fisher and Bajaber profiles still carry "Chat with Afritech on WhatsApp". Confirm whether it stays and that it reaches the Kenyan number.
3. ~~**Personal LinkedIn:**~~ Stays (ruling 2026-11-03). Original note: with contact blocks Afritech-only, the dashboard skill now lists only the Afritech LinkedIn page. Restore Andrew's personal LinkedIn if wanted.
4. **Phone fields inside the forms.** The forms ask for the respondent's and guardian's phone or WhatsApp. Confirm this is fine for intake.
5. **Missing files and assets:** Seb Fisher needs the share card, player card, CV page and CV PDF; Bajaber needs all five. Each needs the Afritech logo and a verified player photo, and confirmation that Afritech may publish each photo.
6. **"Signed" display and "Book a call" by email** (dashboard skill v3.1) are proposed defaults, not yet confirmed.
7. **CTA orange:** #E8701A (dashboard skill, CV Desk) vs #F97316 (other skills). Unresolved.
8. **Making this repo public** exposes its history, which currently holds only this plan and the initial commit.
9. **Dashboard skill upload:** re-upload `afritech-scouting-dashboard.zip` (updated 2026-11-03 with the Afritech-only contact rules) on claude.ai.
