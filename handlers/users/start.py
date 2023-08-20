import re

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.inlineButtons import likes
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.inlineButtons import menuCategory
from loader import dp, bot

from .pagination import (get_current_page_items,
                         get_pagination_keyboard, items_per_page)


@dp.message_handler(Command(["start", "categories"]), state='*')
async def bot_start(message: types.Message):
    categories = {}
    request_url = "http://146.190.138.39/api/v1/category/"
    response = requests.get(request_url)
    
    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
        for category in response_json:
            if category['is_active']:
                categories[category['id']] = category['title']
        print("DATA:", categories)
    else:
        print("API request failed:", response.text)
    
    await message.answer(
        text="Shunchaki qo'shiqchi kategoriyasini jo'nating va men siz uchun musiqa topib beraman!",
        reply_markup=menuCategory(categories)
    )


number_pattern = re.compile(r'^[1-9]\d{0,6}$|0$')
@dp.callback_query_handler(lambda query: number_pattern.match(query.data), state='*')
async def handle_category_callback(call: types.CallbackQuery, state: FSMContext):
    # await call.answer(f"Received valid number: {int(call.data)}")
    await call.answer(cache_time=0.02)
    args = {
        "chat_id": call.message.chat.id,
        "message_id": call.message.message_id
    }
    request_url = "http://146.190.138.39/api/v1/music/?category={call.data}"
    response = requests.get(request_url)
    
    if response.status_code == 200:
        response_json = response.json()
        print("Music: ", response_json)
        
        songs = []
        for song in response_json:
            songs.append(
                    {
                        "artist": song['artist'],
                        "name": song['title'],
                        "url": song['music'],
                        "janr": song['janr'],
                        # "time": time
                    }
            )
            if not songs:
                await call.message.answer("Hech narsa topilmadi 😔")
                return
            await state.update_data({
                "songs": songs
            })
        await show_page(call.message.chat.id, 1, songs)
    else:
        print("API request failed:", response.text)
    
    await call.answer(cache_time=0.02, show_alert=False)


@dp.callback_query_handler(lambda c: c.data.startswith(('next_', 'previous_')), state='*')
async def handle_pagination(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0.02)
    action, page = call.data.split('_')
    data = await state.get_data()
    page = int(page)
    args = {
        "chat_id": call.message.chat.id,
        "message_id": call.message.message_id
    }

    if action == "next":
        await show_page(call.from_user.id, page, data.get('songs'), args)
    elif action == "previous":
        await show_page(call.from_user.id, page, data.get('songs'), args)


@dp.callback_query_handler(lambda c: c.data == 'current_page', state='*')
async def handle_current_page(call: types.CallbackQuery):
    await call.message.delete()


async def show_page(user_id, page, songs, args=None):
    try:
        total_pages = (len(songs) + items_per_page - 1) // items_per_page
    except:
        return
    current_page_items = get_current_page_items(page, songs)

    header = ''
    if len(songs) - page * 10 > (page - 1) * 10 + 1:
        header = f"<b>Natijalar {((page - 1) * 10 + 1)}-{page * 10} {len(songs)} dan</b>\n" + format_data(
            current_page_items)
    else:
        header = f"<b>Natijalar {((page - 1) * 10 + 1)}-{len(songs)} {len(songs)} dan</b>\n" + format_data(
            current_page_items)

    if args is None:
        await bot.send_message(user_id, header,
                               reply_markup=get_pagination_keyboard(page, total_pages, current_page_items))
        return

    await bot.edit_message_text(
        chat_id=args.get('chat_id'),
        message_id=args.get('message_id'),
        text=header,
        reply_markup=get_pagination_keyboard(page, total_pages, current_page_items))


def format_data(data):
    body = ""
    for i, song in enumerate(data):
        body += f"\n<b>{i + 1}</b>. {song.get('artist')} - {song.get('name')} {song.get('janr')}"
    return body


@dp.callback_query_handler(lambda c: c.data.startswith("http"), state='*')
async def chooseSong(call: types.CallbackQuery):
    await call.answer(cache_time=0.02)
    loader = await call.message.answer('Loading...')

    music_url = call.data
    file_name = music_url.split("/")[-1]

    response = requests.get(music_url)

    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
        print(f"Music file '{file_name}' downloaded successfully.")

        with open(file_name, "rb") as music_file:
            await call.message.answer_document(music_file, caption="Here is the music you requested.")
    else:
        print(f"Failed to download music file. Status code: {response.status_code}")

    await loader.delete()
    return


@dp.callback_query_handler(lambda x: x.data in ['text_search'], state='*')
async def change_language(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Shunchaki menga qo'shiqchi yoki qo'shiq nomini jo'nating va men siz uchun musiqa topib beraman!",
        reply_markup=None)




