# Shorts Studio

> Autonomous YouTube Shorts channel operator — anti-AI-slop features included.

Battle-tested on [ForgottenPages](https://youtube.com/@forgottenpages), a history Shorts channel with 660 avg views across 35+ auto-produced videos.

## What makes this different

Most AI YouTube channels get flagged or suppressed because every video has the same TTS voice, same AI image style, zero human signal. This template ships with:

| Feature | What it does |
|---|---|
| **Voice rotation** | Deterministic rotation through 3–4 Kokoro TTS voices per channel |
| **Human intro bumper** | Prepends a real recorded human clip to every video |
| **Archival image mix** | Swaps 2 AI-generated images per video with real Wikimedia Commons photos |
| **Ken Burns variants** | 3 zoom/pan patterns rotated per video |
| **Custom PIL thumbnails** | Channel-branded thumbnails (replaces broken Canva exports) |
| **Quality gates** | Hook + title validation, duplicate detection, rotation enforcement |
| **Retention feedback loop** | YouTube Analytics retention-at-3s feeds back into the quality gate |

## Getting Started

```bash
# Import the company
paperclipai company import https://github.com/paperclipai/companies/tree/main/shorts-studio

# Clone the pipeline code
git clone https://github.com/acunningham-ship-it/shorts-studio
cd shorts-studio

# Install deps
pip install -r requirements.txt

# Configure
cp .env.example .env   # fill in API keys, YouTube OAuth path, CHANNEL_NAME
# drop a 5-8 second human voice clip into assets/human_intro.mp3

# In Paperclip: file an issue on the Producer agent like "Produce a drop for <channel>"
# The Producer will cd into the pipeline dir and run trigger_production.py
```

## Org chart

```
       ┌─────────────┐
       │   Producer  │  (runs pipeline end-to-end)
       └─────────────┘
              │
       ┌──────┴──────┐
       │             │
 ┌───────────┐  ┌──────────┐
 │ Strategist│  │  Analyst │
 │ (calendar)│  │(retention)│
 └───────────┘  └──────────┘
```

Producer is the workhorse. Strategist and Analyst feed it — Strategist picks what to make next, Analyst tells the quality gate what's working.

## Customizing for your niche

The template ships generic; see [CUSTOMIZATION.md](https://github.com/acunningham-ship-it/shorts-studio/blob/main/docs/CUSTOMIZATION.md) in the pipeline repo for a 9-step adapt-for-your-niche guide. Typical edits:

- Quality gate hook patterns (`pipeline/quality_gate.py`)
- Title validation regex (`pipeline/title_validator.py`)
- Topic seeds (`pipeline/seed_topics.txt`)
- Thumbnail brand colors (`pipeline/local_thumbnail.py`)
- Archival image sources (`pipeline/archival_fetcher.py`)

## Links

- [Pipeline code + full docs](https://github.com/acunningham-ship-it/shorts-studio)
- [Agent Companies spec](https://agentcompanies.io/specification)
- [Paperclip](https://github.com/paperclipai/paperclip)

## License

MIT
