from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/{user_id}", response_model=schemas.ProfileOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/{user_id}", response_model=schemas.ProfileOut)
def update_profile(user_id: int, updated: schemas.ProfileCreate, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for field, value in updated.dict().items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile
