from app import hl, bot, hdvb
from aiogram import Dispatcher, executor, types
import logging
import cmds
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import templates

logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)


hl.add('/', {
    '^([^\.,\-,\:].+)$': cmds.films.search_films,
})

hl.add('/mailing', {
    '(?s).*': cmds.mailing.set_data
})

hl.add('/mailing_verify', {
    '^(Старт)$': cmds.mailing.start_mailing,
    '^(Отмена)$': cmds.mailing.cancel_mailing
})


hl.add('special', {
    '^(/start)$': cmds.special.start,
    '^(📕 Подсказки|/help)$': cmds.special.help_menu,
    '^(🔎 Поиск фильмов|/search)$': cmds.special.search_films,
    '^(🎬 Сейчас смотрят|/trends)$': cmds.special.popular_films,
    '^(🔥 Наш канал|/selection)$': cmds.special.selection,
    '^(👻 Контакты|/contacts)$': cmds.special.contacts,
    '^(/analytics)$': cmds.special.analytics,
    '^(/mailing)$': cmds.special.mailing,
})

hl.add_query('^(show_watch_btn\|.+)$', cmds.query.show_watch_btn)
hl.add_query('^(film_info\|.+)$', cmds.query.film_info)
hl.add_query('^(check_join_to_channel)$', cmds.query.check_join_to_channel)


@dp.message_handler(content_types=types.ContentType.ANY)
async def handler(m: types.Message):
    logging.info(
        f'[Message] From: {m.from_user.full_name}(@{m.from_user.username}) | Text: {m.text}')
    await hl.handle_message(m)


@dp.callback_query_handler()
async def handler(c: types.CallbackQuery):
    await hl.handle_query(c)


def start():
    import time

    try:
        executor.start_polling(dp)
    except Exception as e:
        print(e)
        time.sleep(15)
        start()


if __name__ == '__main__':
    start()
