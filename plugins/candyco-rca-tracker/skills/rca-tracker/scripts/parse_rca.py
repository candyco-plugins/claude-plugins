"""Parse SharePoint RCA workbook text dumps (raw/<CODE>_p*.txt) into structured RCA records.

Each workbook holds one RCA per worksheet, laid out on the standard ROOT CAUSE ANALYSIS REPORT
template. The read_resource text gives tab-separated rows per sheet under '## Sheet: <name>' headers.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from paths import HOME as ROOT, MASTER  # noqa: E402
RAW = ROOT / "raw"

LINES = {
    "S1": ("L1", "Sollich 1"), "S2": ("L1", "Sollich 2"), "S3": ("L1", "Sollich 3"),
    "S4": ("L1", "Sollich 4"), "TW": ("L1", "Twist Wrap"), "WH": ("L1", "Warehouse"),
    "ML2": ("L2", "Molding Line 2"), "ML3": ("L2", "Molding Line 3"),
    "ML3-BeltAdj": ("L2", "Molding Line 3"), "ML3-Blade": ("L2", "Molding Line 3"),
    "FFS": ("L2", "Form, Fill & Seal"), "SP": ("L2", "Sorting & Panning"), "GRD": ("L2", "Grinding"),
    "ML1": ("L3", "Molding Line 1"), "ML4": ("L3", "Molding Line 4"), "MFM": ("L3", "Multi-Format Matrix"),
    "TRF": ("L3", "Truffle Line"), "MTX12": ("L3", "Matrix 1 & 2"),
}
SKIP_SHEETS = re.compile(r"^(template|sheet\d*|copy of template)", re.I)
QUESTIONS = [
    ("what", "What happened"), ("where", "Where did"), ("when", "When did"),
    ("who", "Who was"), ("which", "Which was"), ("where_else", "Where else"),
    ("how", "How did"), ("how_much", "How often"),
]
SIXM = ["man", "machine", "method", "material", "measurement", "environment"]


def cells(row):
    return [c.strip() for c in row.split("\t")]


def nonempty(row):
    return [c for c in cells(row) if c]


def parse_date(s):
    s = (s or "").strip()
    for fmt in ("%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d", "%m.%d.%Y", "%m-%d-%Y", "%m.%d.%y"):
        try:
            return datetime.strptime(s.split(" ")[0], fmt).date().isoformat()
        except ValueError:
            pass
    return None


def split_sheets(text):
    parts = re.split(r"^## Sheet: (.+?) — \d+ rows.*$", text, flags=re.M)
    # parts = [preamble, name1, body1, name2, body2, ...]
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def value_after_label(row, label):
    vals = nonempty(row)
    for i, v in enumerate(vals):
        if v.lower().startswith(label.lower()):
            rest = v[len(label):].strip(" :")
            if rest:
                return rest
            return vals[i + 1] if i + 1 < len(vals) else ""
    return ""


def parse_sheet(code, sheet, body):
    rows = [r for r in body.split("\n") if not r.startswith("[") and r.strip()]
    rec = {"code": code, "plant": LINES.get(code, ("?", code))[0], "line": LINES.get(code, ("?", code))[1],
           "sheet": sheet, "id": f"{code}::{sheet}"}
    joined = [" ".join(nonempty(r)) for r in rows]

    def idx(prefix, start=0):
        # 6W2H questions are lettered ("A. What happened") on L1/L3 templates and unlettered on L2
        for i in range(start, len(joined)):
            line = re.sub(r"^[A-H]\. ", "", joined[i]).lower()
            if line.startswith(prefix.lower()):
                return i
        return -1

    for r in rows[:4]:
        if "Name:" in r:
            vals = nonempty(r)
            rec["author"] = value_after_label(r, "Name:")
            if rec["author"].lower().startswith("date of the event"):
                rec["author"] = ""
            rec["event_date_raw"] = value_after_label(r, "Date of the Event:")
            if rec["event_date_raw"].lower().startswith("date"):
                rec["event_date_raw"] = ""
    rec["event_date"] = parse_date(rec.get("event_date_raw", ""))

    i = idx("Initial Problem Statement")
    rec["initial_problem"] = value_after_label(rows[i], "Initial Problem Statement") if i >= 0 else ""

    # 6W2H: answer = rows between this question and the next marker
    markers = [idx(q[1]) for q in QUESTIONS] + [idx("6W2H Refocus")]
    rec["w2h"] = {}
    for n, (key, _) in enumerate(QUESTIONS):
        a, b = markers[n], markers[n + 1]
        if a < 0:
            rec["w2h"][key] = ""
            continue
        if b < 0:
            b = a + 2
        rec["w2h"][key] = " ".join(joined[a + 1:b]).strip()

    r0, r1 = idx("6W2H Refocus"), idx("3. Standards Review")
    rec["refocus"] = " ".join(joined[r0 + 1:r1]).strip() if r0 >= 0 and r1 > r0 else ""

    # Standards review: 3 rows of Yes/No/TRUE answers
    std = {}
    labels = ["Is there a CL associated", "Were the CL's at proper", "Are the CL settings optimal",
              "Is the area/equipment clean", "There's CIL associated", "Was the CIL followed",
              "Check Materials for defects", "Ensure PM's exist", "Check for gaps in training"]
    for r in rows:
        vals = nonempty(r)
        for lab in labels:
            for j, v in enumerate(vals):
                if v.startswith(lab):
                    nxt = vals[j + 1] if j + 1 < len(vals) else ""
                    std[lab] = "" if any(nxt.startswith(l) for l in labels) else nxt
    rec["standards"] = std
    n0 = idx("Notes:")
    rec["standards_notes"] = value_after_label(rows[n0], "Notes:") if n0 >= 0 else ""

    # Brainstorm attendees
    b0, g0 = idx("4. Brainstorm"), idx("4. Gemba")
    attendees = []
    for r in rows[b0:g0] if b0 >= 0 else []:
        vals = nonempty(r)
        for j, v in enumerate(vals):
            if v.startswith("Name:"):
                n = v[5:].strip() or (vals[j + 1] if j + 1 < len(vals) and not vals[j + 1].startswith("Name:") else "")
                if n:
                    attendees.append(n)
    rec["brainstorm_attendees"] = attendees

    # 6M grid: header row then cause rows until Gemba
    h = idx("Man Machine Method")
    sixm = {k: [] for k in SIXM}
    if h >= 0:
        hdr = cells(rows[h])
        cols = {}
        for ci, c in enumerate(hdr):
            cl = c.lower()
            for k in SIXM:
                if (k == "environment" and "nature" in cl) or cl == k:
                    cols[k] = ci
        for r in rows[h + 1:g0 if g0 > h else h + 8]:
            cs = cells(r)
            for k, ci in cols.items():
                if ci < len(cs) and cs[ci]:
                    sixm[k].append(cs[ci])
    rec["sixm"] = sixm

    # Gemba numbered list
    gemba = []
    a0 = idx("5. Action Plan")
    for r in rows[g0:a0] if g0 >= 0 else []:
        vals = nonempty(r)
        if vals and re.fullmatch(r"[1-5]", vals[0]) and len(vals) > 1:
            gemba.append(" ".join(vals[1:]))
    rec["gemba"] = gemba

    # Actions
    def actions(start_label, stop_label):
        s = idx(start_label)
        if s < 0:
            return []
        e = idx(stop_label, s + 1) if stop_label else len(rows)
        e = e if e > s else len(rows)
        out = []
        for r in rows[s + 1:e]:
            cs = cells(r)
            vals = nonempty(r)
            if not vals:
                continue
            # columns: A gemba#, B action, F owner, G due, H completion, I resolved
            pad = cs + [""] * 10
            out.append({"gemba_ref": pad[0], "action": " ".join(x for x in pad[1:5] if x),
                        "owner": pad[5], "due": pad[6], "completed": pad[7], "resolved": pad[8]})
        return out

    rec["short_term"] = actions("Gemba # Short Term", "Gemba # Long Term")
    rec["long_term"] = actions("Gemba # Long Term", None)
    rec["blank"] = not (rec["initial_problem"] or rec["w2h"].get("what"))
    return rec


def main():
    # Later dumps (daily new-sheet reads, weekly full refresh) supersede earlier ones for the same sheet.
    records = {}
    seen_in_dump = {}  # one dump = all part files sharing a prefix like "FFS" or "FFS__2026-10-30"
    for f in sorted(RAW.glob("*_p*.txt"), key=lambda f: f.stat().st_mtime):
        code = f.name.rsplit("_p", 1)[0].split("__")[0]
        if code == "CITRACKER":
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        if text.lstrip().startswith("{") and '"content"' in text[:500]:
            try:
                text = json.loads(text).get("content", text)
            except Exception:
                pass
        in_file = seen_in_dump.setdefault(f.name.rsplit("_p", 1)[0], set())
        for sheet, body in split_sheets(text):
            if SKIP_SHEETS.match(sheet):
                continue
            # Excel allows tab names that differ only by trailing spaces; keep both
            while sheet in in_file:
                sheet += " (2)"
            in_file.add(sheet)
            rec = parse_sheet(code, sheet, body)
            rec["source_file"] = f.name
            if not rec["blank"]:
                records[rec["id"]] = rec
            else:
                records.pop(rec["id"], None)
    out = ROOT / "data" / "rcas.json"
    out.parent.mkdir(exist_ok=True)
    records = list(records.values())
    out.write_text(encoding="utf-8", data=json.dumps(records, indent=1))
    print(f"{len(records)} RCAs -> {out}")


if __name__ == "__main__":
    sys.exit(main())
