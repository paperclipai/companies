---
name: engagement-report
description: "Generate weekly and monthly engagement reports for enterprise clients — completion rates, knowledge gain, ROI calculations, at-risk learner identification."
metadata:
  source: ekatra
  version: 1.0.0
---

# Engagement Report

Produce client-facing engagement reports that demonstrate learning impact and ROI.

## Input

You need:
- **Client/organization ID**: Which client's data to report on
- **Reporting period**: Weekly or monthly, with date range
- **Cohort filter** (optional): Specific team, location, or course
- **Previous period data** (optional): For trend comparison
- **Client's success metrics**: What they defined during onboarding (e.g., "90%
  completion within 2 weeks," "quiz scores ≥70%")

## Report structure

### 1. Executive summary (3-4 bullets)

Lead with the most important outcome:
- "87% of your field team completed the product knowledge course (target: 80%)"
- Top win and top concern
- One actionable recommendation

### 2. Completion funnel

Visualize the learner journey with drop-off at each stage:

```
Enrolled:     250  ████████████████████████████████ 100%
Started:      238  ██████████████████████████████   95%
Day 1 Done:   225  █████████████████████████████    90%
Day 2 Done:   210  ████████████████████████████     84%
Day 3 Done:   198  ██████████████████████████       79%
Completed:    198  ██████████████████████████       79%
```

Highlight: where the biggest drop-off occurs and why.

### 3. Knowledge metrics

- **Average quiz score**: Per day and cumulative, compared to passing threshold
- **Concept mastery**: Which concepts have highest/lowest BKT mastery scores
- **Knowledge gain**: Pre-assessment vs post-assessment delta (if pre-assessment exists)
- **Flashcard retention**: Cards mastered vs still in review (for post-course learners)

### 4. Engagement metrics

- **Average time-to-completion**: Days from enrollment to final module
- **Response latency**: Average time between receiving a lesson and engaging
- **Q&A usage**: How many learners asked questions, most common topics
- **Preferred timing**: When learners are most active (for schedule optimization)

### 5. At-risk learners

Table of learners who need intervention:

| Learner | Status | Days Inactive | Last Activity | Risk Level | Recommended Action |
|---------|--------|--------------|---------------|------------|-------------------|
| [Name]  | Day 1  | 3            | Module 2      | High       | Personal outreach  |

### 6. ROI calculation

Translate learning metrics into business value the client cares about:

- **Cost per learner**: Total Ekatra cost / enrolled learners
- **vs. alternative**: Classroom training cost (travel + trainer + venue + lost productivity)
- **Time savings**: Average time-to-competency with Ekatra vs previous method
- **Completion rate comparison**: Ekatra (X%) vs their previous training method (Y%)

Example:
```
Training 250 field reps via classroom:  ₹12,50,000 (₹5,000/person)
Training 250 field reps via Ekatra:     ₹1,50,000 (₹600/person)
Savings:                                ₹11,00,000 (88% reduction)
Additional benefit:                     Zero travel days, zero productivity loss
```

### 7. Recommendations (max 3)

Each recommendation must be:
- Specific: "Rewrite Day 2 Module 2 to include more examples" not "Improve content"
- Backed by data: "35% drop-off at this module vs 8% average"
- Actionable: Clear next step and owner

## Output

- Formatted report (Markdown) ready for client presentation
- Raw data appendix (CSV) for client's BI team
- Comparison to previous period (if data available)
- Recommended actions with priority ratings
