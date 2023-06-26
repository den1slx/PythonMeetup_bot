from telebot import types
from yookassa import Configuration, Payment
import uuid


keyboard = [
    [
        types.InlineKeyboardButton("Регистрация", callback_data='1'),
        types.InlineKeyboardButton("О нас", callback_data='2'),
    ],
    [
        types.InlineKeyboardButton("Расписание", callback_data='3')
    ],
]
registrate_markup = types.InlineKeyboardMarkup(keyboard)


keyboard = [
    [
        types.InlineKeyboardButton("О нас", callback_data='2'),
    ],
    [
        types.InlineKeyboardButton("Расписание", callback_data='3')
    ],
    [
        types.InlineKeyboardButton("Задать вопрос", callback_data='5')
    ],
    [
        types.InlineKeyboardButton("Задонатить", callback_data='8')
    ],
]
user_menu_markup = types.InlineKeyboardMarkup(keyboard)


keyboard = [
    [
        types.InlineKeyboardButton("Закончить выступление", callback_data='4'),
    ],
]
speaker_menu_markup = types.InlineKeyboardMarkup(keyboard)


keyboard = [
    [
        types.InlineKeyboardButton("Задать вопрос", callback_data='5'),
        types.InlineKeyboardButton("Расписание", callback_data='3'),
    ],
]
event_menu_markup = types.InlineKeyboardMarkup(keyboard)


keyboard = [
    [
        types.InlineKeyboardButton("Заспамить расписание", callback_data='6'),
        types.InlineKeyboardButton("Заспамить эвент", callback_data='7'),
    ],
]
admin_menu_markup = types.InlineKeyboardMarkup(keyboard)


def get_donation_markup(account_id, secret_key, return_url):
    Configuration.configure(account_id, secret_key)

    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": "100.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "description": "Донат на митапе"
    }, idempotence_key)

    confirmation_url = payment.confirmation.confirmation_url

    keyboard = [
        [
            types.InlineKeyboardButton("Отправить 100 руб.", url=confirmation_url),
        ],
    ]
    return types.InlineKeyboardMarkup(keyboard)


accept = types.KeyboardButton(text='Подтвердить')
reject = types.KeyboardButton(text='Отменить')
accept_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
accept_markup.add(accept, reject)
remove_markup = types.ReplyKeyboardRemove()

