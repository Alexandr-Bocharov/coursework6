# from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
# from django.core.mail import send_mail
#
# def send_email():
#     send_mail(
#         'время',
#         f'настоящее время: {datetime.now()}',
#         from_email='counter230620013@yandex.com',
#         recipient_list=['counter23062001@mail.ru'],
#     )
#
# scheduler = BlockingScheduler()
#
# run_date = datetime(2024, 10, 18, 23, 30)
#
# scheduler.add_job(send_email(), 'interval', seconds=5 ,start_date=run_date)
#
# scheduler.start()
print(datetime.now())