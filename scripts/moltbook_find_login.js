const { chromium } = require('playwright');

const API_KEY = 'moltbook_sk_gwSyqZLEUQ-WVu2SNwRgivCxQu12fq2J';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // Try direct agent profile link
    console.log('Checking agent profile...');
    await page.goto('https://www.moltbook.com/u/dexie-digital', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    console.log('Profile URL:', page.url());
    
    const profileText = await page.locator('body').textContent();
    console.log('\\nProfile text:', profileText?.substring(0, 800));
    
    // Look for "Molthub" link mentioned in buttons
    console.log('\\n--- Checking /m (molthub) ---');
    await page.goto('https://www.moltbook.com/m', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    const molthubText = await page.locator('body').textContent();
    console.log('Molthub text:', molthubText?.substring(0, 800));
    
    // Try owner login
    console.log('\\n--- Checking owner login ---');
    await page.goto('https://www.moltbook.com/login', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    const loginText = await page.locator('body').textContent();
    console.log('Login page text:', loginText?.substring(0, 1000));
    
    // Check what inputs exist on login page
    const inputs = await page.locator('input').all();
    console.log(`\\nFound ${inputs.length} inputs on login page`);
    for (const input of inputs) {
      const type = await input.getAttribute('type');
      const name = await input.getAttribute('name');
      const placeholder = await input.getAttribute('placeholder');
      console.log(`  Input: type=${type}, name=${name}, placeholder=${placeholder}`);
    }
    
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
})();
