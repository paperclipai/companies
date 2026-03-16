/**
 * Gemini AI Insights API
 *
 * Endpoint: POST /api/insights
 * Accepts metrics JSON body, sends to Google Gemini for CRO analysis.
 * Returns structured insights as JSON.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
    'Cache-Control': 'public, max-age=900'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'POST required' }) };
  }

  try {
    const apiKey = process.env.GEMINI_API_KEY;
    const metricsData = JSON.parse(event.body);

    // If no Gemini API key, return smart static insights based on the data
    if (!apiKey) {
      const variants = metricsData.variants || [];
      const sorted = [...variants].filter(v => v.active !== false).sort((a, b) => (b.metrics?.cvr || 0) - (a.metrics?.cvr || 0));
      const best = sorted[0];
      const worst = sorted[sorted.length - 1];
      const bestName = best ? best.name.replace(/^variant-[a-z]-/, '').replace(/-/g, ' ') : 'N/A';
      const worstName = worst ? worst.name.replace(/^variant-[a-z]-/, '').replace(/-/g, ' ') : 'N/A';

      return {
        statusCode: 200, headers,
        body: JSON.stringify({
          generated_at: new Date().toISOString(),
          demo: true,
          insights: {
            whats_working: best
              ? `The "${bestName}" variant leads with a ${(best.metrics.cvr * 100).toFixed(2)}% conversion rate from ${best.metrics.pageviews} pageviews, generating $${best.metrics.revenue} in revenue. Its approach resonates well with visitors, suggesting the page structure and messaging align with user intent.`
              : 'Not enough data to determine top performers yet.',
            whats_not_working: worst
              ? `The "${worstName}" variant has the lowest CVR at ${(worst.metrics.cvr * 100).toFixed(2)}% with ${worst.metrics.pageviews} views. Consider revising the headline, CTA placement, or overall page layout to improve engagement and conversion.`
              : 'Not enough data to identify underperformers yet.',
            key_takeaways: [
              `${variants.filter(v => v.active !== false).length} active variants are being tested across the portfolio.`,
              best ? `Top performer "${bestName}" converts at ${((best.metrics.cvr / (metricsData.summary?.avgCvr || 0.01)) * 100 - 100).toFixed(0)}% above the portfolio average.` : 'More data needed to identify clear winners.',
              `Total portfolio has generated $${metricsData.summary?.totalRevenue || 0} in estimated revenue over this period.`,
              'Statistical confidence increases with more traffic — aim for 200+ views per variant before making kill decisions.'
            ],
            recommendation: best
              ? `Focus ad spend to drive more traffic through the router for faster statistical significance. Consider applying winning elements from "${bestName}" to underperforming variants. Monitor for at least 7 days before killing any variants.`
              : 'Continue routing traffic evenly across all variants until sufficient data accumulates for analysis.'
          }
        })
      };
    }

    // Build structured prompt
    const variantSummaries = metricsData.variants.map(v => {
      return [
        `- ${v.name} (${v.active ? 'Active' : 'Killed'}):`,
        `  Views: ${v.metrics.pageviews}`,
        `  Conversions: ${v.metrics.conversions}`,
        `  CVR: ${(v.metrics.cvr * 100).toFixed(2)}%`,
        `  Revenue: $${v.metrics.revenue}`,
        `  Bounce Rate: ${(v.metrics.bounceRate * 100).toFixed(1)}%`,
        `  Avg Session Duration: ${v.metrics.avgDuration}s`
      ].join('\n');
    }).join('\n\n');

    const prompt = `You are an expert CRO (Conversion Rate Optimization) analyst for an A/B testing platform.

Analyze this landing page variant performance data and provide actionable insights.

PERFORMANCE DATA (last ${metricsData.days} days):
Total Views: ${metricsData.summary.totalViews}
Total Conversions: ${metricsData.summary.totalConversions}
Average CVR: ${(metricsData.summary.avgCvr * 100).toFixed(2)}%
Total Revenue: $${metricsData.summary.totalRevenue}
Current Champion: ${metricsData.summary.champion || 'None identified yet'}

VARIANT BREAKDOWN:
${variantSummaries}

Respond with a JSON object containing these exact fields:
{
  "whats_working": "2-3 sentences about the best performing variant(s), why they succeed, and specific strengths.",
  "whats_not_working": "2-3 sentences about the worst performing variant(s), why they fail, and specific weaknesses.",
  "key_takeaways": [
    "First key insight with specific data",
    "Second key insight with specific data",
    "Third key insight with specific data",
    "Fourth key insight with specific data"
  ],
  "recommendation": "2-3 sentences with specific, actionable next steps including traffic allocation suggestions and testing ideas."
}`;

    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: 'gemini-2.0-flash',
      generationConfig: {
        responseMimeType: 'application/json'
      }
    });

    const result = await model.generateContent(prompt);
    const responseText = result.response.text();
    const parsed = JSON.parse(responseText);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        generated_at: new Date().toISOString(),
        insights: parsed
      })
    };

  } catch (error) {
    console.error('API insights error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Failed to generate insights', detail: error.message })
    };
  }
};
