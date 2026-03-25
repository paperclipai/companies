---
name: spaced-repetition
description: "Schedule and manage flashcard reviews using SM-2/FSRS algorithms — calculates next review intervals based on learner recall quality."
metadata:
  source: ekatra
  version: 1.0.0
---

# Spaced Repetition

Manage long-term knowledge retention through algorithmically scheduled flashcard reviews.

## Input

You need:
- **Flashcard deck**: Cards with front (question), back (answer), tags
- **Learner ID**: Phone number or user identifier
- **Review response**: Learner's self-rated recall quality (0-5 scale)

## SM-2 Algorithm

Each flashcard maintains these state variables:
- `ease_factor` (EF): Starts at 2.5, minimum 1.3
- `interval`: Days until next review (starts at 1)
- `repetitions`: Count of consecutive correct recalls

### Scheduling logic

On each review, the learner rates their recall:

| Rating | Meaning | Action |
|--------|---------|--------|
| 0 | Complete blackout | Reset: interval=1, repetitions=0 |
| 1 | Wrong, but recognized answer | Reset: interval=1, repetitions=0 |
| 2 | Wrong, but answer felt familiar | Reset: interval=1, repetitions=0 |
| 3 | Correct with significant difficulty | Don't reset, but don't advance interval |
| 4 | Correct with some hesitation | Advance normally |
| 5 | Perfect recall | Advance normally |

**Ease factor update** (for ratings ≥ 3):
```
EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
```
where q = quality rating. Clamp EF to minimum 1.3.

**Interval calculation**:
- After 1st correct: interval = 1 day
- After 2nd correct: interval = 6 days
- After 3rd+: interval = previous_interval × EF

### WhatsApp delivery format

Send flashcard reviews as interactive messages:

```
🔄 *Review Time!*

[Front of card — question]

Tap when you've thought of the answer:
```

After learner responds:
```
*Answer:* [Back of card]

How well did you remember?
• 😰 Didn't know (0)
• 🤔 Hard (3)
• 👍 Good (4)
• ⭐ Easy (5)
```

## Process

### Step 1 — Initialize deck

After course completion, activate the associated flashcard deck:
- Set all cards to initial state: EF=2.5, interval=1, repetitions=0
- Schedule first review for next day
- Group cards into daily batches of 5-7 (avoid overwhelming)

### Step 2 — Daily review session

Each day at the learner's preferred time:
1. Pull cards where `next_review_date ≤ today`
2. Cap at 7 cards per session
3. Present cards one at a time via WhatsApp
4. Collect recall quality rating for each
5. Update SM-2 state variables
6. Calculate and store next review date

### Step 3 — Adaptive load management

- If learner has 15+ cards due → prioritize lowest EF cards first
- If learner skips a day → carry forward, but cap at 10 cards max
- If learner consistently rates 5 → consider retiring the card (after 5
  consecutive perfect recalls with interval > 30 days)

## Output

- Updated flashcard state (EF, interval, repetitions, next review date)
- Session summary sent to learner: "You reviewed 6 cards today. 4 perfect, 2 need
  more practice. Next review: tomorrow."
- Weekly retention report to Analytics Agent: cards mastered, cards struggling,
  overall retention rate
