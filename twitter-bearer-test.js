require('dotenv').config({ path: './secrets/twitter/.env' });
const { TwitterApi } = require('twitter-api-v2');

const client = new TwitterApi(process.env.TWITTER_BEARER_TOKEN);

async function testBearer() {
  try {
    const user = await client.v2.me({ asApp: true });
    console.log('Bearer read OK - User:', user.data.username);
    
    const timeline = await client.v2.userTimeline(user.data.id, { max_results: 5 });
    console.log('Recent tweets:', timeline.data.map(t => t.text.slice(0,50) + '...'));
  } catch (e) {
    console.error('Bearer fail:', e.code, e.message);
  }
}

testBearer();