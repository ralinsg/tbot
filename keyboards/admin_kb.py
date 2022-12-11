from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1= KeyboardButton('/cancel')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_admin.add(b1)
