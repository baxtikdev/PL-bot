import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types.message import Message
from bs4 import BeautifulSoup as bs

from handlers.users.pagination import show_page
from keyboards.inline.inlineButtons import likes
from loader import dp
from states.baseStates import SearchState

session = requests.session()
session.headers.update({
    'user-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Accept': '*/*', 'Connection': 'keep-alive', 'origin': 'https://z1.fm'})

session.get("https://z1.fm")


@dp.message_handler(content_types=types.ContentType.TEXT, state='*')
async def search(message: Message, state: FSMContext):
    await SearchState.search.set()
    query = message.text
    url = f"https://z1.fm/mp3/search?keywords={query}&sort=views"
    html = session.get(url)
    parsed = bs(html.text, "lxml")
    songs = []
    songs_elem = parsed.select("div.songs-list-item div.song-wrap-xl div.song-xl")
    for id, song in enumerate(songs_elem):
        name = song.select_one("div.song-content div.song-name a").text.strip()
        if "edit" in name.lower() or "remix" in name.lower():
            continue
        artist = song.select_one("div.song-content div.song-artist a").text.strip()
        time = song.select_one("div.song-info span.song-time").text.strip()

        songs.append(
            {
                "artist": artist,
                "name": name,
                "url": "https://z1.fm/download/" + song.get("data-play"),
                "time": time
            }
        )
    if not songs:
        await message.answer("Hech narsa topilmadi 😔")
        return
    await state.update_data({
        "songs": songs
    })
    await show_page(message.from_user.id, 1, songs)
    return


@dp.callback_query_handler(lambda c: c.data.startswith("https"), state='*')
async def chooseSong(call: CallbackQuery):
    await call.answer(cache_time=0.02)
    await call.message.answer_audio(audio=call.data, reply_markup=likes)
    return


@dp.callback_query_handler(lambda c: c.data.startswith("dislike"), state='*')
async def chooseSong(call: CallbackQuery):
    await call.answer(cache_time=0.02)
    await call.message.delete()
    return


@dp.callback_query_handler(lambda c: c.data.startswith("like"), state='*')
async def chooseSong(call: CallbackQuery):
    await call.answer("Yoqtirishlarga qo'shildi", cache_time=0.02, show_alert=False)
    return
