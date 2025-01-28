# scheduler.py
from apscheduler.triggers.interval import IntervalTrigger
from .services import send_clients_email  # функция отправки email клиентам
from scheduler_instance import scheduler, timezone



def schedule_newsletter(newsletter):


    interval_map = {
        'minutely': IntervalTrigger(minutes=1),
        'daily': IntervalTrigger(days=1),
        'weekly': IntervalTrigger(weeks=1),
        'monthly': IntervalTrigger(weeks=4)
    }

    trigger = interval_map.get(newsletter.interval.frequency)

    start_time = newsletter.first_sending_dt.astimezone(timezone)
    end_time = newsletter.last_sending_dt.astimezone(timezone)

    scheduler.add_job(
        send_clients_email,
        trigger,
        id=str(newsletter.id),
        args=[newsletter],
        start_date=start_time,
        end_date=end_time,
        next_run_time=start_time,
        replace_existing=True,
    )


def unschedule_newsletter(newsletter_id):
    try:
        scheduler.remove_job(str(newsletter_id))
    except Exception as e:
        print(f"Не удалось удалить задачу {newsletter_id}: {e}")