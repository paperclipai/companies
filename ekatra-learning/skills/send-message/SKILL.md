---
name: Send Message
slug: send-message
description: Sends a text message to a learner via WhatsApp (Twilio) or Telegram.
---

## What this skill does

Delivers a single text message to a user on WhatsApp or Telegram.

## Inputs

- `channel` (string): "whatsapp" or "telegram".
- `recipient` (string): Phone number (E.164) for WhatsApp, or chat ID for Telegram.
- `text` (string): The message body. Max 4096 characters.

## Secrets required

- WhatsApp: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM`
- Telegram: `TELEGRAM_BOT_TOKEN`

## WhatsApp delivery (Twilio)

POST to `https://api.twilio.com/2010-04-01/Accounts/{SID}/Messages.json`

```
From: whatsapp:{TWILIO_WHATSAPP_FROM}
To: whatsapp:{recipient}
Body: {text}
```

## Telegram delivery

POST to `https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage`

```json
{ "chat_id": "{recipient}", "text": "{text}" }
```

## Output

`{ "status": "sent", "message_id": "..." }` on success.
`{ "status": "error", "reason": "..." }` on failure.

## Error handling

- Twilio 21614 (not a WhatsApp user): log and skip, do not retry.
- Twilio 63038 (daily limit): log, alert Technology agent.
- Telegram 403 (blocked by user): log and remove from active learners.
- Network error: retry once after 5 seconds, then return error.
