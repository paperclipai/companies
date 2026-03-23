/**
 * GA4 Metrics API — Batched Queries
 *
 * Endpoint: GET /api/metrics?range=7d
 * Returns variant performance data from Google Analytics 4.
 * Uses only 3 total GA4 API calls (not per-variant) to stay within rate limits.
 */

const { BetaAnalyticsDataClient } = require('@google-analytics/data');
const { GoogleAuth } = require('google-auth-library');

const REVENUE_PER_CONVERSION = 39;

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
    'Cache-Control': 'public, max-age=300'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers, body: '' };
  }

  try {
    // Parse range parameter
    const params = event.queryStringParameters || {};
    const range = params.range || '7d';
    const days = { '24h': 1, '7d': 7, '30d': 30, '90d': 90 }[range] || 7;
    const demoMode = params.demo === 'true' || params.demo === '1';

    // GA4 authentication — decode Base64 credentials
    const credsB64 = process.env.GA_CREDENTIALS_B64;
    const credsJson = process.env.GA_CREDENTIALS_JSON;
    const propertyId = process.env.GA_PROPERTY_ID;

    const ga4Configured = (credsB64 || credsJson) && propertyId;

    // Fetch active variants config (needed for both live and demo modes)
    const configUrl = process.env.CONFIG_URL ||
      'https://society-lp-router.netlify.app/active_variants.json';
    const configResp = await fetch(configUrl, { headers: { 'Cache-Control': 'no-cache' } });
    const config = await configResp.json();

    // DEMO MODE: return realistic simulated data when GA4 isn't configured
    if (!ga4Configured || demoMode) {
      const demoVariants = config.variants.map((v, i) => {
        // Seed a pseudo-random from variant name for consistency
        const seed = v.name.split('').reduce((a, c) => a + c.charCodeAt(0), 0);
        const baseViews = 150 + (seed % 300) * days / 7;
        const pageviews = Math.round(baseViews + Math.random() * 50);
        const cvr = 0.01 + (seed % 40) / 1000;
        const conversions = Math.round(pageviews * cvr);
        const bounceRate = 0.3 + (seed % 30) / 100;
        const avgDuration = 20 + (seed % 60);

        // Generate daily data
        const daily = [];
        for (let d = 0; d < days; d++) {
          const date = new Date();
          date.setDate(date.getDate() - (days - d - 1));
          const dateStr = date.toISOString().split('T')[0].replace(/-/g, '');
          const dailyViews = Math.round(pageviews / days + (Math.random() - 0.5) * 10);
          daily.push({ date: dateStr, views: Math.max(1, dailyViews), events: Math.max(0, Math.round(dailyViews * 1.5)) });
        }

        return {
          name: v.name,
          url: v.url,
          active: v.active !== false,
          weight: v.weight || 1,
          metrics: {
            pageviews,
            conversions,
            cvr: Math.round(cvr * 10000) / 10000,
            revenue: conversions * REVENUE_PER_CONVERSION,
            bounceRate: Math.round(bounceRate * 10000) / 10000,
            avgDuration,
            totalEvents: Math.round(pageviews * 1.5)
          },
          daily
        };
      });

      const totalViews = demoVariants.reduce((s, v) => s + v.metrics.pageviews, 0);
      const totalConversions = demoVariants.reduce((s, v) => s + v.metrics.conversions, 0);
      const totalRevenue = demoVariants.reduce((s, v) => s + v.metrics.revenue, 0);
      const avgCvr = totalViews > 0 ? totalConversions / totalViews : 0;
      const candidates = demoVariants.filter(v => v.active && v.metrics.pageviews >= 50).sort((a, b) => b.metrics.cvr - a.metrics.cvr);
      const champion = candidates.length > 0 ? candidates[0].name : null;

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          generated_at: new Date().toISOString(),
          range,
          days,
          demo: true,
          summary: {
            totalViews,
            totalConversions,
            avgCvr: Math.round(avgCvr * 10000) / 10000,
            totalRevenue,
            champion
          },
          variants: demoVariants
        })
      };
    }

    if (!ga4Configured) {
      return {
        statusCode: 500, headers,
        body: JSON.stringify({ error: 'GA4 credentials not configured. Set GA_CREDENTIALS_B64 (or GA_CREDENTIALS_JSON) and GA_PROPERTY_ID in Netlify env vars. Add ?demo=true for demo data.' })
      };
    }

    const credentials = credsB64
      ? JSON.parse(Buffer.from(credsB64, 'base64').toString('utf-8'))
      : JSON.parse(credsJson);

    const auth = new GoogleAuth({
      credentials,
      scopes: ['https://www.googleapis.com/auth/analytics.readonly']
    });
    const client = new BetaAnalyticsDataClient({ authClient: await auth.getClient() });

    // Config already fetched above (before demo check)

    const property = propertyId.startsWith('properties/')
      ? propertyId
      : `properties/${propertyId}`;

    // Date range
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(endDate.getDate() - days);
    const startStr = startDate.toISOString().split('T')[0];
    const endStr = endDate.toISOString().split('T')[0];

    // Build hostname lookup from active variants
    const hostnameMap = {};
    for (const v of config.variants) {
      const hostname = v.url.replace('https://', '').replace('http://', '').split('/')[0];
      hostnameMap[hostname.toLowerCase()] = v;
    }

    // ============================================================
    // BATCHED QUERY 1: Aggregate metrics for ALL hostnames at once
    // ============================================================
    const [aggResponse] = await client.runReport({
      property,
      dateRanges: [{ startDate: startStr, endDate: endStr }],
      dimensions: [{ name: 'hostName' }],
      metrics: [
        { name: 'screenPageViews' },
        { name: 'eventCount' },
        { name: 'averageSessionDuration' },
        { name: 'bounceRate' }
      ]
    });

    // Bucket aggregate data by hostname
    const aggByHost = {};
    if (aggResponse.rows) {
      for (const row of aggResponse.rows) {
        const host = row.dimensionValues[0].value.toLowerCase();
        aggByHost[host] = {
          pageviews: parseInt(row.metricValues[0].value) || 0,
          totalEvents: parseInt(row.metricValues[1].value) || 0,
          avgDuration: Math.round(parseFloat(row.metricValues[2].value) || 0),
          bounceRate: parseFloat(row.metricValues[3].value) || 0
        };
      }
    }

    // ============================================================
    // BATCHED QUERY 2: CTA click conversions for ALL hostnames
    // ============================================================
    const [ctaResponse] = await client.runReport({
      property,
      dateRanges: [{ startDate: startStr, endDate: endStr }],
      dimensions: [{ name: 'hostName' }],
      metrics: [{ name: 'eventCount' }],
      dimensionFilter: {
        filter: {
          fieldName: 'eventName',
          stringFilter: { value: 'cta_click', matchType: 'EXACT' }
        }
      }
    });

    // Bucket CTA data by hostname
    const ctaByHost = {};
    if (ctaResponse.rows) {
      for (const row of ctaResponse.rows) {
        const host = row.dimensionValues[0].value.toLowerCase();
        ctaByHost[host] = parseInt(row.metricValues[0].value) || 0;
      }
    }

    // ============================================================
    // BATCHED QUERY 3: Daily breakdown for sparklines
    // ============================================================
    const [dailyResponse] = await client.runReport({
      property,
      dateRanges: [{ startDate: startStr, endDate: endStr }],
      dimensions: [
        { name: 'date' },
        { name: 'hostName' }
      ],
      metrics: [
        { name: 'screenPageViews' },
        { name: 'eventCount' }
      ],
      orderBys: [{ dimension: { dimensionName: 'date' } }]
    });

    // Bucket daily data by hostname
    const dailyByHost = {};
    if (dailyResponse.rows) {
      for (const row of dailyResponse.rows) {
        const date = row.dimensionValues[0].value;
        const host = row.dimensionValues[1].value.toLowerCase();
        if (!dailyByHost[host]) dailyByHost[host] = [];
        dailyByHost[host].push({
          date,
          views: parseInt(row.metricValues[0].value) || 0,
          events: parseInt(row.metricValues[1].value) || 0
        });
      }
    }

    // ============================================================
    // Assemble variant data by matching hostnames
    // ============================================================
    const variants = [];
    for (const v of config.variants) {
      const hostname = v.url.replace('https://', '').replace('http://', '').split('/')[0].toLowerCase();

      const agg = aggByHost[hostname] || { pageviews: 0, totalEvents: 0, avgDuration: 0, bounceRate: 0 };
      const conversions = ctaByHost[hostname] || 0;
      const daily = dailyByHost[hostname] || [];
      const cvr = agg.pageviews > 0 ? conversions / agg.pageviews : 0;

      variants.push({
        name: v.name,
        url: v.url,
        active: v.active !== false,
        weight: v.weight || 1,
        metrics: {
          pageviews: agg.pageviews,
          conversions,
          cvr: Math.round(cvr * 10000) / 10000,
          revenue: conversions * REVENUE_PER_CONVERSION,
          bounceRate: Math.round(agg.bounceRate * 10000) / 10000,
          avgDuration: agg.avgDuration,
          totalEvents: agg.totalEvents
        },
        daily
      });
    }

    // Compute summary
    const totalViews = variants.reduce((s, v) => s + v.metrics.pageviews, 0);
    const totalConversions = variants.reduce((s, v) => s + v.metrics.conversions, 0);
    const totalRevenue = variants.reduce((s, v) => s + v.metrics.revenue, 0);
    const avgCvr = totalViews > 0 ? totalConversions / totalViews : 0;

    // Champion = highest CVR among active variants with >= 50 pageviews
    const candidates = variants
      .filter(v => v.active && v.metrics.pageviews >= 50)
      .sort((a, b) => b.metrics.cvr - a.metrics.cvr);
    const champion = candidates.length > 0 ? candidates[0].name : null;

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        generated_at: new Date().toISOString(),
        range,
        days,
        summary: {
          totalViews,
          totalConversions,
          avgCvr: Math.round(avgCvr * 10000) / 10000,
          totalRevenue,
          champion
        },
        variants
      })
    };

  } catch (error) {
    console.error('API metrics error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Failed to fetch metrics', detail: error.message })
    };
  }
};
