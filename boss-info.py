from config import Config
import discord
import re


CONFIG = Config()

BOSS_POINT_MAP = {
    'バフォメット':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-map-chaotic-temple-baphomet.jpg',
    'カーツ':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-map-ka_tsu.jpg',
    'ガーストロード':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-map-ga_sutoro_do.jpg',
    '四賢者':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-4kenja.jpg',
    'ジャイアントガードアント':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-giant-guard-ant.jpg',
    'スピリッド':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-spirits-ot-forrest.jpg',
    'リカント':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-rikanto.jpg',
    'ネクロマンサー':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-nekuromansa-mojanohaka.jpg',
    'デスナイト':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-nekuromansa-mojanohaka.jpg',
    'アルフィア':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-alfia.jpg',
    '山賊の親分':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-bandidboss.jpg',
    'ファウスト':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-fausuto.jpg',
    'ドッペルゲンガーボス':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-dopperugenga_boss.jpg',
    'ジャイアントワーム':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-heinec-miruwa_mu.jpg',
    '狂風のシャスキー':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-syasuki.jpg',
    '疾風のシャスキー':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-syasuki.jpg',
    'ブラックエルダー':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-blackelder2.jpg',
    'ジャイアントクロコダイル':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-rosasutou.jpg',
    '上ドレイク':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-doreiku.jpg',
    '下ドレイク':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-doreiku.jpg',
    '右ドレイク':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-doreiku.jpg',
    '中ドレイク':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-doreiku.jpg',
    'イフリート':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-kazan-fenikkusu-1.jpg',
    'ジャイアントドレイク':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-giantdoreiku.jpg',
    'ビッグフットマーヨ':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-orenseppeki.jpg',
    'フェニックス':'https://m-s-y.com/wp-content/uploads/2019/05/lineagem-boss-map-kazan-fenix.jpg',
}

BOSS_CHARACTER_MAP = {
    'バフォメット':'https://m-s-y.com/wp-content/uploads/2019/02/linem-baphomet.jpg',
    'カーツ':'https://m-s-y.com/wp-content/uploads/2019/02/linem-ka-tu.jpg',
    'ガーストロード':'https://m-s-y.com/wp-content/uploads/2019/02/linem-garst-road.jpg',
    '四賢者':'https://m-s-y.com/wp-content/uploads/2019/02/linem-casper.jpg',
    'ジャイアントガードアント':'https://m-s-y.com/wp-content/uploads/2019/02/linem-giant-guard-ant.jpg',
    'スピリッド':'https://m-s-y.com/wp-content/uploads/2019/02/linem-spilid.jpg',
    'リカント':'https://m-s-y.com/wp-content/uploads/2019/02/linem-licant.jpg',
    'ネクロマンサー':'https://m-s-y.com/wp-content/uploads/2019/02/linem-necromancer.jpg',
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
    'デーモン':'https://m-s-y.com/wp-content/uploads/2019/02/linem-daemon.jpg',
    'ゼニスクイーン':'https://m-s-y.com/wp-content/uploads/2019/02/linem-zenith-queen.jpg',
    'シアー':'https://m-s-y.com/wp-content/uploads/2019/02/linem-sheer.jpg',
    'ヴァンパイア':'https://m-s-y.com/wp-content/uploads/2019/02/linem-vampire.jpg',
    'ゾンビロード':'https://m-s-y.com/wp-content/uploads/2019/02/linem-zombi-road.jpg',
    'クーガー':'https://m-s-y.com/wp-content/uploads/2019/02/linem-cougar.jpg',
    'マミーロード':'https://m-s-y.com/wp-content/uploads/2019/02/linem-mummy-road.jpg',
    'アイリス':'https://m-s-y.com/wp-content/uploads/2019/02/linem-iris.jpg',
    'ハーピークイーン':'https://m-s-y.com/wp-content/uploads/2019/05/linem-harpy-queen.jpg',
    'グレートミノタウロス':'https://m-s-y.com/wp-content/uploads/2019/05/linem-great-minotaur.jpg',
    'オーガキング':'https://m-s-y.com/wp-content/uploads/2019/05/linem-ogre-king.jpg',
    'コカトリスキング':'https://m-s-y.com/wp-content/uploads/2019/05/linem-cockatrice-king.jpg',
    'ドレイクキング':'https://m-s-y.com/wp-content/uploads/2019/05/linem-drake-king.jpg',
}

BOSS_DROP_MAP = {
    "バフォメット":"バフォメットアーマー\nバフォメットスタッフ\n希少級製作秘法書",
    "カーツ":"カーツソード\n反逆者のシールド\n魔法書(キャンセレーション)\nカーツアーマー\nカーツヘルム\nカーツブーツ\nカーツグローブ\n希少級製作秘法書\nゴールドプレート",
    "ガーストロード":"魔法書(キャンセレーション)\n希少級製作秘法書\nオリハルコンプレート",
    "四賢者":"セマの帽子\nバルタザールの帽子\nメルキオールの帽子\nカスパーの帽子\n希少級製作秘法書",
    "ジャイアントガードアント":"希少級製作秘法書",
    "スピリッド":"希少級製作秘法書",
    "リカント":"希少級製作秘法書\nサイレンスソード",
    "ネクロマンサー":"希少級製作秘法書",
    "デスナイト":"技術書(カウンターバリア)\nデスナイトフレイムブレード\nロンドゥデュアルブレード\nデスナイトアーマー\nデスナイトヘルム\nデスナイトブーツ\nデスナイトグローブ\n希少級製作秘法書\nプラチナプレート",
    "アルフィア":"魔法書(イミューントゥハーム)\n魔法書(フォグオブスリーピング)\n希少級製作秘法書",
    "山賊の親分":"希少級製作秘法書\n魔法書(ホーリーウォーク)",
    "ファウスト":"レイジングウィンド\nフリージングランサー\nエンジェルスタッフ\nマナバゼラード\nライトニングエッジ\nディストラクション\nエンジェルスレイヤー\n輝く古代のネックレス(刻印)\n希少級製作秘法書",
    "ドッペルゲンガーボス":"ドッペルゲンガーアミュレット\nドッペルゲンガーの右リング\nドッペルゲンガーの左リング\n希少級製作秘法書",
    "ジャイアントワーム":"英雄製作秘法書\n精霊の水晶(ポルートウォーター)\n希少級製作秘法書\n闇精霊の水晶(ファイナルバーン)\nブルードラゴンの鱗",
    "狂風のシャスキー":"希少級製作秘法書\nホワイトドラゴンの鱗",
    "疾風のシャスキー":"希少級製作秘法書\nホワイトドラゴンの鱗",
    "ブラックエルダー":"ダークエルダーローブ\nダークエルダーサンダル\n希少級製作秘法書",
    "ジャイアントクロコダイル":"魔力のグローブ\n希少級製作秘法書",
    "上ドレイク":"オリハルコンダガー\n希少級製作秘法書\nグリーンドラゴンの鱗",
    "下ドレイク":"オリハルコンダガー\n希少級製作秘法書\nグリーンドラゴンの鱗",
    "右ドレイク":"オリハルコンダガー\n希少級製作秘法書\nグリーンドラゴンの鱗",
    "中ドレイク":"オリハルコンダガー\n希少級製作秘法書\nグリーンドラゴンの鱗",
    "イフリート":"滅魔のプレートメイル\n技術書(プリング)\nイフリートの魔力アミュレット\n魔王のリング\n英雄製作秘法書\n魔法書(イミューントゥハーム)\n精霊の水晶(ソウルオブフレイム)\n希少級製作秘法書",
    "ジャイアントドレイク":"魔法書(アブソルートバリア)\n滅魔のレザーアーマー\nオリハルコンダガー\nドレイクレザーベルト\n英雄製作秘法書\n腕力のブーツ\n希少級製作秘法書\nグリーンドラゴンの鱗",
    "ビッグフットマーヨ":"滅魔のスケイルメイル\n精霊の水晶(エルヴンウィド)\nマーヨの氷のブーツ\n英雄製作秘法書\n魔法書(アイススパイク)",
    "フェニックス":"魔法書(メテオストライク)\n伝説製作秘法書\n滅魔のローブ\n魔法書(ファイアーストーム)\n魔法書(エクスカリバー)\nフェニックスウィングガーダー\n魔王のリング\n英雄製作秘法書\n精霊の水晶(ソウルオブフレイム)\n希少級製作秘法書\nレッドドラゴンの鱗",
    "エンシェントジャイアント":"闇精霊の水晶(アーマーブレイク)\n古代巨人のリング\nタイタンベルト",
    "モニターデーモン":"魔法書(メテオストライク)\n闇精霊の水晶(シャドウショック)\n伝説製作秘法書\nデーモンの息吹\nデーモンスタッフ\nデーモンアーマー\nデーモンブーツ\nデーモングローブ\n英雄製作秘法書\nデーモンヘルム\nパワーグローブ\n希少級製作秘法書",
    "デーモン":"魔法書(メテオストライク)\n闇精霊の水晶(シャドウショック)\n伝説製作秘法書\nデーモンの息吹\nデーモンスタッフ\nデーモンアーマー\nデーモンブーツ\nデーモングローブ\nデーモンヘルム\n英雄製作秘法書\n技術教本 (ダッシュ)\nパワーグローブ\n希少級製作秘法書",
    "ゼニスクイーン":"ゼニスのリング\n英雄製作秘法書\n魔法書(イミューントゥハーム)\n技術教本(魔法弾：グラブ)\n封印された傲慢の塔1階テレポートアミュレット",
    "シアー":"魔法書(キャンセレーション)\nシアーの心眼\n英雄製作秘法書\n技術教本 (ブレイク：イミューントゥハーム)\n封印された傲慢の塔2階テレポートアミュレット",
    "ヴァンパイア":"魔法書(ファイアーストーム)\nヴァンパイアマント\n英雄製作秘法書\n技術教本 (ブレイク：アースバインド)\nシルバーマント\n封印された傲慢の塔3階テレポートアミュレット",
    "ゾンビロード":"激昂の グローブ\n神聖な腕力のリング\n魔法書(オラクル)\n英雄製作秘法書\n技術教本 (魔法弾：サイレンス)\n封印された祝福付与スクロール\n血濡れた包帯\nプラチナプレート\n封印された傲慢の塔4階テレポートアミュレット",
    "クーガー":"闇精霊の水晶(アーマーブレイク)\nダークネスデュアルブレード\n英雄製作秘法書\nクーガーの牙\nプラチナプレート\n封印された傲慢の塔5階テレポートアミュレット",
    "マミーロード":"マミーロードクラウン\nディープインパクト\n技術教本 (魔法弾：スタン)\n神聖な機敏のリング\n闇精霊の水晶(シャドウマーキング)\n英雄製作秘法書\n精霊の水晶(アースバインド)\nゴールドプレート\n封印された傲慢の塔6階テレポートアミュレット",
    "アイリス":"神聖な機敏のゲートル\n伝説製作秘法書\nマスターピースライフル\nアイリスのアミュレット\n英雄製作秘法書\n精霊の水晶(ポルートウォーター)\n技術教本 (死のスナイピング)\n希少級製作秘法書\n魔法書(アイススパイク)\n封印された傲慢の塔7階テレポートアミュレット",
    "ハーピークイーン":"精霊の水晶(トリプルアップ)\n精霊の水晶(ソウルバリア)\n魔法書(アブソルートバリア)\n伝説製作秘法書\n歴史書第1章の袋\n封印されたエンシェントローブ\n封印された英雄防具製作秘法書\n[変身カード]ハーピー\n希少級製作秘法書",
    "グレートミノタウロス":"技術教本(ブレイク：アブソルートバリア)\n技術書(カウンターバリアー：ベテラン)\n魔法書(インペリアルコール)\n伝説製作秘法書\n歴史書第5章の袋\n封印されたエンシェントプレートメイル\n封印された英雄防具製作秘法書",
    "オーガキング":"オーガキングのベルト\n暗黒技術書(リミットカバー：アベンジャー)\n暗黒技術書(ダークスタン：アベンジャー)\n伝説製作秘法書\n歴史書第4章の袋\n封印されたエンシェントプレートメイル\n封印された英雄防具製作秘法書",
    "コカトリスキング":"ドラゴンナイトの書版(サンダーグラブ：インパクト)\nドラゴンナイトの書版(ピア：インパクト)\nドラゴンナイトの書版(カウンターアサルト)\n伝説製作秘法書\n歴史書第2章の袋\n封印されたエンシェントスケイルメイル\n封印された英雄防具製作秘法書\n希少級製作秘法書\n[マジックドールカード]コカトリス",
    "ドレイクキング":"技術書(クイックリカバリー)\n闇精霊の水晶(ルシファー)\n闇精霊の水晶(シャドウショック)\n伝説製作秘法書\n歴史書第3章の袋\n封印されたエンシェントレザーアーマー\n封印された英雄防具製作秘法書",
}

TARGET_MESSAGE = re.compile(r'^(.+)が.+に湧きます')

client = discord.Client()


@client.event
async def on_ready():
    print(__file__, 'Logged in as %s' % client.user.name)


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if message.channel.id != CONFIG.dbm_register:
        return

    match_result = TARGET_MESSAGE.match(message.content)
    if not match_result:
        return

    boss_name = match_result.group(1)
    drop_info = BOSS_DROP_MAP.get(boss_name)
    if drop_info is None:
        return

    e = discord.Embed(title=boss_name + ' の情報', description=drop_info)
    map_url = BOSS_POINT_MAP.get(boss_name, False)
    if map_url:
        e.set_image(url=map_url)
    character_url = BOSS_CHARACTER_MAP.get(boss_name, False)
    if character_url:
        e.set_thumbnail(url=character_url)
    for channel in [i for i in client.get_all_channels() if i.id == CONFIG.dbm_notify]:
        m = await channel.send('```' + message.content + '```', embed=e)
        for emoji in ['⭕', '❌']:
            await m.add_reaction(emoji)


client.run(CONFIG.token)
