# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="student")  # student / admin / teacher
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    videos = relationship("Video", back_populates="owner")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    language = Column(String(50), default="auto")
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Optional quick access fields
    transcript_text = Column(Text, nullable=True)  # stores full transcript text
    summary_text = Column(Text, nullable=True)     # stores summary text

    # Relationships
    transcript = relationship("Transcript", back_populates="video", uselist=False)
    quizzes = relationship("Quiz", back_populates="video")

    owner = relationship("User", back_populates="videos")


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=True)
    translated_text = Column(Text, nullable=True)
    timestamps = Column(JSON, nullable=True)  # for timestamped subtitles
    created_at = Column(DateTime, default=datetime.utcnow)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)

    video = relationship("Video", back_populates="transcript")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    questions = Column(JSON, nullable=True)  # list of Q&A objects with metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)

    video = relationship("Video", back_populates="quizzes")
