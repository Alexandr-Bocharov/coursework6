from datetime import datetime
from django.core.mail import send_mail
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand
from newsletter.services import send_clients_email

logger = logging.getLogger(__name__)

def send_email():
    try:
        send_mail(
            'Время',
            f'Настоящее время: {datetime.now()}',
            from_email='counter230620013@yandex.com',
            recipient_list=['counter23062001@mail.ru'],
        )
        logger.info("Письмо успешно отправлено.")
    except Exception as e:
        logger.error(f"Ошибка при отправке письма: {e}")

class Command(BaseCommand):
    help = "Запускает APScheduler."

    def handle(self, *args, **options):
        logger.info("Инициализация планировщика задач.")
        scheduler = BlockingScheduler(job_defaults={'misfire_grace_time': 15 * 60})

        run_date = datetime(2024, 10, 27, 10, 5)  # Проверьте время запуска
        scheduler.add_job(send_email, 'interval', minutes=3, start_date=run_date)

        try:
            logger.info("Запуск планировщика.")
            scheduler.start()
        except Exception as e:
            logger.error(f"Ошибка при запуске планировщика: {e}")
