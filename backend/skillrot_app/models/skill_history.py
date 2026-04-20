from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from skillrot_app.models.base import Base

class SkillHistory(Base):
    __tablename__ = "skill_history"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"))
    date = Column(Date, nullable=False)
    usage = Column(Integer)  # 0 or 1
    decay_score = Column(Float)
