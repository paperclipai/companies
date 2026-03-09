<p align="center">
  <strong>Paperclip Company Templates</strong>
</p>

<p align="center">
  <a href="https://github.com/paperclipai/paperclip"><strong>Paperclip</strong></a> ·
  <a href="https://paperclip.ing/docs"><strong>Docs</strong></a> ·
  <a href="https://discord.gg/m4HZY7xNG3"><strong>Discord</strong></a>
</p>

<p align="center">
  <a href="https://github.com/paperclipai/companies/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://github.com/paperclipai/companies/stargazers"><img src="https://img.shields.io/github/stars/paperclipai/companies?style=flat" alt="Stars"></a>
</p>

<br>

## What is this?

# Pre-built agent teams for Paperclip

Ready-to-use company templates that give you a full team of AI agents in minutes. Each template includes role-specific personas, execution checklists, and Paperclip API integration — so your agents know who they are, what to do, and how to coordinate.

**Pick a template. Import it. Your company is running.**

<br>

## Templates

| Template | Agents | Best for |
|----------|--------|----------|
| [**Marketing Agency**](marketing-agency/) | 6 | Content marketing, SEO, social media, growth experiments, design |
| [**Research Team**](research-team/) | 4 | Academic research, data analysis, literature reviews, technical writing |
| [**Startup Essentials**](startup-essentials/) | 4 | Early-stage startups — strategy, engineering, growth |
| [**Default**](default/) | 1 | Minimal starting point — just a CEO |

<br>

## What's in a template?

Each agent directory contains four files:

| File | Purpose |
|------|---------|
| `AGENTS.md` | Identity, memory system, safety rules, file references |
| `SOUL.md` | Persona — strategic posture and communication style |
| `HEARTBEAT.md` | Per-heartbeat execution checklist with Paperclip API integration |
| `TOOLS.md` | Tool inventory (populated as agents acquire tools) |

Templates also include a `README.md` with the agent roster and usage instructions.

<br>

## Template details

### Marketing Agency

A hands-on agency led by a Creative Director. Five specialists cover the full marketing stack.

| Agent | Role | Reports To |
|-------|------|------------|
| CEO | ceo | The board |
| Content Strategist | general | CEO |
| Social Media Manager | general | CEO |
| SEO Specialist | general | CEO |
| Growth Hacker | general | CEO |
| Designer | designer | CEO |

### Research Team

An academic research group led by a Principal Investigator. Three specialists handle data, literature, and writing.

| Agent | Role | Reports To |
|-------|------|------------|
| Lead Researcher | ceo | The board |
| Data Analyst | researcher | Lead Researcher |
| Literature Reviewer | researcher | Lead Researcher |
| Research Writer | general | Lead Researcher |

### Startup Essentials

A lean four-person startup team. The CTO delegates to the Engineer; the CEO handles strategy and growth oversight.

| Agent | Role | Reports To |
|-------|------|------------|
| CEO | ceo | The board |
| CTO | cto | CEO |
| Head of Growth | general | CEO |
| Engineer | engineer | CTO |

<br>

## How it works

Templates plug into [Paperclip](https://github.com/paperclipai/paperclip)'s coordination model:

- **Heartbeats** wake agents on a schedule. Each agent runs its `HEARTBEAT.md` checklist — checking assignments, doing work, extracting facts, and reporting status.
- **The `paperclip` skill** defines the shared protocol all agents follow. `HEARTBEAT.md` is a role-specific overlay that adds domain behavior on top.
- **Org charts** define reporting lines. Lead agents delegate downward; individual contributors escalate upward.
- **Issues** are the unit of work. Agents check out tasks, do the work, and comment results.

<br>

## Quickstart

```sh
# Clone the templates
git clone https://github.com/paperclipai/companies.git

# Pick a template and copy it into your Paperclip project
cp -r companies/startup-essentials/ my-company/
```

Then import the agent configs into your Paperclip instance. See the [Paperclip docs](https://paperclip.ing/docs) for setup details.

<br>

## Contributing

Add a new template by creating a directory with agent subdirectories following the four-file pattern (`AGENTS.md`, `SOUL.md`, `HEARTBEAT.md`, `TOOLS.md`). Include a `README.md` with the agent roster.

<br>

## Credits

Role specialization inspired by [agency-agents](https://github.com/msitarzewski/agency-agents).

<br>

## License

MIT © 2026 Paperclip
