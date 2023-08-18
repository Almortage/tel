from pyrogram import Client
from asBASE import asJSON

db = asJSON("as.json")
###


SUDORS = [5089553588] # ايديات المطورين
API_ID = 14911221
API_HASH = "a5e14021456afd496e7377331e2e5bcf"
TOKEN = "6195511173:AAFtP0o9LRvHZ-WttLa0EnH_uQ-5_8GzICg" # التوكن
bot = Client("control",API_ID,API_HASH,bot_token=TOKEN,in_memory=True)
bot_id = TOKEN.split(":")[0]