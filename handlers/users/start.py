from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.inlineButtons import menuCategory
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command(["start", "categories"]), state='*')
async def bot_start(message: types.Message):
    categories = [
        'lofi', 'hip-hop', 'rap', 'pop', 'hit',
        'teen beats', 'chill', 'lofi-rap', 'study mood',
        'favorites', 'local', 'new hits', 'top chart', 'jazz'
    ]
    
    await message.answer(
        text="Shunchaki qo'shiqchi kategoriyasini jo'nating va men siz uchun musiqa topib beraman!",
        reply_markup=menuCategory(categories)
    )


@dp.callback_query_handler(lambda x: x.data in ['text_search'], state='*')
async def change_language(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Shunchaki menga qo'shiqchi yoki qo'shiq nomini jo'nating va men siz uchun musiqa topib beraman!",
        reply_markup=None)




