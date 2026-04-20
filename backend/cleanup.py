from skillrot_app.db.database import SessionLocal, engine
from skillrot_app.models.base import Base
from skillrot_app.models.subtopic import Subtopic
from skillrot_app.models.skill import Skill
# Ensure models are registered
import skillrot_app.models.user
import skillrot_app.models.skill
import skillrot_app.models.skill_history
import skillrot_app.models.subtopic
import skillrot_app.models.skill_health_history
import skillrot_app.models.reminder

db = SessionLocal()
# Delete bad DBMS subtopics from CN
cn_skill = db.query(Skill).filter(Skill.name == "CN").first()
if cn_skill:
    bad_topics = db.query(Subtopic).filter(Subtopic.skill_id == cn_skill.id).all()
    for topic in bad_topics:
        if "database" in topic.name.lower() or "dbms" in topic.name.lower() or "concurrency" in topic.name.lower():
            print(f"Deleting bad topic: {topic.name} from CN")
            db.delete(topic)
    db.commit()

# Check for `{` in SQL or any skill and delete
bad_bracket_topics = db.query(Subtopic).filter(Subtopic.name.like("%{%") | Subtopic.name.like("%}%")).all()
for topic in bad_bracket_topics:
    print(f"Deleting bracket topic: {topic.name} from skill {topic.skill_id}")
    db.delete(topic)
db.commit()

print("Cleanup complete.")
