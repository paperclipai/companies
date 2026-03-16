// Router function - redirects visitors to random active variant
// Fetches active_variants.json from GitHub to know which variants are live

exports.handler = async (event, context) => {
  try {
    // Fetch active variants config
    // UPDATE THIS URL after you fork the repo!
    const configUrl = process.env.CONFIG_URL || 
      'https://society-lp-router.netlify.app/active_variants.json';
    
    let activeVariants;
    try {
      const response = await fetch(configUrl, {
        headers: { 'Cache-Control': 'no-cache' }
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      activeVariants = await response.json();
    } catch (e) {
      console.error('Could not fetch active_variants.json:', e.message);
      return {
        statusCode: 500,
        body: 'Configuration error - could not load active variants'
      };
    }

    // Filter to only active variants
    const variants = activeVariants.variants.filter(v => v.active);
    
    if (variants.length === 0) {
      return {
        statusCode: 503,
        body: 'No active landing page variants available'
      };
    }

    // Check for segment parameter (for psychographic targeting)
    const params = event.queryStringParameters || {};
    const segment = params.segment;
    
    let selectedVariant;
    
    if (segment) {
      // Filter variants that match this segment
      const segmentVariants = variants.filter(v => 
        v.segments && v.segments.includes(segment)
      );
      
      if (segmentVariants.length > 0) {
        // Random selection from segment-matched variants
        selectedVariant = segmentVariants[Math.floor(Math.random() * segmentVariants.length)];
      }
    }
    
    if (!selectedVariant) {
      // Weighted random selection
      const totalWeight = variants.reduce((sum, v) => sum + (v.weight || 1), 0);
      let random = Math.random() * totalWeight;
      
      for (const variant of variants) {
        random -= (variant.weight || 1);
        if (random <= 0) {
          selectedVariant = variant;
          break;
        }
      }
      
      // Fallback to first variant if something goes wrong
      if (!selectedVariant) {
        selectedVariant = variants[0];
      }
    }

    // Preserve any UTM parameters
    const utmParams = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
    const preservedParams = utmParams
      .filter(param => params[param])
      .map(param => `${param}=${encodeURIComponent(params[param])}`)
      .join('&');
    
    let redirectUrl = selectedVariant.url;
    if (preservedParams) {
      redirectUrl += (redirectUrl.includes('?') ? '&' : '?') + preservedParams;
    }

    // 302 redirect (temporary) so we can change destinations
    return {
      statusCode: 302,
      headers: {
        'Location': redirectUrl,
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'X-Variant': selectedVariant.name  // For debugging
      },
      body: ''
    };

  } catch (error) {
    console.error('Router error:', error);
    return {
      statusCode: 500,
      body: 'Internal server error'
    };
  }
};
