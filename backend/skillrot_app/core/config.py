from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):

    # -----------------------------------
    # 🔹 Core
    # -----------------------------------
    APP_NAME: str = "SkillDelta"
    DATABASE_URL: str

    # -----------------------------------
    # 🔹 Email
    # -----------------------------------
    EMAIL_ADDRESS: str | None = None
    EMAIL_PASSWORD: str | None = None

    # 🔥 SendGrid (recommended for production)
    SENDGRID_API_KEY: str | None = None

    # -----------------------------------
    # 🔐 JWT
    # -----------------------------------
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    # 🔁 Scheduler / Cron
    CRON_SECRET: str | None = None

    # -----------------------------------
    # ⚙ Config
    # -----------------------------------
    class Config:
        env_file = str(Path(__file__).resolve().parent.parent.parent / ".env")
        env_file_encoding = "utf-8"
        extra = "allow"  # 🔥 prevents crashes from unknown env vars


# 🔥 Create global settings object
settings = Settings()

print("ENV FILE LOADED")
print("DATABASE URL USED:", settings.DATABASE_URL)
print("EMAIL LOADED:", settings.EMAIL_ADDRESS)
print("SENDGRID ENABLED:", bool(settings.SENDGRID_API_KEY))

if not settings.EMAIL_ADDRESS and not settings.SENDGRID_API_KEY:
    print("⚠ WARNING: No email provider configured. Email reminders will fail.")