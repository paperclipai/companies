---
name: content-audit
description: "Review micro-course content for quality, accuracy, reading level, cultural sensitivity, and WhatsApp formatting compliance."
metadata:
  source: ekatra
  version: 1.0.0
---

# Content Audit

Systematic quality review of micro-course content before deployment.

## Input

You need:
- **Course content**: JSON files (day1-3, modules 1-3 each)
- **Quiz bank**: Questions with answer keys
- **Flashcard deck**: Front/back pairs
- **Content brief**: Target audience, language, source material
- **Original source material** (optional): For accuracy verification

## Audit dimensions

### 1. Accuracy

- Every factual claim must be traceable to the source material
- Definitions must match the domain's accepted usage
- Statistics and numbers must be current and correctly cited
- If source material is insufficient, flag gaps — never fabricate

### 2. Reading level

Target reading level by audience:
- **Field workers / limited formal education**: Grade 6-8 equivalent. Short sentences.
  Concrete examples. No jargon without definition.
- **College-educated professionals**: Grade 10-12 equivalent. Can use domain terms
  with brief explanations.
- **Mixed audience**: Default to Grade 8. When in doubt, simplify.

Check: run a readability score (Flesch-Kincaid or equivalent) on each module.
Flag any module that exceeds the target level by 2+ grades.

### 3. WhatsApp formatting compliance

- [ ] Only uses `*bold*` (single asterisk), `_italic_`, `•` bullets
- [ ] No markdown headers (#, ##), tables, links, or code blocks
- [ ] No images or media references (WhatsApp text-only modules)
- [ ] Each module ≤ 250 words
- [ ] Line breaks use `\n` in JSON strings
- [ ] 1-2 emojis per module (meaningful, not decorative)
- [ ] No messages exceed WhatsApp's 4096 character limit

### 4. Pedagogical structure

For each module, verify:
- [ ] Opens with a hook (relevance to learner's life)
- [ ] Has one clear concept (can be stated in one sentence)
- [ ] Includes a concrete example
- [ ] Ends with a task, question, or reflection prompt
- [ ] Day progression builds (fundamentals → application → synthesis)

For the quiz bank:
- [ ] Questions test taught concepts (not trivia or trick questions)
- [ ] Each day's questions match that day's difficulty level
- [ ] Answer explanations teach, not just confirm
- [ ] Distractors (wrong options) are plausible but clearly wrong

### 5. Cultural sensitivity

- [ ] Examples are relevant to the target audience's context
- [ ] No assumptions about lifestyle, income, family structure, or religion
- [ ] Gender-neutral language unless audience-specific
- [ ] Local currency, units, and references where appropriate
- [ ] No idioms or humor that doesn't translate across cultures

### 6. Engagement

- [ ] Each module creates curiosity or relevance in the first sentence
- [ ] Avoids "textbook tone" — conversational, direct, human
- [ ] Tasks are doable with what the learner has (phone, daily life experiences)
- [ ] Course feels achievable (not overwhelming at any point)

## Process

1. Read all course content end-to-end as if you were the target learner
2. Score each dimension (1-5) with specific evidence
3. Flag any critical issues (accuracy errors, formatting violations, offensive content)
4. Suggest specific fixes for each flagged issue
5. Provide overall pass/fail recommendation

## Output

Audit report with:
- Overall score (pass/conditional pass/fail)
- Per-dimension scores with evidence
- Critical issues list (must fix before deployment)
- Improvement suggestions (nice to have)
- Revised content for any critical fixes
