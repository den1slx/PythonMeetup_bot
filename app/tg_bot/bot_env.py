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

chats = {}

logging.basicConfig(level=logging.INFO, filename="bot_log.log", filemode="w")