"""Mechanical rubric checks + recurrence candidates for every parsed RCA.

Reads data/rcas.json, writes data/auto_scores.json. Judgment checks (root-cause quality, etc.)
are added later by the review step; see rubric.md for which checks are auto vs judgment.
"""
import json
import math
import re
from collections import Counter
from datetime import date
from pathlib import Path

from paths import HOME as ROOT, MASTER  # noqa: E402
QTY = re.compile(r"\d+\s*(min|mins|minutes|hrs?|hours?|lbs?|pounds|pallets?|totes?|cases?|kg|%)", re.I)
VAGUE_REFOCUS = re.compile(r"(needs? to be (investigated|verified|determined)|(root )?cause (is |remains )?(unknown|not (yet )?(known|determined))|not sure why|tbd|under investigation)", re.I)
STOP = set("the a an and or of to in on at for was were is be been with from by it this that as not no".split())


def substantive(s):
    s = (s or "").strip()
    return bool(s) and s.upper() not in ("N/A", "NA", "NONE", "-") and len(s.split()) >= 4


def is_done(v):
    return (v or "").strip().lower() in ("yes", "y", "done", "complete", "completed")


def auto_score(r):
    s, flags, notes = {}, [], []

    # 1. Problem statement: quantified (3 of the 10; rest is judgment)
    s["problem_quantified"] = 3 if QTY.search(r["initial_problem"]) else 0

    # 2. 6W2H completeness (8) + loss quantified (4)
    answered = sum(substantive(v) for v in r["w2h"].values())
    s["w2h_answered"] = answered
    s["loss_quantified"] = 4 if QTY.search(r["w2h"].get("how_much", "")) else 0
    if not r["refocus"]:
        notes.append("Refocus statement left blank.")
    elif VAGUE_REFOCUS.search(r["refocus"]):
        flags.append("No verified root cause: refocus says the cause is still unknown.")

    # 3. Standards review answered (4)
    std_vals = [v for v in r["standards"].values()]
    filled = sum(1 for v in std_vals if v)
    s["standards_answered"] = round(4 * filled / 9) if std_vals else 0

    # 4. Brainstorm: attendees (5), categories (4), candidate count (3)
    n_att = len(r["brainstorm_attendees"])
    s["brainstorm_attendees"] = 5 if n_att >= 2 else 0
    if n_att < 2:
        flags.append(f"One-person brainstorm ({n_att} named).")
    real = {k: [c for c in v if c.upper() not in ("N/A", "NA")] for k, v in r["sixm"].items()}
    cats = sum(1 for v in real.values() if v)
    s["sixm_categories"] = 4 if cats >= 3 else (2 if cats == 2 else 0)
    n_causes = sum(len(v) for v in real.values())
    s["sixm_causes"] = 3 if n_causes >= 4 else (1 if n_causes >= 2 else 0)

    # 5. Gemba narrowed to <=5 (4)
    g = r["gemba"]
    s["gemba_list"] = 4 if 1 <= len(g) <= 5 else 0
    if not g:
        flags.append("Gemba section left blank.")

    # 7. Actions: owner + due date on every action (4)
    acts = [a for a in r["short_term"] + r["long_term"] if a["action"] and a["action"].upper() != "N/A"]
    if acts:
        complete = sum(1 for a in acts if a["owner"] and a["due"])
        s["actions_owner_due"] = round(4 * complete / len(acts))
        if complete < len(acts):
            flags.append("Action(s) missing an owner or due date.")
    else:
        s["actions_owner_due"] = 0
        flags.append("No actions listed.")
    lt = [a for a in r["long_term"] if a["action"] and a["action"].upper() != "N/A"]
    if not lt:
        notes.append("No long-term action.")
    for a in acts:
        if is_done(a["resolved"]) and not a["completed"]:
            flags.append("Action marked resolved with no completion date.")
            break

    pts = (s["problem_quantified"] + s["w2h_answered"] + s["loss_quantified"] + s["standards_answered"]
           + s["brainstorm_attendees"] + s["sixm_categories"] + s["sixm_causes"] + s["gemba_list"]
           + s["actions_owner_due"])
    return {"auto_points": pts, "auto_max": 41, "components": s, "flags": flags, "notes": notes,
            "open_actions": sum(1 for a in acts if not is_done(a["resolved"]))}


def tokens(r):
    text = " ".join([r["sheet"], r["initial_problem"], r["w2h"].get("what", ""), r["w2h"].get("where", ""),
                     " ".join(r["gemba"])])
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 2]


def recurrence_candidates(rcas, window_days=90, threshold=0.2):
    # Threshold lowered from 0.28 after the first review found missed repeats (ML1 C6 belt, FFS bottom crease);
    # extra candidates are cheap because the judgment step rules each one in or out.
    docs = [Counter(tokens(r)) for r in rcas]
    df = Counter(w for d in docs for w in d)
    n = len(docs)
    vecs = []
    for d in docs:
        v = {w: c * math.log(n / df[w]) for w, c in d.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        vecs.append({w: x / norm for w, x in v.items()})
    out = {}
    for i, a in enumerate(rcas):
        if not a["event_date"]:
            continue
        da = date.fromisoformat(a["event_date"])
        for j, b in enumerate(rcas):
            if i == j or not b["event_date"] or b["line"] != a["line"]:
                continue
            gap = (da - date.fromisoformat(b["event_date"])).days
            if 0 < gap <= window_days:
                sim = sum(x * vecs[j].get(w, 0) for w, x in vecs[i].items())
                if sim >= threshold:
                    out.setdefault(a["id"], []).append({"prior_id": b["id"], "prior_date": b["event_date"],
                                                        "days_since": gap, "similarity": round(sim, 2)})
    return out


def main():
    rcas = json.loads((ROOT / "data" / "rcas.json").read_text(encoding="utf-8"))
    rec = recurrence_candidates(rcas)
    result = {}
    for r in rcas:
        a = auto_score(r)
        a["recurrence_candidates"] = sorted(rec.get(r["id"], []), key=lambda x: -x["similarity"])[:3]
        result[r["id"]] = a
    (ROOT / "data" / "auto_scores.json").write_text(encoding="utf-8", data=json.dumps(result, indent=1))
    print(f"{len(result)} scored; {sum(1 for v in result.values() if v['recurrence_candidates'])} with recurrence candidates")


if __name__ == "__main__":
    main()
