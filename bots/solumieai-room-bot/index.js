require('dotenv').config();
const { Client, GatewayIntentBits, ChannelType, PermissionFlagsBits, ThreadAutoArchiveDuration } = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

const REQUESTS_CHAN = process.env.REQUESTS_CHAN;
const SOLUMIEAI_ID = process.env.SOLUMIEAI_ID;
const CATEGORY_ID = process.env.SOLUMIEAI_CATEGORY;
const GUILD_ID = process.env.GUILD_ID;

client.once('ready', () => {
  console.log(`✅ SolumieAI Room Bot logged in as ${client.user.tag}`);
});

client.on('messageCreate', async (msg) => {
  if (msg.channel.id !== REQUESTS_CHAN || msg.author.bot) return;

  if (msg.mentions.has(SOLUMIEAI_ID)) {
    const requester = msg.author;
    const username = requester.username.replace(/[^a-z0-9]/gi, '').toLowerCase();
    const roomName = `${username}-solumieai`;

    try {
      const guild = await client.guilds.fetch(GUILD_ID);
      const category = await guild.channels.fetch(CATEGORY_ID);

      const room = await guild.channels.create({
        name: roomName,
        type: ChannelType.GuildText,
        parent: category,
        topic: 'Welcome to your private channel with SolumieAI! 👋 Ask Dexie anything.',
        rateLimitPerUser: 2,
        permissionOverwrites: [
          {
            id: guild.id, // @everyone
            deny: [PermissionFlagsBits.ViewChannel],
          },
          {
            id: requester.id,
            allow: [PermissionFlagsBits.ViewChannel, PermissionFlagsBits.SendMessages, PermissionFlagsBits.ReadMessageHistory],
          },
        ],
      });

      await msg.reply(`Hey <@${requester.id}>! 🎉 **Private room created:** ${room} <#${room.id}>\\n\\nChat with Dexie now—no perms needed! 😊`);

      console.log(`Room created for ${requester.tag}: <#${room.id}>`);
    } catch (error) {
      console.error('Room create fail:', error);
      msg.reply('Room create error—Sol check logs.');
    }
  }
});

client.login(process.env.DISCORD_TOKEN).catch(console.error);