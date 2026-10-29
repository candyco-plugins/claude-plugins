# RCA rigor rubric — draft v0.1

This rubric grades every new RCA filed in the Supervisors Toolkit RCA workbooks. It follows the sections of our RCA template in order, then adds the CI practices the template implies. Each RCA gets a 100-point score, a grade band, and a short list of the gaps to coach on. Erandy and Robert own the rubric and can adjust any weight or rule here.

Some checks are mechanical and the script runs them (is the field filled, is there an owner). Others need judgment and Claude makes them (is this a root cause or a symptom). Each check below is marked **auto** or **judgment**.

## 1. Problem statement — 10 pts

- Names the line and the equipment or area, not just the product. (auto: line/equipment term present; judgment for edge cases) — 3
- Quantifies the event in the statement itself: DT minutes, lbs, pallets on hold. (auto) — 3
- States the problem, not a cause or a fix. "Hot caramel on the conbar" is a problem. "Operator didn't monitor temp" is a cause. (judgment) — 4

## 2. 6W2H — 20 pts

- All eight questions answered with something substantive. "N/A" or under 4 words counts as blank. (auto) — 8, 1 per question
- "How much" quantifies the loss in units: DT minutes, scrap lbs, pallets, totes. (auto) — 4
- "Where else" shows someone actually checked other lines or sister equipment. "No other line (to our understanding)" earns half credit. (judgment) — 3
- The refocused statement adds what the 6W2H uncovered and is sharper than the initial one. It must not end in "needs to be investigated." (judgment) — 5

## 3. Standards review — 10 pts

- All nine Yes/No/True checks answered. (auto) — 4
- Every "No" (no CL, CIL not followed, no PM, training gap) has a matching action in the action plan. A standards gap with no action is the most common way a fix fails to hold. (judgment) — 6

## 4. Brainstorm (6M) — 15 pts

- At least 2 named attendees, which the template requires. A one-person brainstorm is a **hard flag**. (auto) — 5
- Maintenance is present when the cause is in Machine. (judgment: match names against the maintenance roster once we have it) — 3
- Causes are listed under at least 3 of the 6M categories, and empty categories are marked N/A, as the template asks. (auto) — 4
- At least 4 distinct candidate causes. A brainstorm that lists only the answer it already had is not a brainstorm. (auto) — 3

## 5. Gemba — 15 pts

- The narrowed list has 5 or fewer causes, and they come from the brainstorm. (auto) — 4
- There is evidence the team went to the floor and ruled causes in or out: the green/yellow/red highlighting, or notes on what was observed. (judgment; see limitation below) — 6
- At least one cause is marked or described as the confirmed most-likely root cause. (judgment) — 5

Limitation: the green/yellow/red highlighting is cell color, and our current SharePoint text read does not see color. Until we can read cell fills, this section is graded from the text alone, and an RCA that relies only on color will be under-credited. The scorecard says so whenever this applies.

## 6. Root cause quality — 15 pts (judgment)

- The root cause answers why, not what. "Filter jammed" is what happened. "No standard for filter checks when running high-viscosity dark chocolate" is a root cause. — 6
- It is controllable and specific enough to act on. "Operator error," "human error," "bad luck," and "old equipment" on their own lose these points unless the RCA says why the error was possible (training, standard, design). — 5
- The causal chain hangs together: the root cause plausibly produces the 6W2H facts. — 4

## 7. Action plan — 15 pts

- Every action has an owner and a due date. (auto) — 4
- There is at least one long-term action (over 48 hours) aimed at the root cause. "N/A" in long-term actions when the root cause is a standards, design or training gap is a **hard flag**. (judgment) — 5
- Each action maps to a Gemba # and addresses that cause. Fixing the broken part is a short-term action, not the fix. (judgment) — 3
- The long-term action changes something durable: a CL, CIL, PM, OPL/SOP, training record, or design change. (judgment) — 3

## Hard flags (shown above the score, regardless of points)

- One-person brainstorm.
- No verified root cause, or a refocus that says the cause is still unknown.
- No long-term action against a standards or design gap.
- Actions with no owner or due date.
- **Recurrence**: the same failure mode on the same line or equipment within 90 days of an earlier RCA. This is the efficacy test for the earlier RCA: its fix did not hold. Both RCAs are linked in the database.
- **Closed but not done**: an action is marked Resolved "Yes" with no completion date, or its due date has passed and it is still open.

## Timeliness (reported, not scored)

Days from event date to filing. The CI Action Items Tracker already notes overdue CI reports on 3rd shift, so the digest shows the median and the slowest by shift.

## Grade bands

- **85–100: Solid.** No coaching needed. A one-line note to the author is optional.
- **70–84: Coach.** Specific gaps listed for Erandy, Robert or Shawn to review with the author.
The grade is a suggestion. On the Scorecard tab, a CI manager can override it with the dropdown in the "CI grade override" column and add a reason. The Final grade column uses the override when there is one. Overrides carry forward every time the database refreshes.

- **Under 70, or any hard flag: Redo.** The RCA goes back before it can be closed. Any single hard flag forces Redo, whatever the score. Scott confirmed this strict rule on 2026-10-29.
