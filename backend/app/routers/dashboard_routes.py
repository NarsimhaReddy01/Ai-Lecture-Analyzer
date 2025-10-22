# backend/app/routers/dashboard_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app import models

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_users = db.query(models.User).count()
    total_videos = db.query(models.Video).count()
    total_quizzes = db.query(models.Quiz).count()
    
    # Most common languages
    languages = (
        db.query(models.Video.language, models.Video.id)
        .all()
    )
    language_count = {}
    for lang, _ in languages:
        language_count[lang] = language_count.get(lang, 0) + 1

    return {
        "total_users": total_users,
        "total_videos": total_videos,
        "total_quizzes": total_quizzes,
        "languages_distribution": language_count
    }


@router.get("/recent_videos")
def recent_videos(limit: int = 5, db: Session = Depends(get_db)):
    videos = db.query(models.Video).order_by(models.Video.uploaded_at.desc()).limit(limit).all()
    return [{"id": v.id, "title": v.title, "uploaded_at": v.uploaded_at, "user_id": v.user_id} for v in videos]
