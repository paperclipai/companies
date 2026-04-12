# SupraWall Secured Marketing Company Template

This is a production-ready [Paperclip](https://paperclipai.com) company template that uses the [SupraWall plugin](https://github.com/wiserautomation/suprawall-plugins-) to secure all external API keys and credentials.

**Zero hardcoded credentials exist in this repository.**

Instead of storing long-lived OpenAI, GitHub, or Stripe keys in a `.env` file where any agent can access them, this template delegates credential management to the SupraWall Vault engine.

## How it works

1. An agent starts a task.
2. The agent asks SupraWall for permission to use a tool (e.g., "Twitter").
3. SupraWall verifies the agent's role (e.g., `marketing`).
4. SupraWall intercepts the HTTP request, injects the real Twitter API key at the network layer, and returns the response to the agent.
5. The agent **never sees the raw API key**, preventing credential theft via prompt injection.

## Quickstart

### 1. Install the Plugin

First, install the SupraWall Vault plugin:

```bash
paperclipai plugin install suprawall-vault
```

This will guide you through creating a free SupraWall dashboard account and will automatically generate your temporary API keys.

### 2. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Add the `SUPRAWALL_API_KEY` you received during the plugin installation.

### 3. Hire the Agents

This template comes with four preconfigured agents. Hire them via the CLI:

```bash
paperclipai hire agents/ceo.json
paperclipai hire agents/marketing.json
paperclipai hire agents/engineering.json
paperclipai hire agents/finance.json
```

## Built-in Role Policies

The SupraWall engine automatically maps the following default permissions based on the agent's `role` property:

| Agent Role | Granted Scopes |
| :--- | :--- |
| **ceo** | `read:all` |
| **marketing** | `linkedin`, `twitter`, `google_ads` |
| **engineering** | `github`, `supabase`, `vercel` |
| **finance** | `stripe` |

If a `marketing` agent tries to use the `stripe` tool, the SupraWall API will automatically block the request and log an audit event in your dashboard.

## Learn More

* [SupraWall Vault Documentation](https://docs.supra-wall.com/paperclip)
* [Paperclip Documentation](https://github.com/paperclipai/paperclip)
