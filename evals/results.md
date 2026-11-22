# Results

Scores 1-5: **E** evidence (every finding traces to a source), **H** honesty about missing data, **P** plan specific to the site, **R** report renders on desktop, tablet and phone.

| Date | Version | Scenario | Site | E | H | P | R | Time | What broke |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-22 | 1.0.0 | post-migration (day 1), bot-protection, no-key-events; GSC + GA4 via browser, 2 of 4 questions skipped | private B2B logistics site, 3 languages | 4 | 5 | 4 | 5 | ~70 min | Found the Russian home page redirecting to the main-language home (hreflang points to a redirect; GSC: "Page with redirect"), while inner pages moved correctly. The host's bot protection returned 429 and a robot check after ~40 browser requests; crawling stopped there and the rest came from GSC (URL Inspection showed Googlebot fetching fine). The PageSpeed API quota was exhausted, so pagespeed.web.dev in the browser was used instead; no CrUX field data. The validator caught a checklist number without a source. The independent fact check found 6 issues (e.g. "213 non-brand queries in the top 10" was only positions 4-10, the real figure being 242; a 4xx share counted only "other 4xx"; a site element claimed but never seen); all fixed before delivery. Template: 0.96% rounded to "1%", now two decimals under 1%. |
| 2026-11-22 | 1.0.0 | english-report (demo, fictional data) | fictional store | - | - | - | 5 | ~15 min | Top-3 validation caught a fix that ranked into the top 3 without alternatives or a pre-mortem; scores adjusted. |
