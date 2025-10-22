# backend/app/services/quiz_service.py

import openai
from fastapi import HTTPException
from backend.app.config import settings

openai.api_key = settings.OPENAI_API_KEY


def generate_quiz_from_text(transcript: str):
    """
    Generates 5 quiz questions with answers based on the lecture transcript.
    """
    try:
        prompt = f"""
        Create a quiz with 5 multiple-choice questions based on the following lecture content.
        Provide 4 options for each question and clearly mark the correct answer.

        Lecture Transcript:
        {transcript}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a quiz generator for educational content."},
                {"role": "user", "content": prompt}
            ]
        )

        quiz_text = response["choices"][0]["message"]["content"]
        return quiz_text.strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {e}")
