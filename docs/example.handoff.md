# Hands-off brief: SEO audit: demo report

> For an AI agent (or a developer) implementing the fixes. Generated from audit.json by seo-audit; the human-readable report is built from the same file.

## How to use this brief

1. Work through the tasks in order unless a dependency says otherwise; each task has an id you can reference in commits and PRs.
2. Before acting on a task listed under "Decisions for a human", stop and ask.
3. A task is done only when every acceptance criterion passes. Report which ones you verified and how.
4. Evidence marked `hypothesis` must be confirmed first; if it is wrong, skip the task and say why.

## Context

- **Main host:** https://www.brightwell.example (new store platform, live 3 weeks)
- **Markets:** UK (en-GB) first, US (en-US) second
- **Old URLs:** 2,310 URLs from the pre-migration sitemap; redirect manager in the store admin
- **Analytics:** GA4 with purchase event
- **Data period:** Search Console and GA4: last 3 months (fictional)

## Constraints

- Do not request indexing or change Search Console settings; list those for a person.
- Import redirects in batches of at most 300 and recrawl after each batch.
- One hop per redirect, 301, target returns 200 and is not the home page.
- Back up the store's redirect table and theme before changes.

## Decisions for a human (before you start)

- **D1** For discontinued products with no close match: 410 or redirect to the category? Default if no answer: Redirect to the closest category.

## Task list

| ID | Task | Owner | ICE | Depends on |
|---|---|---|---|---|
| SEO-01 | Map the 464 home-page redirects to their closest new product or category | developer | 567 | - |
| SEO-02 | Rewrite titles of 20 categories at positions 4-10 | marketing | 378 | SEO-01 |
| SEO-03 | One page per intent for "raised garden beds" | content | 294 | - |
| SEO-04 | Make hreflang reciprocal between UK and US pages | developer | 288 | - |
| SEO-05 | Remove 310 redirecting URLs from the sitemap and collapse 2-hop chains | developer | 280 | - |
| SEO-06 | Restore offers.availability in Product markup |  | 252 | - |
| SEO-07 | Update 1,940 blog links to the new product URLs |  | 180 | - |
| SEO-08 | Watch brand demand after the redesign |  | 162 | - |
| SEO-09 | Canonicalize color variants to the main product |  | 150 | - |
| SEO-10 | Ask the 15 sites that linked to old guides to update links |  | 120 | - |
| SEO-11 | Planting-calendar hub that links to products by season |  | 84 | - |
| SEO-12 | Plain-text buying guides that answer engines can quote |  | 60 | - |

## Tasks

### SEO-01 · Map the 464 home-page redirects to their closest new product or category

- Lens: Migration · Type: optimize · ICE 567 = 9×9×7 · evidence: `observed` · Owner: developer

**Goal:** If each old URL redirects to its closest new page instead of the home page, the old pages' rankings and links move to the new pages, because Google treats redirects to the home page as soft 404s.

**Evidence:** A slow crawl of all 2,310 URLs from the old sitemap: 1,846 redirect one-to-one with 301, 464 redirect to the home page. Those 464 had 182,000 impressions in the 3 months before the migration. Search Console already reports 391 of them as "soft 404".

**Targets:**

| URL / item | Now | Expected |
|---|---|---|
| `464 old product URLs (list from the crawl)` | 301 -> / | 301 -> closest new product or category |

**Steps:**

1. Export the 464 URLs with their impressions from Search Console (Performance > Pages, before the migration date).
2. Match each to the closest new product; for discontinued products use the closest category, not the home page.
3. Add the rules to the platform's redirect manager as 301, one hop.
4. Recrawl the list and confirm every URL ends on a 200 page that is not the home page.
5. In 14 and 28 days, compare clicks to the new pages with the old pages' baseline.

**Acceptance criteria:**

- [ ] Every one of the 464 old URLs returns 301 to a URL that returns 200 and is not https://www.brightwell.example/.
- [ ] No redirect chain longer than one hop in the recrawl.
- [ ] Soft 404 count in Search Console starts falling within 2 weeks (checked by a person).

**Alternatives considered:**

- Return 410 for discontinued products - faster, but throws away their links; keep it for products with no close match and no links.
- Restore the old URLs - rejected: the new platform cannot serve the old paths.

**Pre-mortem:** It failed because the platform's redirect manager caps imports at 300 rules and the rest silently dropped. So import in batches and recrawl after each.

- **Metric:** Share of old URLs with a one-to-one 301 (now 1,846 of 2,310)
- **Success threshold:** 100% of the top 50 URLs and 95% of all 464 mapped within 2 weeks; soft 404 count falling
- **Cheapest test:** Fix the 50 old URLs with the most impressions first; compare 14 days before and after
- **Effort:** 2-3 days
- **Risk:** A wrong match (a product to an unrelated category) is still a soft 404: check the top 50 by hand.
- **Rollback:** Restore the redirect table from the backup.

### SEO-02 · Rewrite titles of 20 categories at positions 4-10

- Lens: CTR and snippets · Type: optimize · ICE 378 = 7×6×9 · evidence: `observed` · Owner: marketing · Depends on: SEO-01

**Goal:** If category titles name the product type and a concrete reason to click (range, delivery), CTR at positions 4-10 rises from 0.96% to 2%, because the current titles are only the category name.

**Evidence:** Non-brand queries at positions 4-10 had 412,000 impressions and 3,950 clicks (0.96%). The 20 categories with the most impressions there all use the bare category name as the title (for example "Planters").

**Targets:**

| URL / item | Now | Expected |
|---|---|---|
| `20 categories at positions 4-10` | title = category name | 10 changed titles, 10 unchanged control |

**Steps:**

1. List the 20 categories with the most impressions at positions 4-10.
2. Write titles up to 60 characters: product type + one fact the page supports (number of products, delivery option).
3. Change 10, leave 10 unchanged as a control.
4. Compare CTR and position after 28 days.

**Copy:**

- "Planters - 140 Indoor and Outdoor Styles | Brightwell" - the range number answers "is there enough choice?".
- "Garden Planters with Free UK Delivery over £40 | Brightwell" - leads with the delivery offer the page states.

**Acceptance criteria:**

- [ ] The 10 changed categories serve the new <title> (curl and grep).
- [ ] Titles are 60 characters or less and every number in them appears on the page.

**Alternatives considered:**

- Add review stars via Product markup - only where reviews are real and on the page.
- Push the categories to the top 3 with links - slower and costs more; test the snippet first.

**Pre-mortem:** It failed because Google rewrote the titles. So keep titles short, match the H1, and check the shown snippet after a week.

- **Metric:** CTR of the changed categories vs control
- **Success threshold:** CTR of changed titles ≥ 1.5x control at the same or better position
- **Cheapest test:** Change 10 titles, keep 10 as control, compare 28 days
- **Effort:** ≈1 day
- **Risk:** Do not promise prices or delivery terms the page does not show.
- **Rollback:** Restore the previous titles (kept in the PR description).

### SEO-03 · One page per intent for "raised garden beds"

- Lens: Clusters · Type: optimize · ICE 294 = 7×7×6 · evidence: `observed` · Owner: content

**Goal:** If the buying guide and the category stop competing for "raised garden beds", one of them climbs into the top 3, because Google now alternates between them.

**Evidence:** For 38 queries about raised garden beds, Search Console shows two URLs: the category (average position 7.4) and the buying guide (9.1), swapping places week by week.

**Targets:**

| URL / item | Now | Expected |
|---|---|---|
| `/raised-garden-beds (category)` | position 7.4, swaps with the guide | single page for commercial queries |
| `/guides/raised-garden-beds` | position 9.1 | refocused on how to build, links to the category |

**Steps:**

1. Keep commercial intent ("buy", "for sale", sizes) on the category; add a short buying section there.
2. Refocus the guide on how to build and fill a raised bed, and link to the category with a descriptive anchor.
3. Remove the overlapping product grid from the guide.
4. Watch the query group's pages tab weekly.

**Acceptance criteria:**

- [ ] The guide's title and H1 no longer contain "buy".
- [ ] The guide links to the category with a descriptive anchor.

**Alternatives considered:**

- Merge the guide into the category with a 301 - rejected: the guide has 15 external links and different intent.
- Noindex the guide - rejected: loses its informational queries.

**Pre-mortem:** It failed because the guide kept the word "buy" in its title. Check titles and H1s of both pages before publishing.

- **Metric:** Number of URLs ranking for the group (target 1) and the category's position
- **Success threshold:** One URL for ≥ 80% of the group's impressions within 28 days
- **Cheapest test:** Refocus the guide on "how to build" and link it to the category; watch 28 days
- **Effort:** 2 days
- **Risk:** The guide may lose informational traffic; watch its clicks separately.

### SEO-04 · Make hreflang reciprocal between UK and US pages

- Lens: Technical base · Type: optimize · ICE 288 = 6×8×6 · evidence: `observed` · Owner: developer

**Evidence:** US product pages declare en-GB alternates, but UK pages do not link back: hreflang is ignored without return links. Search Console shows UK pages ranking in the US for 120 queries.

**Steps:**

1. Generate hreflang en-GB, en-US and x-default on both versions from one template.
2. Validate 20 pairs by hand.
3. Watch US clicks to US pages.

**Acceptance criteria:**

- [ ] Every UK product page lists hreflang en-GB, en-US and x-default, and the US page lists the same set back.

- **Metric:** Share of US clicks landing on US pages
- **Effort:** 1-2 days
- **Risk:** A template error can break all alternates at once: release on one category first.

### SEO-05 · Remove 310 redirecting URLs from the sitemap and collapse 2-hop chains

- Lens: Migration · Type: optimize · ICE 280 = 5×8×7 · evidence: `observed` · Owner: developer

**Evidence:** The new sitemap lists 310 URLs that redirect, and 212 old category URLs go through two hops (http -> https -> new path).

**Steps:**

1. Build the sitemap only from 200, indexable, canonical URLs.
2. Point the http rules straight to the final path.
3. Recrawl the list.

**Acceptance criteria:**

- [ ] post sitemap and category sitemap contain no URL that returns 3xx (check every <loc> with curl).
- [ ] Every old category URL from the crawl reaches its final URL in one 301 hop.

- **Metric:** Redirecting URLs in the sitemap (target 0); 2-hop chains (target 0)
- **Effort:** ≈4 hours
- **Risk:** Low.

### SEO-06 · Restore offers.availability in Product markup

- Lens: Structured data · Type: optimize · ICE 252 = 6×6×7 · evidence: `observed`

**Evidence:** Search Console Enhancements: 820 Product items invalid since the migration, all missing offers.availability.

**Steps:**

1. Map stock status to schema.org InStock / OutOfStock in the product template.
2. Test 5 products in the Rich Results Test.
3. Validate the fix in Search Console.

- **Metric:** Invalid Product items (now 820)
- **Effort:** ≈4 hours
- **Risk:** Show only true stock status.

### SEO-07 · Update 1,940 blog links to the new product URLs

- Lens: Internal links · Type: optimize · ICE 180 = 5×6×6 · evidence: `observed`

**Evidence:** 1,940 internal links in blog posts still point to old product URLs, so every one is a redirect for crawlers and users.

**Steps:**

1. Export links to old URLs from the crawl.
2. Replace them in bulk using the redirect map.
3. Recrawl 20 posts.

- **Metric:** Internal links to redirecting URLs (target 0)
- **Effort:** ≈1 day
- **Risk:** Back up the blog before a bulk replace.

### SEO-08 · Watch brand demand after the redesign

- Lens: Brand · Type: optimize · ICE 162 = 3×6×9 · evidence: `hypothesis`

**Evidence:** Brand queries are 30% of clicks and stable; the new design changed the logo. A brand drop would be an early warning, not an SEO problem.

**Steps:**

1. Save a brand-query filter in Search Console.
2. Check it weekly for 2 months.

- **Metric:** Weekly brand clicks
- **Effort:** 30 minutes
- **Risk:** None.

### SEO-09 · Canonicalize color variants to the main product

- Lens: Indexing · Type: optimize · ICE 150 = 5×6×5 · evidence: `observed`

**Evidence:** 1,390 color-variant URLs are "Duplicate without user-selected canonical" and use crawl budget.

**Steps:**

1. Canonicalize variants to the main product.
2. Keep variants out of the sitemap.
3. Watch the duplicate count.

- **Metric:** Duplicate pages in the index report
- **Effort:** 1 day
- **Risk:** If a color has its own search demand, keep that variant indexable.

### SEO-10 · Ask the 15 sites that linked to old guides to update links

- Lens: Authority · Type: optimize · ICE 120 = 4×5×6 · evidence: `hypothesis`

**Evidence:** GSC Links shows 15 sites linking to old guide URLs that now redirect. Direct links are stronger than redirected ones (hypothesis).

**Steps:**

1. List the 15 sites and linked URLs.
2. Email the editors with the new URL.
3. Track updated links.

- **Metric:** Links updated
- **Effort:** ≈4 hours
- **Risk:** No link buying or exchanges.

### SEO-11 · Planting-calendar hub that links to products by season

- Lens: Content · Type: explore · ICE 84 = 7×4×3 · evidence: `hypothesis`

**Evidence:** Seasonal queries ("what to plant in March") bring guide traffic in spring, but no page ties seasons to products. Demand by month is a guess without a keyword tool.

**Steps:**

1. Pull seasonal queries from 12 months of Search Console.
2. Build one hub page with 12 month sections linking to categories.
3. Measure clicks next spring.

- **Metric:** Clicks to the hub and assisted purchases
- **Effort:** 1-2 weeks
- **Risk:** A thin calendar copied from elsewhere does not rank; write from the store's own range.

### SEO-12 · Plain-text buying guides that answer engines can quote

- Lens: AI search · Type: explore · ICE 60 = 4×3×5 · evidence: `hypothesis`

**Evidence:** GA4 shows 210 sessions from AI assistants in 3 months. Buying guides are long and image-heavy; key facts (sizes, materials) sit in images.

**Steps:**

1. Add a plain-text facts block to the top 10 guides.
2. Check 10 test questions monthly in ChatGPT Search and Perplexity.
3. Watch the AI Assistant channel.

- **Metric:** AI Assistant sessions per month
- **Effort:** 2 days
- **Risk:** Write for people first.

## Measurement

- Baseline: 1,846 of 2,310 old URLs with a one-to-one 301; non-brand CTR at positions 4-10 0.96%.
- Re-check 14 and 28 days after the redirect fix.

## Open gaps (not checked)

- Results page for top queries: No SerpApi or DataForSEO connected.

## Sources

| Sources | Status | Note |
|---|---|---|
| Search Console | ok | connected |
| GA4 | ok | connected |
| Crawl of old sitemap | ok | 2,310 URLs |
| CrUX | ok | origin data |
| Owner's answers (3 of 4) | ok | done |
| GSC Links (backlinks) | demo | partial |
| SerpApi / DataForSEO | no | not connected |
