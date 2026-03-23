---
name: review
description: >
  Pre-landing PR review with two-pass checklist. Pass 1 critical: SQL safety,
  race conditions, LLM trust boundaries, enum completeness. Pass 2 informational:
  side effects, magic numbers, dead code, test gaps. Adversarial review auto-scaled
  by diff size. Scope drift detection.
metadata:
  sources:
    - kind: github-file
      repo: garrytan/gstack
      path: review/SKILL.md
      commit: f4bbfaa5bdfd2d6ce59541c2145432febde57fed
      attribution: Garry Tan
      license: MIT
      usage: referenced
---
