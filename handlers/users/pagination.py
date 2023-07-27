from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, bot

items_per_page = 10


def get_current_page_items(page, songs):
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    return songs[start_idx:end_idx]


def get_pagination_keyboard(current_page, total_pages, songs):
    numbers = []
    number = []
    for i, song in enumerate(songs):
        number.append(InlineKeyboardButton(text=f"{i + 1}", callback_data=f"{song.get('url')}"))
        if len(number) == 5:
            numbers.append(number)
            number = []
    keys = numbers
    if current_page == 1:
        keys.append([
            InlineKeyboardButton(text='❌', callback_data='current_page'),
            InlineKeyboardButton(text='➡️', callback_data=f"next_{current_page + 1}")
        ])
    elif 1 < current_page < total_pages:
        keys.append([
            InlineKeyboardButton(text='⬅️', callback_data=f"previous_{current_page - 1}"),
            InlineKeyboardButton(text='❌', callback_data='current_page'),
            InlineKeyboardButton(text='➡️', callback_data=f"next_{current_page + 1}")
        ])
    if current_page == total_pages:
        keys.append([
            InlineKeyboardButton(text='⬅️', callback_data=f"previous_{current_page - 1}"),
            InlineKeyboardButton(text='❌', callback_data='current_page')
        ])
    numberKeyboard = InlineKeyboardMarkup(
        inline_keyboard=keys
    )
    return numberKeyboard


@dp.callback_query_handler(lambda c: c.data.startswith(('next_', 'previous_')), state='*')
async def handle_pagination(call: CallbackQuery, state: FSMContext):
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
async def handle_current_page(call: CallbackQuery):
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
        body += f"\n<b>{i + 1}</b>. {song.get('artist')} - {song.get('name')} {song.get('time')}"
    return body
