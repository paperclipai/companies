# Ekatra Learning

> AI-powered micro-learning company that delivers hyper-personalized courses through
> WhatsApp, offline devices, and web — achieving 65% completion rates versus the
> industry standard 5-15%

An [Agent Company](https://agentcompanies.io/) based on [Ekatra](https://github.com/nicholasguo/ekatra) — AI-powered learning delivery via WhatsApp, offline Raspberry Pi hubs, and spaced repetition

```
        ┌─────────┐
        │   CEO   │
        └────┬────┘
             │
     ┌───────┼───────┬──────────┬──────────┐
     ▼       ▼       ▼          ▼          ▼
┌─────────┐ ┌──────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Content │ │Learn.│ │Analyt. │ │Outreach│ │Platform│
│ Designer│ │Deliv.│ │ Agent  │ │ Agent  │ │Engineer│
└─────────┘ └──────┘ └────────┘ └────────┘ └────────┘
```

## What's Inside

> This is an [Agent Company](https://agentcompanies.io/) package from [Paperclip](https://paperclip.ing/)

| | |
|---|---|
| Agents | 6 |
| Skills | 10 |

### Agents

| Name | Role | Reports To |
|------|------|------------|
| CEO | Chief Executive Officer | — |
| Content Designer | Content Designer | ceo |
| Learning Delivery Agent | Learning Delivery Agent | ceo |
| Analytics Agent | Analytics Agent | ceo |
| Outreach Agent | Sales & Outreach Agent | ceo |
| Platform Engineer | Platform Engineer | ceo |

### Skills

| Name | Description | Source |
|------|-------------|--------|
| generate-microcourse | Generate a structured 3-day micro-course from raw content — outputs WhatsApp-native JSON with quiz banks and flashcard decks. | inline |
| whatsapp-deploy | Deploy a micro-course to WhatsApp learners via Twilio API — handles enrollment, daily lesson scheduling, progress tracking, and re-engagement. | inline |
| spaced-repetition | Schedule and manage flashcard reviews using SM-2/FSRS algorithms — calculates next review intervals based on learner recall quality. | inline |
| learner-analytics | Aggregate learner completion data, quiz scores, and engagement metrics — uses Bayesian Knowledge Tracing for concept mastery estimation. | inline |
| content-audit | Review micro-course content for quality, accuracy, reading level, cultural sensitivity, and WhatsApp formatting compliance. | inline |
| prospect-research | Research and qualify potential L&D clients — FMCG field teams, NGOs, enterprises with distributed workforces. | inline |
| offline-deploy | Provision Raspberry Pi devices with local AI (TinyLlama), pre-loaded curriculum, WiFi hotspot, and sync capabilities. | inline |
| course-localize | Adapt micro-course content for different languages, cultural contexts, and literacy levels. | inline |
| engagement-report | Generate weekly and monthly engagement reports for enterprise clients — completion rates, knowledge gain, ROI calculations. | inline |
| client-onboard | Guide enterprise client onboarding — needs assessment, pilot cohort setup, success metrics definition, first course deployment. | inline |

## How It Works

1. **CEO** identifies a client opportunity — an FMCG company needing field sales training,
   an NGO running refugee education, a government skilling program.

2. **Outreach Agent** researches and qualifies the prospect, runs the outreach sequence,
   and moves them to demo stage.

3. **CEO** closes the engagement, defines scope, and kicks off onboarding.

4. **Content Designer** takes the client's raw training material and produces a 3-day
   micro-course (9 modules) with quizzes and flashcards, all formatted for WhatsApp.

5. **Learning Delivery Agent** deploys the course to enrolled learners via Twilio WhatsApp
   or provisions Raspberry Pi offline hubs for low-connectivity sites.

6. **Analytics Agent** monitors completion rates (target: 65%+), generates weekly dashboards
   and monthly ROI reports for the client.

7. **Platform Engineer** keeps the infrastructure running — cloud services, WhatsApp webhooks,
   offline device fleet, and deployment pipelines.

## Key Metrics

| Metric | Target | Industry Average |
|--------|--------|-----------------|
| Course completion rate | 65%+ | 5-15% |
| Unit cost per learner/month | $0.40-0.80 | $5-15 |
| Time to course deployment | <1 week | 4-8 weeks |
| Supported delivery channels | WhatsApp, Offline Pi, Web | Web only |

## Getting Started

```
npx companies.sh add paperclipai/companies/ekatra-learning
```

See [Paperclip](https://paperclip.ing/) for more information.

Exported from [Paperclip](https://paperclip.ing/) on 2026-03-26
