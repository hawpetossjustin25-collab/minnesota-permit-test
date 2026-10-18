# Minnesota Class D Permit - Adaptive Knowledge Test Practice

100% free forever. Works fully offline. No subscriptions, no API keys.

## What It Does

- **1,000-question bank** built from the official Minnesota Driver's Manual
- **Every run shows all 1,000 questions** — not just 40
- **Max 15 wrong answers** — the 16th wrong answer **auto-restarts the test instantly**
- **Shuffled every attempt** — new question order each time
- **Smart ordering** — questions you missed come back FIRST, then questions
  you've never answered, then ones you've already gotten right
- **Persistent memory** — your misses are saved between sessions, so the test
  keeps drilling your weak spots until you master them
- **Elapsed-time clock** — tracks how long the full run takes (no limit)
- **Wrong-answer study tab** — every miss shown with your answer, the correct
  answer, and why
- **CSV export** for offline studying

## How to Use

1. Double-click **"MN Permit Test"** on your desktop
   (or run `start_permit_test.bat` in this folder)
2. Click **Start Test**
3. Answer questions — watch the **Wrong: X/15** counter
4. Hit **16 wrong** and the test instantly restarts with a fresh shuffle —
   your missed questions first
5. Finish with 15 or fewer wrong = you pass
6. Study the **Wrong Answers** tab, repeat until you pass every time

## How the Smart Ordering Works

Every run covers all 1,000 questions in this priority:

1. **Questions you got wrong before** (flagged in the database)
2. **Questions you have never seen**
3. **Questions you answered correctly** (last)

Then all 40 are presented so your weakest material hits you first — every
time, until you get them right.

## Files

- `minnesota_permit_test.py` — the application
- `question_bank.py` — 1,000-question bank builder (run it to see stats)
- `start_permit_test.bat` — launcher (auto-installs PyQt6 if missing)
- `minnesota_test_results.db` — attempts, wrong answers, per-question memory
- `wrong_questions_*.csv` — exported study lists

## Requirements

- Windows, Python 3.x, PyQt6 (launcher installs it automatically)

## Honest Disclaimer

Unofficial practice tool. The real exam uses Idemia's AutoTest system with a
protected question bank — these questions come from the same Minnesota
Driver's Manual the real test draws from, but real wording may differ. Read
the free manual from the MN DVS website too.
