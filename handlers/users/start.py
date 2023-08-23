import requests
from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.inlineButtons import menuCategory
from loader import dp


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
