const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  try {
    await page.goto('https://www.moltbook.com/login');
    await page.waitForTimeout(3000);
    
    // Get page content
    const html = await page.content();
    console.log('Page loaded. Content snippet:');
    console.log(html.substring(0, 2000));
    
    // Try to find API docs or CSRF token
    const scripts = await page.$$eval('script', scripts => 
      scripts.map(s => s.src).filter(s => s.includes('moltbook'))
    );
    console.log('Moltbook scripts:', scripts);
    
    // Check for any API endpoints in page
    const links = await page.$$eval('a', links => 
      links.map(a => a.href).filter(h => h.includes('api'))
    );
    console.log('API links:', links.slice(0, 10));
    
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
})();