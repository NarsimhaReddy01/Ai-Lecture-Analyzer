# backend/app/services/dashboard_service.py

from sqlalchemy.orm import Session
from backend.app import models


def get_user_stats(db: Session, user_id: int):
    """Fetch dashboard metrics for a user."""
    lectures = db.query(models.Lecture).filter(models.Lecture.user_id == user_id).all()
    total_lectures = len(lectures)
    total_words = sum(len(l.transcript.split()) for l in lectures)
    avg_summary_length = (
        sum(len(l.summary.split()) for l in lectures) / total_lectures if total_lectures else 0
    )

    return {
        "total_lectures": total_lectures,
        "total_words": total_words,
        "avg_summary_length": round(avg_summary_length, 2),
    }
