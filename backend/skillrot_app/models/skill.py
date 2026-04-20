from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from skillrot_app.models.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Universal skill name (no restriction)
    name = Column(String, nullable=False, index=True)

    # Beginner / Intermediate / Advanced (string, not enum)
    level = Column(String, nullable=False)

    # Optional category for future scalability
    category = Column(String, nullable=True)

    # Starting reference date for decay
    learned_date = Column(Date, nullable=False)

    # For better tracking
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="skills")