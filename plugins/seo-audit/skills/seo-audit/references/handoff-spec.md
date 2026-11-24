# Hands-off brief specification

The second output of an audit: a plain Markdown file (`audit.handoff.md`, optionally `audit.handoff.json`) that the requester gives to an AI agent or a developer to implement the fixes. `scripts/build_handoff.py` renders it from the same `audit.json` as the HTML report, so the two never disagree. No design, no icons, no charts: structure, exact values, checkable criteria.

## What it contains, in order

1. **How to use** - fixed rules for the agent: follow task order and dependencies, stop at human decisions, a task is done only when all acceptance criteria pass, confirm hypotheses first.
2. **Context** (`handoff.context`, `handoff.period`) - hosts and which one is canonical, CMS and SEO plugin per host, URL patterns, languages, analytics setup, the audit date and data period. Only what the agent needs to find and change things.
3. **Constraints** (`handoff.constraints`) - what the agent must not do: no indexing requests on its own, no mass noindex or deletes without review, back up before bulk replace, no manipulative tactics, no changes to product/app paths it does not own, test on staging first when one exists.
4. **Decisions for a human** (`handoff.decisions` plus every task's `detail.human`) - questions with a default if nobody answers.
5. **Task list** - one table: id, task, owner, ICE, dependencies.
6. **Tasks**, sorted by ICE, ids `SEO-01`, `SEO-02`, ... Each has: lens, type, ICE, evidence type (`observed` / `hypothesis`), owner, dependencies; goal (the plan's hypothesis, if any); evidence (`detail.why`); **targets** (`detail.targets`: exact URL or item, current value, expected value); steps; copy variants; **acceptance criteria** (`detail.accept`); metric, threshold, cheapest test, effort, risk, rollback.
7. **Measurement** (`handoff.measurement`) - baselines and the re-check date.
8. **Open gaps** - every check with status `nd`.
9. **Sources** with status.

## Writing good fields

- **targets**: real URLs from the evidence (GSC rows, the crawl, the page source), not placeholders. When a target is a whole pattern, give the pattern and 2-3 examples (`/public/*/loyalty/*`, e.g. `/public/acme/loyalty/show.html`). Current values come from what you observed; expected values are concrete (status `301 -> /blog/product-sharing-101`, `canonical = https://www.example.com/blog/x`, `robots.txt: Disallow: /public/ applies to Googlebot`).
- **accept**: each line is something an agent can check without judgment, preferably with a command or a named tool: `curl -sI https://www.example.com/old.html` returns `301` and `location: https://www.example.com/new`; Google's robots.txt tester / `robots.txt` parsed per RFC 9309 shows `/public/x` disallowed for Googlebot; Rich Results Test shows 0 errors for 3 sample URLs; GSC URL Inspection "Test live URL" shows indexable. Include a "nothing else broke" check where a change is risky (home page still 200, key pages still indexable).
- **owner**: developer, content, analytics, marketing, seo, devops or security.
- **depends**: opportunity ids that must be finished first (for example, fix robots.txt before cleaning sitemaps).
- **human**: anything with business or legal impact, anything that removes content or a host, anything an agent cannot reverse. Say what the options are.
- **rollback**: how to undo (revert the robots.txt commit, remove the redirect rule, restore the backup).

Keep the language of `audit.json`. If the implementer prefers another language, write a second `audit.json` in that language rather than mixing.
