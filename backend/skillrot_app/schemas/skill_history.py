from pydantic import BaseModel
from datetime import date

class SkillUsageCreate(BaseModel):
    usage: int  # 0 = not used, 1 = used
    date: date
