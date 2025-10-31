# import os
# import json
# from .celery_app import celery_app
# from .services.ai_pipeline import process_video_to_artifacts

# @celery_app.task(bind=True, name="process_lecture_video")
# def process_lecture_video(self, video_path: str):
#     """
#     Celery task to process uploaded lecture video asynchronously.
#     """
#     try:
#         use_openai = bool(os.getenv("OPENAI_API_KEY"))
#         artifacts = process_video_to_artifacts(video_path, use_openai=use_openai, whisper_size="base")

#         # Save artifacts locally or to your DB later
#         output_path = f"{video_path}.artifacts.json"
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(artifacts, f, ensure_ascii=False, indent=2)

#         return {
#             "status": "completed",
#             "output_path": output_path,
#         }

#     except Exception as e:
#         self.update_state(state="FAILURE", meta={"error": str(e)})
#         raise


import os
import tempfile
from celery import shared_task
from deep_translator import GoogleTranslator
from django.conf import settings
from .models import LectureVideo
import openai
import ffmpeg  # ✅ Replaces moviepy
import boto3

openai.api_key = os.getenv("OPENAI_API_KEY")


@shared_task
def process_video(video_id):
    try:
        video = LectureVideo.objects.get(id=video_id)
        video.transcription_status = 'pending'
        video.save()

        # 1️⃣ Download video from S3 locally
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=getattr(settings, 'AWS_S3_REGION_NAME', None)
        )

        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        s3.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, video.s3_key, tmp_file)
        tmp_file.close()

        # 2️⃣ Get video duration using FFmpeg
        probe = ffmpeg.probe(tmp_file.name)
        duration = float(probe['format']['duration'])
        video.duration = duration
        video.save()

        # 3️⃣ Transcribe using Whisper API
        with open(tmp_file.name, "rb") as f:
            transcription = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
            transcription_text = transcription['text']

        # 4️⃣ Translate transcription to Hindi
        translated_text = GoogleTranslator(source='auto', target='hi').translate(transcription_text)

        # 5️⃣ Generate Summary
        summary_prompt = f"Summarize this lecture in under 15% of its word count:\n\n{transcription_text}"
        summary_response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=summary_prompt,
            max_tokens=500
        )
        summary_text = summary_response.choices[0].text

        # 6️⃣ Generate Quiz
        quiz_prompt = f"Generate 10 quiz questions (multiple choice and short answer) for this transcript:\n\n{transcription_text}"
        quiz_response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=quiz_prompt,
            max_tokens=500
        )
        quiz_text = quiz_response.choices[0].text

        # Optional: Save summary and quiz if needed
        # video.summary_text = summary_text
        # video.quiz_text = quiz_text
        # video.save()

        # Cleanup
        os.remove(tmp_file.name)
        video.transcription_status = 'done'
        video.save()

        return {"status": "success", "video_id": video_id}

    except Exception as e:
        video.transcription_status = 'error'
        video.save()
        return {"status": "error", "video_id": video_id, "error": str(e)}
