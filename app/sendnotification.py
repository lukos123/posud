from aiogram import Bot
import datetime
from time import sleep
from . import database as db
from . import update
import asyncio
from dotenv import load_dotenv
from . import keyboards as kb
import os
from app.log import log
from app.log import log_in_line
load_dotenv()
bot = Bot(os.getenv('TOKEN'))


async def send_notification(sleep_for):

    while True:
        try:
            now = datetime.datetime.now()
            log_in_line(f"1chas : {now.hour}")
            await asyncio.sleep(sleep_for)
            log_in_line(f"2chas : {now.hour}")
            if now.minute == 15:
                log("now.minute == 15")
            if now.hour == 9:
                log("now.hour == 9")
                name = await db.get_current_user_name()
                await update.run(0, f"Сьогодні черга {name}")
                await asyncio.sleep(60*61)
                log("now.hour == 10")

            elif now.hour == 22:
                log("now.hour == 22")

                # name = await db.get_current_user_name()
                chat_id = await db.get_current_user_chat_id()
                marc = await db.get_tab_marc_from_id(2)
                if marc == "-":
                    log(f"bot.send_message({chat_id},'Сьогодні твоя черга')")
                    await bot.send_message(chat_id, "Сьогодні твоя черга", reply_markup=await kb.get_main_user_keyboard())

                await asyncio.sleep(60*61)
                log("now.hour == 23")
            elif now.hour == 1:
                log("now.hour == 1")

                await db.set_days()
                await asyncio.sleep(60*61)
                log("now.hour == 2")
        except Exception as e:
            log("ERROR")
            log(e)
