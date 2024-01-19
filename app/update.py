from . import database as db
from aiogram import Bot
from dotenv import load_dotenv
from . import keyboards as kb
import os
from app.log import log
load_dotenv()
bot = Bot(os.getenv('TOKEN'))


async def run(id, text):
    while True:
        try:
            for i in range(4):
                chat_id = await db.get_user_chat_id_from_id(i+1)
                if chat_id != id:
                    if id != 0:
                        log(f"bot.send_message({chat_id}, {text}, reply_markup=await kb.get_table_keyboard({chat_id})")
                        await bot.send_message(chat_id, text, reply_markup=await kb.get_table_keyboard(chat_id))
                    else:
                        await db.set_admin_status('main')
                        if chat_id != await db.get_current_user_chat_id():
                            log(f"bot.send_message({chat_id}, {text}, reply_markup=await kb.get_table_keyboard({chat_id})")
                            await bot.send_message(chat_id, text, reply_markup=await kb.get_table_keyboard(chat_id))
                        else:
                            log(f"bot.send_message({chat_id}, {text}, reply_markup=await kb.get_main_user_keyboard()")
                            await bot.send_message(chat_id, text, reply_markup=await kb.get_main_user_keyboard())
                else:
                    if chat_id == await db.get_current_user_chat_id():
                        log(f"bot.send_message({chat_id}, {text}, reply_markup=await kb.get_main_user_keyboard()")

                        await bot.send_message(chat_id, text, reply_markup=await kb.get_main_user_keyboard())
                    else:
                        log(f"bot.send_message({chat_id}, {text}")
                        await bot.send_message(chat_id, text)
            break
        except Exception as e:
            log(e)

    # await bot.send_message(1019757906, text)
    # reply_markup=await kb.get_table_keyboard(1019757906)
