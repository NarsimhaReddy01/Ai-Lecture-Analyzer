# backend/app/services/transcription_service.py

import openai
from fastapi import UploadFile, HTTPException
import os
from backend.app.config import settings

openai.api_key = settings.OPENAI_API_KEY


def transcribe_audio_file(file: UploadFile) -> str:
    """
    Transcribes the given audio/video file into text using OpenAI Whisper.
    """
    try:
        temp_path = f"./temp/{file.filename}"
        os.makedirs("./temp", exist_ok=True)

        # Save temporary file
        with open(temp_path, "wb") as f:
            f.write(file.file.read())

        with open(temp_path, "rb") as audio_file:
            response = openai.Audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        os.remove(temp_path)
        return response["text"].strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")
