require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.DirectMessages,
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

client.once('ready', () => {
  console.log(`✅ RayMirror logged in as ${client.user.tag}`);
});

client.on('messageCreate', async (msg) => {
  if (msg.author.bot) return;
  console.log(`Ray msg from ${msg.author.tag}: ${msg.content}`);

  // Simple history (per user file)
  const userId = msg.author.id;
  const historyFile = `./ray-history/${userId}.json`;
  let history = [];
  try {
    const fs = require('fs');
    if (fs.existsSync(historyFile)) {
      history = JSON.parse(fs.readFileSync(historyFile, 'utf8'));
    }
  } catch (e) {}

  const messages = [...history.slice(-9), {role: 'user', content: msg.content}]; // last 5 exchanges

  const ollamaRes = await fetch('http://localhost:11434/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      model: 'smollm:135m',
      stream: false,
      messages: messages,
      options: {temperature: 0.8, top_p: 0.9}
    })
  }).then(r => r.json());

  let reply = ollamaRes.message.content || 'Ray vibe lost—retry.';
  reply = reply.slice(0, 1900); // Discord limit

  await msg.reply(reply);

  // Update history
  history.push({role: 'user', content: msg.content}, {role: 'assistant', content: reply});
  history = history.slice(-20); // keep 10 exchanges
  require('fs').writeFileSync(historyFile, JSON.stringify(history, null, 2));

  console.log(`Ray replied to ${msg.author.tag}`);
});

process.on('unhandledRejection', (error) => {
  console.error('Unhandled rejection:', error);
});

client.login(process.env.DISCORD_TOKEN).catch((error) => {
  console.error('Login failed:', error);
});
