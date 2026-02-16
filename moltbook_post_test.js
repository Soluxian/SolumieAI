const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // Go to main page and wait for API calls
    await page.goto('https://www.moltbook.com/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    // Get post URL from console network analysis
    // Based on patterns, likely endpoints:
    const endpoints = [
      '/api/v1/posts',
      '/api/posts', 
      '/api/agents/posts',
      '/api/feed/posts',
      '/graphql'  // could be GraphQL
    ];
    
    console.log('Page loaded. Checking for API patterns...');
    
    // Try to find the actual API by looking at network requests
    const pageContent = await page.evaluate(() => {
      // Look for any API configuration in the page
      return window.__NEXT_DATA__ || {};
    });
    
    console.log('Next.js data available:', Object.keys(pageContent).length > 0);
    if (pageContent.buildId) {
      console.log('Build ID:', pageContent.buildId);
    }
    
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
})();
