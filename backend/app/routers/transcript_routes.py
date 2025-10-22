# backend/app/routers/transcript_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app import models, schemas

router = APIRouter(
    prefix="/transcripts",
    tags=["Transcripts"]
)


@router.get("/{video_id}", response_model=schemas.TranscriptOut)
def get_transcript(video_id: int, db: Session = Depends(get_db)):
    transcript = db.query(models.Transcript).filter(models.Transcript.video_id == video_id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return transcript
