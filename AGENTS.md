# Repository Guidelines

## Project Structure & Module Organization

This repository is a catalog of Paperclip agent companies. Each top-level company directory uses a lowercase, hyphenated slug such as `agentsys-engineering/` or `trail-of-bits-security/`.

Expected company layout:

```text
<company-slug>/
  COMPANY.md
  README.md
  LICENSE
  agents/<agent-slug>/AGENTS.md
  skills/<skill-slug>/SKILL.md
  teams/<team-slug>/TEAM.md
  images/
```

`COMPANY.md` contains Agent Companies metadata and must declare `schema: agentcompanies/v1`. Agent instructions live in `agents/**/AGENTS.md`; reusable workflows live in `skills/**/SKILL.md`; org charts and supporting media belong in `images/`.

## Build, Test, and Development Commands

There is no root build system. Validate packages with the Paperclip CLI:

```bash
npx paperclipai company import ./agentsys-engineering --dry-run
npx companies.sh add paperclipai/companies/agentsys-engineering
scripts/refresh-companies --check --repo obra/superpowers
```

Use `--dry-run` before submitting changes to a company. Use the `companies.sh` command when checking the published import path documented in the root `README.md`.
Use `scripts/refresh-companies --check` to inspect upstream skill drift. The script is report-only; it must not rewrite company packages.

## Coding Style & Naming Conventions

Use Markdown for all company, agent, skill, team, and contributor documentation. Keep prose direct and task-oriented. Prefer lowercase, hyphenated slugs for directories: `skills/code-review/SKILL.md`, `agents/staff-engineer/AGENTS.md`.

Keep `README.md` focused on what the company is and how to import it. Keep `AGENTS.md` focused on contributor or agent operating instructions. Do not duplicate long catalog listings between files.

## Testing Guidelines

For any company change, run an import dry-run against the affected directory. For structural edits, spot-check required files:

```bash
find ./agentsys-engineering -name 'COMPANY.md' -o -name 'AGENTS.md' -o -name 'SKILL.md'
```

When adding images, verify relative Markdown links render from the company README.

## Commit & Pull Request Guidelines

Recent commits use short, imperative summaries such as `Replace pnpm with npx for paperclipai CLI commands` and `Enforce CEO as root agent across all 16 companies`. Follow that style and keep one logical change per commit.

Pull requests should describe the company or package changed, summarize validation performed, and link related upstream sources or issues. Keep PRs scoped to one company where practical, especially when importing or refreshing upstream skills.

## Upstream Drift Reports

`.companies-refresh.yaml` lists upstream skill repositories tracked by the scheduled GitHub Actions workflow in `.github/workflows/refresh-companies.yml`. The workflow runs weekly, compares tracked sources with the latest semver tag or default branch HEAD, and reports drift without changing company files.

The workflow reports drift only. It writes a GitHub Actions summary and maintains one issue titled `Company upstream refresh report`. Do not treat that issue as an instruction to blindly mirror upstream; package refreshes are maintainer-authored changes that decide which new skills, support files, docs, and agent assignments belong in the company.

Paperclip import validation is intentionally separate in `.github/workflows/validate-company-packages.yml`. That pull request workflow starts one local Paperclip server and validates changed company packages with `paperclipai@2026.609.0`.
