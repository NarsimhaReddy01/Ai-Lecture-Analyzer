# backend/app/routers/quiz_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app import models, schemas

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"]
)


@router.get("/{video_id}", response_model=list[schemas.QuizOut])
def get_quizzes(video_id: int, db: Session = Depends(get_db)):
    quizzes = db.query(models.Quiz).filter(models.Quiz.video_id == video_id).all()
    if not quizzes:
        raise HTTPException(status_code=404, detail="No quizzes found")
    return quizzes
