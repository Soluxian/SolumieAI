const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Listen to API calls
  page.on('request', request => {
    const url = request.url();
    if (url.includes('api') || url.includes('moltbook')) {
      console.log('API Request:', request.method(), url);
    }
  });
  
  page.on('response', async response => {
    const url = response.url();
    if (url.includes('api') || url.includes('moltbook')) {
      console.log('API Response:', response.status(), url);
      try {
        const text = await response.text();
        if (text.length < 500) {
          console.log('  Body:', text);
        }
      } catch (e) {
        // Ignore binary responses
      }
    }
  });
  
  try {
    await page.goto('https://www.moltbook.com/login', { waitUntil: 'networkidle', timeout: 30000 });
    
    // Wait for any API calls to complete
    await page.waitForTimeout(5000);
    
    // Try to access with API key
    console.log('\n--- Testing API key access ---');
    const response = await fetch('https://www.moltbook.com/api/agents/me', {
      headers: {
        'Authorization': 'Bearer moltbook_sk_gwSyqZLEUQ-WVu2SNwRgivCxQu12fq2J',
        'Content-Type': 'application/json'
      }
    }).catch(() => ({ status: 'network error' }));
    
    console.log('Agent API response:', response.status || response);
    
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
})();
