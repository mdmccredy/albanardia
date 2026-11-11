# Automatic stories: how each run works

A scheduled task runs once a day. Each run writes new stories for every Albanardia website that is due, then publishes them. Max can change how often each site gets stories in `stories/cadence.json`.

## Steps for each run
1. Work in a fresh clone of `mdmccredy/albanardia` on `main`. Read `Worldbuilding-Project-Instructions.md` (the Stories section and the naming rules).
2. Run `python3 tools/stories_due.py`. It lists every site that is due today, how many stories to write, and its latest titles. If nothing is due, stop.
3. For each due site, read that site's last 8 to 10 stories in `stories/stories.json`, and skim the site itself, so new stories continue what is already happening there (follow-ups, results of events that were announced, the next thing on the calendar). Never repeat a story.
4. Append the new stories to `stories/stories.json` (never edit or delete existing stories). Fields:
   - `site`, `slug` (unique for that site, lowercase-with-dashes), `date` (today, YYYY-MM-DD, Pacific time), `cat`, `title`, `dek` (one or two sentences), `body` (2 to 4 short paragraphs), `img` (null unless you reuse an image already on that site), `link` (null), `added` (today's date).
   - Library (`sbpl`) and Schools (`sbps`): also set `link` to `sbpl/#a/<slug>` or `sbps/#a/<slug>` and add `native` in that site's article format (copy the shape of an existing article in its `const DATA` arts list: slug, date like "Nov 12", kind, title, lede, img (reuse an Unsplash id already used on that site), body, and meta for Schools).
   - Larssen Sailing (`larssen`): set `link` to `larssensailing/#/news/<slug>` and add `native` as `[category, title, dek, image, slug, [paragraphs], [product names that exist in the shop], "Month D, YYYY"]`. Only mention boats and products that exist on the site. Never mention sail colors.
5. Run `python3 tools/build_stories.py`. It must finish without errors. Open `stories/data.js` count or the build summary to confirm the new total.
6. Commit as Max McCredy <mdmccredy@hotmail.com> with a message like `Stories: N new for <sites> (<date>)` and the session's attribution trailer, then push to `main`. If the push is rejected, `git pull --rebase` and push again.
7. End with a short summary: which sites got stories, and their titles.

## How the stories should read
- Plain, specific news writing, like a real local paper or club newsletter. Short sentences. No em dashes.
- Match each site's voice: the Times is a daily newspaper; University News covers all UA campuses and the colleges; City of Silverbrooks and Albanardia.gov are government notices; the Library, Schools and Visit Silverbrooks write for residents and visitors; clubs write club newsletters (racing, juniors, social, haul-out, annual meeting); colleges write campus news (athletics, academics, admissions, events); Larssen Sailing writes product and class news (new boats and parts, class rule changes, regatta results in Larssen boats), like West Coast Sailing's news.
- Keep the world consistent. Use the canon in the World Bible docs and on the sites: Silverbrooks in Albanardia (AB), SBTransit (SBMetro buses, SBTrain lettered lines, no nicknames), ALBExpress under NETA, SBX airport, the Voyageurs, UA campuses and mascots, Larssen boats. American street names only (St, Ave, Blvd, Road, Way). Real companies by default.
- Dates and seasons should make sense for today's date (frostbite racing in winter, camps in summer, holidays when they happen).
- Don't invent named private people as the subject of stories. Titles like "the commodore" or "the head coach" are fine.
