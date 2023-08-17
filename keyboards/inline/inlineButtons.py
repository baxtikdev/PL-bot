from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

likes = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❤️", callback_data="like"),
            InlineKeyboardButton(text="❌", callback_data='dislike')]
    ]
)


def songsList(songs):
    songsListKeyboard = InlineKeyboardMarkup(row_width=5)
    for i, song in enumerate(songs):
        songsListKeyboard.add(InlineKeyboardButton(text=f"{i + 1}", callback_data=song.get('url')))

    return songsListKeyboard


def menuCategory(categories):
    menuCategoryKeyboard = InlineKeyboardMarkup(row_width=2)
    for i, category in enumerate(categories):
        menuCategoryKeyboard.insert(InlineKeyboardButton(text=category, callback_data=category))
    menuCategoryKeyboard.add(InlineKeyboardButton(text="Matn boyicha qidirish", callback_data="text_search"))
    
    return menuCategoryKeyboard
