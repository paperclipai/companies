---
name: Deploy Bot
slug: deploy-bot
description: Deploys or redeploys the Socrates Learning Bot to Railway or Fly.io.
---

## What this skill does

Triggers a new deployment of the bot, runs a smoke test, and returns a deploy report.

## Inputs

- `platform` (string): "railway" or "fly". Default: "railway".
- `version` (string, optional): Git tag or commit SHA to deploy. Default: latest main.
- `run_smoke_test` (boolean): Whether to run a test lesson after deploy. Default: true.

## Secrets required

- `DEPLOY_TOKEN`: Railway API token or Fly.io auth token.

## Deploy steps

**Railway**:
1. POST to the Railway GraphQL API with the redeploy mutation.
2. Poll deployment status every 10 seconds until SUCCESS or FAILED (max 5 min).

**Fly.io**:
1. Call the Fly Machines API to trigger a new deployment.
2. Poll for healthy status.

## Smoke test

After deploy, send a test session:
- Topic: "addition" (simple, fast to generate).
- Expected: all 5 lesson messages arrive within 30 seconds, quiz sends.
- Pass condition: all 5 messages received, no error codes.

## Output

```json
{
  "platform": "railway",
  "version": "v1.4.2",
  "deploy_time_seconds": 47,
  "smoke_test": "pass",
  "url": "https://socrates-bot.up.railway.app",
  "rollback_command": "railway redeploy --deployment prev"
}
```

## On failure

If smoke test fails, automatically trigger a rollback to the previous deployment
and return "smoke_test": "fail" with the error details.
