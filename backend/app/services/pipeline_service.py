# backend/app/services/pipeline_service.py

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from backend.app.services import transcription_service, summary_service, quiz_service, translation_service
from backend.app import models
from datetime import datetime


def process_pipeline(db: Session, user_id: int, file: UploadFile, target_language: str = "en"):
    """
    Executes the full AI lecture pipeline:
    1. Transcription
    2. Summary
    3. Quiz Generation
    4. Translation (optional)
    """
    try:
        # Step 1: Transcription
        transcript = transcription_service.transcribe_audio_file(file)

        # Step 2: Summary
        summary = summary_service.generate_summary(transcript)

        # Step 3: Quiz
        quiz_data = quiz_service.generate_quiz_from_text(transcript)

        # Step 4: Translation (if needed)
        translated_summary = None
        if target_language.lower() != "en":
            translated_summary = translation_service.translate_text(summary, target_language)

        # Store results in DB
        lecture = models.Lecture(
            user_id=user_id,
            file_name=file.filename,
            transcript=transcript,
            summary=summary,
            translated_summary=translated_summary,
            quiz=quiz_data,
            uploaded_at=datetime.utcnow(),
        )
        db.add(lecture)
        db.commit()
        db.refresh(lecture)

        return {
            "lecture_id": lecture.id,
            "file_name": file.filename,
            "summary": translated_summary or summary,
            "quiz": quiz_data,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {e}")
