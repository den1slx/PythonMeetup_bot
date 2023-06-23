from datetime import date
from textwrap import dedent

from tg_bot.models import Event, Lecture, Particiant
from tg_bot.bot_env import telebot, bot, chats
from tg_bot.bot_markups import speaker_menu_markup, user_menu_markup, registrate_markup, accept_markup, remove_markup, \
    admin_menu_markup, event_menu_markup


def is_registered_user(chat_id):
    # TODO check user in db
    return True


def is_speaker(chat_id):
    # TODO check user status
    return False


def is_admin(chat_id):
    # TODO check user status
    return False


def get_info(message: telebot.types.Message):
    # TODO add info
    bot.send_message(message.chat.id, f'Информация о нас')
    return


def save_user_in_db(tg_id, fullname, mail):
    Particiant.objects.get_or_create(telegram_id=tg_id, name=fullname, email=mail)
    return


def get_schedule(message: telebot.types.Message):
    # TODO get schedule from db
    current_date = date.today()
    event = Event.objects.filter(date__gte=current_date).first()
    if event is None:
        message_text = 'Митап пока на стадии подготовки. Позже оправим вам дополнительную информацию.'
    else:
        start_text = f'''
                <b>Расписание митапа {event.date}</b> 
                ({event.start.strftime('%H:%M')}-{event.end.strftime('%H:%M')})

                '''
        message_text = dedent(start_text)
        lectures = Lecture.objects.filter(event=event)
        for lecture in lectures:
            message_text += f"{lecture.start.strftime('%H:%M')} - {lecture.title}\n"
    # bot.edit_message_text(message_text, message.chat.id, message.id, parse_mode='HTML', reply_markup=remove_markup)
    #  Убрал маркап тк расписание также используется у зарегистрированных пользователей  # TODO clean up
    bot.edit_message_text(message_text, message.chat.id, message.id, parse_mode='HTML')
    # bot.send_message(message.chat.id, message_text, parse_mode='HTML', reply_markup=registrate_markup)
    return


def change_speaker():
    # TODO change speaker status
    return


def registrate_user(message: telebot.types.Message, step=0):
    user = chats[message.chat.id]
    user['id'] = message.from_user.id
    if step == 0:
        msg = bot.send_message(message.chat.id, f'Введите ваше ФИО')
        bot.register_next_step_handler(msg, registrate_user, 1)
    if step == 1:
        msg = bot.send_message(message.chat.id, f'Ваше ФИО: {message.text}', reply_markup=accept_markup)
        user['fullname'] = message.text
        bot.register_next_step_handler(msg, registrate_user, 2)
    if step == 2:
        if message.text == 'Подтвердить':
            # TODO save user fullname for next steps
            msg = bot.send_message(message.chat.id, f'Введите вашу почту', reply_markup=remove_markup)
            bot.register_next_step_handler(msg, registrate_user, 3)
        else:
            bot.send_message(message.chat.id, f'Используйте команду /start', reply_markup=remove_markup)
            return
    if step == 3:
        msg = bot.send_message(message.chat.id, f'Ваша почта: {message.text}', reply_markup=accept_markup)
        user['mail'] = message.text
        bot.register_next_step_handler(msg, registrate_user, 4)
    if step == 4:
        if message.text == 'Подтвердить':
            msg = bot.send_message(message.chat.id, f'Введите ваш телефон', reply_markup=remove_markup)
            bot.register_next_step_handler(msg, registrate_user, 5)
        else:
            bot.send_message(message.chat.id, f'Используйте команду /start', reply_markup=remove_markup)
            return
    if step == 5:
        msg = bot.send_message(message.chat.id, f'Ваш телефон: {message.text}', reply_markup=accept_markup)
        user['phonenumber'] = message.text
        bot.register_next_step_handler(msg, registrate_user, 6)
    if step == 6:
        if message.text == 'Подтвердить':
            save_user_in_db(user['id'], user['fullname'], user['mail'])
            msg = bot.send_message(
                message.chat.id,
                'Регистрация завершена. Используйте команду /start',
                reply_markup=remove_markup
            )
            return
        else:
            bot.send_message(message.chat.id, f'Используйте команду /start', reply_markup=remove_markup)
            return
        return


def event_start(message):
    msg = bot.send_message(message.chat.id, 'Мероприятие 20.06 началось', reply_markup=event_menu_markup)


def ask_question(message):
    msg = bot.send_message(message.chat.id, 'Введите свой вопрос докладчику')
    bot.register_next_step_handler(msg, question_sent)


def question_sent(message):
    bot.reply_to(message, f'Ваш вопрос отправлен:\n {message.text}')


def get_menu_markup(user_id):
    if is_registered_user(user_id):
        if is_speaker(user_id):
            reply_markup = speaker_menu_markup
        elif is_admin(user_id):
            reply_markup = admin_menu_markup
        else:
            reply_markup = user_menu_markup
    else:
        reply_markup = registrate_markup
    return reply_markup


def start_bot(message: telebot.types.Message):
    user_id = message.from_user.id
    reply_markup = get_menu_markup(user_id)
    current_date = date.today()
    event = Event.objects.filter(date__gte=current_date).first()
    if not is_registered_user(user_id):
        chats[message.chat.id] = {
            'fullname': None,
            'mail': None,
            'id': None,
            'phonenumber': None,
        }
        username = message.from_user.username
    else:
        username = Particiant.objects.get(telegram_id=user_id).name
    message_text = f'''
        Здравствуйте, {username}
        Это чат бот Python митапа.
        Ближайший состоится {event.date.strftime('%d.%m.%Y')}
        
        Здесь вы можете: 
        - зарегистрироваться 
        - узнать расписание митапа
        - задать вопросы докладчикам во время выступлений
        - оперативно получить информацию об изменениях
        - быть в курсе о следующих мероприятиях 
        '''
    message_text = dedent(message_text)
    bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=reply_markup

    )


    # if is_registered_user(user_id):
    #     if is_speaker(user_id):
    #         bot.send_message(
    #             message.chat.id,
    #             f'Здравствуйте, {message.from_user.username}',
    #             reply_markup=speaker_menu_markup)
    #     elif is_admin(user_id):
    #         bot.send_message(
    #             message.chat.id,
    #             f'Здравствуйте, {message.from_user.username}',
    #             reply_markup=admin_menu_markup)
    #     else:
    #         bot.send_message(
    #             message.chat.id,
    #             f'Здравствуйте, {message.from_user.username}',
    #             reply_markup=user_menu_markup
    #         )
    # else:
    #     chats[message.chat.id] = {
    #         'fullname': None,
    #         'mail': None,
    #         'id': None,
    #         'phonenumber': None,
    #     }
    #     bot.send_message(
    #         message.chat.id,
    #         f'Здравствуйте, {message.from_user.username}',
    #         reply_markup=registrate_markup
    #     )
