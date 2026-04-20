import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from skillrot_app.db.database import SessionLocal
from skillrot_app.services.reminder_service import check_and_create_reminders

scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Kolkata"))

def start_scheduler():

    def job():
        db = SessionLocal()
        try:
            print("Running daily IST 9am skill decay reminder check...")
            check_and_create_reminders(db)
        finally:
            db.close()

    # Run strictly every day at 09:00 AM IST instead of randomly every 1 hour upon boot
    scheduler.add_job(job, "cron", hour=9, minute=0)
    scheduler.start()