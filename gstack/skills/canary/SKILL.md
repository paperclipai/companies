---
name: canary
description: >
  Post-deploy monitoring. Watches live app via headless browser for console
  errors, performance regressions, page failures, visual anomalies. Alert on
  deltas not absolutes, transient tolerance (2+ consecutive checks). Default
  10-minute monitoring window. Baseline capture mode.
metadata:
  sources:
    - kind: github-file
      repo: garrytan/gstack
      path: canary/SKILL.md
      commit: f4bbfaa5bdfd2d6ce59541c2145432febde57fed
      attribution: Garry Tan
      license: MIT
      usage: referenced
---
