# mrp-by-fg — query notes & known-unknowns

Everything here was confirmed live against CandyCo's NetSuite (July 2026). Read
this before changing any query or the parser.

## Prerequisite — NetSuite connector
Each person who runs this skill must have the **NetSuite MCP connector enabled
and authenticated** in their Claude session. The skill calls `ns_*` tools
(`ns_runCustomSuiteQL`, `ns_runSavedSearch`, `ns_getSuiteQLMetadata`). In Scott's
environment those tools carry the server prefix
`mcp__8a715704-911b-4006-88dc-91a40704f34e__`. **That prefix is per-connection and
may differ on another machine.** The `allowed-tools` list in SKILL.md is written
for Scott's prefix; on a different install the tools still work but may prompt for
permission, or `allowed-tools` may need the local prefix. If the connector is
missing or auth fails: stop, tell the user to re-authenticate NetSuite, do **not**
retry in a loop and do **not** fabricate numbers.

## Data source 1 — the MRP grid (planning search)
- Use **`searchId="customsearch_st_mrp_consolidated_repor_5"`** — title
  "MRP Consolidated Report - Weekly". With **`type="PlanningEngineResult"`**
  (required — standalone search type; without it the call fails "Unable to
  determine record type").
- **WHY THIS SEARCH, not the "Copy & Paste"/"in Criteria"/"MASTER" ones:** the
  Copy & Paste family (incl. numeric id **9955**, `..._repor_7`, `..._repo_12`
  MASTER) is *pre-filtered to a manually-pasted item list* — that paste IS the
  manual step we're replacing. Confirmed live: 9955 returned only 16 items
  (105–1928) and **none** of a real FG's components. `..._repor_5` is the
  UNFILTERED universe — confirmed to still return rows at offset 800 (≈800+
  items). It carries the identical 7-div formula cells, so filtering it to the
  BOM set reproduces exactly what the manual copy & paste would show.
- **No runtime filter parameter exists** — only `searchId, type, range_start,
  range_end`. You cannot pass an item list. Run the whole search, page through it,
  and keep only rows whose `"Item"` is in the purchased-component set.
- `Current QTY` can be blank (`""`) for some items — treat as null, not zero.
- **JOIN KEY GOTCHA:** the search's `"Item"` column is the item **INTERNAL ID**
  (e.g. `165`, `1940`, `1995`), NOT the displayed itemid. `"Description"` is the
  item description. So match search rows to BOM components on
  `bomrevisioncomponent.item` (= `component_id`, the internal id), which we carry as
  `internal_id`. Matching on the 5-digit itemid finds nothing. Confirmed live:
  internal `165`→itemid `10177`, `1940`→`10228`, `1995`→`41093`, `2632`→`41237`.
- One row per item. Columns: `Item`, `Description`, `" "` (a single-space key that
  holds the row legend — ignore it), `Current QTY`, `Overdue`, `This Week`,
  `Next Week`, `2 Weeks Out` … `30 Weeks Out`.
- Each time-bucket column is an HTML string of **7 stacked `<div>`s**, fixed order:
  `[0]` Date (literal `"Overdue"` in the Overdue column), `[1]` Forecast,
  `[2]` Demand, `[3]` Planned_Demand (tint `#0F9ED5`), `[4]` Supply,
  `[5]` Planned_Supply (tint `#28a745`), `[6]` Ending. `"-"` means null; numbers
  carry thousands separators and left padding. `Current QTY` is a plain number.
  `Description` embeds `\r\n` between name and code. `build_report.py::parse_cell`
  handles all of this — do not re-parse elsewhere.
- The numbers are **planning-engine outputs**. They are NOT reproducible from
  SuiteQL (only Planned_Supply is queryable, via `plannedorder`). So the saved
  search is the single source of truth — this is what guarantees the report
  matches what the team sees in NetSuite today. Do not substitute a SuiteQL rebuild.

## Data source 2 — the BOM (SuiteQL, `bom-explode.sql`)
- Modern BOM tables: `assemblyitembom` → `bomrevisioncomponent`. Legacy `itemmember`
  is **empty** — never use it.
- One level per query; substitute `:parent_itemid`. Recurse in orchestration.
- Active/default BOM = `masterDefault = 'T'` (skips Rework/Convert/alternate BOMs);
  components join on `assemblyitembom.currentRevision` (the authoritative active
  revision — cleaner than `bomrevision` effective-date math).
- **BOOLEAN GOTCHA:** `assemblyitembom.inactive` renders as `'No'`/`'Yes'` in this
  account and matches **neither `'T'` nor `'F'`**. `inactive = 'F'` matches nothing
  and silently drops every BOM (0 rows). Never filter with `= 'F'`. Exclude only
  explicitly-truthy values (`NOT IN ('T','Yes',...)`). Note `masterDefault` DOES
  render `'T'`/`'F'` — the two booleans are inconsistent; handle each on its own.
- `item.displayname` came back null on the component join — do **not** rely on it
  for descriptions. Descriptions come from the saved search `Description` column.

## Component classification by `itemtype` (drives what appears in the grid)
Confirmed against a 4-level case-pack explosion (`30804-Case12`):
- **`Assembly`** → WIP made in-house. Recurse into it; exclude from output rows.
- **`InvtPart`** → purchased raw material / packaging (incl. pallet `41015`, slip
  sheet `40820`, cases, pouches, flow wrap). These are the grid rows.
- **`OthCharge` / `NonInvtPart` / `Service` / etc.** → non-stock BOM lines. Real
  example: a line whose itemid is literally `"Corrugate = $0.06944"` (type
  `OthCharge`) — a per-unit cost artifact, not planned inventory. It is **not** in the
  planning search, so treating it as purchased would produce a bogus DATA GAP. Put
  these in `non_stock_lines`; the report footnotes them and does not track them.

## Recursion (multi-level explosion) — done in orchestration, not SQL
SuiteQL has no recursive CTE. The skill walks the tree itself:
1. Start queue = [ FG itemid ]. `visited = set()`. `depth = 0` (cap 10).
2. Pop a parent, run `bom-explode.sql` for it.
3. For each component row:
   - accumulate rolled-up `qty_per_fg` = (parent's qty_per_fg) × (this line's
     `quantity`); FG's own qty_per_fg = 1.
   - if `component_type == 'Assembly'` → it's WIP; record it in `wip_assemblies`
     and, if not visited, enqueue it (recurse). It is **not** an output row.
   - else → it's a **purchased** leaf (raw material / packaging); add/merge into
     `components` (sum qty_per_fg if the same itemid appears under multiple
     parents).
4. Guard cycles with `visited`; guard runaway depth with the cap. If the cap is
   hit, add a warning rather than looping.

## Two-tier FG structure — SCOPING NOTE (raise with Scott)
CandyCo has **production assemblies** (e.g. `21125`, the bar) and **case-pack /
shipping assemblies** (e.g. `30xxx-CaseN`) that wrap a production item with case,
pallet (`41015`), and slip sheet (`40820`) packaging. Those pallet/case items are
on the case-pack BOM, **not** on `21125`'s own BOM. So:
- If the user enters the **bar-level** number (21125), the report covers raws +
  primary packaging (flow wrap, bulk box) but NOT pallet/case/slip-sheet.
- If they enter the **case-pack** number, pallet/case/slip-sheet are included.
The skill faithfully explodes whatever item number is given. Confirm with Scott
which tier procurement enters, and whether shipping packaging must appear.

## Known-unknowns to validate before trusting for real decisions
- **Location scope:** unconfirmed whether the search aggregates across all locations
  or a single one. Expose a `location` note in output; validate against the manual view.
- **Search universe completeness:** a purchased component absent from the search's
  result set is surfaced as a **DATA GAP** (blank, "unknown ≠ zero") — never a silent
  zero. (An item with no planning demand/supply may legitimately be absent.)
- **Paging cost:** the search has no item filter, so all ≈800+ pages/rows are scanned
  and only the ~handful of matching rows kept. This is why STEP 4 is delegated to a
  subagent. Record page count during validation.
- **VALIDATION PENDING:** until a full run for a known FG is reconciled cell-for-cell
  against the manual NetSuite output, every report carries the pending banner.
