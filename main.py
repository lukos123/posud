import asyncio
from aiogram import Bot, Dispatcher, executor, types
from app import keyboards as kb
from app import database as db
from app import update
from dotenv import load_dotenv
from app import sendnotification as sn
import os

from app.log import log

load_dotenv()
bot = Bot(os.getenv('TOKEN'))

dp = Dispatcher(bot=bot)


async def on_startup(_):
    await db.db_start()
    log('bot started')


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    print()
    log(message.from_user.full_name+": "+message.text)
    await message.answer(f"hi {message.from_user.first_name} ",
                         reply_markup=await kb.get_main_user_keyboard())


@dp.message_handler(text="Зазначити")
async def note(message: types.Message):
    print()
    log(message.from_user.full_name+": "+message.text)
    if message.from_user.id == await db.get_current_user_chat_id():
        await db.note_tab_mark_from_id(2)
        await update.run(await db.get_current_user_chat_id(), "{name} зазначив що помив посуд"
                         .format(name=await db.get_current_user_name()))

    else:
        await message.reply(f"I dont understand you")


@dp.message_handler(text="Відмінити")
async def note(message: types.Message):
    print()
    log(message.from_user.full_name+": "+message.text)

    if message.from_user.id == await db.get_current_user_chat_id():
        await db.denote_tab_mark_from_id(2)
        await update.run(await db.get_current_user_chat_id(), "{name} зазначив що не помив посуд"
                         .format(name=await db.get_current_user_name()))
    else:
        await message.reply(f"I dont understand you")


@dp.message_handler(text="Таблиця")
async def table(message: types.Message):
    print()
    log(message.from_user.full_name+": "+message.text)

    await message.answer('tab',
                         reply_markup=await kb.get_table_keyboard(
                             message.from_user.id))


@dp.message_handler(text="Оновити")
async def update_tab(message: types.Message):
    print()
    log(message.from_user.full_name+": "+message.text)

    await table(message)


@dp.message_handler(text="Повернутись")
async def beak(message: types.Message):
    print()
    log(message.from_user.full_name+": "+message.text)

    if await db.get_current_user_chat_id() == message.from_user.id:
        await message.answer(f"main",
                             reply_markup=await kb.get_main_user_keyboard())
    elif await db.get_user_chat_id_from_id(1) == message.from_user.id:
        if await db.get_user_status_from_id(1) == 'change_tab':
            await message.answer(f"main",
                                 reply_markup=await kb.get_table_keyboard(message.from_user.id))
            await db.set_admin_status("main")
        elif await db.get_user_status_from_id(1) == 'user_change':
            await message.answer("change_tab",
                                 reply_markup=await kb.get_admin_change_tab_panel_keyboard(await db.get_admin_user_change()))
            await db.set_admin_user_change(await db.get_admin_user_change())
            await db.set_admin_status("change_tab")
    else:
        await message.reply(f"I dont understand you")


@dp.message_handler(text="Змінити чергового")
async def change_current_user(message: types.Message):
    print()
    log(message.from_user.full_name+": "+message.text)


    if await db.get_user_chat_id_from_id(1) == message.from_user.id:
        if await db.get_user_status_from_id(1) == 'change_tab':

            await message.answer(f"user_change",
                                 reply_markup=await kb.get_admin_user_change_keyboard())
            await db.set_admin_status("user_change")
    else:
        await message.reply(f"I dont understand you")


@dp.message_handler()
async def other(message: types.Message):
    print()
    log(message.from_user.full_name+": "+message.text)

    async def change_tab(id):
        await message.answer("change_tab",
                             reply_markup=await kb.get_admin_change_tab_panel_keyboard(id))
        await db.set_admin_user_change(id)
        await db.set_admin_status("change_tab")

    if await db.get_user_chat_id_from_id(1) == message.from_user.id:
        status = await db.get_user_status_from_chat_id(message.from_user.id)
        text = message.text
        if status == "main":
            if text == 'Сьогодні':
                await change_tab(2)
            elif text == 'Вчора':
                await change_tab(1)
            elif text == await db.get_tab_date_from_id(2):
                await change_tab(2)
            elif text == await db.get_tab_date_from_id(1):
                await change_tab(1)
        elif status == "change_tab":
            name_user = await db.get_user_name_from_id(await db.get_tab_id_user_from_id(await db.get_admin_user_change()))
            marc = "+"
            user_change = await db.get_admin_user_change()
            if await db.get_tab_marc_from_id(user_change) == "+":
                marc = "-"
            if text == f'Змінити сатус {name_user} на {marc}':
                await db.set_tab_marc(marc)
                await change_tab(user_change)
                ne = ""
                if marc == "-":
                    ne = "не"
                await update.run(await db.get_user_chat_id_from_id(1), "Тепер вважається що {name} {ne} помив посуд"
                                 .format(name=name_user, ne=ne))
                if user_change == 1:
                    if marc == '-':
                        await db.set_tab_second('-')
                        await update.run(await db.get_user_chat_id_from_id(1), "Тепер вважається що сьогодні миє {name}"
                                         .format(name=await db.get_current_user_name()))
                    else:

                        await db.set_tab_second('+')
                        name = await db.get_current_user_name()
                        await update.run(await db.get_user_chat_id_from_id(1), "Тепер вважається що сьогодні миє {name}"
                                         .format(name=await db.get_current_user_name()))
        elif status == "user_change":
            for i in range(3):
                name = await db.get_user_name_from_id(i+2)
                if text == name:
                    await db.set_tab_id_user_from_id(i+2)
                    await change_tab(await db.get_admin_user_change())
                    await update.run(await db.get_user_chat_id_from_id(1), "Тепер вважається що сьогодні миє {name}"
                                     .format(name=name))
                    break

    else:
        await message.reply(f"I dont understand you")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(sn.send_notification(1))

    executor.start_polling(dp, on_startup=on_startup)
