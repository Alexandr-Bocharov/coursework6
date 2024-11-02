from django.conf import settings
import pytz
from newsletter.models import NewsLetter, DeliveryAttempt

from datetime import datetime
from django.core.mail import send_mail
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from scheduler_instance import scheduler

timezone = pytz.timezone('Europe/Moscow')



logger = logging.getLogger(__name__)


def send_clients_email(newsletter_item: NewsLetter):
    current_time = datetime.now(pytz.timezone('Europe/Moscow'))

    if current_time >= newsletter_item.last_sending_dt.astimezone(timezone):

        scheduler.remove_job(str(newsletter_item.id))
        newsletter_item.status = NewsLetter.Status.COMPLETED
        newsletter_item.save()
        logger.info(f"Задача рассылки {newsletter_item.id} завершена и удалена по расписанию.")
        return  # Завершаем выполнение функции

    message_title = newsletter_item.message.title
    message_body = newsletter_item.message.body
    clients = newsletter_item.clients.all()
    email_list = [client.email for client in clients]

    attempt = DeliveryAttempt(newsletter=newsletter_item)
    attempt.save()

    try:
        send_mail(
            message_title,
            message_body,
            settings.EMAIL_HOST_USER,
            email_list,
            fail_silently=False,
        )
        logger.info(f"Рассылка отправлена на адреса: {email_list}")
        attempt.status = 'success'
        attempt.response = 'Сообщение успешно отправлено'

    except Exception as e:
        logger.error(f"Ошибка при отправке рассылки: {e}")
        attempt.status = 'failed'
        attempt.response = f'ошибка: {str(e)}'

    attempt.save()


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

    scheduler.add_job(send_clients_email, trigger, start_date=newsletter_run_date)

    try:
        logger.info("Запуск планировщика.")
        scheduler.start()
    except Exception as e:
        logger.error(f"Ошибка при запуске планировщика: {e}")


# def unschedule_newsletter(newsletter_id):
#     try:
#         scheduler.remove_job(str(newsletter_id))
#     except Exception as e:
#         print(f"Не удалось удалить задачу {newsletter_id}: {e}")
