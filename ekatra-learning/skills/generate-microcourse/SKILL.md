---
name: generate-microcourse
description: "Generate a structured 3-day micro-course from raw content (PDFs, transcripts, manuals) — outputs WhatsApp-native JSON with quiz banks and flashcard decks."
metadata:
  source: ekatra
  version: 1.0.0
---

# Generate Micro-Course

Turn raw source material into a structured 3-day WhatsApp micro-course.

## Input

You need:
- **Source material**: PDF, document, transcript, slide deck, or SME notes
- **Topic**: Clear topic title for the course
- **Target audience**: Who will learn this (e.g., "field sales reps in rural India,"
  "community health workers," "new hires in FMCG distribution")
- **Language**: Primary language for delivery (default: English)
- **Teaching style**: Conversational, formal, or storytelling (default: conversational)
- **Learning goal**: What the learner should be able to do after completing the course

## Process

### Step 1 — Extract key concepts

Read the source material and identify:
- 9 core teachable concepts (3 per day × 3 days)
- Prerequisite relationships between concepts
- Real-world examples relevant to the target audience
- Common misconceptions to address

### Step 2 — Structure the 3-day arc

Organize concepts into the day-theme framework:

| Day | Theme | Focus |
|-----|-------|-------|
| 1 | Fundamentals | Definitions, core concepts, "why this matters to you" |
| 2 | Intermediate Application | Deeper techniques, patterns, worked examples |
| 3 | Synthesis & Assessment | Real-world use cases, mini-projects, cumulative review |

### Step 3 — Generate course content

For each day, produce 3 modules. Each module follows this structure:
1. **Hook** (1-2 sentences): Why this matters, connect to learner's daily life
2. **Concept explanation** (4-6 sentences): Clear, jargon-free, with one concrete example
3. **Task or reflection question** (1-2 sentences): Something the learner does or thinks about

Format as JSON:
```json
{
  "module1": { "content": "📚 *Module 1: [Title]*\n\n[Hook]\n\n[Explanation]\n\n💡 *Try this:* [Task]" },
  "module2": { "content": "..." },
  "module3": { "content": "..." }
}
```

Formatting rules:
- `*bold*` for emphasis and headers (single asterisk — WhatsApp style)
- `_italic_` for terms being defined
- `•` for bullet lists
- 1-2 emojis per module (meaningful, not decorative)
- `\n` for line breaks within the JSON string
- Maximum 250 words per module
- No markdown headers, tables, links, or code blocks

### Step 4 — Generate quiz bank

For each day, create 3-5 questions:
- Multiple choice (4 options, one correct) or short answer
- Map each question to the specific concept it tests
- Include answer key with brief explanations
- Difficulty: Day 1 = recall, Day 2 = application, Day 3 = analysis

### Step 5 — Generate flashcard deck

Create 10-15 flashcards covering key concepts across all 3 days:
- Front: Question or prompt
- Back: Answer (concise, ≤2 sentences)
- Tags: day number, concept, difficulty
- SM-2 initial values: ease_factor=2.5, interval=1, repetitions=0

## Output

Deliver four artifacts:
1. **Course JSON** — 3 files (day1.json, day2.json, day3.json), each with module1-3
2. **Quiz bank** — JSON with questions, options, correct answers, explanations
3. **Flashcard deck** — JSON array with front, back, tags, SM-2 metadata
4. **Content brief** — Markdown summary: topic, audience, source material used,
   concepts covered, estimated completion time (15-20 min/day)

## Quality checklist

Before delivering, verify:
- [ ] Each module is ≤250 words
- [ ] WhatsApp formatting only (no markdown headers/tables)
- [ ] Every module has a hook, explanation, and task
- [ ] Day progression builds (fundamentals → application → synthesis)
- [ ] Language matches target audience reading level
- [ ] Quiz questions map to specific taught concepts
- [ ] Flashcards cover all 9 core concepts
