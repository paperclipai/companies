---
name: course-localize
description: "Adapt micro-course content for different languages, cultural contexts, and literacy levels — includes vocabulary simplification and audio narration scripts."
metadata:
  source: ekatra
  version: 1.0.0
---

# Course Localize

Adapt existing micro-course content for a new language, culture, or literacy level.

## Input

You need:
- **Source course**: Course JSON (3 days × 3 modules), quiz bank, flashcard deck
- **Target language**: Language code and dialect (e.g., hi-IN for Hindi India,
  sw-KE for Swahili Kenya)
- **Target audience profile**: Literacy level, cultural context, daily life references
- **Localization type**: Translation only, cultural adaptation, or literacy-level
  adjustment (or combination)

## Process

### Step 1 — Translation

If target language differs from source:
1. Translate all course content maintaining WhatsApp formatting (`*bold*`, `_italic_`, `•`)
2. Translate quiz questions, options, and explanations
3. Translate flashcard fronts and backs
4. Keep emojis (they're universal)
5. Do NOT translate: proper nouns, brand names, technical acronyms (define them instead)

Quality checks:
- Back-translate a sample (3 modules) to verify meaning preservation
- Check character count — some languages expand 30-50% (adjust if >250 words)
- Verify WhatsApp renders the script correctly (RTL languages, Indic scripts)

### Step 2 — Cultural adaptation

Replace culturally specific references:
- **Currency**: ₹ → KSh, $, or local currency with equivalent amounts
- **Food/agriculture references**: Rice farming → maize farming (for East Africa)
- **Workplace context**: "Your manager" → "Your supervisor" or "The program coordinator"
  depending on whether audience is corporate or community-based
- **Examples and scenarios**: Must reflect the learner's daily reality
- **Units**: Metric vs imperial, local measurement terms
- **Names in examples**: Use common local names

Do NOT adapt:
- Universal concepts (math, basic science, hygiene practices)
- Data and statistics (but add local context)

### Step 3 — Literacy-level adjustment

For low-literacy audiences (Grade 4-6 reading level):
1. Shorten sentences to 8-12 words maximum
2. Use only concrete nouns and action verbs (avoid abstractions)
3. Replace multi-syllable words with simpler equivalents
4. Add more examples and fewer definitions
5. Reduce module length to 150 words maximum
6. Make quiz questions visual where possible (describe scenarios, not definitions)

For audio-first audiences (where learners may have someone read to them):
1. Write in spoken-word style (contractions, natural phrasing)
2. Add pronunciation guides for technical terms
3. Generate audio narration script with pause markers:
   ```
   [PAUSE 2s] Now let's talk about... [PAUSE 1s]
   ```
4. Keep each audio segment under 3 minutes

### Step 4 — Validation

- [ ] All content translates within WhatsApp formatting constraints
- [ ] Cultural references match the target audience's context
- [ ] Reading level matches the audience's literacy profile
- [ ] Quiz questions are fair in the new language/context
- [ ] Flashcards maintain their pedagogical intent after translation
- [ ] No content lost or distorted in adaptation

## Output

- Localized course JSON (3 days × 3 modules) in target language
- Localized quiz bank with answer keys
- Localized flashcard deck
- Audio narration script (if applicable)
- Localization notes: what was changed and why, cultural assumptions made
