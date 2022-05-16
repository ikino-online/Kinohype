from aiogram.types import Message
from app import hdvb, hl
import templates


async def search_films(m: Message):
    await m.answer(f'🔎 Идёт поиск фильма "{m.text}"')

    films = await hdvb.find_by_title(m.text, limit=25)

    if films:
        for film in films:
            caption = '<b>{title} ({year}) {quality}</b>'.format(
                title=film.title,
                year=str(film.year) + '' if film.year else '',
                quality=film.quality
            )
            await m.answer_photo(
                photo=film.poster,
                caption=caption,
                parse_mode="HTML",
                reply_markup=templates.btn_search_film('', film.kinopoisk_id)
            )
    else:
        await m.answer('Простите, я ничего не нашел', reply_markup=templates.STATIC_BTN_HELP)


async def publish_film_search(m: Message):
    try:
        kp_id = int(m.text)
        film = await hdvb.find_by_kp_id(kp_id)

        if film:
            caption = '<b>{title} ({year}) {quality}</b>'.format(
                title=film.title,
                year=str(film.year) + '' if film.year else '',
                quality=film.quality,
                parse_mode=ParseMode.HTML
            )
            await m.answer_photo(film.poster, caption=caption,
                                 reply_markup=templates.btn_pulish_film(kp_id))
            hl.set_user_path('', m.from_user.id)
    except Exception as e:
        print(e)
        await m.answer('Некорректный id либо фильм не найден')