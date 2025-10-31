# backend/app/routers/transcript_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app import models, schemas
from fastapi import APIRouter, BackgroundTasks
from app.tasks import process_lecture_video
from celery.result import AsyncResult
import os


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

router = APIRouter()

@router.post("/process-video")
def start_video_processing(video_path: str):
    """
    Start background video processing job via Celery.
    """
    task = process_lecture_video.delay(video_path)
    return {"task_id": task.id, "status": "queued"}

@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    """
    Get Celery job status and result.
    """
    result = AsyncResult(task_id)
    if result.state == "PENDING":
        response = {"state": result.state, "progress": "Job not started"}
    elif result.state == "STARTED":
        response = {"state": result.state, "progress": "Processing"}
    elif result.state == "SUCCESS":
        response = {"state": result.state, "result": result.result}
    elif result.state == "FAILURE":
        response = {"state": result.state, "error": str(result.info)}
    else:
        response = {"state": result.state}
    return response
