from config import Config
import datetime
import discord
import gspread
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
import re


CONFIG = Config()

PRIOR_NOTICE = datetime.timedelta(minutes=10) # 事前告知する時間

ACCEPT_INTERVAL = datetime.timedelta(seconds=60) # 入力を許可する間合い

BOSS_ALIAS_MAP = {
    'MUNEN':'無念',
    'バフォ':'バフォメット',
    'ガースト':'ガーストロード',
    'カスパ':'四賢者',
    'カスパー':'四賢者',
    'GGA':'ジャイアントガードアント',
    'スピ':'スピリッド',
    'ネクロ':'ネクロマンサー',
    'DK':'デスナイト',
    '蜘蛛':'アルフィア',
    '山賊親分':'山賊の親分',
    '親分':'山賊の親分',
    'ボスクライン':'ファウスト',
    'クライン':'ファウスト',
    'ドッペ':'ドッペルゲンガーボス',
    'ドッペボス':'ドッペルゲンガーボス',
    'ワーム':'ジャイアントワーム',
    '赤シャスキー':'狂風のシャスキー',
    '赤シャス':'狂風のシャスキー',
    '赤':'狂風のシャスキー',
    '緑シャスキー':'疾風のシャスキー',
    '緑シャス':'疾風のシャスキー',
    '緑':'疾風のシャスキー',
    'BE':'ブラックエルダー',
    'DE':'ブラックエルダー',
    'ワニ':'ジャイアントクロコダイル',
    'クロコ':'ジャイアントクロコダイル',
    '上ドレ':'上ドレイク',
    '上':'上ドレイク',
    '下ドレ':'下ドレイク',
    '下':'下ドレイク',
    '右ドレ':'右ドレイク',
    '右':'右ドレイク',
    '中ドレ':'中ドレイク',
    '中':'中ドレイク',
    'イフ':'イフリート',
    '疾風ドレイク':'ジャイアントドレイク',
    '疾風ドレ':'ジャイアントドレイク',
    '大ドレイク':'ジャイアントドレイク',
    '大ドレ':'ジャイアントドレイク',
    'マーヨ':'ビッグフットマーヨ',
    'フェニ':'フェニックス',
    'AG':'エンシェントジャイアント',
    'ジャイアン':'エンシェントジャイアント',
    '青閣下':'モニターデーモン',
    '閣下':'デーモン',
}

BOSS_INTERVAL_MAP = {
    'バフォメット':False,
    'カーツ':datetime.timedelta(minutes=600),
    'ガーストロード':datetime.timedelta(minutes=180),
    '四賢者':datetime.timedelta(minutes=120),
    'ジャイアントガードアント':datetime.timedelta(minutes=120),
    'スピリッド':datetime.timedelta(minutes=180),
    'リカント':datetime.timedelta(minutes=480),
    'ネクロマンサー':False,
    'デスナイト':datetime.timedelta(minutes=420),
    'アルフィア':datetime.timedelta(minutes=240),
    '山賊の親分':datetime.timedelta(minutes=180),
    'ファウスト':datetime.timedelta(minutes=60),
    'ドッペルゲンガーボス':datetime.timedelta(minutes=240),
    'ジャイアントワーム':datetime.timedelta(minutes=120),
    '狂風のシャスキー':datetime.timedelta(minutes=120),
    '疾風のシャスキー':datetime.timedelta(minutes=120),
    'ブラックエルダー':datetime.timedelta(minutes=180),
    'ジャイアントクロコダイル':datetime.timedelta(minutes=180),
    '上ドレイク':datetime.timedelta(minutes=120),
    '下ドレイク':datetime.timedelta(minutes=120),
    '右ドレイク':datetime.timedelta(minutes=180),
    '中ドレイク':datetime.timedelta(minutes=180),
    'イフリート':datetime.timedelta(minutes=120),
    'ジャイアントドレイク':datetime.timedelta(minutes=180),
    'ビッグフットマーヨ':datetime.timedelta(minutes=180),
    'フェニックス':datetime.timedelta(minutes=415),
    'エンシェントジャイアント':datetime.timedelta(minutes=300),
    'モニターデーモン':datetime.timedelta(minutes=420),
    'デーモン':False,
}

TARGET_MESSAGE = re.compile(r'^(>|\?)\s*(\S+)\s*(\S+)?')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

TIME_FORMATS = ['%H:%M', '%H:%M:%S']

LATEST_INPUT_MAP = {}

class BossTimeError(ValueError):
    pass

client = discord.Client()


@client.event
async def on_ready():
    print(__file__, 'Logged in as %s' % client.user.name)


@client.event
async def on_message(message):
    if message.channel.id != CONFIG.dbm_register:
        return

    match_result = TARGET_MESSAGE.match(message.content)
    if not match_result:
        return

    killed = match_result.group(1) != '?'
    target_name = match_result.group(2)
    boss_name = BOSS_ALIAS_MAP.get(target_name.upper(), target_name)
    try:
        interval_time = BOSS_INTERVAL_MAP[boss_name]
        if interval_time:
            try:
                end_time = str(match_result.group(3)).replace(';', ':')
                now = datetime.datetime.now()
                end = now
                if end_time:
                    time_format = end_time.count(':') - 1
                    if time_format >= 0:
                        end = datetime.datetime.combine(now.today(), datetime.datetime.strptime(end_time, TIME_FORMATS[time_format]).time())
                        if now < end:
                            end -= datetime.timedelta(days=1)
                        elapsed_time = now - end
                        if interval_time < elapsed_time:
                            raise BossTimeError
                        interval_time -= elapsed_time
                notify_time = interval_time - PRIOR_NOTICE if interval_time > PRIOR_NOTICE else interval_time
                latest_input = LATEST_INPUT_MAP.get(boss_name, False)
                if latest_input and (now - latest_input) <= ACCEPT_INTERVAL:
                    await message.channel.send("エラー：同時登録を検出しました（最終登録は%sです）" % latest_input.strftime('%Y/%m/%d %H:%M:%S'))
                    return
                    
                LATEST_INPUT_MAP[boss_name] = now
                now += interval_time
                creds = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scopes=SCOPES)
                sheet = gspread.authorize(creds).open_by_key(CONFIG.gspread_key).sheet1
                prev_time = '不明'
                for cell in sheet.range('A2:A40'):
                    if boss_name == cell.value:
                        if killed:
                            sheet.update_cell(cell.row, cell.col + 3, end.strftime('%Y/%m/%d %H:%M:%S'))
                            format_cell_range(sheet, gspread.utils.rowcol_to_a1(cell.row, cell.col + 3), cellFormat(backgroundColor=color(0.94, 0.94, 0.94)))
                        prev_time = sheet.cell(cell.row, cell.col + 3).value
                        break
                for channel in [i for i in client.get_all_channels() if i.id == CONFIG.dbm_notify]:
                    if killed:
                        await channel.send("%s END" % boss_name)
                    else:
                        await channel.send("%s 不発" % boss_name)
                await message.channel.send("$natural in %d minutes send %sが%sに湧きます（最終討伐は%sです）" % (round(notify_time.total_seconds() / 60), boss_name, re.sub(r'0(\d+)', r'\1', now.strftime('%H時%M分%S秒')), prev_time))
            except (ValueError, IndexError):
                await message.channel.send('エラー：時間を指定する場合は 時:分 または 時:分:秒 でお願いします')
            except BossTimeError:
                await message.channel.send('エラー：前回の出現時間より前の時間を指定することはできません')
        else:
            await message.channel.send("エラー：%s は時間管理対象外です" % boss_name)
    except KeyError:
        if boss_name == '無念':
            await message.channel.send('無念です...')
        else:
            await message.channel.send("エラー：%s は知らないボスです" % target_name)


client.run(CONFIG.token)
