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
- **Forms:** the two buttons open the v5.0 forms in the `forms/` folder of this repo (moved here from Player-Scouting-Forms on 2026-11-15, on branch until merged):

| Language | Player / parent | Scout / coach / agent |
|---|---|---|
| English | `player.html` | `scout.html` |
| Français | `player-fr.html` | `scout-fr.html` |
| Português (BR) | `player-ptbr.html` | `scout-ptbr.html` |
| Español (LATAM) | `player-eslatam.html` | `scout-eslatam.html` |

  Base address: `https://afritech-advisory.github.io/afritech-sports-cv-desk/forms/`
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

## 10. One site for the forms (2026-11-15, on branch, not yet live)
- Every form now lives in `forms/` in this repo: the player, scout, coach and coach-hire browser forms in four languages, the three dashboards, the 16 fillable PDFs and the forms list page (`forms/index.html`). 36 files, copied unchanged except that the dashboards' own address now points here.
- The CV Desk buttons link to `forms/player*.html` and `forms/scout*.html`.
- Player-Scouting-Forms becomes redirects only: each old page forwards to the same file name here, and its `404.html` forwards anything else, including the old PDF addresses. It is no longer updated.
- Drafts carry over, because both sites share the address `afritech-advisory.github.io` and the forms keep their file names.
- **Merge order:** this repo first, then Player-Scouting-Forms. The other way round, the old addresses would forward to pages that do not exist yet.
- **After both merges:** tap-test one old form address on a phone, then archive Player-Scouting-Forms (leave Pages on so the redirects keep working).

## 11. Four segments (direction set 2026-11-15)
Afritech Sports is to become the football recruitment and employment hub, built one segment at a time, each in its own session:
1. Players (this desk; forms move above comes first).
2. Coaches. **Live 2026-11-16, see section 12.** History: a first draft of a Coach CV Desk was built and set aside on 2026-11-15: commit `537dd4b` on branch `claude/nifty-lamport-e3od7w`, reverted by `4a8fe30`. Rulings already given for it: a coach's own CV form plus an assessment form open to players, parents, schools, academies, colleges, universities, clubs, federations and agencies in any country; tactical and physical performance coaching both covered; both genders; English first; Afritech's own coaches are the first examples and fill in the form themselves.
3. Scouts. **Built 2026-11-16, see section 13.**
4. Football analysts (all analysis roles, not only data). **Built 2026-11-16, see section 14.** Andrew's instruction of 2026-11-15: apply the coach rulings with "analyst" in place of "coach".

## 12. Coach CV Desk (live 2026-11-16)
The same path as players, for coaches. It lives in `coaches/` in this repo.

- **Front door:** `coaches/index.html`, at `https://afritech-advisory.github.io/afritech-sports-cv-desk/coaches/`. This is the one link to send coaches. The root page links to it from a "Coaches" section under the players.
- **Two forms, English only for now:**

| Who fills it in | Form | File |
|---|---|---|
| The coach | Coach CV & Career Profile Form v1.0 (12 sections) | `coaches/coach-cv.html` |
| Anyone assessing a coach: player, parent, school, academy, college, university, club, federation or agency, in any country | Coach Intelligence & Assessment Form v5.1 | `coaches/coach-assessment.html` |

- **Coach CV form:** covers every kind of coach (head coach, tactical, physical performance, goalkeeping, youth and others), men's and women's football, and the coach's own gender. Tactical coaching (section 6) and physical performance coaching (section 7) are separate sections; a coach completes the ones that fit.
- **Assessment form:** made from the v5.0 Coach-hire form. Changes from v5.0: the assessor list widened beyond clubs, federations and agencies; the kind of coaching and men's or women's football added to the cover; questions for physical performance specialists added to section 9; experience in men's and women's football added to section 3. Added 2026-11-16: "Player or family decision" and "School, academy, college or university decision" under Mandate authority; safeguarding checks in section 3; a plain decision question for players, families and schools in section 14; "Sex" became "Coach's gender" with "Not known".
- **`forms/coach-hire*.html` (v5.0, four languages) is unchanged.** The Coach CV Desk links only to the v5.1 form.
- **Both forms** save a draft on the phone and are sent the same way as the player forms: Review, Save as PDF, email to Advisory@afritechsports.com. Contact, wording and publishing rules are sections 4 and 5.
- **PDF file name (2026-11-16):** Save as PDF names the file after the coach, `Coach CV - <name>.pdf` or `Coach Assessment - <name>.pdf`, taken from "Coach full name" on the cover. With no name typed it keeps the form's title. The blank last page is gone. The same now applies to all 16 forms in `forms/`, in every language: `Player CV - <name>.pdf` (player forms), `Player Scouting - <name>.pdf` (scout forms), `Player Assessment - <name>.pdf` (coach forms about a player) and `Coach Assessment - <name>.pdf` (coach-hire forms). The prefix stays in English in every language so the inbox sorts the same way.
- **Scripts off:** the front page works fully. The forms can be read, with a notice that saving, Add, Review and Save as PDF need scripts on (the player forms behave the same way but show no notice).
- **First coaches:** Afritech Sports' own coaches fill in the Coach CV form themselves. Never invent a coach, a name or a detail. Their profiles go in `coaches/<slug>/` and are listed on `coaches/index.html`, which says none are published yet until the first one is.
- **Published Coach CV layout:** `coaches/sample-layout/index.html` is the template, based on the player profile. Every line in it is marked placeholder. It is not linked from any page and asks search engines not to list it. To publish a coach, copy it to `coaches/<slug>/`, replace every placeholder with the coach's own answers, remove the sample banner and the noindex line, and add the coach's card to `coaches/index.html`.

Open flags for coaches:
1. What an assessor gets back after sending the assessment form is not yet stated on the page beyond "Afritech Sports reviews it".
2. French, Portuguese (BR) and Spanish (LATAM) versions wait until the questions are settled.
3. The dashboard skill builds player profiles only. Coach CVs are built by hand from the sample layout until it learns coaches.
4. Coach share card (`share.png`), coach card and PDF CV are not designed yet.

## 13. Scout CV Desk (built 2026-11-16)
The same path as players and coaches, for scouts. It lives in `scouts/` in this repo.

- **Front door:** `scouts/index.html`, at `https://afritech-advisory.github.io/afritech-sports-cv-desk/scouts/`. This is the one link to send scouts. The root page links to it from a "Scouts" section under the coaches.
- **Two forms, English only for now:**

| Who fills it in | Form | File |
|---|---|---|
| The scout | Scout CV & Career Profile Form v1.0 (12 sections) | `scouts/scout-cv.html` |
| Anyone assessing a scout: player, parent, school, academy, college, university, club, federation or agency, in any country | Scout Intelligence & Assessment Form v1.0 (15 sections) | `scouts/scout-assessment.html` |

- **Not the same as `forms/scout*.html`.** Those are the v5.0 Player Recruitment & Market Intelligence forms, which a scout, coach or agent fills in about a player. They are unchanged. The Scout CV Desk forms are about the scout. Both new forms point a scout who wants to report on a player back to the front page.
- **No base form existed.** There was no "scout-hire" form to build from, so the assessment form is new, v1.0, built on the section pattern of the v5.1 Coach assessment form.
- **Scout CV form:** covers every kind of scout (club, academy, area, independent, agency, video, data, opposition, college recruitment, physical profiling, chief scout), men's and women's football, and the scout's own gender. Technical and tactical scouting (section 6) and physical performance scouting (section 7) are separate; a scout completes the ones that fit. Section 5 is the track record: players identified, with who can confirm it. Section 8 asks how the scout approaches under-18s and families, and whether they have ever charged a player or family.
- **Assessment form:** section 3 lets a family check a scout who has approached them: whether the named club confirmed the scout works for it, whether money was asked for, the FIFA agent licence, safeguarding and background checks. Section 13 has separate decisions for players and families, for clubs, federations and agencies, and for an agency representing the scout. Section 10 (cost) is marked as one players and families can skip.
- **Both forms** save a draft on the phone and are sent like the others: Review, Save as PDF, email to Advisory@afritechsports.com. Save as PDF names the file `Scout CV - <name>.pdf` or `Scout Assessment - <name>.pdf` from "Scout full name". With scripts off the forms can be read, with the same notice as the coach forms. Contact, wording and publishing rules are sections 4 and 5.
- **First scouts:** Afritech Sports' own scouts fill in the Scout CV form themselves. Never invent a scout, a name or a detail. Their profiles go in `scouts/<slug>/` and are listed on `scouts/index.html`, which says none are published yet until the first one is.
- **Published Scout CV layout:** `scouts/sample-layout/index.html`, based on the player profile and the coach sample. Tabs: Profile, How they scout, Players found, Career, Evidence, Contact. Every line in it is marked placeholder. It is not linked from any page and asks search engines not to list it. To publish a scout, copy it to `scouts/<slug>/`, replace every placeholder with the scout's own answers, remove the sample banner and the noindex line, and add the scout's card to `scouts/index.html`.

Open flags for scouts:
1. What an assessor gets back after sending the assessment form is not yet stated beyond "Afritech Sports reviews it" (same as coaches).
2. French, Portuguese (BR) and Spanish (LATAM) versions wait until the questions are settled.
3. The dashboard skill builds player profiles only. Scout CVs are built by hand from the sample layout.
4. Scout share card, scout card and PDF CV are not designed yet.
5. A player named in a scout's track record is published only with the player's (or parent's) agreement and once Afritech Sports can confirm it.

## 14. Analyst CV Desk (built 2026-11-16)
The same path as players and coaches, for football analysts. It lives in `analysts/` in this repo.

- **Front door:** `analysts/index.html`, at `https://afritech-advisory.github.io/afritech-sports-cv-desk/analysts/`. This is the one link to send analysts. The root page links to it from an "Analysts" section under the scouts.
- **Rulings applied (the coach rulings, with "analyst" for "coach"):** two forms, one the analyst fills in about themselves and one for anyone assessing an analyst; the assessment form is open to every football stakeholder in any country; both forms cover tactical and video analysis and physical performance (sports science) data; both cover men's and women's football and the analyst's own gender; English first; the first Analyst CVs are Afritech Sports' own analysts, who fill in the form themselves; never invent an analyst, a name or a detail; contact, wording and publishing rules are sections 4 and 5.
- **Roles covered (both forms):** first-team performance, opposition / pre-match, post-match and video, live (in-game), set-piece, tactical, academy / youth development, goalkeeping, recruitment / scouting, data scientist, data engineer / developer, physical performance / sports science data, medical and injury data, match data collection / tagging / annotation, referee and officiating, federation / league / competition, business / commercial / fan data, media / broadcast / journalism, lecturer / researcher, other.
- **Two forms, English only for now:**

| Who fills it in | Form | File |
|---|---|---|
| The analyst | Analyst CV & Career Profile Form v1.0 (15 sections) | `analysts/analyst-cv.html` |
| Anyone assessing an analyst: player, parent, school, academy, college, university, club, head coach or head of analysis, federation, league, data or technology company, media group or agency, in any country | Analyst Intelligence & Assessment Form v1.0 (15 sections plus 11A and 14A) | `analysts/analyst-assessment.html` |

- **Analyst CV form sections:** 1 About you; 2 Right to work and availability (on site, remote, match days, freelance; equipment); 3 Qualifications, education and safeguarding (including data protection training); 4 Analysis career (men's and women's football experience); 5 Tools and data (video software, event and tracking data, GPS and testing, cameras, coding); 6 Tactical, video and match analysis; 7 Physical performance and sports science data; 8 Recruitment and data science (including leagues with little or no data); 9 Other analysis work (academy, goalkeeping, refereeing, federation, business and media, tagging, research); 10 Working with people (including keeping players' data safe); 11 Results and impact; 12 Evidence and portfolio (work samples, with permission to show); 13 What you are looking for; 14 References; 15 Consent and declaration. An analyst completes the sections that fit their work.
- **Assessment form:** built on the structure of the Coach assessment form v5.1, with analyst content: work-sample evidence and an optional test task (section 5), video and tactical ratings (7), data, recruitment and technical ratings (8), physical performance data (9), communication and adaptability ratings (10), decisions for players and families, for organisations hiring, and for agencies placing (14).
- **Both forms** save a draft on the phone, have Review, Copy text, Save as PDF and Clear saved answers, and read with scripts off (with the same notice as the coach forms). Save as PDF names the file `Analyst CV - <name>.pdf` or `Analyst Assessment - <name>.pdf` from "Analyst full name" on the cover.
- **Published Analyst CV layout:** `analysts/sample-layout/index.html`, based on the player and coach profile. Tabs: Profile, How they work, Impact, Career, Work samples, Contact; views for clubs and federations, schools and academies, players and families. Every line is marked placeholder; not linked from any page; asks search engines not to list it. To publish an analyst, copy it to `analysts/<slug>/`, replace every placeholder with the analyst's own answers, remove the sample banner and the noindex line, and add the analyst's card to `analysts/index.html`.

Open flags for analysts:
1. What an assessor gets back after sending the assessment form is not yet stated beyond "Afritech Sports reviews it" (same as coaches).
2. French, Portuguese (BR) and Spanish (LATAM) versions wait until the questions are settled.
3. The dashboard skill builds player profiles only. Analyst CVs are built by hand from the sample layout.
4. Analyst share card, card and PDF CV are not designed yet.
5. Work samples often belong to a club. The form asks the analyst to share only what they have permission to share; Afritech checks this before anything is shown publicly.
