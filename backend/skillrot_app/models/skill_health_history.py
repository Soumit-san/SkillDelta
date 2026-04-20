from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from skillrot_app.models.base import Base

class SkillHealthHistory(Base):
    __tablename__ = "skill_health_history"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"))
    health = Column(Float)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())