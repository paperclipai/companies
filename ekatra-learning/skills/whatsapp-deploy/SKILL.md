---
name: whatsapp-deploy
description: "Deploy a micro-course to WhatsApp learners via Twilio API — handles enrollment, daily lesson scheduling, progress tracking, and re-engagement."
metadata:
  source: ekatra
  version: 1.0.0
---

# WhatsApp Deploy

Deploy a structured micro-course to learners via WhatsApp using Twilio.

## Input

You need:
- **Course content**: Generated course JSON (3 days × 3 modules)
- **Learner list**: Phone numbers with names (E.164 format: +91XXXXXXXXXX)
- **Schedule**: Start date, preferred delivery time (e.g., 9:00 AM IST)
- **Twilio credentials**: Account SID, Auth Token, WhatsApp sender number

## Process

### Step 1 — Enrollment

For each learner:
1. Send welcome message with course title and 3-day overview
2. Collect learner profile: name, learning goal, preferred language
3. Create learner record with status `Approved`
4. Confirm enrollment with Day 1 start time

### Step 2 — Course generation trigger

Once enrolled:
1. Trigger course content association (status → `Content Created`)
2. Set flow step to `awaiting_start`
3. Send "Your course is ready! Tap *Start Day 1* to begin" message

### Step 3 — Daily delivery

Each day, deliver 3 modules in sequence:

```
Trigger: Learner taps "Start Day X" or sends "start"
  → Flow step: awaiting_start → idle
  → Send Module 1
  → Wait for learner response / 3-minute delay
  → Send Module 2
  → Wait for learner response / 3-minute delay
  → Send Module 3
  → Send day summary + quiz
  → Mark day complete (dayCompleted: true)
  → Flow step → awaiting_next_day (locked until next calendar day)
```

### Step 4 — Day unlock (cron)

Daily cron job (via `/nextday` endpoint):
1. Find all learners with `awaiting_next_day` status where 24h have elapsed
2. Unlock next day's content (flow step → `awaiting_start`)
3. Send reminder: "Day X is ready! Tap *Start* when you're ready 📚"

### Step 5 — Re-engagement

Monitor for inactive learners:
- **24h inactive** during active course: Send gentle reminder with progress summary
- **48h inactive**: Send motivational message with peer completion stats
- **72h+ inactive**: Send final re-engagement with option to restart or pause

### Step 6 — Completion

When all 3 days are complete:
1. Send completion certificate message
2. Transition learner to spaced repetition phase (flashcard reviews)
3. Update learner status to `Completed`
4. Report completion to Analytics Agent

## Status tracking

| Status | Meaning |
|--------|---------|
| `Approved` | Enrolled, content being generated |
| `Content Created` | Course ready, awaiting learner start |
| `Pending` | Course in progress |
| `Failed` | Generation or delivery error |
| `Completed` | All 3 days finished |

| Flow Step | Meaning |
|-----------|---------|
| `alfred_topic` | Collecting topic preference |
| `awaiting_start` | Day unlocked, waiting for learner |
| `idle` | Actively receiving modules |
| `awaiting_next_day` | Day complete, locked until tomorrow |

## Output

- Deployment confirmation: learner count, schedule, estimated completion date
- Daily status: lessons sent, modules completed, response rates
- Final report: per-learner completion status, drop-off points, quiz scores

## Failure handling

- If Twilio delivery fails → retry 3x with exponential backoff, then alert
- If learner sends unexpected message during course → route to Q&A handler
  (Llama 11B, ≤300 words, teaching assistant context)
- If webhook `/cop` is unreachable → alert Platform Engineer immediately
