---
name: mrp-by-fg
description: "Run the MRP Hack Report: given a CandyCo finished-good item number, explode its multi-level NetSuite BOM and produce a consolidated ~30-week time-phased MRP report for every PURCHASED component (raw materials + packaging) on one page — as both an Excel workbook and an HTML dashboard. Replaces procurement's manual, item-by-item 'MRP Consolidated Report - Weekly Copy & Paste' process (paste each component's number into a saved-search criteria and copy the result). Uses the live NetSuite connector: BOM via SuiteQL, the trusted time-phased numbers (Forecast / Demand / Supply / Ending / Planned_Demand / Planned_Supply / System Balance) from the UNFILTERED planning search id 9661 ('MRP Consolidated Report'), filtered client-side to the BOM component set. Components missing from the planning run are flagged as DATA GAPs, never zeroed. Invoke when the user says 'run MRP Hack Report', 'run the MRP Hack Report for <item>', 'MRP Hack Report <item>', 'run MRP for <item>', 'consolidated MRP for <item>', 'BOM MRP for <item>', or 'what do we need to buy for <item>'."
user-invocable: true
metadata:
  version: "0.3.0"
  argument-hint: "run MRP Hack Report <fg_item_number>"
  validation-status: "Data source = search 9661. Validated cell-for-cell on FG 21125 against 9661 (Jul 2026); case-pack 30804-Case12 validated on the prior search layout (parser is legend-driven / format-agnostic). Procurement: confirm against your manual copy & paste output on your first few real runs."
---

# mrp-by-fg

Produce one consolidated MRP page for every purchased component of a finished good,
from CandyCo's live NetSuite data. Users invoke this by saying **"run MRP Hack
Report"** — if they don't include a finished-good item number, ask for one before
proceeding. Validated cell-for-cell on FG 21125 (bar) and 30804-Case12 (case-pack).
On your first few real runs, spot-check a couple of values against the manual NetSuite
output and tell Scott if anything is off.

This skill ships inside the `candyco-mrp` plugin. Its bundled files live under the
plugin root, exposed as `${CLAUDE_PLUGIN_ROOT}`. **Resolve it once:** run
`echo $CLAUDE_PLUGIN_ROOT`, then reference files as
`${CLAUDE_PLUGIN_ROOT}/skills/mrp-by-fg/references/<file>`. Read
`references/query-notes.md` first — confirmed field IDs, the saved-search cell format,
the BOM boolean gotcha, the internal-id join key, itemtype classification, the
recursion method, and the two-tier FG scoping note. SuiteQL is in
`references/bom-explode.sql`; the renderer is `references/build_report.py`.

## ARGS
| Arg | Required | Default | Notes |
|-----|----------|---------|-------|
| `fg_item` | yes | — | The finished-good item **number** (the displayed `itemid`, e.g. `21125`). |
| `weeks` | no | 30 | Informational; the search always returns Overdue + 30 weekly buckets. |
| `location` | no | (as-returned) | Only for labeling; the search has no runtime filter. |
| `out_dir` | no | `~/.claude/runs/mrp-by-fg/` | Where the `.xlsx` + `.html` land. |

**Data source (fixed):** `searchId = "9661"` ("MRP Consolidated Report", the base
report the Copy & Paste MASTER is built from). This is the UNFILTERED planning search
(≈1,085 items). Do **not** use the "…Copy & Paste", "…in Criteria", or "…MASTER"
variants (incl. numeric id 9955, or the older `..._repor_5`) — those are either
pre-filtered to a manually-pasted item list (they silently miss your components) or a
different/older layout. See query-notes.md → Data source 1. The renderer is
**legend-driven** (it reads each row's label legend), so it adapts if the field set
changes — but 9661 is the confirmed correct source.

## STEP 0 — Preconditions
Confirm the NetSuite connector is available (the `ns_*` tools). If not, stop and
ask the user to enable/authenticate NetSuite. Never fabricate data. Create a scratch
dir for this run, e.g. `SCRATCH=$(mktemp -d)`, and note a run stamp `YYYYMMDD-HHMM`.

## STEP 1 — Metadata guard (drift check)
Call `ns_getSuiteQLMetadata` for `item`, `assemblyitembom`, `bomrevisioncomponent`.
Confirm the columns used by `bom-explode.sql` still exist (`assembly`,
`currentRevision`, `masterDefault`, `inactive`, `bomRevision`, `item`, `itemtype`,
`quantity`). On any mismatch, surface a warning and proceed cautiously rather than
silently returning wrong data.

## STEP 2 — Resolve the finished good
Run: `SELECT id, itemid, itemtype FROM item WHERE itemid = '<fg_item>'`.
- No row → stop: "Item `<fg_item>` not found in NetSuite."
- `itemtype` not `Assembly` → stop: "`<fg_item>` is a `<type>`, not an assembly — it
  has no BOM to explode." (Only assemblies have BOMs.)
Keep the FG description if available for the report header.

## STEP 3 — Explode the BOM (multi-level, in orchestration)
Follow the recursion in `references/query-notes.md`:
- Queue starts with the FG; `visited=set()`; depth cap 10.
- For each parent, run `bom-explode.sql` with `:parent_itemid` substituted (use
  `ns_runCustomSuiteQL`). **Do not** add an `inactive = 'F'` filter — the query
  already handles the `'No'/'Yes'` boolean gotcha.
- Roll up `qty_per_fg` = parent's qty × line `quantity` (FG = 1).
- Classify each component by `component_type`:
  - `'Assembly'` → WIP: record in `wip_assemblies`, enqueue if unvisited (recurse). NOT
    an output row.
  - `'InvtPart'` → **purchased leaf**: merge into `components` (sum `qty_per_fg` across
    duplicate parents). These are the raws + packaging procurement buys.
  - anything else (`'OthCharge'`, `'NonInvtPart'`, `'Service'`, `'Description'`, …) →
    **non-stock / costing line**: record in `non_stock_lines` (itemid + type). These are
    BOM costing artifacts (e.g. a `"Corrugate = $0.069"` OthCharge), NOT MRP-planned
    inventory and NOT in the planning search — do not treat as purchased and do not
    let them become false DATA GAPs. They are listed in the report footnote, not
    tracked in the grid.
- **Keep each component's `component_id` (the item INTERNAL ID) as `internal_id`.**
  The planning search keys its rows by internal id, not the itemid — this is the
  join key in STEP 4. `itemid` is display only.
Write the result to `$SCRATCH/bom_<fg>.json` in exactly this shape (the renderer's
contract):
```json
{
  "fg_item": "<fg>", "fg_description": "<desc or null>",
  "generated_at": "<ISO local time>", "location": "<arg or null>", "search_id": "MRP Consolidated Report - Weekly",
  "components": [{"itemid":"41093","internal_id":"1995","type":"InvtPart","qty_per_fg":1.0,"level":1,"parent":"21125"}],
  "wip_assemblies": [{"itemid":"21124","internal_id":"1994","qty_per_fg":0.0093,"level":1,"parent":"21125"}],
  "non_stock_lines": [{"itemid":"Corrugate = $0.069","internal_id":"1336","type":"OthCharge","level":1,"parent":"30804-Case12"}],
  "warnings": []
}
```
Build the **target internal-id set** = the distinct `components[].internal_id`.

## STEP 4 — Pull the MRP grid and filter to the purchased set
The search has **no runtime item filter**, so the whole (unfiltered) search must be
paged and filtered client-side. Each row carries ~30 large HTML cells and the
universe is ~1,085 items, so **do NOT page the search in your own (the orchestrator's)
context — delegate it to a subagent.** The rows would otherwise flood context; the
subagent absorbs them and returns only a summary.

Spawn a subagent (general-purpose) with these instructions:
- Load the tool via ToolSearch. Call `ns_runSavedSearch`
  `searchId="9661"`, `type="PlanningEngineResult"`,
  paging with `range_start`/`range_end`. **Paging is 0-based — start `range_start=0`.**
  (Starting at 1 silently skips index 0, which is item internal id 105 = "Salt - Pure
  Ocean Small", a very common raw material.)
- **PAGE-SIZE CAUTION (learned in validation):** each row is ~13 KB of HTML, so even
  a 50-row page (~680 KB ≈ 170K tokens) can blow the tool-result token cap. The robust
  method: keep the returned page result OUT of your reasoning — for each page,
  immediately filter and DISCARD non-target rows programmatically (write raw page to a
  temp file and parse with Python/grep for the target `"Item"` internal ids), then move
  on. Do not summarize or reason over full rows. If a page errors on size, halve the
  range and retry.
- Keep only rows whose `"Item"` value (the item **internal id**) is in the target
  internal-id set — pass that list of INTERNAL IDS, not the itemids. (The search's
  `"Item"` column is the internal id; matching on itemid finds nothing.)
- Stop when the end of results is reached (a page returns fewer rows than requested),
  or all targets are found, or a hard cap is hit — report which. Universe is ≈1,085
  rows; expect to scan to the end unless all targets are found first.
- Write the kept row dicts **verbatim** (HTML intact) as a JSON array to
  `$SCRATCH/mrp_rows_<fg>.json`.
- Report: total rows scanned, pages fetched, targets found vs not-found (by internal
  id), file path + row count.

Use the not-found list to drive STEP 5.

## STEP 5 — Reconcile (honest gaps)
Any purchased itemid with no matching row in the search is a **DATA GAP** — the
renderer already renders it blank with an "unknown ≠ zero" flag. Do not invent
values. (The reverse — search rows outside the set — are simply not kept.)

## STEP 6 — Render both outputs
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/mrp-by-fg/references/build_report.py" \
  --bom "$SCRATCH/bom_<fg>.json" \
  --mrp "$SCRATCH/mrp_rows_<fg>.json" \
  --out-dir "<out_dir>" \
  --stamp "<run stamp>"
```
The script prints JSON with the output paths, component count, and data-gap list.
If `openpyxl` is missing, `pip install openpyxl` (or `pip3 install --user openpyxl`).

## STEP 7 — Hand off
Give the user a short chat summary: FG number + description, # purchased components,
# WIP sub-assemblies traversed, # DATA GAPs (name them), page count scanned, and the
two file paths. Keep the **VALIDATION PENDING** note visible. Offer to open the HTML.

## VERIFICATION (before this skill is trusted / published)
1. Run for a known FG. Open the `.xlsx` and `.html`.
2. Spot-check several components' weekly `Ending` and `Planned_Supply` against the
   live planning search in NetSuite — must match cell-for-cell.
3. Confirm any known-missing component shows as a DATA GAP, not zero.
4. Confirm WIP sub-assemblies are traversed but excluded from the rows, and the
   purchased leaves under them are present with rolled-up `qty_per_fg`.
5. Run a second FG on a different line to confirm generality.

## NOTES FOR FUTURE MAINTENANCE
- The renderer is legend-driven (maps cell values to the " " column's row labels),
  so a changed field set adapts automatically; if NetSuite changes the search
  layout, update `parse_cell` in `build_report.py` and the fixture note in
  `query-notes.md`.
- The NetSuite tool prefix in `allowed-tools` is Scott's connection's; on another
  install it may differ (see query-notes → Prerequisite).
- Remove the VALIDATION PENDING banner (here, in `plugin.json`, and the report
  headers) only after Scott confirms parity.
