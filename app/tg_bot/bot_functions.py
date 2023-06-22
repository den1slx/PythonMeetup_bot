from datetime import date, datetime
from textwrap import dedent
from telebot.apihelper import ApiTelegramException
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from tg_bot.bot_env import logging, account_id, secret_key, return_url
from tg_bot.models import Event, Lecture, Particiant
from tg_bot.bot_env import telebot, bot, chats
from tg_bot.bot_markups import speaker_menu_markup, user_menu_markup, registrate_markup, accept_markup, remove_markup, \
    admin_menu_markup, event_menu_markup, get_donation_markup

from tg_bot.models import Particiant


from tg_bot.models import Particiant


from tg_bot.models import Particiant


from tg_bot.models import Particiant


def is_registered_user(chat_id):
    try:
        Particiant.objects.get(telegram_id=chat_id)
        return True
    except Particiant.DoesNotExist:
        return False


def is_speaker(chat_id):
    return Particiant.objects.get(telegram_id=chat_id).role == 2


def is_admin(chat_id):
    return Particiant.objects.get(telegram_id=chat_id).role == 1


def add_admin(telegram_id):
    user = Particiant.objects.filter(telegram_id=telegram_id)
    user.update(role=1)


def get_info(message: telebot.types.Message):
    message_text = f'''
    <b>О нас</b>
    Мы решили собрать экспертов, чтобы они поделись опытом и новыми идеями. 
    Чтобы участники могли приобрести новые знакомства и пообщаться в неформальной обстановке.

    Присоединяйтесь к нам!
    '''
    message_text = dedent(message_text)
    bot.edit_message_text(message_text, message.chat.id, message.id,
                          reply_markup=get_menu_markup(message.chat.id), parse_mode='HTML')
    # bot.send_message(message.chat.id, text_message, parse_mode='HTML', reply_markup=get_menu_markup(message.chat.id))
    # return


def save_user_in_db(tg_id, fullname, mail, phone):
    Particiant.objects.get_or_create(telegram_id=tg_id, name=fullname, email=mail, phone=phone)
    return


def spam_schedule_message(message: telebot.types.Message):
    ids = Particiant.objects.get_ids()
    for id_ in ids:
        try:
            msg = bot.send_message(id_, 'Расписание изменено', reply_markup=remove_markup)
            text = get_schedule(msg, text_only=True)
            bot.send_message(id_, text, reply_markup=remove_markup, parse_mode='HTML')
        except ApiTelegramException:
            logging.info(f'Этот пользователь({id_}) не общался с ботом "spam_schedule_message"')
            continue


def spam_event_message(message):
    ids = Particiant.objects.get_ids()
    today = timezone.localtime().now().date()
    event = Event.objects.filter(date__gt=today).order_by('date').first()
    event_date = event.date
    event_info = f'{event.start} - {event.end}'
    for id_ in ids:
        try:
            msg = bot.send_message(id_, f'Следующий эвент будет {event_date}.', reply_markup=remove_markup)
            bot.send_message(id_, f'Время проведения эвента: {event_info}. Посетите нас снова.')
        except ApiTelegramException:
            logging.info(f'Этот пользователь({id_}) не общался с ботом "spam_event_message"')
            continue


def get_schedule(message: telebot.types.Message, text_only=False):
    # TODO get schedule from db
    current_date = date.today()
    event = Event.objects.filter(date__gte=current_date).order_by('date').first()
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
            lecture_start = lecture.start.strftime('%H:%M')
            lecture_end = lecture.end.strftime('%H:%M')
            if message.chat.id == lecture.speaker.telegram_id:
                speaker_text = ' <b>Вы докладчик</b>'
            else:
                speaker_text = ''
            if lecture == event.active_or_next_lecture:
                active_lesson = '🔊'
            else:
                active_lesson = ''
            message_text += f"{active_lesson}{lecture_start} - {lecture_end} <b>{lecture.title}</b> " \
                            f"(<i>{lecture.speaker.name}</i>){speaker_text}\n"
    if text_only:
        return message_text
    # bot.edit_message_text(message_text, message.chat.id, message.id, parse_mode='HTML', reply_markup=remove_markup)
    #  Убрал маркап тк расписание также используется у зарегистрированных пользователей  # TODO clean up
    bot.edit_message_text(message_text, message.chat.id, message.id,
                          reply_markup=get_menu_markup(message.chat.id), parse_mode='HTML')
    # bot.send_message(message.chat.id, message_text, parse_mode='HTML', reply_markup=registrate_markup)
    return


def change_speaker(message):
    speaker = Particiant.objects.filter(role=2)
    speaker_id = speaker.first().telegram_id
    speaker.update(role=3, status=True)
    bot.send_message(speaker_id, 'Ваше выступление завершено. Освободите сцену')
    now = timezone.localtime().now().time()
    today = timezone.localtime().now().date()
    event = Event.objects.filter(date=today).order_by('date').first()
    next_lecture = Lecture.objects.filter(event=event, end__gt=now, status=False).order_by('start').first()
    if not next_lecture or next_lecture == event.active_or_next_lecture:
        event.active_or_next_lecture = None
        return
    event.active_or_next_lecture = next_lecture
    next_speaker_id = next_lecture.speaker.telegram_id
    while timezone.localtime().now().time() < next_lecture.start:  # TODO add normal time skip. need better variant
        pass

    Particiant.objects.filter(telegram_id=next_speaker_id).update(role=2)
    bot.send_message(next_speaker_id, 'Ваше выступление началось. Выходите на сцену')
    # Рассылка:
    ids = Particiant.objects.get_ids()
    name = next_lecture.speaker.name
    theme = next_lecture.title
    for id_ in ids:
        try:
            bot.send_message(
                id_,
                f'Выступление по теме "{theme}" началось. Выступает {name}.',
                reply_markup=remove_markup
            )
        except ApiTelegramException:
            logging.info(f'ApiTelegramException in change_speaker')
            continue


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
            save_user_in_db(user['id'], user['fullname'], user['mail'], user['phonenumber'])
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


def event_start_notification(message=None):
    current_date = date.today()
    event = Event.objects.filter(date__gte=current_date).order_by('date').first()
    if event:
        now = datetime.now().strftime("%H:%M")
        event_date = event.date.strftime('%d.%m.%Y')
        event_start = event.start.strftime('%H:%M')
        if event.date == current_date and event_start == now:
            first_lecture = Lecture.objects.filter(event=event).order_by('start').first()
            first_speaker_id = first_lecture.speaker.telegram_id
            event.active_or_next_lecture = first_lecture
            event.save()
            Particiant.objects.filter(telegram_id=first_speaker_id).update(role=2)
            bot.send_message(first_speaker_id, 'Ваше выступление началось. Выходите на сцену')
            for user in Particiant.objects.all():
                message_text = f'''
                Уважаемый {user.name}!
                Митап {event_date} начался в {event_start}.
                Ознакомтесь с расписанием.
                '''
                message_text = dedent(message_text)
                try:
                    msg = bot.send_message(user.telegram_id, message_text,
                                           reply_markup=get_menu_markup(user.telegram_id))
                except ApiTelegramException:
                    logging.info('AttributeError: chat not found')


def ask_question(message):
    now = timezone.localtime().now()
    event = Event.objects.filter(date=now.date()).order_by('date').first()
    lecture = Lecture.objects.filter(event=event, start__lte=now.time(), end__gte=now.time()).first()
    if lecture:
        speaker = lecture.speaker
        msg = bot.send_message(message.chat.id, f'Доклад: {lecture.title}\nДокладчик: {speaker.name}\n'
                                                f'Введите свой вопрос докладчику')
        bot.register_next_step_handler(msg, question_sent, speaker)
    else:
        bot.send_message(message.chat.id, 'Задавайте вопросы во время ивента')


def question_sent(message, question):
    speaker = Particiant.objects.filter(role=2).first()
    if speaker:
        try:
            speaker_id = speaker.telegram_id
            bot.reply_to(message, f'Ваш вопрос отправлен:\n {message.text}')
            bot.send_message(speaker_id, message.text)
        except AttributeError:
            bot.reply_to(message, f'Ваш вопрос не отправлен:\n {message.text}')
            logging.info('AttributeError: speaker not found')
    else:
        bot.reply_to(message, f'Ваш вопрос не отправлен. Нет активного спикера')


def donate(message):

    donate_markup = get_donation_markup(account_id, secret_key, return_url)
    bot.reply_to(message, 'Ваша поддержка поможет исправить баги в этом чат-боте!\n'
                          'Пример тестовой карты с сайта ЮМани: 5555555555554477', reply_markup=donate_markup)


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
    now = datetime.now().strftime('%H:%M')
    timezone_now = timezone.localtime().now().strftime('%H:%M')
    user_id = message.from_user.id
    reply_markup = get_menu_markup(user_id)
    current_date = date.today()
    event = Event.objects.filter(date__gte=current_date).order_by('date').first()
    if not is_registered_user(user_id):
        chats[message.chat.id] = {
            'fullname': None,
            'mail': None,
            'id': None,
            'phonenumber': None,
        }
        username = message.from_user.username
    else:
        try:
            username = Particiant.objects.get(telegram_id=user_id).name
        except ObjectDoesNotExist:
            username = message.from_user.username
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
        f'Здравствуйте, {username}. Сейчас {now}',
        reply_markup=reply_markup
    )
