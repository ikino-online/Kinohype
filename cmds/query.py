from aiogram.types import Message, CallbackQuery
from app import hdvb, views_counter
import templates, config

async def show_watch_btn(c: CallbackQuery):
    kp_id: int = int(c.data.split('|')[1])
    film = await hdvb.find_by_kp_id(kp_id)

    if film.kinopoisk_id:
        views_counter.increment_day_views()

        await c.bot.edit_message_reply_markup(
            chat_id=c.from_user.id,
            message_id=c.message.message_id,
            reply_markup=templates.btn_search_film(
                film.iframe_url,
                film.kinopoisk_id,
                more_btn=False
            )
        )
        await hdvb.up_film_rating(film)
    else:
        c.answer('Ошибка')


async def film_info(c: CallbackQuery):
    kp_id = int(c.data.split('|')[1])
    film_info = await hdvb.get_film_info(kp_id)

    if not film_info.description:
        film_info.description = 'Отсутсвует'

    new_caption = c.message.caption \
        + f'\n\n<b>Жанр:</b> {"," .join(film_info.genres)} \n<b>Рейтинг:</b> КП {film_info.rating} / IMDb {film_info.ratingImdb} \n\n<b>О фильме:</b> \n<i>{film_info.description}</i>\n\n' \
        + f'➖➖➖➖➖➖➖➖➖➖\n<a href="https://t.me/filmu_besplatno">🍿 Другие фильмы 🍿</a>\n➖➖➖➖➖➖➖➖➖➖\n<a href="https://t.me/movies_filmbot">🔍 Поиск Фильмов | Сериалов</a>\n➖➖➖➖➖➖➖➖➖➖'

    await c.answer('Описание получено 👌')

    await c.bot.edit_message_caption(
        c.from_user.id,
        c.message.message_id,
        caption=new_caption,
        parse_mode="HTML",
        reply_markup=templates.btn_search_film('', kp_id, more_btn=False)
    )

async def check_join_to_channel(c: CallbackQuery):
    member = await c.bot.get_chat_member(chat_id="-1001487776404", user_id=c.from_user.id)
    if member.is_chat_member():
        await c.bot.send_message(c.from_user.id, templates.STATIC_TEXT_SPECIAL_START, reply_markup=templates.STATIC_BTN_HELP)
        await c.answer("Рады видеть тебя в нашем отряде!")
    else:
        await c.answer("Вы не подписались!")