import aiohttp
import asyncio
from config import Config
import datetime
import discord
import gspread
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
import re

CONFIG = Config()

PRIOR_NOTICE = datetime.timedelta(minutes=10) # 事前告知する時間

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
    "DE":"ブラックエルダー",
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
    "疾風ドレイク":"ジャイアントドレイク",
    "疾風ドレ":"ジャイアントドレイク",
    "大ドレイク":"ジャイアントドレイク",
    "大ドレ":"ジャイアントドレイク",
    "マーヨ":"ビッグフットマーヨ",
    "フェニ":"フェニックス",
}

BOSS_INTERVAL_MAP = {
    "バフォメット":False,
    "カーツ":datetime.timedelta(minutes=600),
    "ガーストロード":datetime.timedelta(minutes=180),
    "四賢者":datetime.timedelta(minutes=120),
    "ジャイアントガードアント":datetime.timedelta(minutes=120),
    "スピリッド":datetime.timedelta(minutes=180),
    "リカント":datetime.timedelta(minutes=480),
    "ネクロマンサー":False,
    "デスナイト":datetime.timedelta(minutes=420),
    "アルフィア":datetime.timedelta(minutes=240),
    "山賊の親分":datetime.timedelta(minutes=180),
    "ファウスト":datetime.timedelta(minutes=60),
    "ドッペルゲンガーボス":datetime.timedelta(minutes=240),
    "ジャイアントワーム":datetime.timedelta(minutes=120),
    "狂風のシャスキー":datetime.timedelta(minutes=120),
    "疾風のシャスキー":datetime.timedelta(minutes=120),
    "ブラックエルダー":datetime.timedelta(minutes=180),
    "ジャイアントクロコダイル":datetime.timedelta(minutes=180),
    "上ドレイク":datetime.timedelta(minutes=120),
    "下ドレイク":datetime.timedelta(minutes=120),
    "右ドレイク":datetime.timedelta(minutes=180),
    "中ドレイク":datetime.timedelta(minutes=180),
    "イフリート":datetime.timedelta(minutes=120),
    "ジャイアントドレイク":datetime.timedelta(minutes=180),
    "ビッグフットマーヨ":datetime.timedelta(minutes=180),
    "フェニックス":datetime.timedelta(minutes=420),
}

TARGET_MESSAGE = re.compile(r"^>\s*(\S+)\s*(\S+)?")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class BossTimeError(ValueError):
    pass

async def send_webhook(message):
    async with aiohttp.ClientSession() as session:
        wh = discord.Webhook.from_url(CONFIG.webhook, adapter=discord.AsyncWebhookAdapter(session))
        await wh.send(message)    

client = discord.Client()

@client.event
async def on_ready():
    print(__file__, 'Logged in as %s' % client.user.name)

@client.event
async def on_message(message):
    match_result = TARGET_MESSAGE.match(message.content)
    if match_result:
        target_name = match_result.group(1)
        boss_name = BOSS_ALIAS_MAP.get(target_name.upper(), target_name)
        try:
            interval_time = BOSS_INTERVAL_MAP[boss_name]
            if interval_time:
                try:
                    end_time = match_result.group(2)
                    now = datetime.datetime.now()
                    end = now
                    if end_time:
                        end = datetime.datetime.combine(now.today(), datetime.datetime.strptime(end_time, "%H:%M").time())
                        if now < end:
                            end -= datetime.timedelta(days=1)
                        elapsed_time = now - end
                        if interval_time < elapsed_time:
                            raise BossTimeError
                        interval_time -= elapsed_time
                    notify_time = interval_time - PRIOR_NOTICE if interval_time > PRIOR_NOTICE else interval_time
                    now += interval_time
                    creds = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scopes=SCOPES)
                    sheet = gspread.authorize(creds).open_by_key(CONFIG.gspread_key).sheet1
                    for cell in sheet.range('A2:A30'):
                        if boss_name == cell.value:
                            sheet.update_cell(cell.row, cell.col + 3, end.strftime("%Y/%m/%d %H:%M"))
                            format_cell_range(sheet, gspread.utils.rowcol_to_a1(cell.row, cell.col + 3), cellFormat(backgroundColor=color(0.94, 0.94, 0.94)))
                    await send_webhook("%s END" % boss_name)
                    text = "$natural in %d minutes send %sが%sに湧きます to <#592022570979688463>" % (round(notify_time.total_seconds() / 60), boss_name, re.sub(r'0(\d+)', r'\1', now.strftime("%H時%M分")))
                except ValueError:
                    text = "時間を指定する場合は 時:分 でお願いします"
                except BossTimeError:
                    text = "前回の出現時間より前の時間を指定することはできません"
            else:
                text = "%s は時間管理対象外です" % boss_name
        except KeyError:
            if boss_name == "無念":
                text = "無念です..."
            else:
                text = "%s は知らないボスです" % target_name
        await message.channel.send(text)

client.run(CONFIG.token)
