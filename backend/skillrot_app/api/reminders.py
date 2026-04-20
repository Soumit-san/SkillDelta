from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from skillrot_app.db.database import get_db
from skillrot_app.services.reminder_service import check_and_create_reminders
from skillrot_app.models.reminder import Reminder

router = APIRouter(prefix="/reminders", tags=["Reminders"])


# =====================================================
# 🔹 1️⃣ Manual Reminder Trigger (Admin / Testing)
# =====================================================
@router.post("/run")
def run_reminder_check(db: Session = Depends(get_db)):
    """
    Manually trigger reminder scan.
    Useful for testing before scheduler is added.
    """
    check_and_create_reminders(db)
    return {"message": "Reminder check executed"}


# =====================================================
# 🔹 2️⃣ Get User In-App Reminders
# =====================================================
@router.get("/user/{user_id}")
def get_user_reminders(user_id: int, db: Session = Depends(get_db)):
    """
    Fetch all reminders for a user.
    Frontend will call this after login.
    """
    reminders = (
        db.query(Reminder)
        .filter(Reminder.user_id == user_id)
        .order_by(Reminder.created_at.desc())
        .all()
    )

    return reminders