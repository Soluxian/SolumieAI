const { chromium } = require('playwright');

(async () => {
  // Launch browser in headful mode to see what's happening
  const browser = await chromium.launch({ headless: false, slowMo: 500 });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    console.log('Navigating to Moltbook...');
    await page.goto('https://www.moltbook.com/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    // Look for agent login/link
    const loginLinks = await page.$$('a');
    console.log('Links found:', await Promise.all(
      loginLinks.slice(0, 10).map(async link => ({
        text: await link.textContent(),
        href: await link.getAttribute('href')
      }))
    ));
    
    // Check for "submit" or "post" button
    const buttons = await page.$$('button');
    console.log('Buttons found:', await Promise.all(
      buttons.slice(0, 10).map(async btn => ({
        text: await btn.textContent(),
        type: await btn.getAttribute('type')
      }))
    ));
    
    // Wait to see the page
    await page.waitForTimeout(5000);
    
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
})();
