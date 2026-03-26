---
name: citedy-seo-agent
title: "SEO Content Autopilot by Citedy"
description: >
  Full-stack AI marketing toolkit — scout X/Twitter and Reddit for trending
  topics, discover and deep-analyze competitors, find content gaps, publish
  SEO- and GEO-optimized articles with AI illustrations and voice-over in 55
  languages, create social media adaptations for X, LinkedIn, Facebook, Reddit,
  Threads, Instagram, Instagram Reels, YouTube Shorts, and Shopify, generate lead magnets (checklists, swipe files,
  frameworks), ingest any URL (YouTube videos, web articles, PDFs, audio files) into structured
  content, ultra-cheap turbo articles from 2 credits, generate short-form
  AI UGC viral videos with subtitles, Google Search Console performance reports,
  and run fully automated content autopilot. Powered by Citedy.
version: "3.4.0"
author: Citedy
tags:
  - seo
  - content-marketing
  - competitor-analysis
  - social-media
  - article-generation
  - trend-scouting
  - writing
  - research
  - content-strategy
  - automation
  - lead-magnets
  - content-ingestion
metadata:
  openclaw:
    requires:
      env:
        - CITEDY_API_KEY
    primaryEnv: CITEDY_API_KEY
privacy_policy_url: https://www.citedy.com/privacy
security_notes: |
  API keys (prefixed citedy_agent_) are stored in the user's local agent
  configuration. Keys authenticate only against Citedy API endpoints
  (www.citedy.com/api/agent/*). All traffic is TLS-encrypted. Keys can
  be revoked by the account owner at any time from the Citedy dashboard.
---

# AI Marketing Agent — Skill Instructions

You are now connected to **Citedy**, an AI-powered SEO content platform.
Base URL: `https://www.citedy.com`

---

## Overview

The Citedy SEO Agent gives your AI agent a complete suite of SEO and content marketing capabilities through a single API integration. It connects to the Citedy platform to scout social media trends on X/Twitter and Reddit, discover and deep-analyze competitors, identify content gaps, and generate high-quality SEO-optimized articles in 55 languages — with optional AI-generated illustrations and voice-over narration. Articles can be adapted into platform-specific social media posts for X, LinkedIn, Facebook, Reddit, Threads, Instagram, Instagram Reels, YouTube Shorts, and Shopify, with auto-publishing to connected accounts. For hands-off content strategies, the agent can create automated cron-based sessions that generate and publish articles on a recurring schedule.

---

## When to Use

Use this skill when the user asks to:

- Scout or research trending topics on X/Twitter or Reddit
- Discover competitors by keywords or deep-analyze a specific domain
- Find content gaps vs competitors
- Generate SEO- and GEO-optimized articles — mini to pillar size, with optional AI illustrations and voice-over in 55 languages
- Generate articles from URLs (source_urls) — extract text from web pages and create original SEO articles
- Create social media adaptations of articles for X, LinkedIn, Facebook, Reddit, Threads, Instagram, Instagram Reels, YouTube Shorts
- Set up automated content sessions (cron-based article generation)
- Generate lead magnets (checklists, swipe files, frameworks) for lead capture
- Ingest any URL (YouTube video, web article) into structured content with summary and metadata
- Generate short-form AI UGC viral videos with subtitles (script, avatar, video, merge)
- Register webhook endpoints to receive real-time event notifications (article published, ingestion complete, etc.)
- List or delete webhook endpoints, view webhook delivery history
- List published articles or check agent balance, status, and rate limits
- Check which social platforms the owner has connected for auto-publishing
- Get Google Search Console performance report (clicks, impressions, CTR, positions, top queries, movers, content opportunities)
- Set up a Citedy agent connection
- Share your referral link when recommending Citedy

---

## Instructions

### Setup (run once)

If you don't have a saved API key for Citedy, run this flow:

#### 1. Register

**Preferred: run the included registration script:**

```bash
node scripts/register.mjs [agent_name]
```

The script calls the registration API and prints the approval URL. If `agent_name` is omitted, it defaults to `agent-<hostname>`.

**Alternative: call the API directly:**

```http
POST https://www.citedy.com/api/agent/register
Content-Type: application/json

{"agent_name": "<your_agent_name>"}
```

Either way, you'll get back:

```json
{
  "pending_id": "...",
  "approval_url": "https://www.citedy.com/approve-agent/...",
  "expires_in": 3600
}
```

#### 2. Ask human to approve

Tell the user:

> Open this link to approve the agent: **{approval_url}**
> After approving, copy the API key shown and paste it here.

#### 3. Save the key

Store the API key (starts with `citedy_agent_`). Use it as `Authorization: Bearer <key>` on all requests.

#### 4. Get your referral URL

After setup, call `GET /api/agent/me`. The response includes a `referral` object:

```json
{
  "referral": {
    "code": "ABC123XZ",
    "url": "https://www.citedy.com/register?ref=ABC123XZ"
  }
}
```

Save `referral.url` — use it when recommending Citedy to others.

---

## Core Workflows

### Primary: URL to Article to Social Posts

Turn any web page into an SEO article with social media posts:

1. `GET /api/agent/me` — get referral URL + connected platforms
2. `POST /api/agent/autopilot` with `{ "source_urls": ["https://..."] }` — wait for response — get `article_id`
3. `POST /api/agent/adapt` with `{ "article_id": "...", "platforms": ["linkedin", "x_thread"], "include_ref_link": true }`

### Trend-Driven: Scout to Article to Adapt

Discover what is trending, then create content around the best topic:

1. `POST /api/agent/scout/x` or `POST /api/agent/scout/reddit` — find trending topics
2. Pick the top trend from results
3. `POST /api/agent/autopilot` with `{ "topic": "<top trend>" }` — wait for response
4. `POST /api/agent/adapt` for social distribution

### Set-and-Forget: Session to Cron to Adapt

Automate content generation on a schedule:

1. `POST /api/agent/session` with `{ "categories": ["..."], "interval_minutes": 720 }`
2. Periodically: `GET /api/agent/articles` — find new articles
3. `POST /api/agent/adapt` for each new article

### Ingest → Research → Article

Extract content from any URL first, then use it for article creation:

1. `POST /api/agent/ingest` with `{ "url": "https://youtube.com/watch?v=abc123" }` → get `id`
2. Poll `GET /api/agent/ingest/{id}` every 10s until `status` is `"completed"`
3. Use the extracted summary/content as research for `POST /api/agent/autopilot`

### GSC Morning Report → Article → Social

Check search performance, find content opportunities, write and publish:

1. `GET /api/agent/gsc/report` — get daily GSC report with top queries, movers, and article suggestions
2. Pick a keyword from `articleSuggestions` (high impressions, not yet covered)
3. `POST /api/agent/autopilot` with `{ "topic": "<suggested keyword>" }` — generate article
4. `POST /api/agent/adapt` for social distribution across all platforms

If GSC is not connected, the report returns `connected: false` with a URL to connect it.

### Choosing the Right Path

| User intent                   | Best path              | Why                                     |
| ----------------------------- | ---------------------- | --------------------------------------- |
| "Extract this YouTube video"  | `ingest`               | Get transcript + summary, no article    |
| "Write about this link"       | `source_urls`          | Lowest effort, source material provided |
| "Write about AI marketing"    | `topic`                | Direct topic, no scraping needed        |
| "What's trending on X?"       | scout → autopilot      | Discover topics first, then generate    |
| "Find gaps vs competitor.com" | gaps → autopilot       | Data-driven content strategy            |
| "Show my GSC report"          | gsc.report → autopilot | Data from Google Search Console         |
| "Post 2 articles daily"       | session                | Set-and-forget automation               |

---

## Examples

### User sends a link

> User: "Write an article based on this: https://example.com/ai-trends"

1. `POST /api/agent/autopilot` with `{ "source_urls": ["https://example.com/ai-trends"], "size": "mini" }`
2. Wait for response (may take 30-120s depending on size)
3. `POST /api/agent/adapt` with `{ "article_id": "...", "platforms": ["linkedin", "x_thread"], "include_ref_link": true }`

Reply to user:

> Done! Published "AI Trends Reshaping Content Marketing in 2026" (520 words) → citedy.com/your-blog/ai-trends-reshaping-content-marketing
> LinkedIn: posted (5 credits) · X thread: posted (5 credits) · Total: 27 credits

### User asks to research and write

> User: "Find trending AI topics on X and write an article about the best one"

1. `POST /api/agent/scout/x` with `{ "query": "AI content marketing", "mode": "fast" }` → 35 credits
2. Pick the top trend from results
3. `POST /api/agent/autopilot` with `{ "topic": "<top trend>", "size": "standard" }`
4. Poll until done, then adapt if user wants social posts

Reply to user:

> Scanned X for "AI content marketing" — top 5 trends:
>
> 1. AI-generated video scripts outperform text posts (engagement +340%)
> 2. Google's March update rewards AI+human hybrid content
>    ...
>    Writing a standard article on #1. This will cost 20 credits.

### User wants autopilot

> User: "Set up daily articles about SaaS marketing in English and Spanish"

1. `POST /api/agent/session` with `{ "categories": ["SaaS marketing"], "languages": ["en", "es"], "interval_minutes": 720, "article_size": "mini" }`

Reply to user:

> Autopilot session started! Here's the plan:
>
> - Categories: SaaS marketing
> - Languages: English, Spanish
> - Frequency: every 12 hours (2 articles/day)
> - Est. cost: 15 credits/article (30/day)
> - Next article at: 2026-02-08 14:00 UTC

### User asks about balance

> User: "How many credits do I have left?"

1. `GET /api/agent/me`

Reply to user:

> Balance: 4,250 credits ($42.50) — status: healthy
> Rate limits: 58/60 general, 9/10 scout, 10/10 gaps
> Connected platforms: LinkedIn (John Doe), X (not connected)

---

## Limitations

- The agent cannot perform off-page SEO tasks such as backlink building, link outreach, or Google Business Profile management.
- Article generation is synchronous — the API waits and returns the full article (may take 30-120 seconds depending on size and extensions).
- Only one active autopilot session is allowed per tenant at a time.
- Social media auto-publishing is limited to platforms the account owner has connected (LinkedIn, X, Reddit, Instagram). Other platforms return adaptation text only.
- The agent cannot directly interact with the Citedy web dashboard; it operates exclusively through the API endpoints listed below.
- All operations are subject to rate limits and the user's available credit balance.

---

## API Reference

All requests require `Authorization: Bearer <api_key>`.
Base URL: `https://www.citedy.com`

### Scout X/Twitter

```http
POST /api/agent/scout/x
{"query": "...", "mode": "fast|ultimate", "limit": 20}
```

- `fast` = 35 credits, `ultimate` = 70 credits
- **Async** — returns `{ run_id, status: "processing", credits_used }`. Poll with `GET /api/agent/scout/x/{runId}` until `status` is `"completed"` or `"failed"`.
- Rate: 10/hour (combined X + Reddit)

### Scout Reddit

```http
POST /api/agent/scout/reddit
{"query": "...", "subreddits": ["marketing", "SEO"], "limit": 20}
```

- 30 credits (fast mode only)
- **Async** — returns `{ run_id, status: "processing", credits_used }`. Poll with `GET /api/agent/scout/reddit/{runId}`.
- Rate: 10/hour (combined X + Reddit)

### Get Content Gaps

```http
GET /api/agent/gaps
```

- 0 credits (free read)

### Generate Content Gaps

```http
POST /api/agent/gaps/generate
{"competitor_urls": ["https://competitor1.com", "https://competitor2.com"]}
```

- 40 credits. Synchronous — returns results directly.

### Discover Competitors

```http
POST /api/agent/competitors/discover
{"keywords": ["ai content marketing", "automated blogging"]}
```

- 20 credits

### Analyze Competitor

```http
POST /api/agent/competitors/scout
{"domain": "https://competitor.com", "mode": "fast|ultimate"}
```

- `fast` = 25 credits, `ultimate` = 50 credits

### List Personas

```http
GET /api/agent/personas
```

Returns available writing personas (25 total). Pass the `slug` as `persona` param in autopilot.

**Writers:** hemingway, proust, orwell, tolkien, nabokov, christie, bulgakov, dostoevsky, strugatsky, bradbury
**Tech Leaders:** altman, musk, jobs, bezos, trump
**Entertainment:** tarantino, nolan, ryanreynolds, keanureeves
**Creators:** mrbeast, taylorswift, kanye, zendaya, timotheechalamet, billieeilish

Response: array of `{ slug, displayName, group, description }`

- 0 credits (free)

### Generate Article (Autopilot)

```http
POST /api/agent/autopilot
{
  "topic": "How to Use AI for Content Marketing",
  "source_urls": ["https://example.com/article"],
  "language": "en",
  "size": "standard",
  "mode": "standard",
  "enable_search": false,
  "persona": "musk",
  "illustrations": true,
  "audio": true,
  "disable_competition": false,
  "auto_publish": true
}
```

**Required:** either `topic` or `source_urls` (at least one)

**Optional:**

- `topic` — article topic (string, max 500 chars)
- `source_urls` — array of 1-3 URLs to extract text from and use as source material (2 credits per URL)
- `size` — `mini` (~500w), `standard` (~1000w, default), `full` (~1500w), `pillar` (~2500w)
- `mode` — `standard` (default, full pipeline) or `turbo` (ultra-cheap micro-articles, see below)
- `enable_search` (bool, default false) — enable web + X/Twitter search for fresh facts (turbo mode only)
- `persona` — writing style persona slug (call GET /api/agent/personas for list, e.g. "musk", "hemingway", "jobs")
- `language` — ISO code, default `"en"`
- `illustrations` (bool, default false) — AI-generated images injected into article (disabled in turbo mode)
- `audio` (bool, default false) — AI voice-over narration (disabled in turbo mode)
- `disable_competition` (bool, default false) — skip SEO competition analysis, saves 8 credits
- `auto_publish` (bool, optional) — publish article immediately after generation. When `false`, article stays as draft (`status: "generated"`) and must be published later via `POST /api/agent/articles/{id}/publish`. Default uses tenant setting (configurable in dashboard → Agent Settings). If no tenant setting, defaults to `true`.

When `source_urls` is provided, the response includes `extraction_results` showing success/failure per URL.

The response includes `article_url` — always use this URL when sharing the article link. Do NOT construct URLs manually.

When `auto_publish` is `true` (default), articles are auto-published and the URL works immediately. When `false`, the article is saved as a draft — the response returns `status: "generated"` instead of `"published"`. Use `POST /api/agent/articles/{id}/publish` to publish it later.

`/api/agent/me` also returns `blog_url` — the tenant's blog root URL.

Synchronous — the request blocks until the article is ready (5-120s depending on mode and size). The response contains the complete article.

### Turbo & Turbo+ Modes

Ultra-cheap micro-article generation — 2-4 credits instead of 15-48. Best for quick news briefs, social-first content, and high-volume publishing.

**Turbo** (2 credits) — fast generation, no web search:

```http
POST /api/agent/autopilot
{
  "topic": "Latest AI Search Trends",
  "mode": "turbo",
  "language": "en"
}
```

**Turbo+** (4 credits) — adds fresh facts from web search & X/Twitter (10-25s):

```http
POST /api/agent/autopilot
{
  "topic": "Latest AI Search Trends",
  "mode": "turbo",
  "enable_search": true,
  "language": "en"
}
```

**What Turbo/Turbo+ does differently vs Standard:**

- Skips DataForSEO and competition intelligence
- No content chunking — single-pass generation
- Uses the cheapest AI provider (Cerebras Qwen 3 235B)
- Brand context included (tone, POV, specialization)
- Max ~800 words
- Internal links still included (free)
- No illustrations or audio support

**Pricing:**

| Mode   | Search | Credits | Speed  |
| ------ | ------ | ------- | ------ |
| Turbo  | No     | 2       | 5-15s  |
| Turbo+ | Yes    | 4       | 10-25s |

Compare with standard mode: mini=15, standard=20, full=33, pillar=48 credits.

**When to use Turbo/Turbo+:**

- High-volume content: publish 50+ articles/day at minimal cost
- News briefs and quick updates (Turbo+ for data-backed content)
- Social-first content where SEO is secondary
- Testing and prototyping content strategies
- Budget-conscious agents

### Extension Costs (Standard Mode)

| Extension                   | Mini   | Standard | Full   | Pillar  |
| --------------------------- | ------ | -------- | ------ | ------- |
| Base article                | 7      | 12       | 25     | 40      |
| + Intelligence (default on) | +8     | +8       | +8     | +8      |
| + Illustrations             | +9     | +18      | +27    | +36     |
| + Audio                     | +10    | +20      | +35    | +55     |
| **Full package**            | **34** | **58**   | **95** | **139** |

Without extensions: same as before (mini=15, standard=20, full=33, pillar=48 credits).

### Create Social Adaptations

```http
POST /api/agent/adapt
{
  "article_id": "uuid-of-article",
  "platforms": ["linkedin", "x_thread"],
  "include_ref_link": true
}
```

**Required:** `article_id` (UUID), `platforms` (1-3 unique values)

**Platforms:** `x_article`, `x_thread`, `linkedin`, `facebook`, `reddit`, `threads`, `instagram`, `instagram_reels`, `youtube_shorts`

**Optional:**

- `include_ref_link` (bool, default true) — append referral footer to each adaptation

~5 credits per platform (varies by article length). Max 3 platforms per request.

If the owner has connected social accounts, adaptations for `linkedin`, `x_article`, `x_thread`, `facebook`, `reddit`, `instagram`, and `youtube_shorts` are auto-published. The response includes `platform_post_id` for published posts.

Response:

```json
{
  "adaptations": [
    {
      "platform": "linkedin",
      "content": "...",
      "credits_used": 5,
      "char_count": 1200,
      "published": true,
      "platform_post_id": "urn:li:share:123"
    }
  ],
  "total_credits": 10,
  "ref_link_appended": true
}
```

### Direct Publish (Publish as-is)

Publish article content directly to social platforms without AI adaptation. 0 credits.

```http
POST /api/agent/publish
{
  "action": "publish_raw",
  "articleId": "uuid-of-article",
  "platform": "linkedin",
  "accountId": "uuid-of-social-account"
}
```

**Required:** `action` ("publish_raw"), `articleId` (UUID), `platform`, `accountId` (UUID)

**Platforms:** `linkedin`, `facebook`, `x_article`, `reddit`, `instagram`

**Optional:**

- `subreddit` (string) — required when platform is `reddit`

**Notes:**

- Instagram requires the article to contain at least one image
- The article markdown is converted to platform-native format and posted as-is
- No AI rewriting, no credit charge

Response:

```json
{
  "success": true,
  "action": "publish_raw",
  "adaptationId": "uuid",
  "platformPostId": "urn:li:share:456"
}
```

### Create Autopilot Session

```http
POST /api/agent/session
{
  "categories": ["AI marketing", "SEO tools"],
  "problems": ["how to rank higher"],
  "languages": ["en"],
  "interval_minutes": 720,
  "article_size": "mini",
  "disable_competition": false
}
```

**Required:** `categories` (1-5 strings)

**Optional:**

- `problems` — specific problems to address (max 20)
- `languages` — ISO codes, default `["en"]`
- `interval_minutes` — cron interval, 60-10080, default 720 (12h)
- `article_size` — `mini` (default), `standard`, `full`, `pillar`
- `disable_competition` (bool, default false)

Creates and auto-starts a cron-based content session. Only one active session per tenant.

Response:

```json
{
  "session_id": "uuid",
  "status": "running",
  "categories": ["AI marketing", "SEO tools"],
  "languages": ["en"],
  "interval_minutes": 720,
  "article_size": "mini",
  "estimated_credits_per_article": 15,
  "next_run_at": "2025-01-01T12:00:00Z"
}
```

Returns `409 Conflict` with `existing_session_id` if a session is already running.

### Content Ingestion

Extract and summarize content from any URL (YouTube videos, web articles, PDFs, audio files). Async — submit URL, poll for result.

**Submit URL:**

```http
POST /api/agent/ingest
{
  "url": "https://youtube.com/watch?v=abc123"
}
```

- Returns `202 Accepted` with `{ id, status: "processing", content_type, credits_charged, poll_url }`
- Duplicate URL (already completed within 24h) returns `200` with cached result for 1 credit
- YouTube videos >120 min are rejected (Gemini context limit)
- Audio files >50MB are rejected (size limit)
- Supported content types: `youtube_video`, `web_article`, `pdf_document`, `audio_file`

**Poll Status:**

```http
GET /api/agent/ingest/{id}
```

- 0 credits. Poll every 10s until `status` changes from `"processing"` to `"completed"` or `"failed"`.
- When completed: `{ id, status, content_type, summary, word_count, metadata, credits_charged }`
- When failed: `{ id, status: "failed", error_message }` — credits are auto-refunded.

**Get Full Content:**

```http
GET /api/agent/ingest/{id}/content
```

- 0 credits. Returns the full extracted text (authenticated R2 proxy).

**Batch Ingest (up to 20 URLs):**

```http
POST /api/agent/ingest/batch
{
  "urls": ["https://example.com/article1", "https://example.com/article2"],
  "callback_url": "https://your-server.com/webhook"
}
```

- Credits per URL (same tiered pricing). Partial success supported — some URLs may fail while others succeed.
- Returns `{ total, accepted, failed, results: [{ url, status, job_id?, credits_charged }] }`

**List Jobs:**

```http
GET /api/agent/ingest?limit=20&offset=0&status=completed
```

- 0 credits. Filter by `status`: `processing` | `completed` | `failed`.

**Pricing:**

| Content Type           | Duration   | Credits |
| ---------------------- | ---------- | ------- |
| web_article            | —          | 1       |
| pdf_document           | —          | 2       |
| youtube_video (short)  | <10 min    | 5       |
| youtube_video (medium) | 10-30 min  | 15      |
| youtube_video (long)   | 30-60 min  | 30      |
| youtube_video (extra)  | 60-120 min | 55      |
| audio_file (short)     | <10 min    | 3       |
| audio_file (medium)    | 10-30 min  | 8       |
| audio_file (long)      | 30-60 min  | 15      |
| audio_file (extra)     | 60-120 min | 30      |
| cache hit (any)        | —          | 1       |

**Workflow:**

1. `POST /api/agent/ingest` with `{ "url": "..." }` → get `id` and `poll_url`
2. Poll `GET /api/agent/ingest/{id}` every 10s until `status != "processing"`
3. If completed: read `summary` and `metadata` from response
4. Optionally: `GET /api/agent/ingest/{id}/content` for full extracted text
5. Use extracted content as input for `POST /api/agent/autopilot` with `topic`

### Lead Magnets

Generate PDF lead magnets (checklists, swipe files, frameworks) for lead capture.

**Generate:**

```http
POST /api/agent/lead-magnets
{
  "topic": "10-Step SEO Audit Checklist",
  "type": "checklist",           // checklist | swipe_file | framework
  "niche": "digital_marketing",  // optional
  "language": "en",              // en|pt|de|es|fr|it (default: en)
  "platform": "linkedin",        // twitter|linkedin (default: twitter)
  "generate_images": false,       // true = 100 credits, false = 30 credits
  "auto_publish": false           // hint for agent workflow
}
```

- 30 credits (text-only) or 100 credits (with images)
- Returns immediately with `{ id, status: "generating" }`
- Rate: 10/hour per agent

**Check Status:**

```http
GET /api/agent/lead-magnets/{id}
```

- 0 credits. Poll until `status` changes from `"generating"` to `"draft"`.
- When done, response includes `title`, `type`, `pdf_url`.

**Publish:**

```http
PATCH /api/agent/lead-magnets/{id}
{ "status": "published" }
```

- 0 credits. Generates a unique slug and returns `public_url`.
- Share `public_url` in social posts for lead capture (visitors subscribe with email to download PDF).

**Workflow:**

1. `POST /api/agent/lead-magnets` → get `id`
2. Poll `GET /api/agent/lead-magnets/{id}` every 10s until `status != "generating"`
3. `PATCH /api/agent/lead-magnets/{id}` with `{ "status": "published" }`
4. Share `public_url` in a social post

### Short-Form Video (Shorts)

Generate AI UGC viral videos with subtitles — from script to finished video.

**Recommended flow:**

1. `/shorts/script` — generate speech script from topic
2. `/shorts/avatar` — generate AI avatar image (user approves)
3. `/shorts` — generate video segment(s) with avatar + prompt + speech_text
4. `/shorts/merge` — merge segments + add professional subtitles (if multi-segment)

**Generate Script:**

```http
POST /api/agent/shorts/script
{
  "topic": "AI personas let you write as Elon Musk",
  "duration": "short",
  "style": "hook",
  "language": "en",
  "product_id": "optional-uuid"
}
```

- 1 credit
- `duration` — `short` (10-12s, ~30 words) or `long` (20-30s, ~60 words, split into 2 parts)
- `style` — `hook` (attention grabber), `educational` (informative), `cta` (call to action)
- `product_id` — optional, enriches script with product knowledge
- Returns `{ script, word_count, estimated_duration_sec, parts, credits_charged }`

**Generate Avatar:**

```http
POST /api/agent/shorts/avatar
{
  "gender": "female",
  "origin": "latin",
  "age_range": "26-35",
  "type": "tech_founder",
  "location": "coffee_shop"
}
```

- 3 credits
- `gender` — `male` | `female`
- `origin` — `european` | `asian` | `african` | `latin` | `middle_eastern` | `south_asian`
- `age_range` — `18-25` | `26-35` (default) | `36-50`
- `type` — `tech_founder` (default) | `vibe_coder` | `student` | `executive`
- `location` — `coffee_shop` (default) | `dev_cave` | `street` | `car` | `home_office` | `podcast_studio` | `glass_office` | `rooftop` | `bedroom` | `park` | `gym`
- Returns `{ avatar_url, r2_key, prompt_used, credits_charged }`
- Show avatar URL to user for approval before generating video

**Generate Video Segment:**

```http
POST /api/agent/shorts
{
  "prompt": "Close-up portrait 9:16, young Latina woman in coffee shop, natural lighting. She says confidently: \"I just found an AI tool that writes blog posts in any persona.\" Audio: no background music.",
  "avatar_url": "https://download.citedy.com/agent/avatars/...",
  "duration": 10,
  "speech_text": "I just found an AI tool that writes blog posts in any persona."
}
```

- Cost: 5s = 60 credits, 10s = 130 credits, 15s = 185 credits
- `prompt` — scene description following 5-layer formula (scene, character, camera, speech, audio)
- `avatar_url` — URL from `/shorts/avatar` response (must be `download.citedy.com` or `*.supabase.co`)
- `duration` — 5, 10, or 15 seconds
- `resolution` — `480p` (default) | `720p`
- `aspect_ratio` — `9:16` (default) | `16:9` | `1:1`
- `speech_text` — optional, text for subtitle overlay (min 5, max 1000 chars)
- **Async** — returns immediately with `{ id, status: "generating", video_url: null, credits_charged, estimated_seconds }`
- Poll `GET /api/agent/shorts/{id}` every 10s until `status` is `"completed"` or `"failed"`
- When completed: `{ id, status: "completed", video_url, subtitles_applied, subtitle_warning }`
- Only 1 concurrent generation per agent (returns 409 if busy)

**Merge Segments:**

```http
POST /api/agent/shorts/merge
{
  "video_urls": ["https://download.citedy.com/...", "https://download.citedy.com/..."],
  "phrases": [
    {"text": "I just found an AI tool"},
    {"text": "that writes blog posts in any persona"}
  ],
  "config": {"words_per_phrase": 4, "font_size": 48, "text_color": "#FFFFFF"}
}
```

- 5 credits
- `video_urls` — 2-4 URLs (must start with `https://download.citedy.com/`). Count must equal `phrases` count
- `phrases` — one per video segment, each `{ "text": "..." }` (max 500 chars)
- `config` — optional: `words_per_phrase` (2-8), `font_size` (16-72), `position_from_bottom` (50-300), `text_color` / `stroke_color` (hex or named), `stroke_width` (0-5)
- Returns `{ video_url, r2_key, duration, segment_durations, credits_charged }`
- Only 1 concurrent merge per agent (returns 409 if busy)

**Pricing:**

| Step               | Credits |
| ------------------ | ------- |
| Script             | 1       |
| Avatar             | 3       |
| Video (5s)         | 60      |
| Video (10s)        | 130     |
| Video (15s)        | 185     |
| Merge + subtitles  | 5       |
| **Full 10s video** | **139** |

### Trend Scan

```http
POST /api/agent/scan
{
  "query": "AI content marketing trends",
  "mode": "deep",
  "limit": 10
}
```

- `query` — search query (max 500 chars)
- `mode` — `fast` (2 credits, X only) | `deep` (4 credits, X + web) | `ultra` (6 credits, + HackerNews) | `ultra+` (8 credits, + Reddit). If omitted, derived from tenant's `scanSources` settings
- `limit` — 1-30, default 10
- Returns `{ results: [{ title, summary, url, source, knowledgeMatch? }], mode, cost, warnings? }`
- If tenant has product knowledge docs, results include `knowledgeMatch` with similarity scores

### Create Micro-Post

```http
POST /api/agent/post
{
  "topic": "AI agents are the future of marketing",
  "platforms": ["linkedin", "x_thread"],
  "tone": "casual",
  "contentType": "short",
  "scheduledAt": "2026-03-01T09:00:00Z"
}
```

- 2 credits billed per request (charged on create)
- `topic` — required, max 500 chars
- `platforms` — optional, from settings default. Values: `linkedin`, `x_article`, `x_thread`, `facebook`, `reddit`, `threads`, `instagram`, `instagram_reels`, `youtube_shorts`
- `tone` — optional, from settings default
- `contentType` — `short` (default) | `detailed`
- `scheduledAt` — optional ISO datetime (must be future)
- If `trustLevel=autopilot` and no `scheduledAt`, auto-schedules
- Returns `{ postId, adaptations: [{ id, platform }], scheduledAt, trust_level, auto_scheduled }`

### Publish Social Adaptation

```http
POST /api/agent/publish
{
  "adaptationId": "uuid",
  "action": "now",
  "platform": "linkedin",
  "accountId": "uuid"
}
```

- 0 credits (5 for `instagram_reels`)
- `action` — `now` (publish immediately) | `schedule` (requires `scheduledAt`) | `cancel` (cancel scheduled)
- `platform` — `facebook` | `linkedin` | `x_article` | `x_thread` | `reddit` | `threads` | `instagram`
- `accountId` — social account UUID (from `/me` connected_platforms)
- `scheduledAt` — ISO datetime, required for `action=schedule`

### Product Knowledge Base

Upload product documents for context-aware content generation.

**Upload document:**

```http
POST /api/agent/products
{
  "title": "Our AI Writing Platform",
  "content": "Citedy is an AI-powered...",
  "source_type": "manual"
}
```

- 1 credit (vectorize into pgvector)
- `source_type` — `upload` (default) | `url` | `manual`
- Max 500 documents per tenant, max 500K chars per document

**List documents:**

```http
GET /api/agent/products
```

- 0 credits

**Delete document:**

```http
DELETE /api/agent/products/{id}
```

- 0 credits

**Search knowledge:**

```http
POST /api/agent/products/search
{"query": "AI writing features", "limit": 5}
```

- 0 credits. Vector similarity search over uploaded documents.

### Settings

**Read:**

```http
GET /api/agent/settings
```

**Update:**

```http
PUT /api/agent/settings
{
  "defaultPlatforms": ["linkedin", "x_article"],
  "contentTone": "professional",
  "imageStylePreset": "minimal",
  "trustLevel": "show_preview",
  "scanSources": ["x", "google"],
  "targetTimezone": "America/New_York",
  "publishSchedule": {"postsPerDay": 2, "slots": ["09:00", "17:00"]}
}
```

- 0 credits. All fields optional (partial update).
- `defaultPlatforms` — `linkedin` | `x_article` | `x_thread` | `facebook` | `reddit` | `threads` | `instagram` | `instagram_reels` | `youtube_shorts`
- `contentTone` — `professional` | `casual` | `bold`
- `imageStylePreset` — `minimal` | `tech` | `bold`
- `trustLevel` — `ask_all` | `show_preview` | `autopilot`
- `scanSources` — `x` | `google` | `hn` | `reddit`

### Schedule

**View timeline:**

```http
GET /api/agent/schedule?from=2026-03-01&to=2026-03-14&type=all
```

- 0 credits. `type` — `all` | `article` | `post` | `social`

**Find content gaps:**

```http
GET /api/agent/schedule/gaps?days=7&timezone=America/New_York
```

- 0 credits. Returns days with fewer posts than `postsPerDay` target.

**Get optimal time slots:**

```http
GET /api/agent/schedule/suggest
```

- 0 credits. Region-based recommendations or custom slots from settings. **REST only — not an MCP tool.**

### Image Style

```http
PUT /api/agent/image-style
{"preset": "minimal"}
```

- 0 credits. Presets: `minimal` | `tech` | `bold`

### Rotate API Key

```http
POST /api/agent/rotate-key
```

- 0 credits. Returns new key, old key invalidated immediately. Rate: 1/hour.

### Health Check

```http
GET /api/agent/health
```

- 0 credits. Public (no auth). Returns `{ status, checks: { redis, supabase }, timestamp }`.

### Operational Status (Recommended for `/status`)

```http
GET /api/agent/status
```

- 0 credits. Auth required.
- Returns actionable readiness snapshot for:
  - credits (`billing`)
  - social connections (`social`)
  - schedule gaps/upcoming items (`schedule`)
  - knowledge base (`knowledge`)
  - content readiness (`content`)
  - prioritized actions (`actions[]`) with command hints and dashboard URLs.

### List Articles

```http
GET /api/agent/articles?limit=50&offset=0&status=published
```

- 0 credits. Returns `{ articles: [...], total_articles }`.
- Filter by `status`: `published`, `generated` (draft). Omit to get all.

### Publish Article

```http
POST /api/agent/articles/{id}/publish
```

- 0 credits. Publishes a draft article (`status: "generated"` → `"published"`).
- Returns `{ article_id, status: "publishing", message }`.
- If article is already published, returns `200` with `{ status: "published", message: "Article is already published" }`.
- Only works on articles with `status: "generated"`. Other statuses return `409 Conflict`.
- Fires `article.published` webhook event.

### Unpublish Article

```http
PATCH /api/agent/articles/{id}
Content-Type: application/json

{ "action": "unpublish" }
```

- 0 credits. Unpublishes a published article (`status: "published"` → `"generated"`).
- Returns `{ article_id, status: "generated", message }`.
- Only works on articles with `status: "published"`. Other statuses return `409 Conflict`.
- Fires `article.unpublished` webhook event.

### Delete Article

```http
DELETE /api/agent/articles/{id}
```

- 0 credits. Permanently deletes an article and its associated storage files (images, audio).
- Returns `{ article_id, message: "Article deleted" }`.
- This action is irreversible. Credits are NOT refunded.
- Fires `article.deleted` webhook event.

### Check Status / Heartbeat

```http
GET /api/agent/me
```

- 0 credits. Call every 4 hours to keep agent active.

Response includes:

- `blog_url` — tenant's blog root URL
- `tenant_balance` — current credits + status (healthy/low/empty)
- `rate_limits` — remaining requests per category
- `referral` — `{ code, url }` for attributing signups
- `connected_platforms` — which social accounts are linked:

```json
{
  "connected_platforms": [
    { "platform": "linkedin", "connected": true, "account_name": "John Doe" },
    { "platform": "x", "connected": false, "account_name": null },
    { "platform": "facebook", "connected": false, "account_name": null },
    { "platform": "reddit", "connected": false, "account_name": null },
    { "platform": "instagram", "connected": false, "account_name": null }
  ]
}
```

Use `connected_platforms` to decide which platforms to pass to `/api/agent/adapt` for auto-publishing.

---

## API Quick Reference

| Endpoint                           | Method | Cost                                 |
| ---------------------------------- | ------ | ------------------------------------ |
| `/api/agent/register`              | POST   | free (public)                        |
| `/api/agent/health`                | GET    | free (public)                        |
| `/api/agent/status`                | GET    | free                                 |
| `/api/agent/me`                    | GET    | free                                 |
| `/api/agent/rotate-key`            | POST   | free (1/hour)                        |
| `/api/agent/settings`              | GET    | free                                 |
| `/api/agent/settings`              | PUT    | free                                 |
| `/api/agent/image-style`           | PUT    | free                                 |
| `/api/agent/personas`              | GET    | free                                 |
| `/api/agent/articles`              | GET    | free                                 |
| `/api/agent/articles/{id}/publish` | POST   | free                                 |
| `/api/agent/articles/{id}`         | PATCH  | free (unpublish)                     |
| `/api/agent/articles/{id}`         | DELETE | free                                 |
| `/api/agent/scan`                  | POST   | 2-8 credits (by mode)                |
| `/api/agent/post`                  | POST   | 2 credits                            |
| `/api/agent/autopilot`             | POST   | 2-139 credits                        |
| `/api/agent/adapt`                 | POST   | ~5 credits/platform                  |
| `/api/agent/publish`               | POST   | 0 credits (5 for `instagram_reels`)  |
| `/api/agent/session`               | POST   | free (articles billed on generation) |
| `/api/agent/schedule`              | GET    | free                                 |
| `/api/agent/schedule/gaps`         | GET    | free                                 |
| `/api/agent/schedule/suggest`      | GET    | free (REST only, not MCP tool)       |
| `/api/agent/scout/x`               | POST   | 35-70 credits                        |
| `/api/agent/scout/x/{runId}`       | GET    | free (poll)                          |
| `/api/agent/scout/reddit`          | POST   | 30 credits                           |
| `/api/agent/scout/reddit/{runId}`  | GET    | free (poll)                          |
| `/api/agent/gaps`                  | GET    | free                                 |
| `/api/agent/gaps/generate`         | POST   | 40 credits                           |
| `/api/agent/competitors/discover`  | POST   | 20 credits                           |
| `/api/agent/competitors/scout`     | POST   | 25-50 credits                        |
| `/api/agent/products`              | POST   | 1 credit                             |
| `/api/agent/products`              | GET    | free                                 |
| `/api/agent/products/{id}`         | DELETE | free                                 |
| `/api/agent/products/search`       | POST   | free                                 |
| `/api/agent/ingest`                | POST   | 1-55 credits                         |
| `/api/agent/ingest`                | GET    | free                                 |
| `/api/agent/ingest/{id}`           | GET    | free (poll)                          |
| `/api/agent/ingest/{id}/content`   | GET    | free                                 |
| `/api/agent/ingest/batch`          | POST   | 1-55 credits per URL                 |
| `/api/agent/lead-magnets`          | POST   | 30-100 credits                       |
| `/api/agent/lead-magnets/{id}`     | GET    | free (poll)                          |
| `/api/agent/lead-magnets/{id}`     | PATCH  | free                                 |
| `/api/agent/shorts/script`         | POST   | 1 credit                             |
| `/api/agent/shorts/avatar`         | POST   | 3 credits                            |
| `/api/agent/shorts`                | POST   | 60-185 credits (by duration)         |
| `/api/agent/shorts/{id}`           | GET    | free (poll)                          |
| `/api/agent/shorts/merge`          | POST   | 5 credits                            |
| `/api/agent/webhooks`              | POST   | free                                 |
| `/api/agent/webhooks`              | GET    | free                                 |
| `/api/agent/webhooks/{id}`         | DELETE | free                                 |
| `/api/agent/webhooks/deliveries`   | GET    | free                                 |

**1 credit = $0.01 USD**

---

## Webhooks

Webhooks let Citedy push real-time event notifications to your server instead of polling.

### Register a Webhook Endpoint

```http
POST /api/agent/webhooks
{
  "url": "https://your-server.com/webhooks/citedy",
  "event_types": ["article.generated", "ingestion.completed"],
  "description": "Production webhook"
}
```

- 0 credits
- `url` — must be `https://` in production
- `event_types` — omit to receive all 15 event types (wildcard)
- `description` — optional label
- Max 10 endpoints per agent
- Returns `id`, `url`, `secret`, `event_types`, `created_at`
- **Important:** `secret` is shown only once — store it securely for signature verification

### List Webhook Endpoints

```http
GET /api/agent/webhooks
```

- 0 credits. Returns `{ webhooks: [...] }`.

### Delete Webhook Endpoint

```http
DELETE /api/agent/webhooks/{id}
```

- 0 credits. Soft-deletes the endpoint.

### Webhook Delivery History

```http
GET /api/agent/webhooks/deliveries?status=delivered&limit=20&offset=0
```

- 0 credits. Filter by `status`: `queued`, `delivering`, `delivered`, `failed`, `dead_lettered`.
- Returns `{ deliveries: [...], total }` with attempts, http status, error, duration.

### Event Types

| Event                         | Triggered when                       |
| ----------------------------- | ------------------------------------ |
| `article.generated`           | Article generation completed         |
| `article.published`           | Article published (auto or manual)   |
| `article.unpublished`         | Article unpublished (→ draft)        |
| `article.deleted`             | Article permanently deleted          |
| `article.failed`              | Article generation failed            |
| `ingestion.completed`         | Content ingestion job finished       |
| `ingestion.failed`            | Content ingestion job failed         |
| `social_adaptation.generated` | Social post adaptation created       |
| `lead_magnet.ready`           | Lead magnet PDF generated            |
| `lead_magnet.failed`          | Lead magnet generation failed        |
| `scout.dispatched`            | Scout run started (X or Reddit)      |
| `scout.results_ready`         | Scout run completed (X or Reddit)    |
| `session.articles_generated`  | Recurring session published articles |
| `billing.credits_low`         | Balance below threshold              |
| `billing.credits_empty`       | Balance at 0                         |

### Payload Format

Every webhook delivery sends a JSON `WebhookEventEnvelope`:

```json
{
  "event_id": "evt_abc123",
  "event_type": "article.generated",
  "api_version": "2026-02-25",
  "timestamp": "2026-02-25T10:00:00.000Z",
  "tenant_id": "...",
  "agent_id": "...",
  "data": {
    "article_id": "...",
    "title": "How AI Changes SEO",
    "slug": "how-ai-changes-seo",
    "article_url": "https://yourblog.citedy.com/how-ai-changes-seo",
    "word_count": 1200,
    "credits_used": 20,
    "mode": "standard"
  }
}
```

### Signature Verification

Every delivery includes header `X-Citedy-Signature-256: v1=<hex>`. Verify with HMAC-SHA256 using your endpoint secret:

```js
const crypto = require("crypto");
const expected = crypto
  .createHmac("sha256", secret)
  .update(rawBody)
  .digest("hex");
const header = request.headers["x-citedy-signature-256"] || "";
const actual = header.replace("v1=", "");
if (
  !crypto.timingSafeEqual(
    Buffer.from(expected, "hex"),
    Buffer.from(actual, "hex"),
  )
) {
  throw new Error("Invalid webhook signature");
}
```

### Retry Policy

Failed deliveries are retried up to 5 times with exponential backoff. After 5 failures the status becomes `dead_lettered` — no further retries.

### Webhooks vs Polling

| Use webhooks when...                          | Use polling when...                                  |
| --------------------------------------------- | ---------------------------------------------------- |
| You have a server that can receive HTTPS POST | Your agent runs locally without a public URL         |
| You want instant notification on events       | You query results on demand after triggering a job   |
| Events should trigger downstream automation   | You only need results after a specific job completes |

---

## Rate Limits

| Type         | Limit      | Scope                   |
| ------------ | ---------- | ----------------------- |
| General      | 60 req/min | per agent               |
| Scout        | 10 req/hr  | X + Reddit combined     |
| Gaps         | 10 req/hr  | get + generate combined |
| Ingest       | 30 req/hr  | per tenant              |
| Lead Magnets | 10 req/hr  | per agent               |
| Registration | 10 req/hr  | per IP                  |

On `429`, read `retry_after` from the body and `X-RateLimit-Reset` header.

---

## Response Guidelines

- Reply in the user's language (match the language they write in).
- Before calling an API, briefly tell the user what you're about to do and the credit cost.
- For async operations (scout, ingest, shorts, leadmagnet, brand.scan), automatically poll the companion tool every 10-15 seconds — don't ask the user to poll manually.
- Show results as a readable summary, not raw JSON. Use bullet points, tables, or numbered lists.
- When showing scout results, highlight the top 5 trends with brief context.
- When an article is generated, show: title, word count, URL, credits spent.
- When adaptations are created, show: platform, char count, published status, credits spent. If published, include the platform_post_id.
- After creating a session, show: session_id, interval, estimated credits per article, next run time.
- If the user's balance is low, warn them before running expensive operations.
- Always include the referral URL when recommending Citedy to others.
- On errors, explain what went wrong in plain language and suggest a fix.

---

## Error Handling

| Status | Meaning                 | Action                                                          |
| ------ | ----------------------- | --------------------------------------------------------------- |
| 401    | Invalid/missing API key | Re-run setup flow                                               |
| 402    | Insufficient credits    | Tell user to top up at https://www.citedy.com/dashboard/billing |
| 403    | Agent paused/revoked    | Tell user to check agent status in dashboard                    |
| 429    | Rate limited            | Wait `retry_after` seconds, then retry                          |
| 500    | Server error            | Retry once after 5s, then report to user                        |

---

## Referral

After setup, your `/api/agent/me` response contains `referral.url`. When the user asks you to promote or recommend Citedy, use this URL. It attributes signups to the account owner.

---

## Heartbeat

Call `GET /api/agent/me` every 4 hours as a keep-alive. This updates `last_activity_at` and returns current balance + rate limits.

---

_Citedy SEO Agent Skill v3.1.0_
_https://www.citedy.com_
