---
name: land-and-deploy
description: >
  Merge PR, wait for deploy, verify production health. 10-step workflow:
  pre-flight, CI check, readiness gate, merge (respects merge queue), detect
  platform, wait for deploy, canary verification, revert option, deploy report.
  Auto-detects Fly, Render, Vercel, Netlify, Heroku, GitHub Actions.
metadata:
  sources:
    - kind: github-file
      repo: garrytan/gstack
      path: land-and-deploy/SKILL.md
      commit: f4bbfaa5bdfd2d6ce59541c2145432febde57fed
      attribution: Garry Tan
      license: MIT
      usage: referenced
---
