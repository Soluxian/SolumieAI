// DexieMod - Auto Private Room Bot
// Deploy: 1. discord.com/developers → New App "DexieMod" → Bot → Reset Token (paste below).
// 2. Invite: https://discord.com/api/oauth2/authorize?client_id=APP_ID&permissions=8&scope=bot%20applications.commands
// 3. Run: npm init -y &amp;&amp; npm i discord.js &amp;&amp; node dexiemod.js (token prompt)

// Config (update IDs)
const GUILD_ID = '837765697161265252';
const REQUESTS_CHAN = '1473982322499125258';
const CATEGORY_ID = '1473964764714504272';
const BOT_ID = 'YOUR_NEW_BOT_ID'; // From app

const { Client, GatewayIntentBits, PermissionsBitField } = require('discord.js');
const client = new Client({ 
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent]
});

client.on('ready', () =&gt; {
  console.log(`DexieMod online on ${client.user.tag}`);
});

client.on('messageCreate', async (msg) =&gt; {
  if (msg.channel.id !== REQUESTS_CHAN || !msg.content.includes('&lt;@YOUR_NEW_BOT_ID&gt;')) return; // Ping trigger
  if (msg.author.bot) return;

  const username = msg.author.username.replace(/[^a-zA-Z0-9]/g, ''); // Sanitize
  const userId = msg.author.id;

  try {
    const guild = client.guilds.cache.get(GUILD_ID);
    const category = guild.channels.cache.get(CATEGORY_ID);

    // Create channel
    const newChan = await guild.channels.create({
      name: `${username}-solumieai`,
      type: 0, // Text
      parent: CATEGORY_ID,
      topic: `Private chat with SolumieAI. Ping &lt;@1468433618178150573&gt; for responses! 👋`,
      permissionOverwrites: [
        {
          id: guild.id, // @everyone
          deny: [PermissionsBitField.Flags.ViewChannel]
        },
        {
          id: userId, // Requester
          allow: [PermissionsBitField.Flags.ViewChannel, PermissionsBitField.Flags.SendMessages, PermissionsBitField.Flags.ReadMessageHistory]
        },
        {
          id: BOT_ID, // Bot self
          allow: [PermissionsBitField.Flags.ViewChannel, PermissionsBitField.Flags.SendMessages, PermissionsBitField.Flags.ReadMessageHistory]
        },
        {
          id: '786107169078640650', // Solumie owner
          allow: [PermissionsBitField.Flags.ViewChannel, PermissionsBitField.Flags.SendMessages, PermissionsBitField.Flags.ReadMessageHistory, PermissionsBitField.Flags.ManageChannels]
        },
        {
          id: '1468433618178150573', // OpenClaw bot
          allow: [PermissionsBitField.Flags.ViewChannel, PermissionsBitField.Flags.SendMessages, PermissionsBitField.Flags.ReadMessageHistory]
        }
      ]
    });

    // Welcome msg
    await newChan.send(`Welcome to your private channel, &lt;@${userId}&gt;! Ping me anytime. 💜`);

    // Reply to request
    await msg.reply(`✅ Private channel created: ${newChan}! Refresh Discord. Perfs auto-set (View/Send/History). 😈`);

  } catch (err) {
    console.error(err);
    msg.reply('❌ Room create failed—perms? Check console.');
  }
});

const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
rl.question('Paste BOT TOKEN: ', (token) =&gt; {
  client.login(token).catch(console.error);
  rl.close();
});
