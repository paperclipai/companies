---
name: "Shorts Studio"
description: "Autonomous YouTube Shorts channel operator with anti-AI-slop features — voice rotation, archival image mix, human intro bumper, retention-learning quality gate."
schema: "agentcompanies/v1"
slug: "shorts-studio"
version: "1.0.0"
license: "MIT"
authors:
  - name: "Armani Cunningham"
    github: "acunningham-ship-it"
goals:
  - Run a niche YouTube Shorts channel end-to-end without human-in-the-loop production
  - Beat YouTube's 2026 AI-slop detection via voice rotation, archival image mixing, and a human-recorded intro bumper
  - Learn from YouTube Analytics retention data so the quality gate sharpens over time
  - Keep costs at ~$0.50/video using free LLM provider cascades
tags:
  - youtube
  - shorts
  - content-creation
  - video-production
  - tts
  - automation
  - anti-ai-slop
---

Shorts Studio is a three-agent company that operates a niche YouTube Shorts channel autonomously. It was battle-tested on the ForgottenPages history channel (660 avg views, 35+ videos shipped).

## How it works

**Producer** — end-to-end content factory. When assigned a production issue, it runs the pipeline: research → hook quality gate → TTS with voice rotation → image generation → archival image swap (Wikimedia Commons) → video compilation with captions → YouTube upload with publishAt scheduling.

**Strategist** — weekly content calendar planner. Reads analytics from performance_history.json, rotates hook patterns, picks underused themes, biases toward retention-proven formats.

**Analyst** — daily retention puller. Queries YouTube Analytics for per-video retention-at-3s, updates the quality gate's feedback data. Top/bottom 3 patterns get flagged for the Strategist.

## Why three agents, not one

Separation of concerns. Producer is thick (runs Python pipelines, ffmpeg, OAuth'd YouTube API). Strategist and Analyst are thin — they just read JSON files and summarize. This lets you swap them independently and keeps Producer's budget bounded.

## Prerequisites

- Python 3.11+, ffmpeg, Kokoro TTS
- YouTube Data API OAuth credentials
- At least one LLM API key (OpenRouter recommended; free-tier fallbacks included)
- 5–8 second human voice recording saved as `assets/human_intro.mp3`

## Pipeline repo

The Python pipeline code lives at [acunningham-ship-it/shorts-studio](https://github.com/acunningham-ship-it/shorts-studio). Clone that repo separately — this company template only defines agent coordination.

