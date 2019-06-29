import discord
import re
import datetime


TARGET_MESSAGE = re.compile(r"^>\s*(\S+)\s*(\S+)?")

PRIOR_NOTICE = 10 # n分前に告知する

BOSS_ALIAS_MAP = {
        "MUNEN":"無念",
        "バフォ":"バフォメット",
        "ガースト":"ガーストロード",
        "カスパ":"四賢者",
        "カスパー":"四賢者",
        "GGA":"ジャイアントガードアント",
        "スピ":"スピリッド",
        "ネクロ":"ネクロマンサー",
        "DK":"デスナイト",
        "蜘蛛":"アルフィア",
        "山賊親分":"山賊の親分",
        "親分":"山賊の親分",
        "ボスクライン":"ファウスト",
        "クライン":"ファウスト",
        "ドッペ":"ドッペルゲンガーボス",
        "ドッペボス":"ドッペルゲンガーボス",
        "ワーム":"ジャイアントワーム",
        "赤シャスキー":"狂風のシャスキー",
        "赤シャス":"狂風のシャスキー",
        "赤":"狂風のシャスキー",
        "緑シャスキー":"疾風のシャスキー",
        "緑シャス":"疾風のシャスキー",
        "緑":"疾風のシャスキー",
        "BE":"ブラックエルダー",
        "ワニ":"ジャイアントクロコダイル",
        "クロコ":"ジャイアントクロコダイル",
        "上ドレ":"上ドレイク",
        "上":"上ドレイク",
        "下ドレ":"下ドレイク",
        "下":"下ドレイク",
        "右ドレ":"右ドレイク",
        "右":"右ドレイク",
        "中ドレ":"中ドレイク",
        "中":"中ドレイク",
        "イフ":"イフリート",
        "マーヨ":"ビッグフットマーヨ",
        "フェニ":"フェニックス",
        }

BOSS_INTERVAL_MAP = {
        "バフォメット":120,
        "カーツ":600,
        "ガーストロード":180,
        "四賢者":120,
        "ジャイアントガードアント":120,
        "スピリッド":180,
        "リカント":480,
        "ネクロマンサー":120,
        "デスナイト":420,
        "アルフィア":240,
        "山賊の親分":180,
        "ファウスト":60,
        "ドッペルゲンガーボス":240,
        "ジャイアントワーム":120,
        "狂風のシャスキー":120,
        "疾風のシャスキー":120,
        "ブラックエルダー":180,
        "ジャイアントクロコダイル":180,
        "上ドレイク":120,
        "下ドレイク":120,
        "右ドレイク":180,
        "中ドレイク":180,
        "イフリート":120,
        "ジャイアントドレイク":180,
        "ビッグフットマーヨ":180,
        "フェニックス":420,
        }

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    match_result = TARGET_MESSAGE.match(message.content)
    if match_result:
        target_name = match_result.group(1)
        boss_name = BOSS_ALIAS_MAP.get(target_name.upper(), target_name)
        interval_time = BOSS_INTERVAL_MAP.get(boss_name, False)
        if interval_time:
            try:
                end_time = match_result.group(2)
                now = datetime.datetime.now()
                if end_time:
                    end = datetime.datetime.combine(now.today(), datetime.datetime.strptime(end_time, "%H:%M").time())
                    if now < end:
                        raise ValueError
                    elapsed_time = round((now - end).total_seconds() / 60)
                    if interval_time < elapsed_time:
                        raise ValueError
                    interval_time -= elapsed_time
                    now = end
                notify_time = interval_time - PRIOR_NOTICE if interval_time > PRIOR_NOTICE else interval_time
                now += datetime.timedelta(minutes=interval_time)
                text = "$natural in %d minutes send %sが%sに沸きます to <#592022570979688463>" % (notify_time, boss_name, re.sub(r'0(\d+)', r'\1', now.strftime("%H時%M分")))
            except ValueError:
                text = "スミマセン、倒した時間は 時:分 で書いてください..."
        elif boss_name == "無念":
            text = "無念です..."
        else:
            text = "スミマセン、%s は知らないボスです..." % target_name
        print(text)
        await message.channel.send(text)

client.run("NTk0MTcxMzU2NTY4ODc5MTE1.XRYj9Q.h_e0AVb2iq3HBk-Cp4UWm7tXCLk")

