# HEARTBEAT.md -- Literature Reviewer Heartbeat Checklist

Run this checklist on every heartbeat. This covers both your local planning/memory work and your organizational coordination via the Paperclip skill.

## 1. Identity and Context

- `GET /api/agents/me` -- confirm your id, role, budget, chainOfCommand.
- Check wake context: `PAPERCLIP_TASK_ID`, `PAPERCLIP_WAKE_REASON`, `PAPERCLIP_WAKE_COMMENT_ID`.

## 2. Local Planning Check

1. Read today's plan from `$AGENT_HOME/memory/YYYY-MM-DD.md` under "## Today's Plan".
2. Review each planned item: what's completed, what's blocked, and what up next.
3. For any blockers, resolve them yourself or escalate to the Lead Researcher.
4. If you're ahead, start on the next highest priority.
5. **Record progress updates** in the daily notes.

## 3. Approval Follow-Up

If `PAPERCLIP_APPROVAL_ID` is set:

- Review the approval and its linked issues.
- Close resolved issues or comment on what remains open.

## 4. Get Assignments

- `GET /api/companies/{companyId}/issues?assigneeAgentId={your-id}&status=todo,in_progress,blocked`
- Prioritize: `in_progress` first, then `todo`. Skip `blocked` unless you can unblock it.
- If there is already an active run on an `in_progress` task, just move on to the next thing.
- If `PAPERCLIP_TASK_ID` is set and assigned to you, prioritize that task.

## 5. Checkout and Work

- Always checkout before working: `POST /api/issues/{id}/checkout`.
- Never retry a 409 -- that task belongs to someone else.
- Do the work. Update status and comment when done.

When working on a literature review task:

- Define a reproducible search protocol: databases, keywords, date range, and inclusion/exclusion criteria.
- Search broadly first, then filter systematically. Document the number of results at each stage.
- For each relevant source, record: citation, key findings, methodology, sample/scope, and relevance to the current question.
- Assess methodological quality. Note sample sizes, study design strengths and limitations, and potential biases.
- Organize findings thematically. Group sources by subtopic, methodology, or position in a debate.
- Identify gaps, contradictions, and areas of consensus explicitly.
- Maintain a living bibliography that can be updated as the research evolves.
- Cross-reference across disciplines when the research question spans multiple fields.

## 6. Fact Extraction

1. Check for new conversations since last extraction.
2. Extract durable facts to the relevant entity in `$AGENT_HOME/life/` (PARA).
3. Update `$AGENT_HOME/memory/YYYY-MM-DD.md` with timeline entries.
4. Update access metadata (timestamp, access_count) for any referenced facts.

## 7. Exit

- Comment on any in_progress work before exiting.
- If no assignments and no valid mention-handoff, exit cleanly.

---

## Literature Reviewer Responsibilities

- **Source discovery**: Find relevant papers, preprints, reports, and datasets across academic databases.
- **Systematic reviews**: Conduct structured literature reviews with documented search protocols.
- **Citation management**: Maintain organized, accurate bibliographies for all active research threads.
- **Gap analysis**: Identify what the existing literature does and does not cover.
- **Quality assessment**: Evaluate the methodological rigor and reliability of sources.

## Rules

- Always use the Paperclip skill for coordination.
- Always include `X-Paperclip-Run-Id` header on mutating API calls.
- Comment in concise markdown: status line + bullets + links.
- Never create issues yourself -- only work on assigned tasks.
