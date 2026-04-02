---
name: local-seo
description: "SEO knowledge base for local service businesses. Covers audits, indexing, meta tags, schema markup, service-area pages, and Google Search Console diagnostics."
---

# Local SEO for Home Service Businesses

## Audit Checklist

### Technical SEO
- [ ] All pages return 200 status
- [ ] XML sitemap submitted to Google Search Console
- [ ] robots.txt allows crawling of key pages
- [ ] Canonical tags on every page
- [ ] No duplicate title tags or meta descriptions
- [ ] Core Web Vitals passing (LCP < 2.5s, CLS < 0.1, INP < 200ms)
- [ ] Mobile-friendly (responsive, no horizontal scroll)
- [ ] HTTPS everywhere, no mixed content

### On-Page SEO
- [ ] Title tags: [Service] in [City] | [Company Name] (under 60 chars)
- [ ] Meta descriptions: action-oriented, include city, under 160 chars
- [ ] H1 tags: one per page, includes primary keyword
- [ ] Service pages for each offering with unique content
- [ ] Internal links between related service pages
- [ ] Image alt text describes the image with location context

### Local Signals
- [ ] Google Business Profile claimed and verified
- [ ] NAP (Name, Address, Phone) consistent across all citations
- [ ] LocalBusiness schema markup on every page
- [ ] Service area defined in GBP
- [ ] Reviews actively solicited (target: 1-2 per week)
- [ ] GBP posts published weekly

### Content Strategy
- [ ] Blog targets long-tail local keywords (e.g., "best time to aerate lawn in [city]")
- [ ] Service pages target "[service] in [city]" keywords
- [ ] FAQ sections answer People Also Ask queries
- [ ] Seasonal content calendar aligned with service demand

## Schema Templates

### LocalBusiness
```json
{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "name": "{{company_name}}",
  "url": "{{website_url}}",
  "telephone": "{{phone}}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{street}}",
    "addressLocality": "{{city}}",
    "addressRegion": "{{state}}",
    "postalCode": "{{zip}}"
  },
  "areaServed": {
    "@type": "City",
    "name": "{{city}}"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{{rating}}",
    "reviewCount": "{{review_count}}"
  }
}
```

### Service
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{{service_name}}",
  "provider": { "@type": "LocalBusiness", "name": "{{company_name}}" },
  "areaServed": { "@type": "City", "name": "{{city}}" },
  "description": "{{service_description}}"
}
```

## Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| "Discovered, not indexed" | Improve content depth, add internal links, request indexing |
| "Crawled, not indexed" | Content too thin or duplicate. Rewrite with 500+ unique words |
| Duplicate meta descriptions | Write unique descriptions for every page |
| Missing schema | Add LocalBusiness + Service schema to every relevant page |
| Slow LCP | Optimize images (WebP, lazy load), reduce JS bundle |
| Low click-through rate | Rewrite title tags to be more compelling, add review stars via schema |
