# app/schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class StudentCreate(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = "Student"  # 固定为 Student，也可在后端强制判断

class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class StudentOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True
