from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.CLIENT

class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UploadBase(BaseModel):
    filename: str
    file_url: str
    description: Optional[str] = None

class UploadCreate(UploadBase):
    pass

class UploadResponse(UploadBase):
    id: int
    client_id: int
    status: Optional[str] = "uploaded" # Placeholder
    created_at: datetime
    class Config:
        orm_mode = True

class ReportCreate(BaseModel):
    title: str
    report_url: str
    client_id: int
    upload_id: Optional[int] = None

class ReportResponse(ReportCreate):
    id: int
    admin_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class InquiryCreate(BaseModel):
    name: str
    email: EmailStr
    message: str
