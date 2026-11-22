# Changelog

## 1.0.0 - 2026-11-22

First public release. Built on the approach and report template of [product-lens-audit](https://github.com/artemhorbenko/product-lens-audit) 1.2.1.

- 11 SEO lenses in 4 groups: indexing and crawl, technical base, migration risk; clusters and cannibalization, content, internal links; CTR and snippets, structured data, AI search visibility; backlinks, brand vs non-brand. Search maturity stage (crawlable, indexed, ranking, clicked, converting).
- Data-source check (ok / demo / no) and up to 4 skippable start questions; owner claims are verified on a sample.
- Read-only rules: no indexing requests, sitemap submits or setting changes; stop at 429 or bot checks instead of bypassing them.
- Report template: leaks vs target as the header picture, new technical checklist section with ok / warn / bad / no-data marks, SEO lens icons, search path, matrix, ranked table, full plan, data and confidence. Same annual-report design, light and dark themes, tooltips, stacked phone tables, uk/en labels.
- Rates under 1% show two decimals (0.96% instead of 1%).
- `validate_audit.py`: every number in KPIs, leaks and checks must name a source that is not marked `no`; checks with no data carry no value; 11 unique lenses.
- `check_report.py`: fails on an empty technical checklist; screenshots the checklist.
- Examples: fictional store "Brightwell" in Ukrainian and English.
- Tested on a real site the day after a redesign (see `evals/results.md`).
