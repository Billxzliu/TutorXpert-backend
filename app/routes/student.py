# app/routes/student.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/students", tags=["students"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=schemas.UserOut)
def register_student(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_pw,
        role="student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login_student(user: schemas.UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not existing_user or not pwd_context.verify(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {
        "id": existing_user.id,
        "email": existing_user.email,
        "role": existing_user.role
    }
