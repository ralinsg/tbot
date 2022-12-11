import sqlite3 as sq

from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('list_tasks')
    cur = base.cursor()
    base.execute(
        'CREATE TABLE IF NOT EXISTS list(name TEXT, description TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO list VALUES (?,?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for result in cur.execute('SELECT * FROM list').fetchmany(5):
        await bot.send_message(message.from_user.id, f'{result[0]}\n{result[1]}')


async def sql_read2():
    return cur.execute('SELECT * FROM list').fetchmany(5)


async def sql_delete_command(data):
    cur.execute('DELETE FROM list WHERE name = ?', (data, ))
    base.commit()
