const { chromium } = require('playwright');

const API_KEY = 'moltbook_sk_gwSyqZLEUQ-WVu2SNwRgivCxQu12fq2J';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Intercept all API calls
  const apiCalls = [];
  page.on('request', request => {
    const url = request.url();
    if (url.includes('moltbook') && !url.includes('_next') && !url.includes('.css') && !url.includes('.js')) {
      apiCalls.push({ url, method: request.method(), headers: request.headers() });
    }
  });
  
  try {
    // Navigate to login
    await page.goto('https://www.moltbook.com/login', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    
    console.log('API calls detected:', apiCalls.slice(-10));
    
    // Check what inputs are on the page
    const inputs = await page.$$eval('input', inputs => 
      inputs.map(i => ({ type: i.type, name: i.name, id: i.id }))
    );
    console.log('Form inputs:', inputs);
    
    // Try using the platform
    // Look for an agent login vs human login difference
    const links = await page.$$eval('a', links => 
      links.map(a => ({ text: a.textContent, href: a.href })).filter(l => l.text?.includes('agent') || l.text?.includes('Agent'))
    );
    console.log('Agent links:', links);
    
    // Save cookies to check auth
    const storage = await context.storageState();
    console.log('Storage state has cookies:', storage.cookies.length > 0);
    
  } catch (e) {
    console.error('Error:', e.message);
    console.error(e.stack);
  }
  
  await browser.close();
})();
