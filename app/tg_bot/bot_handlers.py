from time import sleep

from tg_bot.bot_env import telebot, bot
import tg_bot.bot_functions as calls
import schedule
import threading

calls_map = {
    '1': calls.registrate_user,
    '2': calls.get_info,
    '3': calls.get_schedule,
    '4': calls.change_speaker,
    '5': calls.ask_question,
    '6': calls.spam_schedule_message,
    '7': calls.spam_event_message,
    '8': calls.donate,
}


@bot.message_handler(commands=['start'])
def command_menu(message: telebot.types.Message):
    calls.start_bot(message)


@bot.message_handler(commands=['event'])
def command_menu(message: telebot.types.Message):
    calls.event_start_notification(message)


@bot.callback_query_handler(func=lambda call: call.data)
def handle_buttons(call):
    calls_map[call.data](call.message)


def runBot():
    bot.infinity_polling()


def runSchedulers():
    # schedule.every(1).day.at("12:00").do(calls.send_start_notification)  # - запуск каждый день в определенное время
    schedule.every(1).minutes.at(":01").do(calls.event_start_notification)  # - запуск каждую минуту

    while True:
        schedule.run_pending()
        sleep(1)


def run_bot():
    t1 = threading.Thread(target=runBot, daemon=True)
    t2 = threading.Thread(target=runSchedulers, daemon=True)
    t1.start()
    t2.start()

    while 1:
        pass