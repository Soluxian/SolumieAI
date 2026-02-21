require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

client.once('ready', () => {
  console.log(`✅ RayMirror logged in as ${client.user.tag}`);
});

client.on('messageCreate', async (msg) => {
  if (msg.author.bot || !msg.content.startsWith('!ray')) return;
  console.log(`!ray cmd from ${msg.author.tag}: ${msg.content}`);

  const args = msg.content.slice(5).trim().split(/ +/);
  const command = args.shift()?.toLowerCase();

  if (command === 'yo') {
    msg.reply("Yo, what's good? Mirror Ray here—hit me.");
  } else if (command === 'mirror') {
    msg.reply(`Ray vibe: ${args.join(' ')} Sounds like me already.`);
  } else {
    msg.reply('Ray style: Chill af. Say !ray yo or !ray mirror [vibe]. Drop Ray quotes to train.');
  }
});

process.on('unhandledRejection', (error) => {
  console.error('Unhandled rejection:', error);
});

client.login(process.env.DISCORD_TOKEN).catch((error) => {
  console.error('Login failed:', error);
});
