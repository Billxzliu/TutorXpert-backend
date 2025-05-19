from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    education_level: Optional[str] = None
    major: Optional[str] = None
    certifications: Optional[str] = None
    working_with_children_check: Optional[str] = None
    subjects: Optional[str] = None
    has_experience: Optional[bool] = None
    experience_details: Optional[str] = None
    availability: Optional[str] = None
    accepts_short_notice: Optional[bool] = None

class UserCreate(ProfileBase):
    email: EmailStr
    password: str
    role: str = "student"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProfileCreate(ProfileBase):
    pass

class ProfileOut(ProfileCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True
