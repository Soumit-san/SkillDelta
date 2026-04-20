from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from skillrot_app.db.database import get_db
from skillrot_app.models.user import User
from skillrot_app.schemas.user import UserCreate, UserOut, UserUpdate
from skillrot_app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


@router.get("/me", response_model=UserOut)
def get_user_me(current_user: User = Depends(get_current_user)):
    """
    Returns the currently authenticated user's profile.
    """
    return current_user


@router.put("/update", response_model=UserOut)
def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Updates the currently authenticated user's profile.
    """
    current_user.name = user_update.name
    db.commit()
    db.refresh(current_user)
    return current_user