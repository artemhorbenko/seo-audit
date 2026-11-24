#!/usr/bin/env python3
"""Turn an audit.json into a hands-off brief for AI agents.

Usage: python build_handoff.py audit.json audit.handoff.md [--json audit.handoff.json] [--force]

The brief is plain Markdown with no design: context, constraints, decisions a
human must make, then one task per opportunity sorted by ICE (ids SEO-01,
SEO-02, ...), each with evidence, exact targets, steps, acceptance criteria,
dependencies, owner, risk and rollback; then measurement and open gaps.
It is built from the same audit.json as the HTML report, so the two never
disagree. Validates first (validate_audit.py). Standard library only.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from validate_audit import validate  # noqa: E402

L = {
    "en": {
        "title": "Hands-off brief", "for": "For an AI agent (or a developer) implementing the fixes. Generated from audit.json by seo-audit; the human-readable report is built from the same file.",
        "how": "How to use this brief", "howList": [
            "Work through the tasks in order unless a dependency says otherwise; each task has an id you can reference in commits and PRs.",
            "Before acting on a task listed under \"Decisions for a human\", stop and ask.",
            "A task is done only when every acceptance criterion passes. Report which ones you verified and how.",
            "Evidence marked `hypothesis` must be confirmed first; if it is wrong, skip the task and say why.",
        ],
        "context": "Context", "constraints": "Constraints", "decisions": "Decisions for a human (before you start)",
        "tasks": "Tasks", "summary": "Task list", "id": "ID", "task": "Task", "owner": "Owner", "ice": "ICE", "dep": "Depends on",
        "goal": "Goal", "evidence": "Evidence", "targets": "Targets", "url": "URL / item", "now": "Now", "want": "Expected",
        "steps": "Steps", "accept": "Acceptance criteria", "metric": "Metric", "effort": "Effort", "risk": "Risk", "rollback": "Rollback",
        "human": "Needs a human decision", "hyp": "Hypothesis to test", "test": "Cheapest test", "thr": "Success threshold",
        "measure": "Measurement", "gaps": "Open gaps (not checked)", "sources": "Sources", "status": "Status", "note": "Note",
        "lens": "Lens", "type": "Type", "alt": "Alternatives considered", "pm": "Pre-mortem", "default": "Default if no answer", "copy": "Copy", "opt": "optimize", "ex": "explore", "none": "none", "period": "Data period",
    },
    "uk": {
        "title": "Hands-off бриф", "for": "Для AI-агента (або розробника), що впроваджує виправлення. Згенеровано з audit.json скілом seo-audit; звіт для людей зібрано з того самого файлу.",
        "how": "Як користуватися брифом", "howList": [
            "Виконуйте задачі по черзі, якщо залежності не кажуть інакше; у кожної задачі є ID для комітів і PR.",
            "Перед задачею з розділу «Рішення для людини» зупиніться й запитайте.",
            "Задача виконана, лише коли пройдено всі критерії приймання. Напишіть, які перевірили й як.",
            "Доказ із позначкою `hypothesis` спершу підтвердьте; якщо він хибний — пропустіть задачу й поясніть чому.",
        ],
        "context": "Контекст", "constraints": "Обмеження", "decisions": "Рішення для людини (до початку роботи)",
        "tasks": "Задачі", "summary": "Список задач", "id": "ID", "task": "Задача", "owner": "Виконавець", "ice": "ICE", "dep": "Залежить від",
        "goal": "Мета", "evidence": "Докази", "targets": "Цілі", "url": "URL / об'єкт", "now": "Зараз", "want": "Має бути",
        "steps": "Кроки", "accept": "Критерії приймання", "metric": "Метрика", "effort": "Зусилля", "risk": "Ризик", "rollback": "Відкат",
        "human": "Потрібне рішення людини", "hyp": "Гіпотеза", "test": "Найдешевша перевірка", "thr": "Поріг успіху",
        "measure": "Вимірювання", "gaps": "Відкриті прогалини (не перевірено)", "sources": "Джерела", "status": "Статус", "note": "Примітка",
        "lens": "Лінза", "type": "Тип", "alt": "Розглянуті альтернативи", "pm": "Pre-mortem", "default": "Якщо відповіді немає", "copy": "Тексти", "opt": "оптимізація", "ex": "дослідження", "none": "немає", "period": "Період даних",
    },
}


def cell(s):
    return str(s if s is not None else "").replace("|", "\\|").replace("\n", " ")


def task_ids(audit):
    """Order opportunities by ICE (stable for ties) and give them SEO-01... ids."""
    ops = audit.get("ops") or []
    order = sorted(range(len(ops)), key=lambda i: -(ops[i]["I"] * ops[i]["C"] * ops[i]["E"]))
    return {i + 1: f"SEO-{rank + 1:02d}" for rank, i in enumerate(order)}, order


def build_tasks(audit):
    ids, order = task_ids(audit)
    ops, det, plans = audit.get("ops") or [], audit.get("detail") or {}, audit.get("plans") or {}
    tasks = []
    for i in order:
        o, oid = ops[i], i + 1
        d = det.get(str(oid), {})
        p = plans.get(str(oid), {})
        tasks.append({
            "id": ids[oid], "op": oid, "title": o["t"], "lens": o.get("ln", o.get("l")), "type": o.get("x"),
            "evidence_type": "observed" if o.get("ev") == "obs" else "hypothesis",
            "ice": o["I"] * o["C"] * o["E"], "I": o["I"], "C": o["C"], "E": o["E"],
            "owner": d.get("owner", ""), "depends": [ids.get(x, str(x)) for x in d.get("depends", [])],
            "human": d.get("human", ""), "goal": p.get("h", ""), "evidence": d.get("why", ""),
            "targets": d.get("targets", []), "steps": d.get("steps", []), "accept": d.get("accept", []),
            "metric": d.get("metric", p.get("m", "")), "effort": d.get("effort", ""), "risk": d.get("risk", ""),
            "rollback": d.get("rollback", ""), "test": p.get("t", ""), "threshold": d.get("thr", ""),
            "alternatives": d.get("alt", []), "premortem": d.get("pm", ""), "copy": d.get("copy", []),
        })
    return tasks


def render_md(audit):
    t = L.get(audit.get("lang"), L["en"])
    h = audit.get("handoff") or {}
    tasks = build_tasks(audit)
    out = [f"# {t['title']}: {audit.get('title', '')}", "", f"> {t['for']}", ""]

    out += [f"## {t['how']}", ""] + [f"{n}. {x}" for n, x in enumerate(t["howList"], 1)] + [""]

    ctx = [f"- **{k}:** {v}" for k, v in (h.get("context") or {}).items()]
    if h.get("period"):
        ctx.append(f"- **{t['period']}:** {h['period']}")
    if ctx:
        out += [f"## {t['context']}", ""] + ctx + [""]

    if h.get("constraints"):
        out += [f"## {t['constraints']}", ""] + [f"- {c}" for c in h["constraints"]] + [""]

    decisions = [x for x in tasks if x["human"]]
    if h.get("decisions") or decisions:
        out += [f"## {t['decisions']}", ""]
        for dd in h.get("decisions") or []:
            out.append(f"- **{dd.get('id', '')}** {dd.get('q', '')}" + (f" {t['default']}: {dd['default']}" if dd.get("default") else ""))
        for x in decisions:
            out.append(f"- **{x['id']}:** {x['human']}")
        out.append("")

    out += [f"## {t['summary']}", "", f"| {t['id']} | {t['task']} | {t['owner']} | {t['ice']} | {t['dep']} |", "|---|---|---|---|---|"]
    for x in tasks:
        out.append(f"| {x['id']} | {cell(x['title'])} | {cell(x['owner'])} | {x['ice']} | {cell(', '.join(x['depends']) or '-')} |")
    out.append("")

    out += [f"## {t['tasks']}", ""]
    for x in tasks:
        out += [f"### {x['id']} · {x['title']}", ""]
        meta = [f"{t['lens']}: {x['lens']}", f"{t['type']}: {t.get(x['type'], x['type'])}", f"ICE {x['ice']} = {x['I']}×{x['C']}×{x['E']}",
                f"evidence: `{x['evidence_type']}`"]
        if x["owner"]:
            meta.append(f"{t['owner']}: {x['owner']}")
        if x["depends"]:
            meta.append(f"{t['dep']}: {', '.join(x['depends'])}")
        out += ["- " + " · ".join(meta), ""]
        if x["human"]:
            out += [f"**{t['human']}:** {x['human']}", ""]
        if x["goal"]:
            out += [f"**{t['goal']}:** {x['goal']}", ""]
        if x["evidence"]:
            out += [f"**{t['evidence']}:** {x['evidence']}", ""]
        if x["targets"]:
            out += [f"**{t['targets']}:**", "", f"| {t['url']} | {t['now']} | {t['want']} |", "|---|---|---|"]
            out += [f"| `{cell(g.get('url', ''))}` | {cell(g.get('now', ''))} | {cell(g.get('want', ''))} |" for g in x["targets"]]
            out.append("")
        if x["steps"]:
            out += [f"**{t['steps']}:**", ""] + [f"{n}. {s}" for n, s in enumerate(x["steps"], 1)] + [""]
        if x["copy"]:
            out += [f"**{t['copy']}:**", ""] + [f"- {c}" for c in x["copy"]] + [""]
        if x["accept"]:
            out += [f"**{t['accept']}:**", ""] + [f"- [ ] {a}" for a in x["accept"]] + [""]
        if x["alternatives"]:
            out += [f"**{t['alt']}:**", ""] + [f"- {s}" for s in x["alternatives"]] + [""]
        if x["premortem"]:
            out += [f"**{t['pm']}:** {x['premortem']}", ""]
        rows = [(t["metric"], x["metric"]), (t["thr"], x["threshold"]), (t["test"], x["test"]), (t["effort"], x["effort"]),
                (t["risk"], x["risk"]), (t["rollback"], x["rollback"])]
        out += [f"- **{k}:** {v}" for k, v in rows if v] + [""]

    if h.get("measurement"):
        out += [f"## {t['measure']}", ""] + [f"- {m}" for m in h["measurement"]] + [""]

    gaps = [c for c in audit.get("checks") or [] if c.get("st") == "nd"]
    if gaps:
        out += [f"## {t['gaps']}", ""] + [f"- {c['t']}" + (f": {c['note']}" if c.get("note") else "") for c in gaps] + [""]

    out += [f"## {t['sources']}", "", f"| {t['sources']} | {t['status']} | {t['note']} |", "|---|---|---|"]
    out += [f"| {cell(s.get('name'))} | {s.get('status')} | {cell(s.get('note'))} |" for s in audit.get("sources") or []]
    out.append("")
    return "\n".join(out)


def render_json(audit):
    h = audit.get("handoff") or {}
    return {"title": audit.get("title"), "lang": audit.get("lang"), "context": h.get("context", {}), "period": h.get("period"),
            "constraints": h.get("constraints", []), "decisions": h.get("decisions", []), "tasks": build_tasks(audit),
            "measurement": h.get("measurement", []), "gaps": [c for c in audit.get("checks") or [] if c.get("st") == "nd"],
            "sources": audit.get("sources", [])}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audit")
    ap.add_argument("out")
    ap.add_argument("--json", help="also write a JSON variant to this path")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    with open(a.audit, encoding="utf-8") as f:
        audit = json.load(f)
    err, warn = validate(audit)
    for w in warn:
        print("[WARN] ", w)
    for e in err:
        print("[ERROR]", e)
    if err and not a.force:
        print(f"Not built: {len(err)} error(s). Fix them or pass --force.")
        return 1
    md = render_md(audit)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Written {a.out} ({len(md.splitlines())} lines, {len(build_tasks(audit))} tasks)")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(render_json(audit), f, ensure_ascii=False, indent=1)
        print(f"Written {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
