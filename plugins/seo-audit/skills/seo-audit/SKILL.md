---
name: seo-audit
description: Audit a website's search performance through 11 SEO lenses - indexing and crawl, technical (status codes, redirects, canonicals, hreflang, sitemap, robots, Core Web Vitals), migration and redesign risk, query clusters and cannibalization, content depth, internal links, CTR vs position and snippets, structured data, AI search visibility, backlinks, brand vs non-brand demand - using Search Console, GA4, PageSpeed and the live site read-only, and deliver a visual report for people plus a hands-off Markdown brief that an AI agent can implement. Use when someone asks for an SEO audit, why organic traffic dropped or does not grow, whether a redesign or migration hurt search, or what to fix first in SEO.
---

# SEO Audit

Look at a site through 11 SEO lenses and return a short, prioritized list of fixes in a visual report. Each lens is a different question; the value is in seeing what one lens misses (a "technical" redirect problem is often the reason for a "CTR" drop).

Respond in the user's language, and write the report in it too.

Files next to this SKILL.md (read each when its step comes, not up front):
- `references/data-sources.md` - which tools to look for, what to read in each, fallbacks, polluted-data signs, how to stay read-only (steps 0-1).
- `references/lenses.md` - the 11 lenses, their questions, icon and group ids, the search maturity stage (step 2).
- `references/report-spec.md` and `references/audit.schema.json` - the report's sections and the shape of its data (step 4).
- `references/handoff-spec.md` - the hands-off brief for AI agents: what goes in it and how to write targets and acceptance criteria (step 4).
- `assets/report-template.html` - the report page; it renders everything from one JSON block. `assets/example-audit.json` (Ukrainian) and `assets/example-audit.en.json` (English) are full examples for a fictional site.
- `scripts/validate_audit.py`, `scripts/build_report.py`, `scripts/build_handoff.py`, `scripts/check_report.py` - data check, page build, hands-off brief build, render check (steps 4-5).

Stay on search. Pricing, positioning, onboarding and the funnel after the landing page belong to a product audit (`product-lens-audit`); name it as a next step in one line if those come up.

## 0. Check which data sources are connected

Before gathering, look at the tools this session actually has (search the tool list / ToolSearch; never assume): a browser (for the GSC and GA4 web UIs and the site), GSC or GA4 connectors, Ahrefs, DataForSEO, SerpApi, Semrush, PageSpeed Insights / CrUX, a CMS connector **for this site**. Build a source list with a status for each: `ok`, `demo` (partial, sample, screenshot), `no` (not connected, error, no plan, blocked). `references/data-sources.md` lists what to read in each.

Use every source read-only: never press "Request indexing", submit sitemaps, change redirects or settings, or submit forms. If an important source is missing, say which one in one line and continue; never fill the gap with invented numbers.

## 0.5 Ask the requester (every question skippable)

First look for saved context: a previous `audit.json` or an `seo-context.md` in the project or attached. Read it and ask only about what it does not cover. With a previous `audit.json`, say in the report what changed since then (which fixes were done, how clicks, indexed pages and CTR moved).

Then ask one short round of up to 4 questions. Use a multiple-choice question tool when available (AskUserQuestion or similar) and give every question a "Skip" option; otherwise ask in plain text and say they can skip any. Never block: if the person skips, state the assumption you take and continue.

Pick the questions that change the analysis most:
- **What search should bring this quarter** (leads, sales, keep traffic through a redesign, grow non-brand)?
- **Which markets and languages matter**?
- **What changed recently** (redesign, new CMS, URL structure, domain, language versions) and when, and were redirects set?
- **What was already done** (agency work, sitemap resubmitted, disavow, content updates)?
- **Who will implement the fixes** (an AI coding agent with the site's code, an agent with a CMS connector only, people)? This shapes the hands-off brief.

An owner's claim ("all old URLs 301 to the new ones") is something to verify on a sample, not a fact; report what you found. Record each answer in `answers`; a skipped one shows the assumption taken. When the person shares data mid-run, revise the main leak and priorities instead of appending.

## 1. Gather the material (before judging anything)

In this order, as far as sources allow (details in `references/data-sources.md`):
1. **Search Console**, last 3 months, web: totals; queries and pages tables (max rows); Indexing > Pages with reasons; Sitemaps; Crawl stats (response codes, response time, host status); Core Web Vitals; Enhancements; URL Inspection for 3-5 key URLs.
2. **GA4**, same period: channels with engagement; organic landing pages; key events; AI Assistant channel; daily trend around any deploy.
3. **The site**: robots.txt, sitemaps, a sample of old -> new URLs, home and key pages (title, description, canonical, hreflang, robots meta, H1, JSON-LD, alt, analytics tag). Go slowly; stop at the first 429 or "are you a robot" page and never bypass it - record it and check in GSC whether Googlebot is affected.
4. **PageSpeed Insights / CrUX** for the home page and the biggest landing page, mobile: field data first, lab labelled as lab.
5. **Backlinks and SERP** only with Ahrefs / DataForSEO / SerpApi / GSC Links.

Then compute, and keep the numbers with their source and period: brand vs non-brand (write the regex), CTR by position band for non-brand, query clusters with their ranking URLs, old vs new URL share of impressions after a migration, indexed vs not indexed with reasons.

**Find the search maturity stage**: 0 Crawlable, 1 Indexed, 2 Ranking, 3 Clicked, 4 Converting (`references/lenses.md`). Name it from evidence and weight the lenses by it.

**After a migration or redesign**, check before anything else: one-to-one 301s for old URLs (not to the home page), hreflang and canonicals pointing to 200 URLs, sitemaps listing only new URLs, analytics still recording after the deploy. On day 1-3 after a deploy say that ranking effects cannot be measured yet and give a re-check date.

## 2. Apply the lenses

Read `references/lenses.md` and go through all 11 lenses in 4 groups: access for search (indexing and crawl, technical, migration), match the query (clusters and cannibalization, content, internal links), chosen in results (CTR and snippets, structured data, AI search visibility), authority and demand (backlinks, brand vs non-brand). For each write 1-3 findings tied to what you saw, and score it 0-100. Put what you checked into `checks` (the technical checklist), including the items you could not check (`nd`).

## 3. Prioritize

Collect all findings into one table:

| # | Fix | Lens | Evidence | Impact | Confidence | Effort | ICE | Type |

- Impact, Confidence, Ease each 1-10; ICE = product. Low confidence when based on guesses.
- Type = **Optimize** (fix or improve what exists) or **Explore** (new page type, new cluster, new language market, AI-answer content).
- Put the biggest leak first unless something clearly dominates; a blocking technical error (wrong redirect, noindex, broken hreflang) usually does.
- Label each finding **observed** (seen in data or on the site) or **hypothesis**.
- For the top 3, compare at least 2 alternative fixes, write the experiment with its risk type and a success threshold (for example, "CTR of the page at positions 6-10 from 0.07% to 1% in 28 days, position not worse"), and a pre-mortem.
- List **measurement gaps** (no key events, polluted Direct, no backlink source) as their own opportunity when they block decisions.
- Snippet changes get 2 title/description variants with a one-line reason each, using only facts the site states.

## 4. Output: a report for people and a hands-off brief for agents

Read `references/report-spec.md`. Write the audit as one `audit.json` following `references/audit.schema.json` (start from `assets/example-audit.json` or `.en.json`): language, the report's own text (headlines that state their point), KPIs, leaks vs target, stage, 11 lens scores, checks, search path, opportunities with a `detail` entry each, `plans` for the top 3, answers, sources and glossary. You write data only; the template draws every chart, table and label and computes ICE, the health index, quick wins and confidence.

- **With a shell:** `python scripts/build_report.py audit.json report.html`. It runs `validate_audit.py` first and refuses to build on errors (an opportunity without evidence, ICE outside 1-10, a number with no source or a source marked `no`, a top-3 fix without alternatives or pre-mortem). Fix the data, not the template.
- **Without a shell:** copy `assets/report-template.html`, set `<html lang>` and `<title>`, and replace the content of its `<script type="application/json" id="audit">` block with your JSON. Write `<\/` instead of `</` inside strings. Check the rules from `validate_audit.py` yourself.

**The hands-off brief.** Unless the requester asked for only one output, also build the brief for AI agents: read `references/handoff-spec.md`, add the optional fields to `audit.json` (`handoff` with context, constraints, decisions and measurement; per opportunity in `detail`: `owner`, `depends`, `targets`, `accept`, `human`, `rollback`), then run `python scripts/build_handoff.py audit.json audit.handoff.md` (add `--json audit.handoff.json` for task trackers). Without a shell, write the Markdown yourself in the order the spec gives. Targets and acceptance criteria must come from what you observed: real URLs, real current values, checks an agent can run.

Save `audit.json` next to the report: the next run compares against it. Deliver the report as one self-contained HTML page: publish it as an artifact when an artifact tool exists (private unless the person says otherwise), otherwise send the .html file. Send the hands-off brief as a .md file (it is meant to be pasted or attached to an agent, not viewed). In chat, reply with 3-5 summary bullets, the link or file, and one line on what was checked and what could not be.

## 5. Check before delivering

Never deliver a report you have not checked.

1. **Facts.** Every number in the text, KPIs, leaks, checks, `why`, `targets` and `accept` fields must trace to a source in `sources` or to the owner's answers, and the arithmetic must hold (CTR = clicks / impressions, shares, sums of rows vs rounded totals). In Claude Code, give this to a separate subagent that has not seen your reasoning: pass it `audit.json` and the raw material (exports, notes of what each GSC and GA4 screen showed) and ask it to list every number it cannot trace. Elsewhere, do the pass yourself, number by number. Fix or remove what does not trace.
2. **Script.** `node --check` on the template's main script if you edited anything beyond the JSON.
3. **Render**, when Python and a Chromium-based browser are available (`pip install playwright`, `playwright install chromium`): `python scripts/check_report.py report.html --out ./report-check`. It opens the page as desktop (1280px), tablet (820px, touch) and phone (390px, touch) and fails on page or console errors, sideways scroll, empty charts, leaks or checklist, overlapping or overflowing labels, tooltips that do not open on hover or tap or do not close on a second tap, broken phone table cells and filters. It saves screenshots, including dark mode.
4. **Look at the screenshots**: radar labels, matrix dots, the checklist values, dark-theme contrast.
5. **Fix and re-check**, at most twice. If something still fails, say what in one line.
6. **No headless browser:** open the published page with any browser tool at desktop and narrow width and check the same list by looking; otherwise say which visual checks were not done.

## Rules
- Every finding points to evidence or is clearly marked as a hypothesis.
- Never invent numbers, search volumes, rankings, backlinks, competitors' data or AI-answer appearances. Unknown = "no data" in the report and a `no` source.
- Rounded GSC totals ("80.5K") stay rounded; sums of the top-1,000 rows are labelled as such.
- Read-only: no indexing requests, sitemap submits, setting or redirect changes, form submits; never bypass bot protection or CAPTCHAs.
- Do not recommend manipulative tactics: doorway pages, hidden text, fake reviews or ratings in schema, bought links, auto-generated thin pages, fake "updated" dates.
- Fewer, sharper recommendations over long lists; mostly optimize, a few explore bets.
- Lens scores are judgments: base each on findings and keep the scale consistent (below 40 = big leak, 40-60 = partial, above 60 = solid).
