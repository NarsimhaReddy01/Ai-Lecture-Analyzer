# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime


# --------------------
# User Schemas
# --------------------
class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode


# --------------------
# Transcript Schemas
# --------------------
class TranscriptBase(BaseModel):
    original_text: str
    translated_text: Optional[str] = None
    timestamps: Optional[Dict] = None  # JSON field in DB


class TranscriptOut(TranscriptBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --------------------
# Quiz Schemas
# --------------------
class QuizBase(BaseModel):
    questions: List[Dict]  # List of Q&A dictionaries


class QuizOut(QuizBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --------------------
# Video Schemas
# --------------------
class VideoBase(BaseModel):
    title: str
    language: str


class VideoCreate(VideoBase):
    user_id: int


class VideoOut(VideoBase):
    id: int
    filename: str
    file_url: str
    uploaded_at: datetime
    transcript: Optional[TranscriptOut] = None
    quizzes: List[QuizOut] = []
    user_id: int

    class Config:
        from_attributes = True
