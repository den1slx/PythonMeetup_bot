from environs import Env
import telebot


env = Env()
env.read_env()
tg_bot_token = env('TG_CLIENTS_TOKEN')
bot = telebot.TeleBot(tg_bot_token)