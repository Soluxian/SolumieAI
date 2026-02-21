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
    const tweet = await client.v2.tweet('Dexie test tweet from OpenClaw! 🚀 #VTuberLive');
    console.log('Posted:', tweet.data.text, tweet.data.id);
  } catch (e) {
    console.error('Error:', e);
  }
}

postTest();