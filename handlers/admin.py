from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from create_bot import bot, dp
from data_base import sqlite_db
from keyboards import kb_admin


class FSMAdmin(StatesGroup):
    """Машина состояний.

    Первым отрабатывает добавление имени задачи
    Вторым отрабатывает добавления описания задачи
    """
    name = State()
    description = State()


async def send_welcome(message: types.Message):
    """Активирует бота."""
    await message.answer('TbotMy запущен!')


async def set_default_commands(dp):
    """Выводит в меню список доступных команд для бота."""
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустить бота'),
            types.BotCommand('add', 'Добавть задачу'),
            types.BotCommand('list', 'Открыть список задач'),
            types.BotCommand('delete', 'Удалить задачу'),
        ]
    )


async def cm_add(message: types.Message):
    """Активирует машину состояний."""
    await FSMAdmin.name.set()
    await bot.send_message(
        message.from_user.id, 'Твой помошник активирован!',
        reply_markup=kb_admin
    )
    await message.reply('Добавьте имя задачи.')


async def command_help(message: types.Message):
    pass


async def cancel_handler(message: types.Message, state: FSMContext):
    """Отменяет добавление задачи."""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Добавление задачи отменено!')


async def add_name(message: types.Message, state: FSMContext):
    """Добавляет задачу."""
    async with state.proxy() as data:
        data['name'] = str(message.text)
    await FSMAdmin.next()
    await message.reply('Добавьте описание задачи.')


async def add_description(message: types.Message, state: FSMContext):
    """Добавляет описание задачи."""
    async with state.proxy() as data:
        data['description'] = str(message.text)
    await sqlite_db.sql_add_command(state)
    await state.finish()


async def list_command(message: types.Message):
    """Выводит список задач."""
    await sqlite_db.sql_read(message)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    """Обращается к БД и удаляет задачу."""
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(
        text=f"{callback_query.data.replace('del ', '')} удалена.",
        show_alert=True
    )


async def delete_command(message: types.Message):
    """Выводит инлайн-клавиатуру для удаления задач."""
    read = await sqlite_db.sql_read2()
    for ret in read:
        await bot.send_message(
            message.from_user.id, text='^',
            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                f'Удалить {ret[0]}', callback_data=f'del {ret[0]}'
            )
            )
        )


def register_handlers_admin(dp: Dispatcher):
    """Регистрируем обработчики команд."""
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(cm_add, commands=['add'], state=None)
    dp.register_message_handler(cancel_handler, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(
        equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(add_name, state=FSMAdmin.name)
    dp.register_message_handler(add_description, state=FSMAdmin.description)
    dp.register_message_handler(list_command, commands=['list'])
    dp.register_message_handler(delete_command, commands=['delete'])
