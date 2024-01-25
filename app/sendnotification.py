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

load_dotenv()
bot = Bot(os.getenv('TOKEN'))


async def send_notification(sleep_for):

    while True:
        try:
            now = datetime.datetime.now()
            log(f"1chas : {now.hour}", in_line=True)
            await asyncio.sleep(sleep_for)
            log(f"2chas : {now.hour}", in_line=True)
            if now.minute == 30:
                log("now.minute == 30", after_line=True)
                log("Before now.minute == 31")
                await asyncio.sleep(60)
                log("After now.minute == 31")

            if now.hour == 9 and now.minute == 1:
                log("now.hour == 9 and now.minute == 1", after_line=True)
                name = await db.get_current_user_name()
                await update.run(0, f"Сьогодні черга {name}")
                log("Before now.hour == 9 and now.minute == 2")
                await asyncio.sleep(61)
                log("After now.hour == 9 and now.minute == 2")

            elif now.hour == 22 and now.minute == 1:
                log("now.hour == 22 and now.minute == 1", after_line=True)

                # name = await db.get_current_user_name()
                chat_id = await db.get_current_user_chat_id()
                marc = await db.get_tab_marc_from_id(2)
                if marc == "-":
                    log(f"bot.send_message({chat_id},'Сьогодні твоя черга')")
                    await bot.send_message(chat_id, "Сьогодні твоя черга", reply_markup=await kb.get_main_user_keyboard())

                log("Before now.hour == 22 and now.minute == 2")
                await asyncio.sleep(61)
                log("After now.hour == 22 and now.minute == 2")
            elif now.hour == 1 and now.minute == 1:
                log("now.hour == 1 and now.minute == 1", after_line=True)

                await db.set_days()
                log("Before now.hour == 1 and now.minute == 2")
                await asyncio.sleep(61)
                log("After now.hour == 1 and now.minute == 2")
        except Exception as e:
            log("ERROR", after_line=True)
            log(e)
