from telebot import types


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
]
user_menu_markup = types.InlineKeyboardMarkup(keyboard)


keyboard = [
    [
        types.InlineKeyboardButton("Закончить выступление", callback_data='4'),
    ],
]
speaker_menu_markup = types.InlineKeyboardMarkup(keyboard)


accept = types.KeyboardButton(text='Подтвердить')
reject = types.KeyboardButton(text='Отменить')
accept_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
accept_markup.add(accept, reject)
remove_markup = types.ReplyKeyboardRemove()

