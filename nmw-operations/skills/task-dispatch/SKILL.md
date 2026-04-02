---
name: task-dispatch
description: "Task dispatching and accountability system for agent swarms. Covers task creation, assignment, status tracking, and proof-of-completion requirements."
---

# Task Dispatch

## Task Lifecycle

1. **Created:** Task defined with clear scope, assigned to an agent
2. **In Progress:** Agent has checked out the task and is working
3. **Blocked:** Agent needs input or access they don't have
4. **Review:** Work complete, awaiting verification
5. **Done:** Verified complete with proof

## Dispatch Rules

- Every task has a single owner. No shared assignments.
- Task description includes: what to do, what files/systems to touch, what "done" looks like.
- Always specify the three layers: Tools (what to use), Risks (what to flag), Format (what output looks like).
- Don't say "based on your findings." Read the actual findings and specify exactly what to do.

## Proof of Completion

No task is "done" without evidence:
- **Code task:** File exists (ls), committed (git log), deployed (curl), output attached
- **Research task:** Sources cited, confidence rated, findings summarized with "so what"
- **Communication task:** Message sent (ID/timestamp), recipient confirmed, template used
- **Analysis task:** Data source identified, methodology stated, conclusions actionable

## Escalation

- Agent blocked for > 30 minutes: escalate to Henry
- Task requires cross-agent coordination: Henry orchestrates
- Task touches customer data: requires verification before and after
- Task involves money (invoicing, pricing): double-check before executing
