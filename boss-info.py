from config import Config
import discord
import re

CONFIG = Config()

BOSS_INTERVAL_MAP = {
    "バフォメット":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-map-chaotic-temple-baphomet.jpg",
    "カーツ":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-map-ka_tsu.jpg",
    "ガーストロード":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-map-ga_sutoro_do.jpg",
    "四賢者":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-4kenja.jpg",
    "ジャイアントガードアント":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-giant-guard-ant.jpg",
    "スピリッド":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-spirits-ot-forrest.jpg",
    "リカント":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-rikanto.jpg",
    "ネクロマンサー":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-nekuromansa-mojanohaka.jpg",
    "デスナイト":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-nekuromansa-mojanohaka.jpg",
    "アルフィア":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-alfia.jpg",
    "山賊の親分":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-bandidboss.jpg",
    "ファウスト":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-fausuto.jpg",
    "ドッペルゲンガーボス":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-dopperugenga_boss.jpg",
    "ジャイアントワーム":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-heinec-miruwa_mu.jpg",
    "狂風のシャスキー":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-syasuki.jpg",
    "疾風のシャスキー":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-syasuki.jpg",
    "ブラックエルダー":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-blackelder2.jpg",
    "ジャイアントクロコダイル":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-rosasutou.jpg",
    "上ドレイク":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-doreiku.jpg",
    "下ドレイク":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-doreiku.jpg",
    "右ドレイク":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-doreiku.jpg",
    "中ドレイク":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-doreiku.jpg",
    "イフリート":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-kazan-fenikkusu-1.jpg",
    "ジャイアントドレイク":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-giantdoreiku.jpg",
    "ビッグフットマーヨ":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-orenseppeki.jpg",
    "フェニックス":"https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-kazan-fenix.jpg",
}

TARGET_MESSAGE = re.compile(r"^(.+)が\d+時\d+分に湧きます")

client = discord.Client()

@client.event
async def on_ready():
    print(__file__, 'Logged in as %s' % client.user.name)

@client.event
async def on_message(message):
    match_result = TARGET_MESSAGE.match(message.content)
    if match_result:
        boss_name = match_result.group(1)
        map_url = BOSS_INTERVAL_MAP.get(boss_name, False)
        if map_url:
            e = discord.Embed()
            e.set_image(url=map_url)
            await message.channel.send('', embed=e)

client.run(CONFIG.token)
