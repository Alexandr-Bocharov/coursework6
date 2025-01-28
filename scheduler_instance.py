from apscheduler.schedulers.background import BackgroundScheduler
import pytz

timezone = pytz.timezone('Europe/Moscow')
scheduler = BackgroundScheduler(timezone=timezone)
scheduler.start()
