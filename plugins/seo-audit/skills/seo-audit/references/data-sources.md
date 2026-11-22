# Data sources

Check what this session can actually reach before gathering: search the tool list (ToolSearch or similar) for each source below. Never assume a connector exists, and never fill a gap with invented numbers. Use every source **read-only**: no "Request indexing", no sitemap submits, no redirect or setting changes, no form submits. Suggest those as steps in the plan instead.

## Status

| Status | When |
|---|---|
| `ok` | Connected and used, or the owner's own answer or screenshot with a visible date range. |
| `demo` | A sample, a partial export, a cut-off screenshot, a free tier with partial data, or a sample of pages instead of a full crawl. |
| `no` | Not connected; returns an error, "no plan" or "no access"; blocked by bot protection; a plugin that is installed but inactive. Try a failing call once more; if it fails again, mark `no` and move on. |

Confidence in the report is the average of ok = 1, demo = 0.6, no = 0, so list only sources that matter for this site.

## Google Search Console (the main source)
- **Tools:** a GSC MCP server, Ahrefs' GSC tools, or the GSC web UI through a browser (Claude in Chrome with the owner's sign-in). Screenshots with the date range visible as a fallback.
- **Performance, last 3 months, web search:** totals; queries and pages with clicks, impressions, CTR, position (set rows per page to the maximum and read the table; it shows up to 1,000 rows, so say that sums of rows are "top 1,000 queries", not the total); countries; devices; search appearance.
- **Derive:** brand vs non-brand split (write the regex); CTR by position band for non-brand queries; query groups by intent with their ranking URLs (cannibalization); pages with many impressions and few clicks; pages on old URLs vs new URLs after a migration.
- **Indexing > Pages:** indexed vs not indexed and every reason with its count; note the report's last update date.
- **Sitemaps:** submitted sitemaps, last read, status, discovered URLs; stale sitemaps from old setups.
- **URL Inspection:** for 3-5 key URLs (home page of each language, the biggest-leak page, a migrated URL): indexed or not, last crawl, user vs Google-selected canonical, referring sitemap. Read the existing result; "Test live URL" is fine; never press "Request indexing".
- **Settings > Crawl stats:** total requests, average response time, responses by code (look for 429, 5xx, 404 shares), host status.
- **Core Web Vitals, Enhancements, Links, Manual actions, Security issues.**
- **Feeds:** every lens; it is the source of the header picture.

## GA4
- **Tools:** Google's official GA4 MCP, a community one, or the GA4 UI through a browser.
- **Queries, same 3 months:** sessions by default channel group with engagement rate; Organic Search landing pages; key events (are any configured? which fire from organic sessions?); AI Assistant channel; daily trend around a deploy date (did tracking stop?).
- **Polluted data:** Direct above ~40% with a low engagement rate; sudden country spikes (data centers: Singapore, Ashburn, Boardman); 0-second sessions. Report it; do not "correct" the numbers.
- **Feeds:** stage (Clicked vs Converting), AI visibility, brand demand, migration.

## The site itself (browser)
- **Tools:** Claude in Chrome, the built-in browser, a cloud browser, or WebFetch for public pages. A shell is often blocked from the site; use the browser.
- **Check:** robots.txt (groups, AI bots, Sitemap line); sitemap index and child sitemaps (counts per language, any URLs with parameters or redirects); a sample of old URLs -> where they land (`fetch()` from a page on the same origin shows the final URL; `performance.getEntriesByType('navigation')[0].redirectCount` shows a redirect happened; GSC crawl stats show 301 vs 302 shares); home and key pages: title and length, description, canonical, hreflang set (reciprocal, x-default), meta robots, H1, JSON-LD types and their language, images without alt, analytics tag present.
- **Be gentle:** pause between requests and stop at the first 429 or "are you a robot" page. Never solve a CAPTCHA or bypass bot protection. Record the block as a finding (does it also hit Googlebot? check crawl stats and URL Inspection) and continue with GSC.
- **Feeds:** technical, migration, structured data, internal links, AI visibility.

## PageSpeed Insights / CrUX
- **Tools:** the PageSpeed Insights API (it has a shared daily quota and often returns 429; then use pagespeed.web.dev in the browser), the CrUX API, or GSC Core Web Vitals.
- **Read:** field data (CrUX) first: LCP, INP, CLS at the 75th percentile for the URL and the origin. If there is none, say "no field data" and give lab numbers (performance score, LCP, CLS, TBT) as lab, mobile.
- **Feeds:** technical.

## Ahrefs / DataForSEO / SerpApi / Semrush (optional)
- **Ahrefs:** Domain Rating works for any domain without a plan; most other tools need a plan and fail on other domains: mark them `no` when they do. With a plan: referring domains and trend, organic keywords, top pages, organic competitors, broken backlinks.
- **DataForSEO / SerpApi:** what the results page looks like for the top non-brand queries (ads, local pack, marketplaces, AI overview) to explain low CTR; search volume for clusters.
- **Without them:** backlinks from GSC Links (top linking sites and linked pages) as `demo`; SERP look from a manual search is not reliable (personalized, location); say so.
- **Feeds:** authority, CTR, clusters.

## CMS connector
- **Tools:** a WordPress (or other CMS) connector **for this site**. A connector for another site does not count.
- **Read:** SEO plugin and its settings (titles, sitemaps, schema), redirect plugin rules, posts and pages per language, last modified dates, noindex flags, broken internal links.
- **Feeds:** content freshness, internal links, migration, structured data.

## The owner
- Up to 4 start questions (see SKILL.md). One sentence like "we set 301s for everything" is a claim to verify, not a fact: check a sample and say what you found.

## Recording numbers

For every number you use, keep the metric definition, the period, the source and known gaps (rounded GSC totals like "80.5K", top-1,000 row limit, anonymized queries, index report lag of a few days). A number in a KPI, a leak or a check must name its source (`src` in `audit.json`), and that source must not be marked `no`.
