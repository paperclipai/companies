# Software Factory Method

Portable [Paperclip](https://paperclip.ing) / Agent Companies package for running a reusable software factory with BMAD-inspired workflows.

This package is community-maintained and is not an official BMad Code or Paperclip template.

## What This Package Contains

- `20` agents covering leadership, product, architecture, delivery, QA, docs, support, and release.
- `53` skills, flattened to portable slug-based directories under `skills/`.
- A cleaned Paperclip extension manifest in `.paperclip.yaml` with runtime defaults only.

## What Was Intentionally Removed

This package does **not** ship with the original exported operational state.

Removed during normalization:

- original tenant-specific backlog and issue history
- recurring routines and schedules
- project/repo bindings tied to a single workspace
- attachment links and execution logs
- local filesystem paths and subscription-specific defaults

That is deliberate. A public company package should define the operating model, not leak a tenant's runtime history.

## Operating Model

The package is organized around a BMAD-style flow:

1. Discovery and product framing
2. Planning and requirements
3. Architecture and technical decomposition
4. Implementation by package or domain owner
5. QA and readiness review
6. Documentation, release, and follow-through

The agents are pre-wired around that flow:

- `ceo`, `orchestrator`, `cto`, `pm`, `analyst`, `cmo`
- `architect`, `backend`, `frontend`, `mobile`, `devcodex`, `devops`
- `qa`, `tea`, `security`, `releasemanager`
- `docsmemory`, `support`, `dataanalytics`, `uxdesigner`

## Skill Layout

The `skills/` directory was normalized to portable one-skill-per-slug folders:

- BMAD workflow skills such as `bmad-prd`, `bmad-quick-dev`, `bmad-create-story`, `bmad-check-implementation-readiness`
- utility/editorial skills such as `bmad-investigate`, `bmad-code-review`, `bmad-index-docs`
- Paperclip operational skills vendored locally, such as `paperclip`, `paperclip-create-agent`, `paperclip-dev`
- one company tone skill: `caveman`

Agent skill references were converted from export-specific ids like `local/<hash>/...` and `company/<uuid>/...` to stable shortnames.

## Import

Dry-run import with the Paperclip CLI:

```bash
paperclipai company import --from /path/to/software-factory-method --dry-run
```

Dry-run import with `companies.sh`:

```bash
npx companies.sh add /path/to/software-factory-method --dry-run
```

Live import:

```bash
paperclipai company import --from /path/to/software-factory-method
```

or

```bash
npx companies.sh add /path/to/software-factory-method
```

## Post-Import Setup

This package is intentionally repo-agnostic, so after import you should:

1. Create or attach your real project/repository inside Paperclip.
2. Point the working agents at the active repo/workspace.
3. Review runtime permissions, budgets, heartbeat intervals, and model settings.
4. Optionally trim the org chart if you want a smaller starting team.

## Notes

- `tasks/` and `projects/` were removed on purpose to keep the package public and reusable.
- `.paperclip.yaml` still contains Paperclip-specific runtime defaults. Review them before production use.
- The package ships with MIT licensing for publication convenience, but BMAD-related naming and attribution should remain descriptive rather than implying official endorsement.

## Attribution

This package preserves and adapts BMAD-derived workflows and skills for a Paperclip company-package shape.

- BMAD upstream: [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
- Paperclip ecosystem: [paperclipai/paperclip](https://github.com/paperclipai/paperclip)
- Paperclip companies catalog: [paperclipai/companies](https://github.com/paperclipai/companies)

## References

- [Paperclip](https://paperclip.ing)
- [Paperclip Docs](https://paperclip.ing/docs)
- [Agent Companies spec](https://github.com/paperclipai/paperclip/blob/master/docs/companies/companies-spec.md)
- [companies.sh](https://github.com/paperclipai/companies-tool)
