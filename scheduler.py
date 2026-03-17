from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import panel

from utils import get_payment_day

scheduler = BackgroundScheduler()


def auto_reset():
    today = datetime.date.today()
    payment_day = get_payment_day()

    if today.day == payment_day:
        panel.login()
        panel.reset_traffic()
        print("Traffic reset automatically")


scheduler.add_job(auto_reset, "cron", hour=0, minute=5)
scheduler.start()