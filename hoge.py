from config import Config
import discord

BOSS_CHARACTER_MAP = {
    #'バフォメット':'https://m-s-y.com/wp-content/uploads/2019/02/linem-baphomet.jpg',
    'カーツ':'https://m-s-y.com/wp-content/uploads/2019/02/linem-ka-tu.jpg',
    'ガーストロード':'https://m-s-y.com/wp-content/uploads/2019/02/linem-garst-road.jpg',
    '四賢者':'https://m-s-y.com/wp-content/uploads/2019/02/linem-casper.jpg',
    'ジャイアントガードアント':'https://m-s-y.com/wp-content/uploads/2019/02/linem-giant-guard-ant.jpg',
    'スピリッド':'https://m-s-y.com/wp-content/uploads/2019/02/linem-spilid.jpg',
    'リカント':'https://m-s-y.com/wp-content/uploads/2019/02/linem-licant.jpg',
    #'ネクロマンサー':'https://m-s-y.com/wp-content/uploads/2019/02/linem-necromancer.jpg',
    'デスナイト':'https://m-s-y.com/wp-content/uploads/2019/02/linem-dk.jpg',
    'アルフィア':'https://m-s-y.com/wp-content/uploads/2019/02/linem-alfia.jpg',
    '山賊の親分':'https://m-s-y.com/wp-content/uploads/2019/02/linem-bandit-boss.jpg',
    'ファウスト':'https://m-s-y.com/wp-content/uploads/2019/02/linem-faust.jpg',
    'ドッペルゲンガーボス':'https://m-s-y.com/wp-content/uploads/2019/02/linem-doppelganger-boss.jpg',
    'ジャイアントワーム':'https://m-s-y.com/wp-content/uploads/2019/02/linem-giant-worm.jpg',
    '狂風のシャスキー':'https://m-s-y.com/wp-content/uploads/2019/02/linem-kyouhu-shasky.jpg',
    '疾風のシャスキー':'https://m-s-y.com/wp-content/uploads/2019/02/linem-sppuu-shasky.jpg',
    'ブラックエルダー':'https://m-s-y.com/wp-content/uploads/2019/02/linem-great-black-elder.jpg',
    'ジャイアントクロコダイル':'https://m-s-y.com/wp-content/uploads/2019/02/linem-giant-crocodile.jpg',
    '上ドレイク':'https://m-s-y.com/wp-content/uploads/2019/02/linem-drake.jpg',
    '下ドレイク':'https://m-s-y.com/wp-content/uploads/2019/02/linem-drake.jpg',
    '右ドレイク':'https://m-s-y.com/wp-content/uploads/2019/02/linem-drake.jpg',
    '中ドレイク':'https://m-s-y.com/wp-content/uploads/2019/02/linem-drake.jpg',
    'イフリート':'https://m-s-y.com/wp-content/uploads/2019/02/linem-ifrit.jpg',
    'ジャイアントドレイク':'https://m-s-y.com/wp-content/uploads/2019/02/linem-sippu-no-giant-drake.jpg',
    'ビッグフットマーヨ':'https://m-s-y.com/wp-content/uploads/2019/02/linem-bigfoot-mayo.jpg',
    'フェニックス':'https://m-s-y.com/wp-content/uploads/2019/02/linem-pheniciks.jpg',
    'エンシェントジャイアント':'https://m-s-y.com/wp-content/uploads/2019/02/linem-ancient-giant.jpg',
    'モニターデーモン':'https://m-s-y.com/wp-content/uploads/2019/02/linem-daemon-monitor.jpg',
}

CONFIG = Config()

client = discord.Client()

@client.event
async def on_ready():
    print(__file__, 'Logged in as %s' % client.user.name)
    for channel in [i for i in client.get_all_channels() if i.id == CONFIG.dbm_proxy]:
        for boss_name, character_url in BOSS_CHARACTER_MAP.items():
            e = discord.Embed()
            e.set_author(name=boss_name, icon_url=character_url)
            message = await channel.send('>' + boss_name, embed=e)
            for emoji in ['⭕', '❌']:
                await message.add_reaction(emoji)


client.run(CONFIG.token)
