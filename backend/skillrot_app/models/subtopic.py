from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from skillrot_app.models.base import Base

class Subtopic(Base):
    __tablename__ = "subtopics"

    id = Column(Integer, primary_key=True, index=True)

    skill_id = Column(
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(String, nullable=False)

    # 🔥 Keep consistent scale with main health (0–100)
    health_score = Column(Float, default=100.0)

    last_practiced = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())