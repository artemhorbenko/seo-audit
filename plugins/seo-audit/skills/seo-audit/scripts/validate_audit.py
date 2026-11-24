#!/usr/bin/env python3
"""Check an seo-audit audit.json before it becomes a report.

Usage: python validate_audit.py audit.json

Errors (exit 1) break the report or the skill's rules; warnings (exit 0)
are worth a look. Standard library only.
"""
import json
import re
import sys

ICONS = {"idx", "tech", "mig", "clus", "cont", "link", "ctr", "schema", "ai", "auth", "brand"}
GROUPS = {"access", "match", "serp", "trust"}
CHECK_ST = {"ok", "warn", "bad", "nd"}
N_LENSES = len(ICONS)
LANGS = {"uk", "en"}
STATUSES = {"ok", "demo", "no"}
TOKENS = re.compile(r"\{(health|qw|n|conf)\}")
TEXT_KEYS = ["headline", "lead", "lensesH", "journeyH", "matrixH", "opsH", "nextH", "planH", "dataH"]


def validate(a):
    err, warn = [], []
    E, W = err.append, warn.append

    if not isinstance(a, dict):
        return ["the file is not a JSON object"], []

    sources = a.get("sources") or []
    names = {s.get("name") for s in sources}

    def src_check(p, src):
        """A literal number must name a source that is in sources and not marked 'no'."""
        if not src:
            E(f"{p} has a number but no src: name the source it came from")
        elif src not in names:
            E(f"{p}.src '{src}' is not in sources")
        elif next((s for s in sources if s.get("name") == src), {}).get("status") == "no":
            E(f"{p} cites '{src}', which is marked as not available")

    lang = a.get("lang")
    if lang not in LANGS:
        W(f"lang '{lang}' has no interface dictionary; labels fall back to English (add an entry to UI in the template)")

    text = a.get("text") or {}
    for k in TEXT_KEYS:
        if not str(text.get(k, "")).strip():
            E(f"text.{k} is missing: every section needs a heading that states its point")
    if "<" in json.dumps(text, ensure_ascii=False):
        W("text contains '<': HTML is shown as plain text; use [[...]] to highlight words in the headline")

    # lenses
    lenses = a.get("lenses") or []
    if len(lenses) != N_LENSES:
        W(f"{len(lenses)} lenses instead of {N_LENSES}")
    if len({l.get("i") for l in lenses}) != len(lenses):
        E("two lenses share one icon id i: each SEO lens appears once")
    for i, l in enumerate(lenses):
        p = f"lenses[{i}]"
        if l.get("i") not in ICONS:
            E(f"{p}.i '{l.get('i')}' is not an icon id ({', '.join(sorted(ICONS))})")
        if l.get("g") not in GROUPS:
            E(f"{p}.g '{l.get('g')}' is not a group ({', '.join(sorted(GROUPS))})")
        s = l.get("s")
        if not isinstance(s, (int, float)) or not 0 <= s <= 100:
            E(f"{p}.s must be a number 0-100")
        if not l.get("k"):
            E(f"{p}.k (short name) is missing")

    # header picture
    funnel, leaks = a.get("funnel"), a.get("leaks")
    if funnel and leaks:
        E("use either funnel or leaks, not both")
    if funnel:
        if len(funnel) < 2:
            E("funnel needs a base step and at least one more")
        hot = 0
        for i, f in enumerate(funnel):
            n = f.get("n")
            if n is not None and (not isinstance(n, (int, float)) or n < 0):
                E(f"funnel[{i}].n must be a number or null (no data)")
            hot += bool(f.get("hot"))
        if hot > 1:
            W("more than one funnel step is marked as the constraint (hot)")
        if all(f.get("n") is None for f in funnel) and not any(s.get("status") == "no" for s in a.get("sources", [])):
            W("funnel has no numbers but no source is marked 'no': say which data is missing")
    if leaks:
        for i, f in enumerate(leaks):
            for k in ("l", "t"):
                if f.get(k) in (None, ""):
                    E(f"leaks[{i}].{k} is missing")
            if f.get("v") is not None and not f.get("b"):
                E(f"leaks[{i}] has v but no base b")
            if f.get("v") is not None:
                src_check(f"leaks[{i}]", f.get("src"))
    if not funnel and not leaks:
        W("no funnel or leaks: the header has no picture")

    st = a.get("stage")
    if st is not None and (not isinstance(st.get("cur"), int) or not 0 <= st["cur"] <= 4):
        E("stage.cur must be 0-4 (Crawlable, Indexed, Ranking, Clicked, Converting)")

    for i, r in enumerate(a.get("route") or []):
        if r.get("st") not in ("ok", "warn", "bad"):
            E(f"route[{i}].st must be ok, warn or bad")

    # opportunities
    ops = a.get("ops") or []
    if not ops:
        E("ops is empty")
    seen_pts = {}
    for i, o in enumerate(ops):
        p, oid = f"ops[{i}] (#{i + 1})", i + 1
        for k in ("I", "C", "E"):
            v = o.get(k)
            if not isinstance(v, int) or not 1 <= v <= 10:
                E(f"{p}.{k} must be a whole number 1-10")
        if o.get("x") not in ("opt", "ex"):
            E(f"{p}.x must be opt or ex")
        if o.get("ev") not in ("obs", "hyp"):
            E(f"{p}.ev must be obs (observed) or hyp (hypothesis)")
        if o.get("l") not in ICONS:
            E(f"{p}.l '{o.get('l')}' is not an icon id")
        if not o.get("t") or not o.get("ln"):
            E(f"{p} needs t (title) and ln (lens label)")
        if isinstance(o.get("I"), int) and isinstance(o.get("E"), int):
            seen_pts.setdefault((o["E"], o["I"]), []).append(oid)
        d = (a.get("detail") or {}).get(str(oid))
        if not d:
            E(f"{p} has no detail[\"{oid}\"]: every opportunity needs its evidence and steps")
            continue
        if not str(d.get("why", "")).strip():
            E(f"detail[\"{oid}\"].why is empty: every finding must point to evidence")
        if len(d.get("steps") or []) < 2:
            E(f"detail[\"{oid}\"].steps needs at least 2 concrete steps")
        for k in ("metric", "effort", "risk"):
            if not str(d.get(k, "")).strip():
                E(f"detail[\"{oid}\"].{k} is missing")
        if o.get("ev") == "hyp" and isinstance(o.get("C"), int) and o["C"] > 7:
            W(f"{p} is a hypothesis with confidence {o['C']}: confidence above 7 needs evidence")
    for pt, ids in seen_pts.items():
        if len(ids) > 2:
            W(f"opportunities {ids} share one matrix point (effort {11 - pt[0]}, impact {pt[1]}); the dots are spread, but check the scores")
    for k in (a.get("detail") or {}):
        if not k.isdigit() or not 1 <= int(k) <= len(ops):
            E(f"detail[\"{k}\"] does not match any opportunity")

    ranked = sorted(range(1, len(ops) + 1), key=lambda j: (-(ops[j - 1].get("I", 0) * ops[j - 1].get("C", 0) * ops[j - 1].get("E", 0)), j))
    for oid in ranked[:3]:
        pl = (a.get("plans") or {}).get(str(oid))
        if not pl or not all(str(pl.get(k, "")).strip() for k in ("h", "m", "t")):
            E(f"top-3 opportunity #{oid} needs plans[\"{oid}\"] with h (hypothesis), m (metric), t (cheapest test)")
        d = (a.get("detail") or {}).get(str(oid)) or {}
        for k in ("alt", "rtype", "thr", "pm"):
            if not d.get(k):
                E(f"top-3 opportunity #{oid} needs detail.{k} (alternatives, risk type, threshold, pre-mortem)")

    # hands-off fields (optional; used by build_handoff.py, ignored by the report)
    OWNERS = {"developer", "content", "analytics", "marketing", "seo", "devops", "security"}
    for k, d in (a.get("detail") or {}).items():
        p = f"detail[\"{k}\"]"
        for dep in d.get("depends", []):
            if not isinstance(dep, int) or not 1 <= dep <= len(ops) or str(dep) == k:
                E(f"{p}.depends has {dep!r}: use other opportunity ids (1-{len(ops)})")
        if d.get("owner") and d["owner"] not in OWNERS:
            E(f"{p}.owner must be one of {sorted(OWNERS)}")
        if "accept" in d and (not isinstance(d["accept"], list) or not all(str(x).strip() for x in d["accept"])):
            E(f"{p}.accept must be a list of checkable criteria")
        for j, g in enumerate(d.get("targets", [])):
            if not g.get("url") or not (g.get("now") or g.get("want")):
                E(f"{p}.targets[{j}] needs url and now and/or want")
    if a.get("handoff"):
        for oid in ranked[:5]:
            if not ((a.get("detail") or {}).get(str(oid)) or {}).get("accept"):
                W(f"opportunity #{oid} (top 5) has no accept list: the hands-off brief will have no acceptance criteria for it")
        if not (a["handoff"].get("context")):
            W("handoff.context is empty: agents get no site context")

    # technical checklist
    for i, c in enumerate(a.get("checks") or []):
        p = f"checks[{i}]"
        if not c.get("t"):
            E(f"{p}.t (what was checked) is missing")
        if c.get("st") not in CHECK_ST:
            E(f"{p}.st must be ok, warn, bad or nd (no data)")
        elif c["st"] == "nd":
            if re.search(r"\d", str(c.get("v", ""))):
                E(f"{p} is nd (no data) but has a value: leave v empty")
        elif re.search(r"\d", str(c.get("v", ""))):
            src_check(p, c.get("src"))
    if not a.get("checks"):
        W("no checks: the technical checklist section will be hidden")

    # sources and numbers
    if not sources:
        E("sources is empty: list what was used and what was missing")
    for i, s in enumerate(sources):
        if s.get("status") not in STATUSES:
            E(f"sources[{i}].status must be ok, demo or no")
    for i, k in enumerate(a.get("kpis") or []):
        v = str(k.get("v", ""))
        if not TOKENS.search(v) and re.search(r"\d", v):
            src_check(f"kpis[{i}] '{k.get('v')}'", k.get("src"))

    for i, q in enumerate(a.get("answers") or []):
        if not q.get("q") or not q.get("a"):
            E(f"answers[{i}] needs q and a (for a skipped question, a = the assumption taken)")

    gl = a.get("glossary") or {}
    for k, v in gl.items():
        if not v.get("g") or not v.get("d"):
            E(f"glossary['{k}'] needs g (short gloss) and d (definition)")
    if not gl:
        W("glossary is empty: terms will have no tooltips")
    return err, warn


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    with open(sys.argv[1], encoding="utf-8") as f:
        try:
            a = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[ERROR] not valid JSON: {e}")
            return 1
    err, warn = validate(a)
    for e in err:
        print("[ERROR]", e)
    for w in warn:
        print("[WARN] ", w)
    print("OK" if not err else f"{len(err)} error(s)")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
