# Contributing

Thanks for your interest in contributing to the Paperclip companies collection! This repo contains ready-to-import agent company templates for [Paperclip](https://github.com/paperclipai/paperclip).

## What's in this repo

Each top-level directory is a self-contained agent company that follows the [Agent Companies spec](https://agentcompanies.io/specification):

```
<company-slug>/
  COMPANY.md      # Company metadata (name, description, schema, authors, goals)
  README.md       # Human-readable overview
  LICENSE          # License file
  agents/          # One subdirectory per agent, each with an AGENTS.md
  skills/          # One subdirectory per skill, each with a SKILL.md
  teams/           # (Optional) Team definitions with TEAM.md files
```

## Adding a new company

1. **Create a directory** at the repo root with your company's slug (lowercase, hyphenated).
2. **Add a `COMPANY.md`** with YAML frontmatter containing at minimum:
   - `name`, `description`, `slug`
   - `schema: agentcompanies/v1`
   - `version` (semver)
   - `license`
   - `authors` (list with `name` field)
   - `goals` (list of strings)
3. **Add a `README.md`** that explains how the company works, its org chart, skills, and how to import it.
4. **Add a `LICENSE`** file.
5. **Define agents** in `agents/<agent-slug>/AGENTS.md`.
6. **Define skills** in `skills/<skill-slug>/SKILL.md`. Skills can be inline or reference an upstream repo.
7. **Test the import** locally:
   ```bash
   paperclipai company import /path/to/your-company --dry-run
   ```

## Improving an existing company

- Fix bugs, improve agent instructions, or add skills via pull request.
- Keep changes scoped to one company per PR when possible.
- If a company references upstream skills (e.g., gstack, superpowers), prefer updating the upstream repo and bumping the reference commit rather than forking the skill inline.

## Conventions

- Use `agentcompanies/v1` as the schema version.
- Agent slugs should match directory names (lowercase, hyphenated).
- Keep AGENTS.md files focused on the agent's role and cognitive mode.
- Skills should be single-purpose and composable.
- Include a getting-started section in your README with the `paperclipai company import` command.
- Reference the [Agent Companies spec](https://agentcompanies.io/specification) and [Paperclip repo](https://github.com/paperclipai/paperclip) in your README.

## Submitting a PR

1. Fork the repo and create a branch.
2. Make your changes.
3. Verify your company imports cleanly with `--dry-run`.
4. Open a pull request with a clear description of what the company does and why it's useful.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).
