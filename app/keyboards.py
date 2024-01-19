import datetime
from aiogram.types import ReplyKeyboardMarkup
from . import database as db
from app.log import log

async def get_main_user_keyboard():
    log("get_main_user_keyboard")
    mark = await db.get_tab_marc_from_id(2)
    main = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # main.add('1').add('2').add('3').add('4')

    param = "Відмінити"
    if mark == "-":
        param = "Зазначити"
    arg = [param, "Таблиця"]
    main.add(*arg)

    return main


async def get_table_keyboard(chat_id):
    log(f"get_table_keyboard({chat_id})")
    temp_data = await db.get_tabs_all()

    temp_date = datetime.datetime.strptime(
        temp_data[-1]["date"], '%Y-%m-%d').date() + datetime.timedelta(days=1)

    temp_data.append({
        "date": temp_date.strftime('%Y-%m-%d'),
        "id": ((temp_data[-1]["id"]) % 4)+1,
        "marc": "B"
    })
    if temp_data[-1]["id"] == 1:
        temp_data[-1]["id"] = 2

    table_data = [[], ["Вчора", "Сьогодні", "Завтра"], []]

    for r in temp_data:
        table_data[0].append(r["date"])

    # for r in temp_data:

        table_data[2].append(await db.get_user_name_from_id(r["id"]) + " | " + r["marc"])

    arr = []
    for i in table_data:
        for r in range(len(i)):
            arr.append(i[r])
    arr.append('Оновити')
    if await db.get_current_user_chat_id() == chat_id:
        arr.append('Повернутись')

    table = ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=len(table_data[0]))
    # table.add('1').add('2').add('3').add('4')
    table.add(*arr)

    return table


async def get_admin_change_tab_panel_keyboard(id):
    log(f"get_admin_change_tab_panel_keyboard({id})")
    

    arr = []
    row_width = 1
    name = await db.get_user_name_from_id(await db.get_tab_id_user_from_id(id))
    marc = "+"
    if await db.get_tab_marc_from_id(id) == "+":
        marc = "-"

    if id == 2:
        arr = [f'Змінити сатус {name} на {marc}',
               'Змінити чергового',  'Повернутись']
    else:
        arr = [f'Змінити сатус {name} на {marc}',  'Повернутись']

    main = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)

    main.add(*arr)
    return main


async def get_admin_user_change_keyboard():
    log("get_admin_user_change_keyboard()")

    arr = []
    row_width = 1
    arr = []
    for i in range(3):
        name = await db.get_user_name_from_id(i+2)
        if name != await db.get_user_name_from_id(
                await db.get_tab_id_user_from_id(await db.get_admin_user_change())):

            arr.append(name)
    arr.append('Повернутись')

    main = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)

    main.add(*arr)
    return main
