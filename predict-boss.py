import aiohttp
import asyncio
from config import Config
import datetime
from discord import Webhook, AsyncWebhookAdapter
import gspread
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
import re
import time

CONFIG = Config()

WAIT_TIME = datetime.timedelta(minutes=30) # 討伐猶予

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

async def webhook_send(message):
    async with aiohttp.ClientSession() as session:
        wh = Webhook.from_url(CONFIG.webhook, adapter=AsyncWebhookAdapter(session))
        await wh.send(message)    

while True:
    now = datetime.datetime.now()
    creds = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scopes=SCOPES)
    sheet = gspread.authorize(creds).open_by_key(CONFIG.gspread_key).sheet1
    for cell in sheet.range('E2:E30'):
        try:
            end_time = datetime.datetime.strptime(re.sub(r' (\d):', r' 0\1:', cell.value), "%Y/%m/%d %H:%M")
            if (end_time + WAIT_TIME) < now:
                next_time = datetime.datetime.strptime(re.sub(r' (\d):', r' 0\1:', sheet.cell(cell.row, cell.col + 1).value), "%Y/%m/%d %H:%M")
                if next_time > now:
                    text = "%sが%d分経過しても討伐されませんでした\n次の出現時間は%sです" % (sheet.cell(cell.row, 1).value, round(WAIT_TIME.total_seconds() / 60), re.sub(r'0(\d+)', r'\1', next_time.strftime("%H時%M分")))
                    asyncio.get_event_loop().run_until_complete(webhook_send(text))
                    sheet.update_cell(cell.row, cell.col - 1, end_time.strftime("%Y/%m/%d %H:%M"))
                    format_cell_range(sheet, gspread.utils.rowcol_to_a1(cell.row, cell.col - 1), cellFormat(backgroundColor=color(1, 0.5, 0.5)))
        except ValueError:
            continue
    time.sleep(60)
