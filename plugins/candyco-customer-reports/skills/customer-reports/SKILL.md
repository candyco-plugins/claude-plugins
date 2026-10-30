---
name: customer-reports
description: "Build CandyCo's Hershey customer reports with Amy Hadrich from the synced S Drive and NetSuite: the Hershey Production Report (LPN trace log, with shipping columns filled from NetSuite) and Hersheys Daily Summary plus its email draft (Amy sends). Feastables and Mondelez come next. Invoke when the user says 'build the Hershey production report', 'Hershey reports for yesterday', 'run the Hershey trial for <date>', 'set up customer reports', 'run the customer reports', or similar."
user-invocable: true
metadata:
  version: "0.1.0"
  argument-hint: "build the Hershey production report for <date | yesterday>"
  owner: "Scott Maxfield · Amy Hadrich (daily run)"
---

# customer-reports

You are building Amy's customer reports with her. The numbers come from code in the `candyco-ops-reports`
repo; your job is to run it, show Amy what changed, and save only when she says so. **Never invent a number.**
Every figure comes from NetSuite, the Daily Report, SafetyChain, or Amy's own answer.

The production day **D** is the folder Amy saves inputs into: `Daily Shift Reports/<YEAR>/<MM-Month>/<Mon-D>/`
(September folders are `Sept-D`). Its NetSuite completions export covers ~07:00 on D to ~07:00 on D+1, so rows
after midnight carry the next calendar date — that's expected. "Yesterday" on a Monday means Saturday if the
plants ran Saturday, otherwise Friday — ask if unsure.

Talk to Amy like a colleague: short sentences, numbers first, one question at a time.

## Setup ("set up customer reports")

Same as the `candyco-labor-detail` Setup section (Git, Python 3.10+, `openpyxl`, the repo clone, pull to latest). Also
confirm the NetSuite connector is connected in the Claude app (the shipping step runs SuiteQL with it); if it
isn't, tell Amy how to connect it and tell Scott. Then confirm `automation/customer-reports/scripts/` exists.

## Paths

- Repo: `~/CandyCo KPI/candyco-ops-reports` (Git Bash on Windows: `/c/Users/<name>/CandyCo KPI/...`). Run commands
  from the repo root. Use `python` on Windows if `python3` isn't found.
- Scripts: `automation/customer-reports/scripts/`. The method is in each script's header.
- The S Drive is found automatically under the OneDrive sync (same finder as the labor-detail skill). If it isn't,
  set `CANDYCO_SDRIVE` to the folder that holds `Operations`.
- Setup (Git, Python 3.10+, `openpyxl`, the repo clone, connectors) is the same as `candyco-labor-detail`; follow
  its Setup section if this computer hasn't run it.

## Hershey Production Report (daily, internal)

`Production Analytics/Hershey's Molding/Hershey Production Report - <YEAR>.xlsx` — one tab per Hershey
case/pallet/sack/box item. For each day Hershey pack items were completed, the day's LPNs go at the bottom of
the item's tab: A Date, B WO #, C LPN, D Quantity, E Add Date, F Hershey's Batch Code (= NetSuite lot number).
Columns G–J (Shipper, Distrib. Center, Distrib. #, Ship Date) are filled from NetSuite by the shipping step
below, only where they're blank; Laura Brady's own entries and the K/L check columns are never changed. The file
is never sent; other teams read it on the S Drive.

1. **Update.** `git -C "~/CandyCo KPI/candyco-ops-reports" pull --rebase --autostash origin main`
2. **Check the input.** The day folder must hold one `ProductionWorkOrderCompletionsForAmy*.xlsx` (Amy saves it
   each morning for the Daily Report). If it's missing or there are two, ask Amy; don't guess.
3. **Dry run.** `python3 automation/customer-reports/scripts/hershey_production_report.py build --date D`
   (repeat `--date` to catch up several days). This writes a copy to `automation/customer-reports/out/` and prints,
   per item, the LPNs added, the cases, and how many were already there. It must end `TIE-OUT OK`.
4. **Show Amy** the table in plain words: "Adding 37 LPNs / 6,058 cases to 30780-Case12; 104 were already in."
   Call out:
   - **NEW ITEM** lines: a Hershey pack item with no tab yet. Ask Amy for the Hershey item number, then add the
     tab by copying an existing item tab's layout (title in A1: `Item <item> -  <Hershey no.> - <description>`,
     headers in row 2) and re-run.
   - Rows for an earlier day are merged in by Add Date, next to the day before them; her blank separator rows
     stay with the run that followed them. Say where a back-filled day landed ("rows 454–490").
5. **Save** only after Amy says so. She closes the file in Excel first, then:
   `python3 automation/customer-reports/scripts/hershey_production_report.py build --date D --live`
   It backs up the current file to `automation/customer-reports/out/` before writing. Re-running a day never
   duplicates rows (matched on LPN).
6. **Shipping columns.** An LPN is a NetSuite bin; the item fulfillment that shipped it comes from the sales order
   that holds the DC (ship-to line 1, "3060 - MIDWEST") and the DN number (notes field). Run the two SuiteQL queries
   in the header of `automation/customer-reports/scripts/hershey_shipping_fill.py` with the NetSuite connector,
   START = three weeks before today for Q1/Q2 and January 1 for Q3 (relabels), `pageSize: 1000`, every page. Copy
   each saved result file into one new folder (LPN pages as `lpn_0.json`, `lpn_1.json`…, the fulfillment query as
   `ifs.json`, the relabel query as `relabels.json`); never retype results. Then
   `python3 automation/customer-reports/scripts/hershey_shipping_fill.py fill --results <folder> --workbook "<the out/ copy>"`
   (or `--live` after the save in step 5). It fills blank G–J (ship date = the fulfillment date, which is what
   Laura uses) and prints:
   - **REVIEW** lines: Laura's entries that differ from NetSuite, left as is. Common causes: a dragged range that
     auto-incremented SO numbers and dates, or a ship date a day off ("Mark as Shipped" clicked the next morning;
     the fulfillment date stays the source). Send her the list; don't change her cells. Rows she confirms are wrong
     can be rewritten from NetSuite with `--correct <tab>:<first row>-<last row>` (repeatable).
   - **GAP** lines: an SO with no DC or DN number to read. Leave for Laura.
   - **RELABEL** lines: a pallet relabelled or split by a bin transfer after production. The fill follows the
     original LPN to the new ones and fills the original row once they've all shipped; nothing for Laura to do.
   - **Shipped LPNs that don't trace to any tab**: should be empty. If not, tell Scott; don't hand Laura a list.
   Logistics doesn't need any other check from this step (Laura, 2026-10-29): marking shipped sends nothing to
   Hershey, they already work an open-IF list, and the Dock Date is Hershey's due date, not a delivery appointment.

## Hersheys Daily Summary (morning after each Hershey production day, emailed to Hershey)

`Production Analytics/Hershey's Molding/Hersheys Daily Summary - <YEAR>.xlsx` — one tab per line per month
(`October-ML3`, `October-FFS`). Each Hershey item a line ran on D gets one row in that day's week block. Numbers
come from the Daily Report (line tab per-SKU units and lbs; Summary row scrap, line hours, DT minutes) and, for
case/sack/pallet/box items, the NetSuite completed total. C/D/F repeat Amy's last row for the same item.

1. **Check the inputs.** D's folder needs `Daily Report M-D-YY.xlsx` and the completions export.
2. **Dry run.** `python3 automation/customer-reports/scripts/hershey_daily_summary.py build --date D` writes a copy
   to `out/` and prints each row it added ("October-ML3 row 29: 21098 qty 1,225,680 hours 22.5").
3. **Walk Amy through the flags**, one at a time:
   - **Split day** ("line ran 2 items"): hours, scrap and DT were split by each item's share of actual lbs. Amy
     usually knows the real run times and where the downtime happened; take her numbers and edit the copy.
   - **First time on the Daily Summary**: ask for the Hershey item no., description wording and UoM.
   - **NetSuite completed … but no line tab shows its base SKU**: ask Amy which line made it.
   - **New month tab** ("new month tab (layout copied from this line's latest month)"): the first Hershey day of a
     month (or of a line's run in a month) creates `<Month>-<Line>` from that line's latest tab: same columns and
     styles, title updated, one week block per week from that day to month end, spacer rows, % formulas and Total.
     Tell Amy it was made; a line that never had a tab before is flagged instead.
   - **No free row in the week block**: unhide or insert a row in that week, then re-run.
   - Negative adjustment rows (IMS cycle counts, damaged cases) are Amy's; ask if she has any for D.
   Rows go in Amy's week blocks: same week as the line's last row, otherwise the next block. On a split day the
   item carried over from the previous day goes first.
4. **Draft the email.** `python3 automation/customer-reports/scripts/draft_hershey_email.py draft --date D --workbook "<the out/ copy>"`
   writes `out/Hershey's Daily Summary - MM-DD-YY.eml`: her To/Cc, subject, one-line body, a month-to-date
   table for each line that ran D (in place of her screenshot), and the workbook attached.
5. **Save** after Amy approves: close the workbook in Excel, run step 2 with `--live`, re-run step 4 without
   `--workbook` (so the live file is attached), and open the `.eml` — Outlook shows it as a draft; Amy sends.

`hershey_daily_summary.py check --date D` compares what build would write with rows already in her file (use it
to re-verify past days).

## Trial week (parallel run, Oct 30 – Nov 6 2026)

Amy and Laura keep doing both Hershey files by hand and Amy sends her own email. The tool only compares;
**nothing is written to the S Drive and no `--live` or `--correct` is used.** When Amy says "run the Hershey trial
for <date | yesterday>", after she has sent her Hershey email:

1. Production Report dry run for D (step 3 above) against her updated file. Any LPN it would add is one missing
   from her tabs; "Already in" should equal the day's LPN count. Must end `TIE-OUT OK`.
2. `hershey_daily_summary.py check --date D`: list each value that differs from her row, with both numbers.
   A new month tab is a test of its own: compare its layout with the tab Amy built.
3. Shipping fill (step 6 above) against the step 1 copy: count of blanks it would fill and the REVIEW, GAP and
   RELABEL lines. REVIEW lines are differences from Laura's entries, not errors on her part by default.
4. `draft_hershey_email.py draft --date D --workbook "<step 1 copy>"`, but show Amy the `.html` table only and
   compare it to the email she sent. Never open the `.eml` during the trial; it is addressed to Hershey.
5. Write `out/trial - MM-DD-YY.txt` with each difference and Amy's one-line reason (her typo, tool wrong, judgment
   call), and say "all matched" when nothing differs. Amy replies to Scott's trial email with that file or "all matched".

## Coming next

Feastables
Production Summary v3 + EOM Inventory Tool (emailed daily), and Mondelez weekly/monthly/quarterly scorecards
(emailed internally). Each will build the file, list the inputs that still need Amy (IMS adjustments, samples,
holds, quality and safety figures), and save the email to Amy's Outlook Drafts — she sends.
