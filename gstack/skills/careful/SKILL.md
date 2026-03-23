---
name: careful
description: >
  Warns before destructive commands (rm -rf, DROP TABLE, force-push, git reset
  --hard, kubectl delete, docker force-rm). Session-scoped. Exceptions for
  common temp dirs (node_modules, .next, __pycache__).
metadata:
  sources:
    - kind: github-file
      repo: garrytan/gstack
      path: careful/SKILL.md
      commit: f4bbfaa5bdfd2d6ce59541c2145432febde57fed
      attribution: Garry Tan
      license: MIT
      usage: referenced
---
