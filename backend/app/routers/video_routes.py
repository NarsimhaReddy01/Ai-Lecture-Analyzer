# backend/app/routers/video_routes.py
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
import os
from typing import List

from backend.app.database import get_db
from backend.app import models, schemas

# AI Processing
import whisper
from backend.app.utils.summarizer import summarize_text
from backend.app.utils.quiz_generator import generate_quiz  # you should implement this


router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)

# Upload folder
BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=schemas.VideoOut)
async def upload_video(
    title: str = Form(...),
    language: str = Form("auto"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Form(...),
):
    """
    Upload a lecture video and automatically process transcription, summary, and quiz.
    """

    # Validate file type
    if not file.filename.lower().endswith((".mp4", ".avi", ".mkv")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only MP4, AVI, MKV allowed.")

    # Save video file
    file_ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    file_url = f"/data/{unique_filename}"

    # Save Video entry in DB first
    new_video = models.Video(
        title=title,
        filename=unique_filename,
        file_url=file_url,
        language=language,
        user_id=user_id
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    # 1️⃣ Transcription
    transcript_text = ""
    try:
        model = whisper.load_model("base")
        result = model.transcribe(file_path, language=language)
        transcript_text = result.get("text", "")
    except Exception as e:
        print(f"Transcription failed: {str(e)}")

    # 2️⃣ Summarization
    summary_text = ""
    try:
        summary_text = summarize_text(transcript_text) if transcript_text else ""
    except Exception as e:
        print(f"Summarization failed: {str(e)}")

    # 3️⃣ Quiz Generation
    quiz_questions = []
    try:
        quiz_questions = generate_quiz(transcript_text) if transcript_text else []
    except Exception as e:
        print(f"Quiz generation failed: {str(e)}")

    # 4️⃣ Save Transcript
    if transcript_text:
        transcript = models.Transcript(
            original_text=transcript_text,
            translated_text=summary_text,  # storing summary as translated_text optionally
            timestamps=None,
            video_id=new_video.id
        )
        db.add(transcript)
        db.commit()
        db.refresh(transcript)
        new_video.transcript = transcript

    # 5️⃣ Save Quiz
    if quiz_questions:
        quiz = models.Quiz(
            questions=quiz_questions,
            video_id=new_video.id
        )
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        new_video.quizzes.append(quiz)

    db.commit()
    db.refresh(new_video)

    return new_video


@router.get("/", response_model=List[schemas.VideoOut])
def list_videos(db: Session = Depends(get_db)):
    """
    List all uploaded videos with transcripts and quizzes
    """
    videos = db.query(models.Video).all()
    return videos


@router.get("/{video_id}", response_model=schemas.VideoOut)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """
    Get a specific video by ID
    """
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
