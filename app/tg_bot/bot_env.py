from textwrap import dedent

from environs import Env
import telebot
import logging


env = Env()
env.read_env()

account_id = env('ACCOUNT_ID')
secret_key = env('SECRET_KEY')
return_url = env('RETURN_URL', default='https://www.example.com/return_url')
tg_bot_token = env('TG_CLIENTS_TOKEN')
allowed_hosts = env.list("ALLOWED_HOSTS", [])
bot = telebot.TeleBot(tg_bot_token)

bot.set_my_commands([
    telebot.types.BotCommand("/start", "В начало"),
])

description_text = '''
        - зарегистрировать на Python мипап
        - узнать расписание митапа
        - задать вопросы докладчикам во время выступлений
        - оперативно получить информацию об изменениях
        - быть в курсе о следующих мероприятиях 
'''

bot.set_my_description(dedent(description_text))

chats = {}

logging.basicConfig(level=logging.INFO, filename="bot_log.log", filemode="w")

chats = {}
