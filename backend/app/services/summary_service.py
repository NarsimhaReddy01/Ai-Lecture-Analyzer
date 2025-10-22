# backend/app/services/summary_service.py

import os
import openai
from fastapi import UploadFile, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from backend.app import models
from backend.app.config import settings

openai.api_key = settings.OPENAI_API_KEY


def upload_and_transcribe(file: UploadFile, db: Session, user_id: int):
    """Uploads a lecture file and generates transcript + summary."""
    try:
        # Save file temporarily
        temp_path = f"./temp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file.file.read())

        # Use Whisper or external transcription API
        transcript = transcribe_audio(temp_path)
        summary = generate_summary(transcript)

        lecture = models.Lecture(
            user_id=user_id,
            file_name=file.filename,
            transcript=transcript,
            summary=summary,
            uploaded_at=datetime.utcnow(),
        )
        db.add(lecture)
        db.commit()
        db.refresh(lecture)

        os.remove(temp_path)
        return lecture

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def transcribe_audio(file_path: str) -> str:
    """Transcribes audio using OpenAI Whisper."""
    try:
        audio_file = open(file_path, "rb")
        response = openai.Audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return response["text"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")


def generate_summary(transcript: str) -> str:
    """Generates summary from transcript using GPT."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI summarizer."},
                {"role": "user", "content": f"Summarize this lecture:\n{transcript}"}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {e}")
