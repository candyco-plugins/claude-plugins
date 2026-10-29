---
name: labor-detail
description: "Build CandyCo's daily labor reports with Amy Hadrich: each plant's Labor Shift Detail (1st/2nd/3rd Shift + Total Plant, with her per-shift Summary drafted), the day's rows in her monthly Labor by Shift files, the Labor Detail - OEE workbook and the 'Labor Detail - OEE and Summary' email, from the plants' shift workbooks and daily schedules on the synced S Drive plus NetSuite work-order completions. Claude rebuilds the Daily Report numbers, walks Amy through every item that needs her judgment (runs off schedule, unscheduled runs, NetSuite vs supervisor count gaps, planned changeover / cleaning / lunch time, lunch rotations, unmapped downtime, missing standards), records her answers, builds everything in her own layouts with live formulas, and after she approves saves it to the S Drive and puts the email in her Outlook Drafts. Invoke when the user says 'build the labor detail', 'labor detail for yesterday', 'run the labor detail for <date>', 'make the daily labor report', 'set up the labor detail', or similar."
user-invocable: true
metadata:
  version: "0.3.1"
  argument-hint: "build the labor detail for <date | yesterday>"
  owner: "Scott Maxfield (scorecard) · Amy Hadrich (daily run)"
---

# labor-detail

You are building Amy's daily labor reports with her: each plant's **Labor Shift Detail**, the day's rows in her
**monthly Labor by Shift** files, and the **Labor Detail - OEE** workbook with its email. The numbers come from code in the
`candyco-ops-reports` repo; your job is to run it, put every judgment call in front of Amy in plain
words, record her answers, and publish only when she says so. **Never invent a number.** Every figure
comes from the shift workbooks, the schedule, NetSuite or Amy's own answer.

The production day **D** runs from each plant's 1st-shift start to the next morning (L1 7:16 AM, L2 6:16 AM,
L3 6:46 AM). "Yesterday" on a Monday means Saturday if the plants ran Saturday, otherwise Friday — ask if
unsure.

Talk to Amy like a colleague: short sentences, numbers first, one question at a time. She knows this report
better than anyone; you're saving her the typing.

## Paths

- Repo: `~/CandyCo KPI/candyco-ops-reports` (Git Bash on Windows: `/c/Users/<name>/CandyCo KPI/...`).
  All commands below run from the repo root. Use `python` on Windows if `python3` isn't found.
- Scripts: `automation/kpi-recon/scripts/` · the full method is in each script's header.
- The S Drive is found automatically under the OneDrive sync. If it isn't, set
  `CANDYCO_SDRIVE` to the folder that holds `Operations` (e.g. `C:\Users\amy\OneDrive - Mrs. Call's Candy Company\Documents\S Drive`).
  Past weeks' shift workbooks move to Supervisors Toolkit's "Old shift exchange" folder; they're found there too.
- OneDrive must have the files on the computer, not just in the cloud: if a read stalls or a file is missing, ask
  Amy to open OneDrive and let it sync (or right-click the S Drive folder → Always keep on this device), then retry.

## Installing (Claude desktop app, Code tab)

`/plugin` commands don't run in the desktop app's Code tab. Install from **+ → Add plugins** (or
**Plugins → Browse plugins**) in a **Local** session, then start a new session. If the CandyCo marketplace
isn't listed, run in PowerShell: `claude plugin install candyco-labor-detail@candyco --marketplace candyco-plugins/claude-plugins`.
Git for Windows must be installed first (quit and reopen the app after installing it). Invoke this skill by name:
`/candyco-labor-detail:labor-detail set up` or `/candyco-labor-detail:labor-detail yesterday`.

## Setup (first run on a computer — "set up the labor detail")

Check each item and fix what you can; tell Amy plainly what she or Scott must do for the rest.

1. **Git and Python.** `git --version`, `python --version` (3.10+). Missing Python on Windows:
   `winget install Python.Python.3.12`, then reopen the Claude app. Then `python -m pip install openpyxl`.
2. **Repo.** If `~/CandyCo KPI/candyco-ops-reports` doesn't exist:
   `git clone https://github.com/d-scott-code/candyco-ops-reports.git "~/CandyCo KPI/candyco-ops-reports"`.
   An access error means Scott still has to add her GitHub account to the repo — stop and say so.
3. **S Drive.** `python automation/kpi-recon/scripts/amy_daily.py prepare --date <a recent weekday>` finds it or
   says it can't. If it can't, ask Amy where OneDrive keeps the S Drive and set `CANDYCO_SDRIVE`.
4. **Connectors.** The NetSuite tools (`ns_runCustomSuiteQL`) and Microsoft 365 / Outlook tools must be
   available in this session. If not: Settings → Connectors in the Claude app; NetSuite needs her role to read
   transactions.
5. Run the daily steps once on a recent day and compare with her own file for that day (step 7).

## Daily run

### 0. Update
`git -C "~/CandyCo KPI/candyco-ops-reports" pull --rebase --autostash origin main`

### 1. NetSuite completions
Run this SuiteQL with the NetSuite connector for D (replace the dates: from D 05:00 to D+1 08:00), with
`pageSize: 1000`, every page (`pageIndex` 0..numberOfPages-1):

```sql
SELECT q.itemid, q.ts, q.qty, RPAD('x',300,'x') AS pad FROM (SELECT i.itemid AS itemid, TO_CHAR(t.createddate,'YYYY-MM-DD HH24:MI') AS ts, SUM(tl.quantity) AS qty FROM transaction t JOIN transactionline tl ON tl.transaction=t.id JOIN item i ON i.id=tl.item WHERE t.type='WOCompl' AND t.createddate >= TO_DATE('D 05:00','YYYY-MM-DD HH24:MI') AND t.createddate < TO_DATE('D+1 08:00','YYYY-MM-DD HH24:MI') AND tl.linesequencenumber=0 AND tl.quantity>0 GROUP BY i.itemid, TO_CHAR(t.createddate,'YYYY-MM-DD HH24:MI')) q ORDER BY 2,1
```
The `pad` column makes the tool save each page to a file. Then:
`python automation/kpi-recon/scripts/save_completions.py <page files in order>` — it must print `OK`.
If a page came back inline instead of as a file, re-run that page; never retype results. On a Saturday the last
entries come in before midnight; that's enough (prepare no longer waits for Sunday morning).

### 2. Prepare
`python automation/kpi-recon/scripts/amy_daily.py prepare --date D`

It reads the three plants' shift workbooks (this week's `L1/L2/L3 <Monday> to <Saturday>.xlsx` in Supervisors
Toolkit) and the two daily schedules (`Daily Schedule Jobs by Department MM-DD-YYYY.xlsx`, including the Notes
column, where the scheduler writes a lower goal like `0.5` or `(50%)` and which Matrix machines run), takes scrap
pounds from the SafetyChain scrap forms, rebuilds the Daily Report numbers and prints the **review list**
(answered flags show as answered, so a re-run shows only what's left). If it prints `MISSING`, tell Amy which file isn't there yet (a
shift tab not filled in, a schedule not posted) and offer to try again in 30 minutes. If it prints
`NEED NETSUITE`, go back to step 1.

### 3. Review with Amy (the important part)
Go through the review list **one line at a time** (L1, then L2, then L3). For each flag, say what you found in
one sentence and ask the one question. Record each answer with:

`python automation/kpi-recon/scripts/amy_daily.py override --date D --line <LINE> --shift <1|2|3> --field <field> [--sku <item>] --value <number> [--hc <crew>] --note "<her words>"`

| Flag | What to ask | Field |
|---|---|---|
| **off schedule** — hours or units far from the schedule, or an item run / not run | "Sollich-4 1st made 255,900 against 163,200 on a 4-hour schedule. What hours ran should I use, and should scheduled units change?" Hours ran drive OEE: when production moved, the schedule's hours leave the rate over 100% until she gives the real hours | `line_hrs`, `sched_units` (+ `--sku`) |
| **made … but the schedule didn't have it** — an unscheduled product ran beside scheduled ones | The flag quotes the shift notes. "S2 1st made 2,728 of 30521, not on the schedule. Notes say 'ran 30521 until 9:00'. How many hours did it run?" Until she answers, its hours are estimated at its standard rate | `run_hrs` with `--sku` |
| **made on another day** — labels or completions entered today for another day's production (she'll usually say so) | "The 1,920 jars of 30521 were made 10/26 and labeled 10/27: take them out of today's hours and OEE?" (they keep units and sales; standard = actual) | `oee_exclude` `--value 1` with `--sku` |
| **count gap** — NetSuite and the supervisor differ | "ML2 1st: NetSuite 337,250, supervisor 308,750. Keep NetSuite?" (her rule: NetSuite unless labels/recording had a problem; then move the difference between shifts so the day total still matches NetSuite). A shift NetSuite has nothing for counts 0 when NetSuite completed the item that day | `prod_units` (+ `--sku`) |
| **units at 0 hours** — NetSuite counted units into a shift the line didn't run | "S2 3rd: 584 counted, but the line was cleaning. Late entries from 2nd, or did it run?" | `prod_units` or `line_hrs` |
| **late start** — the shift started 30+ min late with less downtime logged than the time lost | "TR1 1st started 9:47 with no downtime logged. Count the 197 min lost as downtime?" | `total_dt` or `line_hrs` |
| **planned time** — the schedule planned changeover / cleaning / lunch | "Sollich-4 had 4 h of cleaning/lunch rotation planned. Any downtime to take out?" (ML2/ML3's first 30 CIL minutes a shift are already taken out) | `total_dt` |
| **downtime cause** — a reason the map couldn't place | "'Capture test' on ML4 3rd, 20 min — count it as downtime?" | `total_dt` if it changes |
| **no standard crew** | "No standard crew on file for <item>. What should standard be?" | `std_hc` |
| **training note** — the shift's HC Notes name people in training but its Training HC cell is blank | "L3 3rd notes say '3 Training on WDS', Training HC is blank. Book 3 × 8 h training?" | `training_hrs` with `--hc` (`--line` = the plant, e.g. L3) |
| **lunch rotations** (always, per plant) | Rows the schedule plans as "LUNCH ROTATION" are booked already (that line's crew × the hours; MFM 2 h a shift). Show them, plus the shift notes that mention lunch, and ask for the rest, especially a mixed "CLEANING/LUNCH ROTATION" block (Sollich-4) | `lunch_hrs` with `--hc` (her answer replaces the schedule's for the plant) |
| **line cleaning** (when she wants to change the estimate) | A crew on a line that made nothing that shift (a Level 2 clean) is booked as crew × 8 h cleaning, and a short shift as crew × hours it didn't run. "ML4 Sat 3rd: I have 20 crew × 8 h cleaning. Right?" | `cleaning_hrs` with `--hc` |

Rules: one question at a time; accept "keep it" and move on; never fill an answer she didn't give. When
the list is done, run `prepare` again so her answers apply, and tell her how many items are left (should be 0
or only ones she chose to leave).

### 4. Build
`python automation/kpi-recon/scripts/amy_daily.py build --date D`

It makes, in her own layouts:
- **Labor Shift Detail** for each plant (`reports/kpi-recon/labor-shift/D/LN - Labor Shift Detail - M-D-YY.xlsx`):
  1st/2nd/3rd Shift tabs (each shift's units, pounds, scrap, hours and crew; the day's products in the same rows on
  every tab) and Total Plant (the three added up). Each shift tab's **Summary** box is drafted per line: "Sol-2:
  Scrap achieved - HC miss - Labor achieved" (met in green, missed in red) plus the shift's downtime ("- Chiller
  fault (-45 mins)").
- A preview of the day's rows in her **monthly Labor by Shift** files (same folder). Nothing on the S Drive changes yet.
- The **Labor Detail - OEE** workbook: each day is the plant's Total Plant, as she pastes it.
- The email text (`automation/kpi-recon/out/amy/D/email.txt`).

Show Amy, in a few lines: company Labor % actual vs standard, OEE against the day's goal, LBS attainment, and each
plant's Labor %, then the file paths. Point out anything unusual: a Labor % far from the week's others, a run with
**no sales value** (a new item whose case isn't priced yet; its plant's Labor % is overstated until it is), a rate
cell with a "Rate from the 2026 line schematics" note (no rate of hers on file: ask her for it and tell Scott),
OEE over 110% (usually hours ran still on the schedule).

**Her words are hers to change:** she can edit any shift's Summary wording in the Labor Shift Detail files and the
email's downtime reasons (the supervisors' words are a draft). **Numbers change only through her answers:** record
the answer (step 3), run `prepare` and `build` again. Don't type numbers into the built files: the monthly file gets
each shift's totals from the build.

### 5. Publish — only after Amy says "approved", "publish", "send it" or similar
1. `python automation/kpi-recon/scripts/amy_daily.py publish --date D` — saves:
   - each plant's Labor Shift Detail to `S Drive/Operations/Production Analytics/Labor by shift/<YYYY>/<MM-Month>/Lindon-N/`;
   - the day's shift totals typed into her live monthly `LN - Labor by Shift Detail - <Month> - <YYYY>.xlsx` there
     (the seven numbers she types per shift). The first working day of a month starts the month's file from last
     month's, split into weeks the way she does it (a week cut by the month end is named for its last day, e.g. 11-30-26);
   - the Labor Detail workbook to `S Drive/Operations/Production Analytics/Labor Detail/<YYYY>/<MM-Month>/`;
   - the day's data to the ops portal repo. If the push fails (no GitHub access), say so; the files are still saved.
2. Put the email in **Amy's Outlook Drafts** (`outlook_create_draft`, `bodyType: html`) — she reviews and sends it
   herself: subject from the first line of `email.txt`, body = the rest as HTML paragraphs and bullet lists, plus a
   link to the workbook:
   `https://mrscalls.sharepoint.com/sites/CandyCoServer/Shared Documents/S Drive/Operations/Production Analytics/Labor Detail/<YYYY>/<MM-Month>/<file name>`.
   Address it to her usual Labor Detail list (the same as the Daily Report); confirm the list with her the first time.
   Never send it yourself.
3. Tell Amy what was saved and pushed, with the links, and that the email is waiting in her Drafts.

### 6. If something breaks
Say what failed in one sentence and what you need (a file, a connector, an answer). Don't work around a
missing source by estimating it. Scott owns the scripts; tell Amy to forward the error to him.

### 7. Parallel-run check (first two weeks)
When Amy's own Labor Detail for D exists, compare:
read her workbook from the S Drive with
`python automation/kpi-recon/scripts/xlsx_to_text.py "<her file>" > /tmp/amy.txt`, then
`python automation/kpi-recon/reference/amy-build/parse_amy_values.py /tmp/amy.txt /tmp/amy.json` and
`KPI_PLANT_CORE=plant-built python automation/kpi-recon/scripts/tieout_amy.py --date D --amy /tmp/amy.json`.
Do the same with her own Labor Shift Detail files for D (each shift tab's row 32 against the build's shift totals).
Walk her through the differences by cause and note any rule she gives you for Scott. Expected differences that
aren't errors: prices (the build uses NetSuite's current sales-order prices, which Ryan reviewed; where her price table
is older, e.g. 30703 $2,544.12 vs $2,587, her table needs the update), and Matrix 1 & 2 rates (see below).

## How the numbers work (so you can explain them)

- **OEE** = uptime × rate. Rate = what the line made ÷ (hours ran less downtime × the line's standard rate at 100%).
  Her rate table is the standard; where she has none, the 2026 schematic's rate with its planned efficiency taken out
  (the 35g Caramel Heart: 20,400 an hour at 85% → 24,000).
- **Standards.** Her rate table (rate, haircut, crew), from her own workbooks. Scott's approved exceptions are in
  `reference/rate-decisions.csv`: Sollich-4 wrapped pieces at a 75% haircut for 2026 (a new line); the FEA Heart 35g
  crew at 16 (2 more per shift for the packaging change). A new standard goes to Scott, not into the files.
- **Goals.** Each line's standard goal is fixed for the year (S1 75%, S2 90%, S3 86%, S4 75%, ML2/ML3 85%, FFS 87%,
  TR1/ML1/MM12 85%, ML4 75%, MFM 87%). When the scheduler sets a run under standard in the schedule's Notes column, that
  is the line's goal for the day, and the run's labor standard is held to it too (Amy's efficiency haircut). The plant
  goal is its standard (L1 87%, L2 85%, L3 80%), or on a reduced day the average goal of its lines that ran (L2 Oct 26:
  50% and 85% → 68%). CandyCo's goal is 80%.
- **Matrix 1 & 2 (MM12).** One machine's standard from her pouch table: large pouch (10 oz and up) 2,040 an hour
  (34 a minute, crew 7), small pouch 1,800 (30 a minute); a shift that ran both machines has twice the standard. The
  shift workbook shows a block per machine. Amy sometimes types 40–60 a minute; that's her call, so expect MM12 OEE to
  differ from her sheet by a few points.
- **Sales value.** A finished good at NetSuite's current sales-order price. WIP is valued at what its line packed that
  day (the schedule's Pack rows): pieces × case price ÷ pieces per case where the case says it ("Display Box
  32ct/Case2" = 64; ML1/ML4 caddies 144), and on Sollich-2 the cases NetSuite completed (30733-Case6, 30751-Case6,
  30544-Bulk150) × their price.
- **Misc labor** (same in standard and actual): CILs (0.25 h a person on S1–S3, TR1, ML1, ML4; 0.5 h on ML2, ML3, FFS)
  only for crews on lines that produced that shift; training, sanitation and wash/mold washing head counts × 8 h;
  lunch rotations; line cleaning. **Rework** (actual only) from every shift's rework block, L3 included.
- **Scrap pounds** from the SafetyChain scrap forms by line and shift; each shift's scrap goes to the products that
  ran that shift.
- **Shift Summary goals:** scrap achieved at or under 3% of pounds made; HC achieved when the shift's crew is at or
  under standard; labor achieved when actual labor is at or under standard.
- **Colors** follow her rules automatically (they're conditional formats, not typed): Act Labor red over standard /
  green at or under; scrap % red above 3%; crew red above standard; in the monthly files Act Labor % red above Std
  Labor % and Scrap % red above the goal.

## Reference
- `references/SOP.html` — the standard operating procedure (print it; one copy at Amy's desk).
- Method details: headers of `build_daily_report.py`, `review_flags.py`, `sku_runs.py`, `build_labor_shift.py`,
  `build_labor_detail.py`.
- Her layouts: `reference/labor-shift-template-L1/L2/L3.xlsx` and `reference/labor-detail-template.xlsx`, made from
  her own files by `make_lsd_template.py` / `make_ld_template.py`. If she changes her sheet design, Scott re-runs them.
