---
name: Ekatra Learning
description: AI-powered micro-learning company that delivers hyper-personalized courses through WhatsApp, offline devices, and web — achieving 65% completion rates versus the industry standard 5-15%
slug: ekatra-learning
schema: agentcompanies/v1
version: 1.0.0
license: MIT
authors:
  - name: Ekatra
goals:
  - Acquire enterprise and NGO clients who need scalable workforce training or education programs
  - Generate structured micro-courses from raw content using AI, optimized for WhatsApp delivery
  - Deploy courses to learners via WhatsApp (Twilio) with daily lesson scheduling and spaced repetition
  - Provision offline Raspberry Pi learning hubs for areas without internet connectivity
  - Track learner completion rates, engagement metrics, and knowledge mastery using Bayesian Knowledge Tracing
  - Generate ROI reports for enterprise clients demonstrating training impact and cost savings
  - Localize and adapt course content for different languages, literacy levels, and cultural contexts
  - Maintain unit economics at $0.40-0.80 per learner per month
---

Ekatra Learning is an AI-powered micro-learning company built to reach underserved
populations — refugee camps, rural communities, FMCG field sales teams — through
channels they already use: WhatsApp, offline WiFi hubs, and simple web interfaces.

## How Work Flows

1. **CEO** identifies a client or market opportunity — an NGO needing refugee education,
   an enterprise needing field sales training, a government wanting community health workers
   upskilled. Runs needs assessment, defines success metrics, signs the engagement.

2. **Content Designer** takes raw material (PDFs, training manuals, SME interviews,
   video transcripts) and generates structured 3-day micro-courses. Each day has 3 modules
   following a proven arc: Day 1 fundamentals, Day 2 intermediate application, Day 3
   synthesis and assessment. Output is WhatsApp-native JSON with quiz banks and flashcard decks.

3. **Learning Delivery Agent** deploys the course to enrolled learners via Twilio WhatsApp
   API. Manages the full learner lifecycle: enrollment → daily lesson scheduling →
   progress tracking → spaced repetition reminders → completion certification. For offline
   deployments, coordinates with Platform Engineer on Raspberry Pi provisioning.

4. **Analytics Agent** monitors learner outcomes in real time. Tracks completion rates
   (target: 65%+), quiz scores, time-on-task, and concept mastery using Bayesian Knowledge
   Tracing (BKT). Generates weekly engagement reports and monthly ROI summaries for
   enterprise clients.

5. **Outreach Agent** runs the sales pipeline. Identifies prospects (FMCG companies with
   distributed field teams, NGOs with education mandates, enterprises with compliance
   training needs), qualifies leads, runs outreach sequences, and schedules demos.

6. **Platform Engineer** maintains the technical infrastructure. Manages Azure/AWS
   deployments, Twilio webhook reliability, MongoDB/Cosmos DB health, and the Raspberry Pi
   offline device fleet. Handles incident response and capacity planning.

The philosophy: each agent is a specialist with a distinct cognitive mode. The CEO thinks
in markets and margins. The Content Designer thinks in learning arcs and retention curves.
The Learning Delivery Agent thinks in message flows and scheduling. They don't overlap —
they hand off.

Generated from [Ekatra](https://github.com/nicholasguo/ekatra) with the company-creator skill from [Paperclip](https://github.com/paperclipai/paperclip)
