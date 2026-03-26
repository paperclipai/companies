---
name: Generate Lesson
slug: generate-lesson
description: Takes a topic and learner profile, returns a 5-message micro-lesson.
---

## What this skill does

Generates a micro-lesson on any topic as exactly 5 short messages suitable for
WhatsApp or Telegram. Each message is self-contained and builds on the previous one.

## Inputs

- `topic` (string): What to teach. E.g. "compound interest", "photosynthesis", "basic SQL".
- `level` (string, optional): "beginner", "intermediate", or "advanced". Default: "beginner".
- `language` (string, optional): ISO 639-1 language code. Default: "en".

## Output

A JSON array of 5 strings. Each string is one chat message, max 160 characters.

```json
[
  "Message 1: hook / headline",
  "Message 2: core concept defined simply",
  "Message 3: concrete example or analogy",
  "Message 4: a common pitfall or misconception",
  "Message 5: one actionable takeaway or summary"
]
```

## Constraints

- Each message must be under 160 characters (fits one SMS segment).
- No markdown formatting — plain text only.
- Avoid jargon unless the level is "advanced".
- The 5 messages must form a coherent mini-narrative, not just 5 facts.

## Example

Input: topic="photosynthesis", level="beginner"

```json
[
  "Photosynthesis is how plants make their own food using sunlight.",
  "Plants capture light energy in green pigments called chlorophyll.",
  "Think of chlorophyll as tiny solar panels inside every leaf.",
  "Common mistake: plants don't eat soil — soil just provides minerals.",
  "Takeaway: every meal you eat started as sunlight absorbed by a plant."
]
```
