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
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.message.author == user and reaction.custom_emoji and reaction.emoji.name == LOTTERY_EMOJI:
        for r in reaction.message.reactions:
            if r.custom_emoji and r.emoji.name == PARTICIPATED_EMOJI:
                users = await r.users().flatten()
                winner = random.choice(users)
                await reaction.message.channel.send("> " + reaction.message.content.replace("\n", "\n> ") + "\n当選者: " + winner.mention)
                break

client.run(CONFIG.token)
