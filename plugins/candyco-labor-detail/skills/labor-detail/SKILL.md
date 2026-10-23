---
name: labor-detail
description: "Build CandyCo's daily Labor Detail (OEE, labor vs standard, misc labor) and the 'Labor Detail - OEE and Summary' email with Amy Hadrich, from the plants' shift workbooks and daily schedules on the synced S Drive plus NetSuite work-order completions. Claude rebuilds the Daily Report numbers, walks Amy through every item that needs her judgment (runs off schedule, NetSuite vs supervisor count gaps, planned changeover / cleaning / lunch time, lunch rotations, unmapped downtime, missing standards), records her answers, builds the workbook in her layout with live formulas and her summary email, and publishes both only after she approves. Invoke when the user says 'build the labor detail', 'labor detail for yesterday', 'run the labor detail for <date>', 'make the daily labor report', 'set up the labor detail', or similar."
user-invocable: true
metadata:
  version: "0.1.0"
  argument-hint: "build the labor detail for <date | yesterday>"
  owner: "Scott Maxfield (scorecard) · Amy Hadrich (daily run)"
---

# labor-detail

You are building Amy's daily **Labor Detail** with her. The numbers come from code in the
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
If a page came back inline instead of as a file, re-run that page; never retype results.

### 2. Prepare
`python automation/kpi-recon/scripts/amy_daily.py prepare --date D`

It reads the three plants' shift workbooks (this week's `L1/L2/L3 <Monday> to <Saturday>.xlsx` in Supervisors
Toolkit) and the two daily schedules (`Daily Schedule Jobs by Department MM-DD-YYYY.xlsx`), rebuilds the Daily
Report numbers and prints the **review list**. If it prints `MISSING`, tell Amy which file isn't there yet (a
shift tab not filled in, a schedule not posted) and offer to try again in 30 minutes. If it prints
`NEED NETSUITE`, go back to step 1.

### 3. Review with Amy (the important part)
Go through the review list **one line at a time** (L1, then L2, then L3). For each flag, say what you found in
one sentence and ask the one question. Record each answer with:

`python automation/kpi-recon/scripts/amy_daily.py override --date D --line <LINE> --shift <1|2|3> --field <field> [--sku <item>] --value <number> [--hc <crew>] --note "<her words>"`

| Flag | What to ask | Field |
|---|---|---|
| **off schedule** — hours or units far from the schedule, or an item run / not run | "Sollich-4 1st made 255,900 against 163,200 on a 4-hour schedule. What hours ran should I use, and should scheduled units change?" | `line_hrs`, `sched_units` (+ `--sku`) |
| **count gap** — NetSuite and the supervisor differ | "ML2 1st: NetSuite 337,250, supervisor 308,750. Keep NetSuite?" (her rule: NetSuite unless labels/recording had a problem; then move the difference between shifts so the day total still matches NetSuite) | `prod_units` (+ `--sku`) |
| **planned time** — the schedule planned changeover / cleaning / lunch | "Sollich-4 had 4 h of cleaning/lunch rotation planned. Any downtime to take out?" | `total_dt` |
| **downtime cause** — a reason the map couldn't place | "'Capture test' on ML4 3rd, 20 min — count it as downtime?" | `total_dt` if it changes |
| **no standard crew** | "No standard crew on file for <item>. What should standard be?" | `std_hc` |
| **lunch rotations** (always, per plant) | Show the shift notes that mention lunch (they're in the workbook's Lunch Rotations comment) and ask for crew and hours per shift | `lunch_hrs` with `--hc` |
| **line cleaning** (when she wants to change the estimate) | "ML1 3rd: I have 4 crew × 8 h cleaning. Right?" | `cleaning_hrs` with `--hc` |

Rules: one question at a time; accept "keep it" and move on; never fill an answer she didn't give. When
the list is done, run `prepare` again so her answers apply, and tell her how many items are left (should be 0
or only ones she chose to leave).

### 4. Build
`python automation/kpi-recon/scripts/amy_daily.py build --date D`

Show Amy, in a few lines: company Labor % actual vs standard, OEE, LBS attainment, and each plant's Labor %;
then the workbook path and the email text (`automation/kpi-recon/out/amy/D/email.txt`). Point out anything
unusual (a Labor % far from the week's others, an unpriced item, OEE over 110%). Let her edit the email's
downtime reasons — the supervisors' words are a draft; she may want to shorten them as she does today.

### 5. Publish — only after Amy says "approved", "publish", "send it" or similar
1. `python automation/kpi-recon/scripts/amy_daily.py publish --date D` — saves the workbook to
   `S Drive/Operations/Production Analytics/Labor Detail/<YYYY>/<MM-Month>/` and pushes the day's data to
   the ops portal repo. If the push fails (no GitHub access), say so; the workbook is still saved.
2. Send the email with the Outlook tool (`outlook_send_mail`, `bodyType: html`): subject from the first line
   of `email.txt`, body = the rest as HTML paragraphs and bullet lists, plus a link to the workbook:
   `https://mrscalls.sharepoint.com/sites/CandyCoServer/Shared Documents/S Drive/Operations/Production Analytics/Labor Detail/<YYYY>/<MM-Month>/<file name>`.
   **Recipients:** during the parallel run (until Scott says to switch) send only to Amy and
   scott.maxfield@candyco.com. After the switch, use Amy's usual distribution — confirm the list with her
   before the first full send.
3. Tell Amy what was saved, pushed and sent, with the links.

### 6. If something breaks
Say what failed in one sentence and what you need (a file, a connector, an answer). Don't work around a
missing source by estimating it. Scott owns the scripts; tell Amy to forward the error to him.

### 7. Parallel-run check (first two weeks)
When Amy's own Labor Detail for D exists, compare:
read her workbook from the S Drive with
`python automation/kpi-recon/scripts/xlsx_to_text.py "<her file>" > /tmp/amy.txt`, then
`python automation/kpi-recon/reference/amy-build/parse_amy_values.py /tmp/amy.txt /tmp/amy.json` and
`KPI_PLANT_CORE=plant-built python automation/kpi-recon/scripts/tieout_amy.py --date D --amy /tmp/amy.json`.
Walk her through the differences by cause and note any rule she gives you for Scott.

## Reference
- `references/SOP.html` — the standard operating procedure (print it; one copy at Amy's desk).
- Method details: headers of `build_daily_report.py`, `review_flags.py`, `sku_runs.py`, `build_labor_detail.py`.
