from config import Config
import discord
import random
import re

CONFIG = Config()

box = {}

async def reset(message, num):
    global box
    try:
        n = min(10000, int(num))
    except:
        n = 100
    tickets = list(range(1, n + 1))
    random.shuffle(tickets)
    box[message.channel] = tickets
    await message.channel.send('%sのくじをリセットしました（残り%d枚）' % (message.channel, len(tickets)))

async def lottery(message, num):
    global box
    try:
        n = max(int(num), 1)
    except:
        n = 1
    tickets = box.get(message.channel, None)
    if tickets:
        results = map(str, tickets[-n:])
        tickets = tickets[0:-n]
        await message.channel.send('抽選結果：%s （残り%d枚）' % (', '.join(results), len(tickets)))
        box[message.channel] = tickets[0:-n]
    else:
        await message.channel.send('くじがありません。「抽選リセット」でくじを補充してください')

async def selection(message, targets, *_):
    winner = random.choice(targets.strip().split())
    await message.channel.send('結果：%s' % winner)

COMMAND_MAP = {
    re.compile(r"^抽選\s*リセット\s*(\d+)$"): reset,
    re.compile(r"^抽選\s*(\d+)?$"): lottery,
    re.compile(r"^選択((\s+\S+)+)$"): selection,
}

client = discord.Client()

@client.event
async def on_ready():
    print(__file__, 'Logged in as %s' % client.user.name)

@client.event
async def on_message(message):
    for k, v in COMMAND_MAP.items():
        match_result = k.match(message.content)
        if match_result:
            await v(message, *match_result.groups())
            break

client.run(CONFIG.token)
