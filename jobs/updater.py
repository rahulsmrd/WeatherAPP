from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from jobs.jobs import get_cities_and_update_DB, get_aggregates

def start_job1():
    scheduler1 = BackgroundScheduler()
    scheduler1.add_job(func=get_cities_and_update_DB, trigger='interval', minutes=5)
    scheduler1.start()

def start_job2():
    scheduler2 = BackgroundScheduler()
    scheduler2.add_job(func=get_aggregates, trigger='cron', hour=23, minute=55)
    scheduler2.start()