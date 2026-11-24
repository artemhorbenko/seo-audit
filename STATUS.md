# Status

Living state of the work. Update at the end of every session. Public repo: no real site names, client data or private links here.

**Version:** 1.1.0 (2026-11-24)

## Done recently

- 1.1.0: hands-off brief for AI agents (`build_handoff.py` → `audit.handoff.md` + optional JSON): context, constraints, human decisions, ICE-sorted tasks with exact targets, acceptance criteria, dependencies, rollback; alternatives and pre-mortem for the top 3.
- 1.0.0: 11 SEO lenses, search maturity stage, report template adapted from product-lens-audit (leaks vs target, technical checklist), validator that requires a source for every number, render check, fictional demo (uk + en).
- Test runs: B2B logistics site the day after a redesign; B2B SaaS with several subdomains (first hands-off run). Both found by the independent fact check to need fixes before delivery. See `evals/results.md`.
- Repo docs: CLAUDE.md and STATUS.md added.

## In progress

- Nothing open in this repo.

## Next

1. Maintainer: create git tags v1.0.0 and v1.1.0 and a GitHub Release (the session cannot push tags).
2. Apply the production-domain rule in SKILL.md and `references/data-sources.md`: ask which host is production, keep other hosts out of findings unless confirmed live.
3. Test in Claude Code desktop and in the Claude app (upload the ZIP); run trigger evals from `evals/trigger-evals.json` with the skill-creator skill.
4. Add a check script for agents that runs the brief's `curl` acceptance criteria and marks them passed or failed (see ROADMAP.md).
5. Test on an e-commerce site and a site with several languages and markets.
6. Rerun the two test audits about 4 weeks after fixes, comparing against their saved `audit.json`.

## Open questions

- Which real site becomes the public case study (owner consent needed)?
- Move the shared report core into its own repo once 2–3 sibling skills exist?
- Should the validator fail (not warn) when a top-5 task has no acceptance criteria?

## Links

- Public demo (fictional store): EN https://claude.ai/artifact/WY6Vo8mEAYck5h31ha9LYh
- Example hands-off brief: `docs/example.handoff.md`
- Roadmap: `ROADMAP.md`
