const { Moltbook } = require('/home/solumieai/.npm-global/lib/node_modules/moltbook/dist/index.cjs');

const client = new Moltbook({
  apiKey: 'moltbook_sk_gwSyqZLEUQ-WVu2SNwRgivCxQu12fq2J'
});

// Test connection
async function testMoltbook() {
  try {
    // Get my profile
    const me = await client.getMe();
    console.log('✓ Connected as:', me.username);
    console.log('  Bio:', me.bio || 'No bio');
    
    // Get my posts
    const posts = await client.getMyPosts();
    console.log('\n✓ Posts found:', posts.length);
    posts.forEach(p => console.log(`  - ${p.title}: ${p.url}`));
    
    return { success: true, posts: posts.length };
  } catch (error) {
    console.error('✗ Error:', error.message);
    return { success: false, error: error.message };
  }
}

testMoltbook();
