# The 11 SEO lenses

Each lens is one question about how the site wins search traffic. For each, write 1-3 findings tied to something you actually saw: a Search Console row, a URL and its status code, a tag in the page source, a PageSpeed number. If a lens has no data at all, score it on what you could see, say so in one line, and lower the confidence of its findings.

Scores 0-100 say how much of the lens's potential the site already uses: below 40 = big leak or untapped potential, 40-60 = partial, above 60 = solid. Base every score on findings and keep the scale consistent. In `audit.json` each lens has an icon id `i` and a group `g`:

| Lens | `i` | `g` |
|---|---|---|
| Indexing and crawl | idx | access |
| Technical base | tech | access |
| Migration and redesign risk | mig | access |
| Query and page clusters, cannibalization | clus | match |
| Content depth and freshness | cont | match |
| Internal links | link | match |
| CTR vs position and snippets | ctr | serp |
| Structured data | schema | serp |
| AI search visibility | ai | serp |
| Backlinks and authority | auth | trust |
| Brand vs non-brand demand | brand | trust |

## Access for search (can Google reach and keep the pages?)

- **Indexing and crawl** - How many URLs are submitted, indexed and not indexed, and why (GSC Pages report reasons: crawled - not indexed, duplicate, noindex, 404, redirect)? Does the sitemap list only canonical 200 URLs? Crawl stats: response codes, average response time, host problems. Large "crawled - currently not indexed" = Google sees the pages but finds them not worth indexing: usually a content or duplication problem, not a technical one.
- **Technical base** - Status codes (200/301/302/404/410/5xx/429), redirect chains and loops, canonical tags (self-referencing, pointing to 200 pages), hreflang (reciprocal, pointing to 200 canonical URLs, x-default), robots.txt (no accidental blocks, sitemap line), meta robots, HTTPS and www/non-www consolidation, Core Web Vitals (field data from CrUX first; lab data from PageSpeed Insights only as a hint, labelled as lab). Bot protection or rate limits that could answer Googlebot with 429/403.
- **Migration and redesign risk** - Only when URLs, templates, CMS, domain or languages changed recently. Is every old URL 301-redirected one-to-one to its closest new equivalent (not to the home page)? Do hreflang, canonicals, sitemaps and internal links already use the new URLs? Are old URLs still in the sitemap? How much traffic did the old URLs carry (GSC pages, last 3 months), so you know what is at stake? Was analytics still recording after the deploy? Compare before and after by date when enough days have passed; on day 1-3 say it is too early and set a check date.

## Match the query (does the right page answer the right query?)

- **Query and page clusters, cannibalization** - Group queries by intent (service, route, product, informational, brand) and map each group to the page that ranks. Cannibalization = one query group split between two or more URLs of the same language, each ranking worse than one strong page would. Separate it from legitimate language versions. Note clusters with demand but no dedicated page.
- **Content depth and freshness** - Does the ranking page answer the query fully (prices or price factors, timing, steps, documents, FAQ) for its intent? Thin, outdated (old dates, past-year rules), or machine-translated pages; language versions that are much thinner than the main one. Pages with impressions but low positions (11-30) are content candidates.
- **Internal links** - Do the money pages get links from the menu, home page and related articles with descriptive anchors? Orphan pages (in the sitemap, no internal links), links that still point to old URLs (redirects inside the site), breadcrumbs.

## Chosen in the results (do people pick the snippet?)

- **CTR vs position and snippets** - CTR by position band (1-3, 4-10, 11-20, 21+), brand and non-brand separately. Queries and pages with many impressions at positions 1-10 and almost no clicks: check the title (length, query words, the offer), description, language of the snippet versus the query, and what else is on that results page (ads, maps, marketplaces, AI overview). Targets in this lens are suggested benchmarks, not industry standards; say so.
- **Structured data** - Organization, BreadcrumbList, Article, Service or Product, FAQ where honest, LocalBusiness for offices. Valid in GSC Enhancements; language of names matches the page language.
- **AI search visibility** - Can AI search crawlers reach the site (robots.txt and CDN rules for OAI-SearchBot, ChatGPT-User, PerplexityBot, Google-Extended, ClaudeBot and so on - training crawlers and search/answer crawlers are different decisions)? AI Assistant sessions in GA4, GSC's AI features report if present. Are the key facts (services, routes, contacts, prices) stated in plain text that an answer engine can quote? Never claim a ranking in an AI answer you did not see.

## Authority and demand (does the web trust the site, and do people look for it?)

- **Backlinks and authority** - Referring domains, their relevance and trend, lost links, links to pages that now redirect or 404. Only with a backlink source (GSC Links report, Ahrefs, DataForSEO); without one, mark the source `no` and keep findings as hypotheses.
- **Brand vs non-brand demand** - Share of clicks and impressions from brand queries (company name, misspellings, transliterations) versus non-brand. A site that lives on brand clicks is invisible for new customers; a sudden brand drop is a business signal, not an SEO one. Write the brand regex you used into the report's "how" section.

## Search maturity stage (header strip)

Name the stage from evidence: 0 **Crawlable** (pages reachable, but not reliably indexed) -> 1 **Indexed** (pages in the index, few rankings) -> 2 **Ranking** (positions for non-brand queries, few clicks) -> 3 **Clicked** (non-brand clicks arrive, conversions unknown or low) -> 4 **Converting** (organic traffic brings tracked leads or sales). Weight the lenses by it: at stages 0-1 access lenses dominate; at 2 content, clusters and links; at 3 CTR and conversion tracking; at 4 authority and AI visibility. Work on a later stage than the evidence supports (link building while key pages are not indexed) is itself a finding.

## Where SEO ends

This skill stays on search. Pricing, positioning, funnels after the landing page, sales and retention belong to a product audit (the `product-lens-audit` skill): mention it as the next step in one line instead of auditing them here. Conversion tracking from organic traffic is in scope, because without it the stage cannot pass "Clicked".
