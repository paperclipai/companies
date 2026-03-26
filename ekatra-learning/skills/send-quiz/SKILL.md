---
name: Send Quiz
slug: send-quiz
description: Sends a 3-question MCQ quiz over chat, collects answers, and returns a score.
---

## What this skill does

Delivers three multiple-choice questions one at a time over WhatsApp or Telegram,
waits for single-character answers (A/B/C/D), and returns the final score.

## Inputs

- `channel` (string): "whatsapp" or "telegram".
- `recipient` (string): Phone number or chat ID.
- `questions` (array): 3 question objects.

```json
[
  {
    "question": "What does chlorophyll do?",
    "options": { "A": "...", "B": "...", "C": "...", "D": "..." },
    "answer": "B"
  }
]
```

## Delivery flow

1. Send question 1 with options formatted as:
   ```
   Q1: What does chlorophyll do?
   A) Absorbs water  B) Captures sunlight  C) Makes seeds  D) Stores food
   Reply A, B, C or D
   ```
2. Wait up to 60 seconds for a single-letter reply.
3. Acknowledge: "Correct!" or "Not quite. The answer was B."
4. Repeat for questions 2 and 3.
5. Return final score.

## Output

```json
{
  "score": 2,
  "total": 3,
  "answers": ["B", "A", "D"],
  "correct": [true, true, false]
}
```

## Constraints

- Only accept A, B, C, or D as valid answers (case-insensitive).
- If no answer in 60 seconds, record as wrong and move to next question.
- Do not reveal the correct answer until after the user has answered.
