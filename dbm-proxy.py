from config import Config
import datetime
import discord
import re


CONFIG = Config()

TARGET_MESSAGE = re.compile(r'\W*(.+)が(\d+時\d+分\d+秒)に湧きます')

client = discord.Client()


async def proxy_default(payload):
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    for channel in [i for i in client.get_all_channels() if i.id == CONFIG.dbm_register]:
        await channel.send(message.content)


async def proxy_from_notify(payload):
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    match_result = TARGET_MESSAGE.match(message.content)
    if not match_result:
        return

    boss_name = match_result.group(1)
    boss_time = datetime.datetime.strptime(match_result.group(2), '%H時%M分%S秒')
    emoji = payload.emoji.name
    text = ''
    if emoji == '⭕':
        text = ">%s" % boss_name
    elif emoji == '❌':
        text = "?%s %s" % (boss_name, boss_time.strftime('%H:%M:%S'))
    
    for channel in [i for i in client.get_all_channels() if i.id == CONFIG.dbm_register]:
        await channel.send(text)


PROXY_CHANNEL_MAP = {
    CONFIG.dbm_notify:proxy_from_notify,
    CONFIG.dbm_proxy:proxy_default,
}


@client.event
async def on_ready():
    print(__file__, 'Logged in as %s' % client.user.name)


@client.event
async def on_raw_reaction_add(payload):
    if client.get_user(payload.user_id).bot:
        return

    func = PROXY_CHANNEL_MAP.get(payload.channel_id, False)
    if func:
        await func(payload)


client.run(CONFIG.token)
