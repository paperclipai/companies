---
name: learner-analytics
description: "Aggregate learner completion data, quiz scores, and engagement metrics — uses Bayesian Knowledge Tracing for concept mastery estimation."
metadata:
  source: ekatra
  version: 1.0.0
---

# Learner Analytics

Transform raw learner interaction data into actionable insights.

## Input

Data sources:
- **Learner records**: Status, progress, flow step, timestamps
- **Course content**: Module structure, quiz questions, flashcard decks
- **Interaction logs**: Messages sent/received, response times, Q&A queries
- **Quiz responses**: Answers, correctness, time taken

## Metrics

### Individual learner metrics

| Metric | Calculation | Target |
|--------|-------------|--------|
| Completion rate | Days completed / 3 | 100% |
| Quiz score | Correct answers / total questions | ≥70% |
| Time-on-task | Timestamp(last module response) - Timestamp(first module sent) | 15-20 min/day |
| Q&A engagement | Questions asked during course | ≥1 per day |
| Response latency | Time between lesson received and first interaction | <2 hours |
| Flashcard retention | Cards with EF > 2.0 after 2 weeks / total cards | ≥80% |

### Bayesian Knowledge Tracing (BKT)

For each concept taught in the course, maintain a mastery estimate:

**Parameters** (calibrated per content type):
- P(L₀) = 0.1 — Prior probability of knowing before instruction
- P(T) = 0.3 — Probability of learning from one instruction exposure
- P(G) = 0.25 — Probability of guessing correctly (4-option MCQ)
- P(S) = 0.1 — Probability of slipping (wrong answer despite knowing)

**Update rule** after each observation (quiz answer):

If answer is correct:
```
P(L|correct) = P(L) * (1 - P(S)) / (P(L) * (1 - P(S)) + (1 - P(L)) * P(G))
```

If answer is incorrect:
```
P(L|incorrect) = P(L) * P(S) / (P(L) * P(S) + (1 - P(L)) * (1 - P(G)))
```

After update, apply learning transition:
```
P(L_new) = P(L|observation) + (1 - P(L|observation)) * P(T)
```

**Mastery threshold**: P(L) ≥ 0.95 → concept mastered.

### Cohort metrics

| Metric | Calculation |
|--------|-------------|
| Cohort completion rate | Learners completed / learners enrolled |
| Average time to completion | Mean(completion_date - enrollment_date) |
| Drop-off by day | Count dropped per day / total enrolled |
| Module-level drop-off | Count who stopped at each module |
| Knowledge gain | Mean(post_mastery - pre_mastery) per concept |
| NPS proxy | (Learners who completed + asked questions) / enrolled |

## Process

### Step 1 — Data collection

Query learner database for:
- All learners in the target cohort/organization/course
- Status, progress, timestamps, quiz responses
- Flashcard review history (SM-2 state)

### Step 2 — Compute metrics

For each learner: compute individual metrics.
For cohort: aggregate and compute distributions (not just means — show medians
and percentiles too).

### Step 3 — Identify patterns

- **High drop-off module**: If >20% of learners drop at the same module → content issue
- **Low quiz scores on specific concept**: If mean score <50% → concept needs reteaching
- **Time-on-task outliers**: If a learner takes 3x average → possible comprehension issue
- **Disengaged cohort segment**: If a demographic/location group underperforms → delivery
  channel or timing issue

### Step 4 — Generate report

Structure as:
1. Executive summary (3 bullets: completion rate, top concern, top win)
2. Completion funnel (enrolled → started → Day 1 → Day 2 → Day 3 → completed)
3. Per-concept mastery heatmap
4. At-risk learner list (with recommended interventions)
5. Recommendations (max 3, each actionable)

## Output

- Formatted analytics report (Markdown or PDF-ready)
- At-risk learner alerts with intervention recommendations
- Concept mastery matrix (learners × concepts × P(L))
- Raw data export (CSV) for client's own BI tools
