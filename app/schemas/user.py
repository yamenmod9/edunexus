from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    sat_exam_date: Optional[date] = None
    target_score: Optional[int] = Field(None, ge=400, le=1600)


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    full_name: Optional[str] = None
    sat_exam_date: Optional[date] = None
    target_score: Optional[int] = Field(None, ge=400, le=1600)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    sat_exam_date: Optional[date]
    target_score: Optional[int]

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None
    type: Optional[str] = None
