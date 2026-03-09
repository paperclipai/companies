# Startup Essentials

A lean startup template with four agents covering the core functions of an early-stage company: strategy, technology, growth, and engineering.

## Agent Roster

| Agent | Role | Reports To | Focus |
|-------|------|------------|-------|
| CEO | ceo | The Board | Strategy, fundraising, runway/PMF, hiring, product vision |
| CTO | cto | CEO | Architecture, tech decisions, code review, infra |
| Head of Growth | general | CEO | Marketing, analytics, user acquisition, retention |
| Engineer | engineer | CTO | Build features, fix bugs, write tests, ship code |

## Usage

1. Create a company using this template via the Paperclip API.
2. The CEO agent wakes first, reviews strategy, and delegates work downward.
3. The CTO owns technical direction and delegates implementation to the Engineer.
4. The Head of Growth operates independently on assigned growth tasks.
5. All agents follow the HEARTBEAT.md checklist on every wake cycle.

## Credits

Role specialization inspired by [agency-agents](https://github.com/msitarzewski/agency-agents).
