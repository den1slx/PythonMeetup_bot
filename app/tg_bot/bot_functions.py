from tg_bot.bot_env import telebot, bot
from tg_bot.bot_markups import speaker_menu_markup, user_menu_markup, registrate_markup, accept_markup, remove_markup


def is_registered_user(chat_id):
    # TODO check user in db
    return False


def is_speaker(chat_id):
    # TODO check user status
    return True


def get_info(message: telebot.types.Message):
    # TODO add info
    bot.send_message(message.chat.id, f'Информация о нас')
    return


def get_schedule(message: telebot.types.Message):
    # TODO get schedule from db
    bot.send_message(message.chat.id, f'Расписание выступлений')
    return


def change_speaker():
    # TODO change speaker status
    return


def registrate_user(message: telebot.types.Message, step=0):
    if step == 0:
        msg = bot.send_message(message.chat.id, f'Введите ваше ФИО')
        bot.register_next_step_handler(msg, registrate_user, 1)
    if step == 1:
        msg = bot.send_message(message.chat.id, f'Ваше ФИО: {message.text}', reply_markup=accept_markup)
        bot.register_next_step_handler(msg, registrate_user, 2)
    if step == 2:
        if message.text == 'Подтвердить':
            # TODO save user fullname for next steps
            msg = bot.send_message(message.chat.id, f'Введите вашу почту', reply_markup=remove_markup)
            bot.register_next_step_handler(msg, registrate_user, 3)
        else:
            return
    if step == 3:
        msg = bot.send_message(message.chat.id, f'Ваша почта: {message.text}', reply_markup=accept_markup)
        bot.register_next_step_handler(msg, registrate_user, 4)
    if step == 4:
        if message.text == 'Подтвердить':
            # TODO save user in db
            msg = bot.send_message(
                message.chat.id,
                'Регистрация завершена. Используйте команду /start',
                reply_markup=remove_markup
            )
            return
        return


def start_bot(message: telebot.types.Message):
    user_id = message.from_user.id
    if is_registered_user(user_id):
        if is_speaker(user_id):
            bot.send_message(
                message.chat.id,
                f'Здравствуйте, {message.from_user.username}',
                reply_markup=speaker_menu_markup)
        else:
            bot.send_message(
                message.chat.id,
                f'Здравствуйте, {message.from_user.username}',
                reply_markup=user_menu_markup
            )
    else:
        bot.send_message(
            message.chat.id,
            f'Здравствуйте, {message.from_user.username}',
            reply_markup=registrate_markup
        )
