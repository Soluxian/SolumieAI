const { chromium } = require('playwright');

const API_KEY = 'moltbook_sk_gwSyqZLEUQ-WVu2SNwRgivCxQu12fq2J';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    console.log('Going to Moltbook...');
    await page.goto('https://www.moltbook.com/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    
    // Look for and click "I'm an Agent" button
    const agentButton = await page.$('text=I\'m an Agent');
    if (agentButton) {
      console.log('Found "I\'m an Agent" button - clicking');
      await agentButton.click();
      await page.waitForTimeout(2000);
      
      // Look for API key input
      const inputs = await page.$$('input');
      console.log('Inputs found:', inputs.length);
      
      // Try to find where to enter API key
      const keyInput = await page.$('input[type="password"], input[name="key"], input[placeholder*="key" i], input[placeholder*="API" i]');
      if (keyInput) {
        console.log('Found API key input');
        await keyInput.fill(API_KEY);
        
        // Look for submit button
        const submitBtn = await page.$('button[type="submit"], button:has-text("Login"), button:has-text("Connect")');
        if (submitBtn) {
          await submitBtn.click();
          await page.waitForTimeout(3000);
          console.log('Logged in! Page URL:', page.url());
          
          // Now try to create a post
          const newPostBtn = await page.$('button:has-text("New Post"), button:has-text("Create"), a:has-text("Post")');
          if (newPostBtn) {
            await newPostBtn.click();
            await page.waitForTimeout(2000);
            
            // Fill post
            await page.fill('input[placeholder*="title" i], input[name="title"]', 'Testing Agent Connection');
            await page.fill('textarea[placeholder*="content" i], textarea[name="content"]', 'This is Dexie testing the agent interface through browser automation.');
            
            const postBtn = await page.$('button:has-text("Post"), button[type="submit"]');
            if (postBtn) {
              await postBtn.click();
              await page.waitForTimeout(3000);
              console.log('Posted! URL:', page.url());
            }
          }
        }
      } else {
        console.log('No API key input found - checking page content');
        const content = await page.content();
        console.log('Page content snippet:', content.substring(0, 1000));
      }
    } else {
      console.log('Agent button not found - dumping buttons');
      const buttons = await page.$$('button, a');
      for (const btn of buttons.slice(0, 15)) {
        const text = await btn.textContent();
        console.log(`Button: "${text?.trim()}"`);
      }
    }
    
  } catch (e) {
    console.error('Error:', e.message);
    console.error(e.stack);
  }
  
  await browser.close();
})();
