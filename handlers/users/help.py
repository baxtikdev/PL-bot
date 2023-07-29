from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message):
    await message.answer("🔥 Buyruqlar"
                         "\nShunchaki menga qo'shiqchi yoki qo'shiq nomini jo'nating va men siz uchun musiqa topib beraman!"
                         "\n\nBog'lanish uchun aloqa: @baxtikdev")
    return
