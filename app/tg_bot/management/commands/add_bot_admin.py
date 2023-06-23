from django.core.management.base import BaseCommand
from tg_bot.bot_functions import add_admin


class Command(BaseCommand):
    help = 'Add admin for bot'

    def add_arguments(self, parser):
        parser.add_argument('telegram_id', type=int, help='Telegram user id')

    def handle(self, *args, **options):
        add_admin(options['telegram_id'])