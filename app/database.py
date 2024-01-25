import datetime
import sqlite3 as sq
from app.log import log
db = sq.connect('tg.db')
cur = db.cursor()


async def db_start():

    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "name TEXT,"
                "status TEXT,"
                "user_change INTEGER,"
                "chat_id INTEGER)"

                )
    cur.execute("CREATE TABLE IF NOT EXISTS tabs("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "date TEXT,"
                "id_user INTEGER,"
                "marc TEXT)"
                )

    users = cur.execute("SELECT * FROM users").fetchone()
    if not users:
        cur.execute(
            "INSERT INTO users (name,status,chat_id) VALUES ('admin' ,'main',5143076235)")
        cur.execute(
            "INSERT INTO users (name,status,chat_id) VALUES ('Максім' ,'main',1019757906)")
        cur.execute(
            "INSERT INTO users (name,status,chat_id) VALUES ('Саша' ,'main',563225235)")
        cur.execute(
            "INSERT INTO users (name,status,chat_id) VALUES ('Олексій' ,'main',900417477)")
    tabs = cur.execute("SELECT * FROM tabs").fetchone()

    if not tabs:
        date = (datetime.datetime.now().date() -
                datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        cur.execute(
            "INSERT INTO tabs (date,id_user,marc) VALUES ('{date}' ,3,'+')".format(date=date))
        date = (datetime.datetime.now().date()).strftime('%Y-%m-%d')
        cur.execute(
            "INSERT INTO tabs (date,id_user,marc) VALUES ('{date}' ,4,'-')".format(date=date))

    db.commit()


async def get_user_name_from_id(id):

    name = cur.execute(
        "SELECT name FROM users WHERE id == {id}".format(id=id)).fetchone()[0]
    log(f"get_user_name_from_id({id}) -> {name}")
    return name


async def get_user_name_from_chat_id(chat_id):
    name = cur.execute(
        "SELECT name FROM users WHERE chat_id == {chat_id}".format(chat_id=chat_id)).fetchone()[0]
    log(f"get_user_name_from_chat_id({chat_id}) -> {name}")

    return name


async def get_user_status_from_id(id):
    status = cur.execute(
        "SELECT status FROM users WHERE id == {id}".format(id=id)).fetchone()[0]
    log(f"get_user_status_from_id({id}) -> {status}")

    return status


async def get_user_status_from_name(name):
    status = cur.execute(
        "SELECT status FROM users WHERE name == '{name}'".format(name=name)).fetchone()[0]

    log(f"get_user_status_from_name('{name}') -> {status}")
    return status


async def get_user_status_from_chat_id(chat_id):
    status = cur.execute(
        "SELECT status FROM users WHERE chat_id == {chat_id}".format(chat_id=chat_id)).fetchone()[0]
    log(f"get_user_status_from_chat_id({chat_id}) -> {status}")

    return status


async def get_user_chat_id_from_name(name):
    chat_id = cur.execute(
        "SELECT chat_id FROM users WHERE name == '{name}'".format(name=name)).fetchone()[0]
    log(f"get_user_chat_id_from_name('{name}') -> {chat_id}")

    return chat_id


async def get_user_chat_id_from_id(id):
    chat_id = cur.execute(
        "SELECT chat_id FROM users WHERE id == {id}".format(id=id)).fetchone()[0]
    log(f"get_user_chat_id_from_id({id}) -> {chat_id}")

    return chat_id


async def get_tab_date_from_id(id):
    date = cur.execute(
        "SELECT date FROM tabs WHERE id == {id}".format(id=id)).fetchone()[0]
    log(f"get_tab_date_from_id({id}) -> {date}")

    return date


async def get_tab_marc_from_id(id):
    marc = cur.execute(
        "SELECT marc FROM tabs WHERE id == {id}".format(id=id)).fetchone()[0]
    log(f"get_tab_marc_from_id({id}) -> {marc}")

    return marc


async def get_tab_marc_from_date(date):
    marc = cur.execute(
        "SELECT marc FROM tabs WHERE date == '{date}'".format(date=date)).fetchone()[0]
    log(f"get_tab_marc_from_date('{date}') -> {marc}")

    return marc


async def get_tab_id_user_from_date(date):
    id_user = cur.execute(
        "SELECT id_user FROM tabs WHERE date == '{date}'".format(date=date)).fetchone()[0]
    log(f"get_tab_id_user_from_date('{date}') -> {id_user}")

    return id_user


async def get_tab_id_user_from_id(id):
    id_user = cur.execute(
        "SELECT id_user FROM tabs WHERE id == {id}".format(id=id)).fetchone()[0]
    log(f"get_tab_id_user_from_id({id}) -> {id_user}")

    return id_user


async def get_current_user_chat_id():
    chat_id = await get_user_chat_id_from_id(await get_tab_id_user_from_id(2))
    log(f"get_current_user_chat_id() -> {chat_id}")

    return chat_id


async def get_current_user_name():
    name = await get_user_name_from_id(await get_tab_id_user_from_id(2))
    log(f"get_current_user_name() -> {name}")

    return name


async def get_current_user_status():
    status = await get_user_status_from_id(await get_tab_id_user_from_id(2))
    log(f"get_current_user_status() -> {status}")

    return status


async def get_tabs_all():

    tabs = cur.execute("SELECT * FROM tabs").fetchall()
    tabs = [{
        'date': tabs[0][1],
        'id': tabs[0][2],
        'marc': tabs[0][3]
    }, {
        'date': tabs[1][1],
        'id': tabs[1][2],
        'marc': tabs[1][3]
    }]
    log("get_tabs_all()")

    return tabs


async def note_tab_mark_from_id(id):
    cur.execute(
        "UPDATE tabs SET marc = '+' WHERE id == {id}".format(id=id))
    log(f"note_tab_mark_from_id({id}) ")

    db.commit()


async def denote_tab_mark_from_id(id):
    cur.execute(
        "UPDATE tabs SET marc = '-' WHERE id == {id}".format(id=id))
    log(f"denote_tab_mark_from_id({id}) ")

    db.commit()


async def set_admin_user_change(id):
    cur.execute(
        "UPDATE users SET user_change = {id} WHERE id == 1".format(id=id))
    log(f"set_admin_user_change({id}) ")

    db.commit()


async def set_admin_status(status):
    cur.execute(
        "UPDATE users SET status = '{status}' WHERE id == 1".format(status=status))
    log(f"set_admin_status('{status}') ")

    db.commit()


async def get_admin_user_change():
    user_change = cur.execute(
        "SELECT user_change FROM users WHERE id == 1").fetchone()[0]
    log(f"get_admin_user_change() -> {user_change}")

    return user_change


async def set_tab_id_user_from_id(id_user):
    tab_id = await get_admin_user_change()
    cur.execute(
        "UPDATE tabs SET id_user = '{id_user}' WHERE id == {id}".format(id_user=id_user, id=tab_id))
    log(f"set_tab_id_user_from_id({id_user})")

    db.commit()


async def set_tab_marc(marc):
    id = await get_admin_user_change()
    cur.execute(
        "UPDATE tabs SET marc = '{marc}' WHERE id == {id}".format(id=id, marc=marc))
    log(f"set_tab_marc('{marc}')")

    db.commit()


async def set_tab_second(marc):

    temp_date = datetime.datetime.strptime(
        await get_tab_date_from_id(1), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    # print("1", date)
    date = temp_date.strftime('%Y-%m-%d')

    if marc == "-":

        id_user = await get_tab_id_user_from_id(1)

    else:

        id_user = ((await get_tab_id_user_from_id(1)) % 4)+1
        if id_user == 1:
            id_user = 2

    cur.execute(
        "UPDATE tabs SET marc = '{marc}' WHERE id == 2".format(marc='-'))
    cur.execute(
        "UPDATE tabs SET date = '{date}' WHERE id == 2".format(date=date))
    cur.execute(
        "UPDATE tabs SET id_user = {id_user} WHERE id == 2".format(id_user=id_user))
    log(f"set_tab_second('{marc}')")

    db.commit()


async def set_days():

    date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    temp_date = (datetime.datetime.now().date() -
                 datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    marc = "-"
    id_user = (await get_tab_id_user_from_id(2) % 4)+1
    if id_user == 1:
        id_user = 2
    if await get_tab_marc_from_id(2) == "-":
        cur.execute(
            "UPDATE tabs SET marc = '{marc}' WHERE id == 1".format(marc='-'))
        cur.execute(
            "UPDATE tabs SET date = '{date}' WHERE id == 1".format(date=temp_date))
        cur.execute(
            "UPDATE tabs SET id_user = {id_user} WHERE id == 1".format(id_user=await get_tab_id_user_from_id(2)))
        cur.execute(
            "UPDATE tabs SET date = '{date}' WHERE id == 2".format(date=date))
    else:
        cur.execute(
            "UPDATE tabs SET marc = '{marc}' WHERE id == 1".format(marc=await get_tab_marc_from_id(2)))
        cur.execute(
            "UPDATE tabs SET date = '{date}' WHERE id == 1".format(date=temp_date))
        cur.execute(
            "UPDATE tabs SET id_user = {id_user} WHERE id == 1".format(id_user=await get_tab_id_user_from_id(2)))
        cur.execute(
            "UPDATE tabs SET marc = '{marc}' WHERE id == 2".format(marc=marc))
        cur.execute(
            "UPDATE tabs SET date = '{date}' WHERE id == 2".format(date=date))
        cur.execute(
            "UPDATE tabs SET id_user = {id_user} WHERE id == 2".format(id_user=id_user))
    log(f"set_days('{marc}')")

    db.commit()
