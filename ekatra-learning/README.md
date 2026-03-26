# Socrates Learning Bot

A WhatsApp and Telegram teaching bot that turns any topic into a micro-lesson and
quiz — delivered conversationally, one message at a time.

## What it does

A learner sends any topic: "explain photosynthesis", "what is compound interest",
"teach me SQL joins". The bot replies with 5 short chat messages (a micro-lesson),
then sends a 3-question quiz. No app to download. No account to create. Just a chat.

## The Company

| Agent | Role |
|-------|------|
| CEO | Qualifies leads, closes deals, sets company priorities |
| Marketing | Content marketing, prospect research, outreach |
| Learning | Generates lessons, delivers them, runs quizzes, tracks learners |
| Technology | Deploys the bot, monitors webhooks, handles incidents |

## Skills

| Skill | Used by |
|-------|---------|
| `generate-lesson` | Learning |
| `send-message` | Learning, Technology |
| `send-quiz` | Learning |
| `prospect-outreach` | CEO, Marketing |
| `deploy-bot` | Technology |

## Channels

- **WhatsApp** via Twilio (requires `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM`)
- **Telegram** via Bot API (requires `TELEGRAM_BOT_TOKEN`)

## Deploy

```bash
npx paperclipai company import . --yes
```

## License

MIT
