from textwrap import dedent

from environs import Env
import telebot
import logging


env = Env()
env.read_env()
tg_bot_token = env('TG_CLIENTS_TOKEN')
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
