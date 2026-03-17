from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import panel
import os
from dotenv import load_dotenv

load_dotenv()

payment_day = int(os.getenv("PAYMENT_DAY"))

scheduler = BackgroundScheduler()


def auto_reset():
    today = datetime.date.today()

    if today.day == payment_day:
        panel.login()
        panel.reset_traffic()
        print("Traffic reset automatically")


scheduler.add_job(auto_reset, "cron", hour=0, minute=5)
scheduler.start()