# backend/app/routers/summary_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app import models, schemas

router = APIRouter(
    prefix="/summaries",
    tags=["Summaries"]
)


@router.get("/{video_id}", response_model=str)
def get_summary(video_id: int, db: Session = Depends(get_db)):
    transcript = db.query(models.Transcript).filter(models.Transcript.video_id == video_id).first()
    if not transcript or not transcript.original_text:
        raise HTTPException(status_code=404, detail="Summary not available")
    
    # Here you can generate or return stored summary
    return transcript.original_text[:500]  # Return first 500 chars as a sample
