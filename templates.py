from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def btn_help():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('📕 Подсказки'), KeyboardButton('🔎 Поиск фильмов'))
    kb.add(KeyboardButton('🎬 Сейчас смотрят'), KeyboardButton('👻 Контакты'))
    kb.add(KeyboardButton('🔥 Наш канал'))
    return kb


def btn_search_film(iframe_url: str, kinopoisk_id: int, more_btn=True):
    kb = InlineKeyboardMarkup()

    if iframe_url:
        kb.add(
            InlineKeyboardButton(
                '🍿 Смотреть онлайн',
                url=f'https://ikino-online.github.io//cm/index.html?f={iframe_url}?d=skyfilm.org'
            )
        )
    else:
        kb.add(
            InlineKeyboardButton(
                '🔮 Кнопка для просмотра',
                callback_data=f'show_watch_btn|{kinopoisk_id}'
            )
        )

    if more_btn:
        kb.add(
            InlineKeyboardButton(
                '📙 КиноПоиск',
                url=f'https://www.kinopoisk.ru/film/{kinopoisk_id}'
            ),
            InlineKeyboardButton(
                '📙 Подробнее',
                callback_data=f'film_info|{kinopoisk_id}'
            ),
        )
    else:
        kb.add(
            InlineKeyboardButton(
                '📙 КиноПоиск',
                url=f'https://www.kinopoisk.ru/film/{kinopoisk_id}'
            )
        )
    return kb


def btn_link_to_channel():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            'Перейти в канал 👻',
            url='https://t.me/+HO-ispLLw844Yjgy'
        )
    )
    return kb


def btn_join_to_channel():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            'Подписаться ➡️',
            url='https://t.me/+HO-ispLLw844Yjgy'
        ),
        InlineKeyboardButton(
            'Я подписался 👍',
            callback_data='check_join_to_channel'
        )
    )
    return kb



STATIC_TEXT_JOIN_TO_CHANNEL = """Привет друзья! Наш бот абсолютно бесплатен и без рекламы! Но доступ у него открыт только подписчикам нашего канала👉 [iKino | Фильмы 2020](https://t.me/+HO-ispLLw844Yjgy)

Подпишитесь, что бы не пропускать новинки! После подписки нажмите кнопку "Я подписался". Доступ будет открыт автоматически."""

STATIC_TEXT_SPECIAL_HELP = """
🔎 Отправь название фильма или сериала и я покажу тебе результаты поиска

📌 Также ты можете использовать следующие команды:
⚡️ /trends - Популярные фильмы
⚡️ /search - Поиск фильмов
⚡️ /selection - Наш канал телеграм
⚡️ /contacts - Контакты
⚡️ /help - Подсказки
"""

STATIC_TEXT_SPECIAL_HELP_ADMIN = """
👷🏻‍♂️ Вы являетесь админом бота. Для вас доступны следующие команды:
⚡️ /mailing - Рассылка сообщений
⚡️ /analytics - Аналитика бота

"""

STATIC_TEXT_SPECIAL_START = """
Хеллоу, я iKino Cinema 👻🍿

🔎 В моей библиотеке ты найдешь множество фильмов, сериалов, новинок киноиндустрии, а также крутые подборки и рекомендации!

⚡️Нажми кнопку "📕 Подсказки" или используй команду /help, чтобы узнать список всех моих возможностей"""

STATIC_TEXT_SPECIAL_SEARCH_FILMS =  """
👋Добро пожаловать в поиск! Напиши мне название фильма, мультфильма или сериала и я найду их для тебя.

❗️ВАЖНО! Год выпуска, номер сезона или номер серии писать не нужно! Название должно быть правильным (как в Кинопоиске)! В обратном случае, я ничего не смогу найти для тебя. Например:

✅Правильно:  Ведьмак
✅Правильно: The Witcher
❌Неправильно: Ведьмак 2019
❌Неправильно: Ведьмак 1 сезон

Жду от тебя названия фильма👇
Приятного просмотра!🍿
"""

STATIC_TEXT_SPECIAL_CONTACTS = """
📝 Контакты
@screlizer - тех. поддержка, реклама 
"""

STATIC_TEXT_SPECIAL_SELECTION = '🍿 Не знаешь, что посмотреть?' \
                                'Тогда переходи в наш канал. Здесь ты найдешь кучу крутых подборок с фильмами, мультфильмами и сериалами на свой вкус 🔥' \
                                '👉 [iKino | Фильмы 2020](https://t.me/+HO-ispLLw844Yjgy)'

infodesc = """
➖➖➖➖➖➖➖➖➖➖
<a href="https://t.me/+HO-ispLLw844Yjgy">🍿 Другие фильмы 🍿</a>
➖➖➖➖➖➖➖➖➖➖
<a href="https://t.me/searchikino_bot">🔍 Поиск Фильмов | Сериалов</a>
➖➖➖➖➖➖➖➖➖➖
"""

STATIC_BTN_HELP = btn_help()

STATICT_BTN_LINK_TO_CHANNEL = btn_link_to_channel()

STATICT_BTN_JOIN_TO_CHANNEL = btn_join_to_channel()
