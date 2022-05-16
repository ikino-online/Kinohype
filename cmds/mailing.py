from aiogram.types import Message
from aiogram.utils.exceptions import BotBlocked,  CantParseEntities
from app import hl
import templates
import config

class MailingData:
    text: str
    photo_id: str
    caption: str

    def __init__(self):
        self.text = ''
        self.photo_id = ''
        self.caption = ''

mailing_data = MailingData()

async def set_data(m: Message):
    global mailing_data

    if m.text:
        mailing_data.text = m.text
    elif m.photo:
        mailing_data.photo_id = m.photo[0].file_id
        mailing_data.caption = m.caption
    else:
        await m.answer('Некорректное сообщение')
        return

    m.set_action_path('/mailing_verify')

    await m.answer('Напишите "Старт" - чтобы начать рассылку, или "Отмена"')

async def start_mailing(m: Message):
    global mailing_data

    all_user_ids = hl.get_all_ids()
    await m.answer('📤 Бот начал рассылку')
    m.set_action_path('/')

    k = 0
    for user_id in all_user_ids:
        try:
            if mailing_data.text:
                await m.bot.send_message(user_id, mailing_data.text, parse_mode="HTML")

            elif mailing_data.photo_id:
                await m.bot.send_photo(user_id, photo=mailing_data.photo_id, caption=mailing_data.caption, parse_mode="HTML")

            k += 1
        except BotBlocked:
            pass
        except CantParseEntities as e:
            mailing_data = MailingData()
            await m.answer(e)
            return 

    await m.answer(f'📩 Рассылка закончена. Кол-во отправленных сообщений: {k}')
    mailing_data = MailingData()

async def cancel_mailing(m: Message):
    global mailing_data

    mailing_data = MailingData()
    m.set_action_path('/')
    await m.answer('Рассылка отменена')