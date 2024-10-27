from django.conf import settings
from django.core.mail import send_mail

from newsletter.models import Client, Message, NewsLetter

from datetime import datetime
from django.core.mail import send_mail
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger


logger = logging.getLogger(__name__)


def send_clients_email(newsletter_item: NewsLetter):

    message_title = newsletter_item.message.title
    message_body = newsletter_item.message.body

    clients = newsletter_item.clients.all()

    email_list = [client.email for client in clients]

    send_mail(
        message_title,
        message_body,
        settings.EMAIL_HOST_USER,
        email_list,
    )

def send_daily_report():
    print('Отчет отправлен')


def schedule_newsletter(self, newsletter_item: NewsLetter):
    logger.info("Инициализация планировщика задач.")
    scheduler = BlockingScheduler(job_defaults={'misfire_grace_time': 15 * 60})

    newsletter_run_date = newsletter_item.first_sending_dt
    interval = newsletter_item.interval.frequency

    interval_map = {
        'minutely': IntervalTrigger(minutes=1),
        'daily': IntervalTrigger(days=1),
        'weekly': IntervalTrigger(weeks=1),
        'monthly': IntervalTrigger(weeks=4)
    }

    trigger = interval_map.get(interval)

    scheduler.add_job(send_clients_email, trigger , start_date=newsletter_run_date)

    try:
        logger.info("Запуск планировщика.")
        scheduler.start()
    except Exception as e:
        logger.error(f"Ошибка при запуске планировщика: {e}")
