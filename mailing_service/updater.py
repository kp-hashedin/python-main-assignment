from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_emails

def start():
    scheduler = BackgroundScheduler()
    
    #This will trigger at 10:00PM
    # scheduler.add_job(schedule_emails, 'interval',seconds = 10) 
    scheduler.add_job(schedule_emails, 'cron', hour= 22, minute= 00)
    scheduler.start()