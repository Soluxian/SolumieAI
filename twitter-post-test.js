require('dotenv').config({ path: './secrets/twitter/.env' });
const { TwitterApi } = require('twitter-api-v2');

const client = new TwitterApi({
  appKey: process.env.TWITTER_CLIENT_ID,
  appSecret: process.env.TWITTER_CLIENT_SECRET,
  accessToken: process.env.TWITTER_ACCESS_TOKEN,
  accessSecret: process.env.TWITTER_ACCESS_SECRET,
});

async function postTest() {
  try {
    // Free tier write-only: Try post despite read fail
    const tweet = await client.v2.tweet('Dexie OpenClaw Twitter test! Moss gremlin VTuber loading... 🚀 #solumie #DexieAI');
    console.log('✅ Posted:', tweet.data.id, tweet.data.text);
  } catch (e) {
    console.error('❌ Post fail:', e.code || e.statusCode, e.message);
    if (e.data?.detail) console.error('Detail:', e.data.detail);
  }
}

postTest();