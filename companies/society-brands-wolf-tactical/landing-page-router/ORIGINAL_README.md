# Landing Page Optimizer - Auto A/B Testing

Automated landing page testing system using AI Studio templates, Netlify hosting, GA4 tracking, and n8n for auto-kill logic.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    How It Works                              │
├─────────────────────────────────────────────────────────────┤
│  1. Single deployment with 5 variants (URL params)          │
│  2. Traffic: cleanomic-test.netlify.app/?v=a (or b,c,d,e)  │
│  3. GA4 tracks by variant_id                                │
│  4. n8n polls GA4 every 6 hours                            │
│  5. If variant < 1.5% CVR after 200 sessions → KILL        │
│  6. Winners get more traffic, losers get removed           │
└─────────────────────────────────────────────────────────────┘
```

## Files

- `cleanomic-variants/` - React landing page with variant system
  - `App.tsx` - Main app with variant-aware components
  - `variantConfig.ts` - 5 headline/CTA/price variants
  - `analytics.ts` - GA4 + PostHog tracking

- `n8n_auto_ab_test.json` - Import this into n8n for auto-kill workflow
- `n8n_workflow_fixed.json` - Alternative simpler workflow

## Variants

| ID | Headline | CTA | Color |
|----|----------|-----|-------|
| A | Clean Your Home, Not the Planet | Shop Starter Kit | Emerald |
| B | One Left In Stock | Buy Now - Limited Stock | Red |
| C | Stop Paying for Shipped Water | Get My Kit | Blue |
| D | The Last Cleaning Product | Start Saving Today | Orange |
| E | Your Kids Lick Everything | Protect My Family | Purple |

## Quick Start

### 1. Deploy to Netlify

```bash
# Copy variant files to the AI Studio project
cp -r cleanomic-variants/* ~/Downloads/cleanomic-cro-landing-page/src/

# Build
cd ~/Downloads/cleanomic-cro-landing-page
npm run build

# Deploy to Netlify
netlify deploy --prod --dir=dist
```

### 2. Configure GA4

1. Create GA4 property at analytics.google.com
2. Get Measurement ID (G-XXXXXXXX)
3. Update `App.tsx` line 8: `const GA4_ID = 'G-YOUR_ID'`
4. Create custom dimension: `variant_id`

### 3. Import n8n Workflow

1. Go to your n8n instance (https://societybdev.app.n8n.cloud)
2. Import `n8n_auto_ab_test.json`
3. Update credentials:
   - Google OAuth for GA4 API
   - Slack webhook for alerts
   - (Optional) Airtable for logging

### 4. Get Shopify Variant ID

```bash
# Find the Starter Kit variant ID from Cleanomic Shopify
curl -s "https://cleanomic.com/products/starter-kit.json" | jq '.product.variants[0].id'
```

Update `App.tsx` line 11: `const SHOPIFY_VARIANT_ID = 'YOUR_ID'`

### 5. Test Traffic Routing

Open these URLs and verify different experiences:
- `https://your-netlify-site.netlify.app/?v=a` (Emerald CTA)
- `https://your-netlify-site.netlify.app/?v=b` (Red CTA + timer)
- `https://your-netlify-site.netlify.app/?v=c` (Blue CTA)
- `https://your-netlify-site.netlify.app/?v=d` (Orange CTA)
- `https://your-netlify-site.netlify.app/?v=e` (Purple CTA)

## Auto-Kill Logic

```javascript
// From n8n workflow
const threshold = 1.5;     // 1.5% conversion rate minimum
const minSessions = 200;   // Wait for 200 sessions before judging

if (sessions >= minSessions && conversionRate < threshold) {
  action = 'KILL';  // Remove from rotation
} else if (conversionRate >= threshold) {
  action = 'KEEP';  // Winner - keep running
} else {
  action = 'WAIT';  // Not enough data yet
}
```

## Cost

- Netlify: Free tier (100GB bandwidth)
- GA4: Free
- n8n: Free tier (5 workflows)
- PostHog: Free tier (1M events/mo)

**Total: $0/month for ~100 variant tests**

## Scaling

To test 100+ variants:
1. Add more configs to `variantConfig.ts`
2. Use ad platform targeting: Ad A → `?v=a`, Ad B → `?v=b`, etc.
3. Let n8n kill underperformers automatically
4. Manual: Review winners, create evolved variants from top 3

## From Brendan's Call (Jan 29, 2026)

Key decisions:
- AI Studio over Lovable (already paying for Gemini)
- 200 impressions/conversions threshold for kill
- Meta-prompt Gemini for new variants weekly
- Single Netlify deploy, variants via URL params
- GA4 for tracking (could upgrade to PostHog for real-time)
