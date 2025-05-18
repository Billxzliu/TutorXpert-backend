# app/routes/student.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/students", tags=["students"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 注册
@router.post("/register", response_model=schemas.StudentOut)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    # 检查邮箱是否存在
    existing = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 哈希密码
    hashed_pw = pwd_context.hash(student.password)
    
    # 创建学生对象
    new_student = models.Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        hashed_password=hashed_pw,
        role=student.role
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# 登录
@router.post("/login")
def login_student(student: schemas.StudentLogin, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.email == student.email).first()
    if not db_student or not pwd_context.verify(student.password, db_student.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful", "student_id": db_student.id}
