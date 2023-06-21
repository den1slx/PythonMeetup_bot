import telebot
from environs import Env

import tg_bot.bot_functions as calls


env = Env()
env.read_env()
tg_bot_token = env('TG_CLIENTS_TOKEN')
bot = telebot.TeleBot(tg_bot_token)


calls_map = {
    '1': calls.registrate_user,
    '2': calls.get_info,
    '3': calls.get_schedule,
    '4': calls.change_speaker,
}


@bot.message_handler(commands=['start'])
def command_menu(message: telebot.types.Message):
    calls.start_bot(message)


@bot.callback_query_handler(func=lambda call: call.data)
def handle_buttons(call):
    calls_map[call.data](call.message)


def run_bot():
    bot.infinity_polling()