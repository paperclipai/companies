# Landing Page A/B Test Optimizer - Process Documentation

## Purpose
Template system for rapid landing page variant testing across Society Brands portfolio.

## Architecture

### URL-Based Variant System
- Single deployment, multiple variants via URL parameter
- `?v=a` through `?v=e` (extensible to more)
- Default to random assignment if no param

### Tech Stack
- **Framework:** React + Vite + TypeScript
- **Styling:** Tailwind CSS + Framer Motion
- **Analytics:** GA4 (primary) + PostHog (optional, real-time)
- **Checkout:** Shopify cart integration (not custom checkout)
- **Hosting:** Netlify (free tier sufficient)
- **Automation:** n8n for auto-kill logic

## File Structure
```
projects/landing-page-optimizer/
├── PROCESS_DOCUMENTATION.md    # This file
├── README.md                   # Setup guide
├── n8n_auto_ab_test.json       # Auto-kill workflow
│
├── cleanomic-variants/         # Cleanomic prototype
│   ├── App.tsx
│   ├── variantConfig.ts
│   └── analytics.ts
│
└── wolf-tactical-variants/     # Wolf Tactical version
    ├── App.tsx
    ├── variantConfig.ts
    └── (analytics.ts - reuse from cleanomic)
```

## Key Files Explained

### variantConfig.ts
Central configuration for all variants:
```typescript
export const variants = {
  a: {
    headline: "...",
    subheadline: "...",
    ctaText: "...",
    ctaColor: "...",
    urgencyElement: null | { type: 'countdown' | 'stock', value: ... },
    badges: ['...'],
  },
  // ... b, c, d, e
}
```

### App.tsx
- Reads `?v=` param from URL
- Loads corresponding variant config
- Fires GA4 event on load with variant dimension
- Links to Shopify cart with variant ID

### analytics.ts
- `trackVariantView(variant)` - fires on page load
- `trackCTAClick(variant)` - fires on button click
- Sends custom dimensions to GA4

### n8n_auto_ab_test.json
Workflow that:
1. Polls GA4 Data API every 6 hours
2. Calculates conversion rate per variant
3. Kills (redirects to control) any variant with:
   - 200+ sessions AND
   - <1.5% conversion rate

## Pre-Launch Checklist

### Brand Assets Required
- [ ] Correct logo (PNG/SVG)
- [ ] Product images (hero, lifestyle, detail)
- [ ] Brand color codes (primary, secondary, CTA)
- [ ] Brand guidelines document

### Copy Required
- [ ] Headlines per variant (5x)
- [ ] Subheadlines per variant (5x)
- [ ] CTA text per variant (5x)
- [ ] Trust badges (factual only - no false claims)
- [ ] Social proof (real reviews/testimonials)

### Technical Setup
- [ ] GA4 Measurement ID
- [ ] Shopify variant ID for cart link
- [ ] Netlify account connected
- [ ] n8n workflow imported

### Legal Review
- [ ] No false claims (e.g., "veteran-owned" if not true)
- [ ] Accurate product descriptions
- [ ] Compliant discount/urgency claims

## Deployment Steps

1. **Update variantConfig.ts** with approved copy
2. **Replace placeholder images** with real assets
3. **Set GA4 Measurement ID** in App.tsx
4. **Set Shopify variant ID** in variantConfig.ts
5. **Deploy:** `netlify deploy --prod`
6. **Import n8n workflow** to societybdev.app.n8n.cloud
7. **Test all variants** manually before traffic

## Success Metrics
- Primary: Conversion Rate (orders / sessions)
- Secondary: Add-to-Cart Rate
- Auto-kill threshold: <1.5% CVR after 200 sessions

## Extending to New Brands

1. Copy `wolf-tactical-variants/` to `{brand}-variants/`
2. Update `variantConfig.ts` with brand-specific copy/colors
3. Update logo/images
4. Update Shopify variant ID
5. Deploy to new Netlify site
6. Create new GA4 property or use brand's existing

## Lessons Learned
- Lovable has no API (can't programmatically create pages)
- AI Studio > Lovable for template-based work
- URL params simpler than subdomain routing
- Shopify checkout > custom checkout (trust, reliability)
- GA4 has 24-48hr lag; PostHog is real-time but costs extra
