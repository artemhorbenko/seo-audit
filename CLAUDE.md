# seo-audit — notes for Claude and contributors

Start every session by reading this file and STATUS.md, then continue from Next. End every session by updating STATUS.md and committing.

A public Claude skill (Claude Code plugin + Claude app skill ZIP) that audits a website's search performance through 11 SEO lenses and outputs two files from one `audit.json`: a visual HTML report for people and a Markdown hands-off brief for AI agents (plus an optional JSON variant). Strategy and product questions belong to the sibling skill `product-lens-audit`.

## Layout

```
.claude-plugin/marketplace.json        this repo is a plugin marketplace
plugins/seo-audit/                     the only folder that ships to users
  .claude-plugin/plugin.json
  skills/seo-audit/
    SKILL.md                           the process Claude follows
    references/                        lenses, data sources, report spec, handoff spec, audit.schema.json
    assets/                            report-template.html, example audits (uk, en)
    scripts/                           validate_audit, build_report, build_handoff, check_report
evals/                                 scenarios, trigger prompts, results log (anonymised)
docs/                                  README screenshots, example hands-off brief
seo-audit-skill.zip                    Claude app upload, rebuilt on every skill change
CLAUDE.md, STATUS.md, CHANGELOG.md,    repo docs; never move them into plugins/
ROADMAP.md
```

## Rules

- Respond to the maintainer in Ukrainian; code, docs and commits in English.
- Never invent numbers. Missing data shows as "no data", the source is marked `no`, and confidence drops. Every number in KPIs, leaks and checks names its source.
- Audit only the production domain the user names; ignore other subdomains and hosts found via Search Console or search unless the user confirms they are live.
- Real audits stay private (private artifacts or local files). Nothing in this repo may name a real audited site, client data or private links; log runs in `evals/results.md` anonymised.
- Public demos use fictional products only.
- Claude writes only `audit.json`; the template and scripts render everything. When layout breaks, change the template, not the data.
- Keep `SKILL.md` short; details go to `references/`.
- Use data sources read-only: no "Request indexing", no sitemap submits or removals, no setting or redirect changes, never submit real forms, payments or messages, never bypass bot protection or CAPTCHAs.
- Every real report gets an independent fact check of its numbers before delivery.

## Build and check

```
S=plugins/seo-audit/skills/seo-audit
python $S/scripts/validate_audit.py audit.json
python $S/scripts/build_report.py audit.json report.html
python $S/scripts/build_handoff.py audit.json audit.handoff.md --json audit.handoff.json
python $S/scripts/check_report.py report.html --out ./report-check   # needs playwright + Chromium
```

Before committing a template or script change, run all four on both `assets/example-audit.json` and `assets/example-audit.en.json`, check that a deliberately broken input fails, and regenerate `docs/example.handoff.md` from the English example. For screenshots in the real typeface without access to Google Fonts, install Sofia Sans and Sofia Sans Condensed locally.

## Release

1. Bump the version in `.claude-plugin/marketplace.json` and `plugins/seo-audit/.claude-plugin/plugin.json`.
2. Add a section to `CHANGELOG.md` (user-facing changes only).
3. Rebuild the ZIP: `cd plugins/seo-audit/skills && rm -f ../../../seo-audit-skill.zip && zip -qr ../../../seo-audit-skill.zip seo-audit -x '*/__pycache__/*'`
4. `claude plugin validate .`
5. Commit, push; tags and GitHub releases are created by the maintainer.

## Related repos

Same report core and design: `product-lens-audit` (where shared core changes are made first, then copied), `qa-audit`, `ui-review`, `ux-review`, `competitor-teardown` (all under github.com/artemhorbenko).
