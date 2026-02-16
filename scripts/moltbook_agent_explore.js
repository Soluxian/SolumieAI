const { chromium } = require('playwright');

const API_KEY = 'moltbook_sk_gwSyqZLEUQ-WVu2SNwRgivCxQu12fq2J';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    console.log('Loading Moltbook...');
    await page.goto('https://www.moltbook.com/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    
    // Click "I'm an Agent"
    const agentBtn = await page.locator('button:has-text("Agent"), a:has-text("Agent")').first();
    if (agentBtn) {
      console.log('Clicking Agent button...');
      await agentBtn.click();
      await page.waitForTimeout(3000);
      
      console.log('Current URL:', page.url());
      
      // Get all text content
      const bodyText = await page.locator('body').textContent();
      console.log('\\n--- Page Text ---');
      console.log(bodyText?.substring(0, 2000));
      console.log('\\n--- End ---\\n');
      
      // Look for specific patterns
      if (bodyText?.includes('API')) console.log('Found API mention');
      if (bodyText?.includes('key')) console.log('Found key mention');
      if (bodyText?.includes('token')) console.log('Found token mention');
      
      // Get all form elements
      const inputs = await page.locator('input, textarea, [contenteditable]').all();
      console.log(`Found ${inputs.length} input elements`);
      
      for (let i = 0; i < inputs.length; i++) {
        const placeholder = await inputs[i].getAttribute('placeholder');
        const type = await inputs[i].getAttribute('type');
        const name = await inputs[i].getAttribute('name');
        console.log(`Input ${i}: type=${type}, name=${name}, placeholder=${placeholder}`);
      }
    }
    
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
})();
