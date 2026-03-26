---
name: Prospect Outreach
slug: prospect-outreach
description: Finds target prospects and drafts personalised outreach messages.
---

## What this skill does

Identifies organisations that would benefit from Socrates Learning Bot and drafts
a short, personalised outreach message for each.

## Inputs

- `segment` (string): Target segment. One of:
  - `"fmcg"` — consumer goods companies with large field sales teams
  - `"ngo"` — nonprofits with training or education mandates
  - `"schools"` — secondary and vocational schools
- `count` (integer): Number of prospects to return. Default: 10.

## Output

A JSON array of prospect objects:

```json
[
  {
    "org": "Unilever Nigeria",
    "contact_name": "Chidi Okonkwo",
    "contact_role": "Head of Sales Capability",
    "linkedin_url": "https://linkedin.com/in/example",
    "why_relevant": "40,000 field reps across West Africa needing SKU training",
    "outreach_message": "Hi Chidi, we built a bot that teaches field reps product knowledge in 5 WhatsApp messages. Worth a 15-min demo?"
  }
]
```

## Outreach message rules

- Under 60 words.
- Lead with the specific pain or opportunity (field reps, refugee education, etc.).
- Include one concrete metric or proof point if available.
- End with a single low-friction CTA: "Worth a 15-min demo?" or "Want to try it yourself?"
- No marketing buzzwords. Plain English.

## Research sources

LinkedIn, NGO directories (devex.com, reliefweb.int), school databases, and public
company websites.
