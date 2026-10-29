# CandyCo RCA Tracker

This plugin reviews every RCA filed in the Supervisors Toolkit line workbooks and grades it for rigor. It checks whether the team walked through the 6W2H, brainstormed with more than one person, went to the Gemba, confirmed a real root cause, and wrote a long-term action that will keep the failure from coming back. It also catches repeat failures, where an earlier RCA's fix didn't hold.

Each weekday morning it adds new RCAs to the RCA Master Database and emails Chad and Shawn the new grades and issue types. If a grade looks wrong, change it in the CI grade override column on the Scorecard tab and add a reason. Overrides carry forward every time the database refreshes.

**Owner:** Shawn Jewkes · **Built by:** Scott Maxfield

## Where things live

| What | Where |
|---|---|
| Master workbook | S Drive › Operations › Continuous Improvement › Root Cause Analysis (RCA) › RCA Master Database.xlsx |
| Working data (parsed RCAs, grades, overrides, email history, run log) | Same folder › RCA Tracker data |
| Grading rules | `skills/rca-tracker/references/rubric.md` in this plugin |
| Who gets the email | RCA Tracker data › config › workbooks.json → `recipients` |

## Setup for Shawn (Windows, about 15 minutes, once)

1. **Install Git for Windows** if it isn't already, from git-scm.com. Quit and reopen the Claude app afterward.
2. **Install the plugin.** In a Claude Code session, run `/plugin marketplace update candyco` and then `/plugin install candyco-rca-tracker@candyco`.
3. **Sync the folder.** In SharePoint, open S Drive › Operations › Continuous Improvement. Select the **Root Cause Analysis (RCA)** folder and click **Add shortcut to My files**. Once it shows up in File Explorer under your OneDrive, right-click it and choose **Always keep on this device**.
4. **Connect Microsoft 365** in the Claude app's connector settings if it isn't already. The daily email goes out from your mailbox.
5. **Tell Claude:** "Set up the RCA tracker." It checks Python, the synced folder and Microsoft 365, then creates the weekday 6:30 AM schedule for you to approve.
6. **Let Scott know** it's running so he can turn his copy off.

The schedule runs only while the Claude app is open. If the app is closed at 6:30, the run happens the next time you open it.

## Everyday use

You don't have to do anything; the morning run handles it. You can also say "run the RCA tracker" anytime to pick up RCAs filed since the last run.

## When something goes wrong

The run sends no email if any step fails, so a quiet morning can mean a failure as well as no new RCAs. The last line of RCA Tracker data › run_log.md says which. Common causes:

- **The workbook was open in desktop Excel on your laptop**, so it couldn't be saved. Close it and say "run the RCA tracker."
- **"Data folder not found."** OneDrive hasn't synced the shortcut, or the folder isn't kept on the device. Redo step 3.
- **"Insufficient tasks on account."** The Microsoft 365 connector is out of quota. Let Scott know.
