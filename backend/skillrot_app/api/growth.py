from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from skillrot_app.db.database import get_db
from skillrot_app.services.growth_service import get_growth_data

router = APIRouter(
    prefix="/growth",
    tags=["Growth Analytics"]
)

@router.get("/skills/{skill_id}")
def get_skill_growth(skill_id: int, db: Session = Depends(get_db)):

    data = get_growth_data(skill_id, db)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    return data