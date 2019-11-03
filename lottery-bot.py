from config import Config
import discord
import random

CONFIG = Config()

PARTICIPATED_EMOJI = "participated"

LOTTERY_EMOJI ="lottery"

client = discord.Client()

@client.event
async def on_ready():
    print(__file__, 'Logged in as %s' % client.user.name)

@client.event
async def on_raw_reaction_add(payload):
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    emoji = payload.emoji

    if message.author.id == payload.user_id and emoji.is_custom_emoji() and emoji.name == LOTTERY_EMOJI:
        for r in message.reactions:
            if r.custom_emoji and r.emoji.name == PARTICIPATED_EMOJI:
                users = await r.users().flatten()
                winner = random.choice(users)
                await message.channel.send("> " + message.content.replace("\n", "\n> ") + "\n当選者: " + winner.mention)
                break

client.run(CONFIG.token)
