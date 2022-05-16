from lib.v2.handler import Handler
from lib.v2.hdvbDriver import HDVB
from lib.v2.vcounter import ViewsCounter
from db.mydb import Database
from aiogram import Bot
import config

bot = Bot(token=config.BOT_TOKEN)

mydb = Database('db/mydb.sqlite')

hl = Handler(db=mydb)
hdvb = HDVB(hdvb_token=config.HDVD_TOKEN, kp_token=config.KP_TOKEN, db=mydb)
views_counter = ViewsCounter()
