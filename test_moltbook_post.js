const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // Try to access Moltbook
    await page.goto('https://moltbook.com/login', { waitUntil: 'domcontentloaded' });
    console.log('Loaded login page');
    
    // Check if login form exists
    const hasForm = await page.$('input[type="password"]') !== null;
    console.log('Has login form:', hasForm);
    
    if (hasForm) {
      // Fill in credentials if we had them
      // await page.fill('input[type="email"]', '...');
      // await page.fill('input[type="password"]', '...');
      // await page.click('button[type="submit"]');
      // await page.waitForURL('**/dashboard');
      console.log('Login form present - need credentials');
    }
    
    // Check current URL
    console.log('Current URL:', page.url());
    
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
})();
