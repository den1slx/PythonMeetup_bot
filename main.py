import logging

from environs import Env
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, Updater, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def command_start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Регистрация", callback_data='1'),
            InlineKeyboardButton("О нас", callback_data='2'),
        ],
        [InlineKeyboardButton("Расписание", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_bot_token = env('TG_CLIENTS_TOKEN')
    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", command_start))
    updater.start_polling()
    updater.idle()

