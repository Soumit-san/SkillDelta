from skillrot_app.db.database import engine
from skillrot_app.models.base import Base
from skillrot_app.models import user, skill, skill_history

def init_db():
    Base.metadata.create_all(bind=engine)
