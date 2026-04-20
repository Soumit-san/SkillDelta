from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from skillrot_app.models.skill import Skill
from skillrot_app.models.skill_history import SkillHistory
from skillrot_app.models.reminder import Reminder
from skillrot_app.models.user import User
from skillrot_app.services.decay_service import recalculate_skill_decay
from skillrot_app.services.email_service import send_email


HEALTH_THRESHOLD = 50
INACTIVITY_DAYS = 14


def check_and_create_reminders(db: Session):

    skills = db.query(Skill).all()

    for skill in skills:

        user = db.query(User).filter(User.id == skill.user_id).first()
        if not user:
            continue

        # 🔥 Recalculate health
        health = recalculate_skill_decay(skill, db)

        # 🔥 Determine last usage
        history = (
            db.query(SkillHistory)
            .filter(SkillHistory.skill_id == skill.id)
            .order_by(SkillHistory.date.desc())
            .first()
        )

        last_used = history.date if history else skill.learned_date
        days_since = (date.today() - last_used).days

        print(f"SkillDelta Reminder → Skill: {skill.name}")
        print(f"Health: {health}, Days since: {days_since}")

        # 🔥 Trigger condition
        if health < HEALTH_THRESHOLD or days_since > INACTIVITY_DAYS:

            # ✅ Avoid duplicate reminder within 24h
            recent_reminder = (
                db.query(Reminder)
                .filter(
                    Reminder.skill_id == skill.id,
                    Reminder.created_at >= datetime.utcnow() - timedelta(hours=24),
                    Reminder.email_sent == True
                )
                .first()
            )

            if recent_reminder:
                print("Recent successful reminder exists. Skipping.")
                continue

            message = f"Skill '{skill.name}' needs attention. Health: {health}"

            reminder = Reminder(
                user_id=user.id,
                skill_id=skill.id,
                message=message,
                email_sent=False
            )

            db.add(reminder)
            db.commit()

            # 🔥 Professional SkillDelta HTML Email
            subject = f"SkillDelta: Quick update on your '{skill.name}' skill"

            text_body = f"""Hello {user.name},

We noticed that your skill '{skill.name}' hasn't been practiced recently.

Current Health: {round(health, 2)}%
Days Since Last Practice: {days_since}

Regular practice helps maintain skill retention. Consider dedicating a few minutes to review this topic soon!

Best regards,
The SkillDelta Team

---
SkillDelta Notifications
You are receiving this automated email because you opted into skill reminders on SkillDelta.
To unsubscribe or manage your preferences, please visit your account settings in the application.
"""

            html_body = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkillDelta Reminder</title>
  </head>
  <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #333333; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">

    <p style="font-size: 16px;">Hello {user.name},</p>

    <p style="font-size: 16px;">We noticed that your skill <strong>{skill.name}</strong> hasn't been practiced recently.</p>

    <div style="background-color: #f4f4f5; padding: 20px; border-radius: 12px; margin: 24px 0; border: 1px solid #e4e4e7;">
      <p style="margin: 0 0 10px 0; font-size: 15px;"><strong>Current Health:</strong> <span style="color: #ea580c; font-weight: bold;">{round(health, 2)}%</span></p>
      <p style="margin: 0; font-size: 15px;"><strong>Days Since Last Practice:</strong> {days_since}</p>
    </div>

    <p style="font-size: 16px;">Regular practice helps maintain skill retention. Consider dedicating a few minutes to review this topic soon!</p>

    <p style="font-size: 16px; margin-top: 32px;">
      Best regards,<br>
      <strong>The SkillDelta Team</strong>
    </p>

    <img src="https://raw.githubusercontent.com/metadroix35/SkillDelta/main/backend/skillrot_app/assets/skilldelta_logo.png" width="120" height="auto" style="margin-top: 24px; margin-bottom: 24px; display: block;" alt="SkillDelta" />

    <hr style="border: none; border-top: 1px solid #e4e4e7; margin: 32px 0;">

    <div style="font-size: 12px; color: #71717a; text-align: left;">
      <p style="margin: 0 0 8px 0;"><strong>SkillDelta Notifications</strong></p>
      <p style="margin: 0 0 8px 0;">You are receiving this automated email because you opted into skill reminders on SkillDelta.</p>
      <p style="margin: 0 0 16px 0;">To unsubscribe or manage your preferences, please <a href="https://skilldelta.com/profile" style="color: #ea580c; text-decoration: none;">visit your account settings</a>.</p>
      <p style="margin: 0;">&copy; {datetime.now().year} SkillDelta. All rights reserved.</p>
    </div>

  </body>
</html>"""

            success = send_email(user.email, subject, html_body, text_body)

            if success:
                reminder.email_sent = True
                db.commit()
                print("SkillDelta Email sent successfully.")
            else:
                print("SkillDelta Email sending failed.")