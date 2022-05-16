from aiogram.types import Message
from app import hl, hdvb, views_counter
import templates
import config


async def search_films(m: Message):
    await m.answer(templates.STATIC_TEXT_SPECIAL_SEARCH_FILMS)


async def popular_films(m: Message):
    films = await hdvb.get_popular_films()
    if films:
        n = len(films)
        for film in reversed(films):
            caption = "<b>{title} ({year}) {quality}</b>".format(
                title=film.title,
                year=str(film.year) + '' if film.year else '',
                quality=film.quality,
                parse_mode="HTML"
            )
            await m.answer_photo(
                photo=film.poster,
                caption=caption,
                reply_markup=templates.btn_search_film('', film.kinopoisk_id),
                parse_mode="HTML"
            )
            n -= 1
    else:
        await m.answer('Рейтинг пуст')


async def contacts(m: Message):
    await m.answer(templates.STATIC_TEXT_SPECIAL_CONTACTS)


async def help_menu(m: Message):
    await m.answer(templates.STATIC_TEXT_SPECIAL_HELP, reply_markup=templates.STATIC_BTN_HELP)

    if m.from_user.id == config.ADMIN_ID:
        await m.answer(templates.STATIC_TEXT_SPECIAL_HELP_ADMIN)


async def start(m: Message):
    await m.answer(templates.STATIC_TEXT_SPECIAL_START, reply_markup=templates.STATIC_BTN_HELP)


async def mailing(m: Message):
    if m.from_user.id == config.ADMIN_ID:
        await m.answer('📝 Введите текст сообщения')
        m.set_action_path('/mailing')


async def analytics(m: Message):
    t = '📊 Статистика бота\n\n' \
        + f'👨🏻‍💻 Кол-во пользователей: {hl.get_all_count()}\n'\
        + f'👀 Просмотров за сутки: {views_counter.get_day_views()}'

    await m.answer(t)


async def selection(m: Message):
    await m.answer(templates.STATIC_TEXT_SPECIAL_SELECTION, reply_markup=templates.STATICT_BTN_LINK_TO_CHANNEL, disable_web_page_preview=True, parse_mode="MARKDOWN")
