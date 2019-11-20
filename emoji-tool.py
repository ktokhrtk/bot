from config import Config
import discord
import functools
import random
import pytz
import re


CONFIG = Config()

client = discord.Client()


async def lottery(payload):
    await m_lottery(payload)


async def m_lottery(payload):
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if message.author.id == payload.user_id:
        users = []
        for r in [i for i in message.reactions if i.custom_emoji and (i.emoji.name == 'participated' or i.emoji.name == 'm_participated')]:
            users += await r.users().flatten()
        winner = random.choice(list(set(users)))
        e = discord.Embed(description=message.clean_content)
        e.set_author(name=message.author.nick + message.created_at.replace(tzinfo=pytz.utc).astimezone().strftime(' %Y/%m/%d %H:%M:%S'))
        await message.channel.send('当選者 ' + winner.mention, embed=e)


async def m_distribution(payload):
    receipt_emoji = next(iter([i for i in client.emojis if i.name == 'm_receipt']))
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if message.author.id == payload.user_id:
        users = []
        for r in [i for i in message.reactions if i.custom_emoji and (i.emoji.name == 'participated' or i.emoji.name == 'm_participated')]:
            users += await r.users().flatten()
        text = "分配を受け取った人は%sをリアクションしてください\n" % receipt_emoji
        for user in set(users):
            text += user.mention + "\n"
        e = discord.Embed(description=message.clean_content)
        e.set_author(name=message.author.nick + message.created_at.replace(tzinfo=pytz.utc).astimezone().strftime(' %Y/%m/%d %H:%M:%S'))
        m = await message.channel.send(text, embed=e)
        await m.add_reaction(receipt_emoji)


async def m_receipt(payload):
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    user = client.get_user(payload.user_id)
    if user:
        await message.edit(content=re.sub(r"^%s$" % user.mention.replace('@', '@!'), r"~~\g<0>~~", message.content, flags=re.M))


@client.event
async def on_ready():
    print(__file__, 'Logged in as %s' % client.user.name)


@client.event
async def on_raw_reaction_add(payload):
    await eval(payload.emoji.name + '(payload)')


client.run(CONFIG.token)
