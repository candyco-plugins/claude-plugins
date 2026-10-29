"""Render the RCA review email for Chad and Shawn.

  python3 scripts/render_email.py daily   -> RCAs reviewed but not yet emailed (data/state.json)
  python3 scripts/render_email.py intro   -> 60-day backfill summary for the first send

Writes out/email_subject.txt and out/email.html (Outlook-safe HTML: tables, p, b, lists only).
`--mark-sent` records the listed RCA ids as emailed; run it only after the send succeeds.
"""
import collections
import html
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_db  # noqa: E402

ROOT = build_db.ROOT
STATE = ROOT / "data" / "state.json"
WORKBOOK_URL = (ROOT / "config" / "workbook_url.txt").read_text(encoding="utf-8").strip() if (ROOT / "config" / "workbook_url.txt").exists() else ""
ORDER = {"Redo": 0, "Coach": 1, "Solid": 2}


def esc(s):
    return html.escape(str(s or ""))


def final_grade(x, overrides):
    return overrides.get(x["r"]["id"], {}).get("CI grade override") or x["band"]


def issue_table(items):
    counts = collections.Counter(t for x in items for t in x["issues"])
    if not counts:
        return "<p>No issues flagged.</p>"
    rows = "".join(f"<tr><td>{esc(t)}</td><td>{n}</td></tr>" for t, n in counts.most_common())
    return f'<table><tr><th>Issue type</th><th>RCAs</th></tr>{rows}</table>'


def rca_rows(items, overrides):
    out = []
    for x in sorted(items, key=lambda x: (ORDER.get(final_grade(x, overrides), 3), x["score"])):
        r, j = x["r"], x["j"]
        coach = (j.get("coaching") or [""])[0]
        out.append(f"<tr><td><b>{esc(final_grade(x, overrides))}</b><br>{x['score']}</td>"
                   f"<td><b>{esc(r['line'])}: {esc(r['sheet'])}</b><br>{esc(r['event_date'])} · {esc(r.get('author'))}</td>"
                   f"<td>{esc(', '.join(x['issues']) or 'None')}</td><td>{esc(coach)}</td></tr>")
    return ('<table><tr><th>Grade</th><th>RCA</th><th>Issue types</th><th>First coaching point</th></tr>'
            + "".join(out) + "</table>")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    rcas, auto, judged = build_db.load()
    rows = [x for x in build_db.merge(rcas, auto, judged) if x["score"] is not None]
    overrides = json.loads(build_db.OVERRIDES.read_text(encoding="utf-8")) if build_db.OVERRIDES.exists() else {}
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"emailed_ids": []}

    if mode == "intro":
        items = rows
        grades = collections.Counter(final_grade(x, overrides) for x in items)
        subject = f"RCA rigor review: {len(items)} RCAs from the last 60 days"
        lead = (f"<p>Chad and Shawn,</p><p>I've set up a tool that reviews every RCA filed in the Supervisors Toolkit "
                f"line workbooks and grades it for rigor. It checks whether the team actually walked through the 6W2H, "
                f"the brainstorm, the Gemba and a real root cause, and whether the actions will stop the failure from coming back. "
                f"I'd like the two of you to see these first. You can decide when it's ready to share with Robert and Erandy.</p>"
                f"<p>Across the last 60 days, {len(items)} RCAs were reviewed: {grades['Solid']} Solid, {grades['Coach']} Coach "
                f"and {grades['Redo']} Redo. Any hard flag sends an RCA to Redo. These are the issues showing up most:</p>")
        tail = ("<p>Going forward, you'll get a short email each weekday morning listing any new RCAs and how they graded. "
                "If you disagree with a grade, change it in the CI grade override column on the Scorecard tab and add a reason. "
                "Your call sticks, and it will help us tune the grading.</p><p>Let me know what you think.</p>"
                "<p>Scott</p>")
        weakest = sorted(items, key=lambda x: (ORDER.get(final_grade(x, overrides), 3), x["score"]))[:25]
        body_list = rca_rows(weakest, overrides)
        list_head = "<p><b>The 25 weakest, worst first</b> (the full list is in the workbook):</p>"
    else:
        items = [x for x in rows if x["r"]["id"] not in set(state["emailed_ids"])]
        if not items:
            print("nothing new")
            return
        grades = collections.Counter(final_grade(x, overrides) for x in items)
        subject = (f"RCA review {date.today():%b} {date.today().day}: {len(items)} new — "
                   f"{grades['Redo']} Redo, {grades['Coach']} Coach, {grades['Solid']} Solid")
        lead = f"<p>{len(items)} new RCA{'s' if len(items) != 1 else ''} filed since the last review.</p>"
        tail = ("<p>To change a grade, use the CI grade override column on the Scorecard tab.</p>"
                "<p>RCA Tracker (automated review)</p>")
        body_list = rca_rows(items, overrides)
        list_head = ""

    link = f'<p><a href="{esc(WORKBOOK_URL)}">Open the RCA Master Database</a></p>' if WORKBOOK_URL else ""
    body = lead + issue_table(items) + list_head + body_list + link + tail
    (ROOT / "out").mkdir(exist_ok=True)
    (ROOT / "out" / "email_subject.txt").write_text(encoding="utf-8", data=subject)
    (ROOT / "out" / "email.html").write_text(encoding="utf-8", data=body)
    (ROOT / "out" / "email_ids.json").write_text(encoding="utf-8", data=json.dumps([x["r"]["id"] for x in items]))
    print(subject)

    if "--mark-sent" in sys.argv:
        state["emailed_ids"] = sorted(set(state["emailed_ids"]) | {x["r"]["id"] for x in items})
        state["last_sent"] = date.today().isoformat()
        STATE.write_text(encoding="utf-8", data=json.dumps(state, indent=1))


if __name__ == "__main__":
    main()
