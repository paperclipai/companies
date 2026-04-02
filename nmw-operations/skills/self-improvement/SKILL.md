---
name: self-improvement
description: "Captures learnings, errors, and corrections to enable continuous improvement across the agent team."
---

# Self-Improvement

## When to Log

1. A command or operation fails unexpectedly
2. The owner corrects you ("No, that's wrong...", "Actually...")
3. A requested capability doesn't exist yet
4. An external API or tool fails
5. Your knowledge turns out to be outdated or incorrect
6. A better approach is discovered for a recurring task

## Learning Format

```
### [Date] — [Category]
**Trigger:** What happened
**Learning:** What we now know
**Action:** What changes going forward
**Confidence:** High / Medium / Low
```

## Categories

- **Process:** How we do things (scheduling, routing, handoffs)
- **Technical:** Code, APIs, tools, infrastructure
- **Customer:** Customer behavior, preferences, complaints
- **Market:** Competitor moves, industry changes, pricing shifts
- **Operational:** Equipment, logistics, seasonal patterns

## Review Cadence

- **Daily:** Each agent checks their learnings file before starting work
- **Weekly:** Henry reviews all draft learnings, promotes confirmed ones
- **Monthly:** Team retrospective on patterns across all agent learnings

## Rules

- Log immediately. Context is freshest right after the issue.
- Include the specific error message or correction, not just "something went wrong."
- If the same mistake happens twice, escalate it to a permanent rule.
- Learnings are append-only during the week. Only Henry prunes during weekly review.
