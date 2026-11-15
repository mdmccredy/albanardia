# The Sunday edition of The Silverbrooks Times

`media/times/index.html` is the paper, laid out like the print edition: sections A (News), B (Metro & Transit), C (Business & the Port), D (Sports), E (Arts) and F (On the Water). A new edition replaces it every Sunday. Old editions are kept as back issues in `media/times/editions/<date>/`. A weekly scheduled task does this; the daily stories task does not touch the paper's content.

## Steps for each Sunday run
1. Work in a fresh clone of `mdmccredy/albanardia` on `main`. Read `stories/AUTOMATION.md` (writing rules) and this file.
2. Run `python3 tools/times_edition.py archive`. It saves the current paper as a back issue. Never edit or delete back issues. If it prints STOP, today's edition is already out: change nothing and end the run.
3. Run `python3 tools/times_edition.py next`. It prints today's folio: volume, issue number and date.
4. Read the Times stories from the past week in `stories/stories.json` (site `times`), and skim the City, SBTransit, SBX, Port and club sites for what is coming up this week.
5. Rewrite `media/times/index.html` for today:
   - Keep everything outside the sections as is: the `<head>`, CSS, masthead, section nav, the `<!--alb-stories-->`, `<!--times-editions-->` and `<!--app-shell-->` blocks, the page-turn script, pager and footer.
   - Update the folio (volume, number, date from step 3; price `$6.00` on Sundays) and the ear box (`Sunday Edition` plus today's weather).
   - Replace the content of all six sections, keeping the same HTML structure and classes (`grid`/`lead`/`side`/`row` on A; `sechead` plus `g2` or `g3` and a `row` on B to F). Each section needs a lead story, a sidebar and briefs. A gets the week's biggest story, three sidebar items, a weather box and an SBTransit Today list. D gets a scoreboard, F gets a tide table and SBFerry status.
   - Only use images already in `media/times/img/`. Keep the advertisements (Kwáani, Larssen, Asia Pacific Airlines, Rutherford Public Library); their copy can change.
   - Remove all `<!--alb-pub-->...<!--/alb-pub-->` marks you copied over; the build puts them back.
6. Each section's lead story (six in all) is a new story. Append each to `stories/stories.json`: `site` "times", today's `date` and `added`, a `slug`, `cat`, `title` (exactly the headline on the page), `dek`, `body` (the same paragraphs as the page), `img` null, `link` `media/times/#<section id>` (front, metro, business, sports, arts, water). Sidebar items that repeat a story from this week should use that story's title exactly, so the page shows its real published date. New short briefs don't need a story.
7. Run `python3 tools/times_edition.py index`, then `python3 tools/build_stories.py`. Both must finish without errors.
8. Commit only `media/times/`, `stories/` and what the build rebuilt, as Max McCredy <mdmccredy@hotmail.com>, message `Times: Sunday edition (<date>)`, and push to `main` (on rejection: `git pull --rebase`, push again).

## How the paper should read
- A real Sunday paper: the week's biggest local story leads, follow-ups on what happened this week, and what is coming up this week. Results of events that happened (games, races, hearings, votes) should match the daily stories.
- Same rules as the daily stories: short sentences, no em dashes, no named private people, real companies, American street names, transit lines by letter only, dates and seasons that fit the day.
