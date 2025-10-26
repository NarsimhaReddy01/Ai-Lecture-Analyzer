# backend/videos/tasks.py

import os
import tempfile
from celery import shared_task
from moviepy.editor import VideoFileClip
from deep_translator import GoogleTranslator
from django.conf import settings
from .models import LectureVideo
import openai  # For summarization and quiz generation

# Make sure OPENAI_API_KEY is set in your environment
openai.api_key = os.getenv("OPENAI_API_KEY")


@shared_task
def process_video(video_id):
    try:
        video = LectureVideo.objects.get(id=video_id)
        video.transcription_status = 'pending'
        video.save()

        # 1️⃣ Download video from S3 locally
        import boto3
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=getattr(settings, 'AWS_S3_REGION_NAME', None)
        )

        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        s3.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, video.s3_key, tmp_file)
        tmp_file.close()

        # 2️⃣ Extract audio duration
        clip = VideoFileClip(tmp_file.name)
        video.duration = clip.duration
        clip.close()
        video.save()

        # 3️⃣ Transcribe using Whisper or OpenAI
        from openai import Audio
        transcription_text = ""
        with open(tmp_file.name, "rb") as f:
            transcription = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
            transcription_text = transcription['text']

        # 4️⃣ Translate to Hindi using deep-translator
        translated_text = GoogleTranslator(source='auto', target='hi').translate(transcription_text)

        # Store transcription & translation in DB (you can extend model if needed)
        video.transcription_status = 'done'
        video.save()

        # 5️⃣ Generate summary
        summary_prompt = f"""
        Summarize the following lecture transcript in multi-paragraph format,
        covering all key teaching points. Keep summary <= 15% of original word count.

        Transcript: {transcription_text}
        """
        summary_response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=summary_prompt,
            max_tokens=500
        )
        summary_text = summary_response.choices[0].text

        # 6️⃣ Generate Quiz
        quiz_prompt = f"""
        Generate 10+ quiz questions (multiple-choice and short answer) in English
        for the following lecture transcript. Include Bloom's taxonomy levels.

        Transcript: {transcription_text}
        """
        quiz_response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=quiz_prompt,
            max_tokens=500
        )
        quiz_text = quiz_response.choices[0].text

        # Optional: save summary & quiz to S3 or DB
        # video.summary_text = summary_text
        # video.quiz_text = quiz_text
        # video.save()

        # Delete temp file
        os.remove(tmp_file.name)

        return {"status": "success", "video_id": video_id}

    except Exception as e:
        video.transcription_status = 'error'
        video.save()
        return {"status": "error", "video_id": video_id, "error": str(e)}
