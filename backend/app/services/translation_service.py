# backend/app/services/translation_service.py

import openai
from fastapi import HTTPException
from backend.app.config import settings

openai.api_key = settings.OPENAI_API_KEY


def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates text to a target language using OpenAI GPT.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a multilingual translator."},
                {"role": "user", "content": f"Translate this text to {target_language}:\n{text}"}
            ]
        )

        translation = response["choices"][0]["message"]["content"].strip()
        return translation

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {e}")
