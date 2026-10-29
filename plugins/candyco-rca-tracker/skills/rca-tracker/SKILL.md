---
name: rca-tracker
description: CandyCo RCA rigor review. Finds new RCAs filed in the Supervisors Toolkit line workbooks, grades each against the RCA rubric (6W2H, brainstorm, Gemba, root cause, actions, repeat failures), updates the RCA Master Database in SharePoint, and emails the new reviews to Chad Stone and Shawn Jewkes. Use for "run the RCA tracker", "review new RCAs", "RCA daily review", "set up the RCA tracker", or the scheduled weekday run.
---

# RCA Tracker

Owner: Shawn Jewkes. Built by Scott Maxfield, 2026-10. This skill grades every new RCA for rigor and flags the issue types CI managers should coach on. The grading rules are in `references/rubric.md`; read it before grading anything.

**Paths.** `SKILL_DIR` means the folder this SKILL.md is in. Scripts are in `SKILL_DIR/scripts`. Run them with `python` on Windows (or `python3` if `python` isn't found) from Git Bash, which the Claude app uses on Windows. The working data is not in the plugin. It lives in SharePoint, in `S Drive/Operations/Continuous Improvement/Root Cause Analysis (RCA)/RCA Tracker data`, synced to this computer through OneDrive. `python SKILL_DIR/scripts/paths.py` prints where it found the data and the master workbook. Below, `DATA` means that folder.

## Hard rules

- Email goes **only** to the addresses in `DATA/config/workbooks.json` → `recipients.to`. Today that is Chad and Shawn. Never add Robert, Erandy, supervisors or RCA authors unless Shawn or Chad says to in this conversation, and then update the config.
- Never write to the line RCA workbooks. They are read-only sources.
- Never overwrite a grade override. Overrides live in the master workbook's Scorecard tab and in `DATA/data/overrides.json`, and `build_db.py` carries them forward. Always rebuild with that script; never edit the workbook by hand.
- If the Microsoft 365 tools return "insufficient tasks on account", that is a connector quota, not a transient error. Stop, don't retry in a loop, don't send an email, and report it.
- If any step fails, send no email. A missed day is fine. A wrong email is not.

## First-time setup (run once on a new computer)

Do this when Shawn says "set up the RCA tracker", or when a daily run finds a step below missing. Fix each item before moving on.

1. **Git and Python.** Run `git --version` and `python --version` (3.10 or newer). If Python is missing on Windows, run `winget install Python.Python.3.12`, then have Shawn quit and reopen the Claude app. Then run `python -m pip install openpyxl`.
2. **Microsoft 365 connector.** Confirm the Microsoft 365 tools work (`read_resource`, `outlook_send_mail`) by reading one line workbook in step 1 of the daily run. If they aren't connected, have Shawn connect Microsoft 365 in the app's connector settings. Emails go out from his mailbox.
3. **Synced data folder.** Run `python SKILL_DIR/scripts/paths.py`. If it says not found, walk Shawn through it: in SharePoint, open S Drive → Operations → Continuous Improvement, select the "Root Cause Analysis (RCA)" folder, and click **Add shortcut to My files**. Wait for OneDrive to sync, then right-click the folder in File Explorer and choose **Always keep on this device**. Rerun until both the data folder and the master workbook show as found.
4. **Schedule.** Create a scheduled task named `rca-tracker-daily` that runs weekdays at 6:30 AM local time with the prompt "Run the CandyCo RCA Tracker daily review using the rca-tracker skill." Shawn approves it in the app. Remind him that scheduled tasks only run while the Claude app is open, and that a run missed while the app was closed happens on the next launch.
5. **Hand-off check.** Append "setup complete on <computer name>, <date>" to `DATA/run_log.md`. Tell Shawn to let Scott know, so Scott can turn off the run on his own Mac.

## Daily run

1. **Find new sheets.** For each workbook code in `DATA/config/workbooks.json` → `workbooks`, call `read_resource` on `file:///<drive_id>/<item_id>` with `startPage=1, endPage=1`. The response lists every worksheet by number. Compare those names with the sheet names already in `DATA/data/rcas.json` for that code, ignoring `Template`, `Sheet*` and `Copy of template`. Names not seen before are new. Microsoft Graph often returns 429 rate-limit errors, so wait and retry the same call.
   - **On Mondays**, run a full refresh instead: re-read every sheet of every workbook. This catches RCAs edited after they were filed (completion dates added, actions closed).
2. **Download.** Read the new sheets by number in as few calls as possible, using `startPage`/`endPage` ranges. Save each response verbatim to `DATA/raw/<CODE>__<YYYY-MM-DD>_p<startPage>.txt`, using UTF-8. If the tool saves a large result to a file, copy that file; if it returns text inline, write it exactly as returned. The double underscore matters, because the parser treats newer dumps as replacing older ones.
3. **Parse and run the auto checks.** Run `python SKILL_DIR/scripts/parse_rca.py`, then `python SKILL_DIR/scripts/score_auto.py`.
4. **Grade the new RCAs.** Take every RCA in `DATA/data/rcas.json` that has an event date and doesn't yet appear in any `DATA/data/judge_output_*.json`. Build its input the same way the items in `DATA/data/judge_input_1.json` are built (`rca`, `auto`, `recurrence_candidates` with each prior RCA's problem, refocus, Gemba and actions). Score the 14 judgment fields in the rubric, using the schema of `DATA/data/judge_output_1.json`, and write `DATA/data/judge_output_<YYYY-MM-DD>.json`. To stay consistent with past grades, read 3–4 examples from the existing judge outputs first. For 10 or more new RCAs, split the work across subagents of about 30 each.
5. **Rebuild.** Run `python SKILL_DIR/scripts/build_db.py`. It reads the grade overrides from the master workbook, rebuilds it, and saves it in place, and OneDrive syncs the result to SharePoint. If it says the file is open in Excel, ask Shawn to close it (or, on a scheduled run, log it and send no email).
6. **Email.** Run `python SKILL_DIR/scripts/render_email.py daily`. If it prints "nothing new", stop: no email on days with no new RCAs. Otherwise send `DATA/out/email.html` as HTML, with the subject from `DATA/out/email_subject.txt`, to `recipients.to` using `outlook_send_mail`. Only after the send succeeds, run `python SKILL_DIR/scripts/render_email.py daily --mark-sent`.
7. **Log.** Append one line to `DATA/run_log.md`: the date, the computer, the new RCAs found, their grades, whether the email was sent, and any warnings.

## Changing who gets the email

When Chad or Shawn decide to bring Robert Villarreal and Erandy Ceja in, add `robert.villarreal@candyco.com` and `erandy.ceja@candyco.com` to `recipients.to` in `DATA/config/workbooks.json` (confirm both addresses with `search_people` first). Make that change only when one of them asks.

## Known quirks

- L2 workbooks (ML2, ML3, FFS) use unlettered 6W2H questions. The parser handles them.
- Excel allows two tabs whose names differ only by trailing spaces. The parser adds " (2)" to the second.
- The same RCA is sometimes pasted into two line workbooks. `build_db.py` dedupes on event date plus problem text and notes "Also filed in…".
- Gemba green/yellow/red highlighting is cell color and isn't visible in the text read. Grade Gemba from the text, and set `gemba_color_unverifiable` when appropriate.
- The Outlook HTML allowlist rejects attributes on tables (no border or cellpadding). `render_email.py` already produces compliant HTML.
