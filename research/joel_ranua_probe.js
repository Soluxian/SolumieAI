const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  const results = {
    timestamp: new Date().toISOString(),
    searches: []
  };
  
  // Search 1: Business registrations
  await page.goto('https://www.google.com/search?q=Joel+Ranua+Electronic+Home+Systems+Nimbus+360');
  await page.waitForLoadState('networkidle');
  const results1 = await page.$$eval('div.g h3', els => els.slice(0,5).map(e => ({title: e.innerText, link: e.closest('a')?.href})));
  results.searches.push({query: 'Joel Ranua EHS Nimbus', results: results1});
  
  // Search 2: Hawaii property
  await page.goto('https://www.google.com/search?q=Joel+Ranua+Kuki%27o+Hawaii+property');
  await page.waitForLoadState('networkidle');
  const results2 = await page.$$eval('div.g h3', els => els.slice(0,5).map(e => ({title: e.innerText, link: e.closest('a')?.href})));
  results.searches.push({query: 'Joel Ranua Kuki Hawaii', results: results2});
  
  // Search 3: LinkedIn/professional
  await page.goto('https://www.google.com/search?q=Joel+Ranua+surveillance+AV+integration+installer');
  await page.waitForLoadState('networkidle');
  const results3 = await page.$$eval('div.g h3', els => els.slice(0,5).map(e => ({title: e.innerText, link: e.closest('a')?.href})));
  results.searches.push({query: 'Joel Ranua surveillance AV', results: results3});
  
  console.log(JSON.stringify(results, null, 2));
  await browser.close();
})();
