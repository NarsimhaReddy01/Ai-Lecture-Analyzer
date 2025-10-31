import os
import tempfile
import logging
import ffmpeg
import requests
import boto3
from celery import shared_task
from deep_translator import GoogleTranslator
from django.conf import settings
from .models import LectureVideo
from openai import OpenAI

logger = logging.getLogger(__name__)

# Load keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Initialize OpenAI client if available
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


@shared_task(bind=True)
def process_video(self, video_id, mode="paid"):
    """
    Background Celery task to:
    - Download video from S3
    - Extract audio
    - Transcribe (Whisper API or Hugging Face)
    - Translate (English → Hindi)
    - Summarize (OpenAI only)
    - Generate Quiz (OpenAI only)
    """
    logger.info(f"🎬 Starting video processing task for video_id={video_id} (Mode={mode})")

    video = LectureVideo.objects.get(id=video_id)
    tmp_video, audio_path = None, None

    try:
        video.transcription_status = "processing"
        video.save()

        # 1️⃣ Download video from S3
        logger.info("⬇️ Downloading video from S3...")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=getattr(settings, "AWS_S3_REGION_NAME", None),
        )

        tmp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        s3.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, video.s3_key, tmp_video)
        tmp_video.close()

        # 2️⃣ Extract audio using ffmpeg
        logger.info("🎧 Extracting audio using ffmpeg...")
        audio_path = tmp_video.name.replace(".mp4", ".mp3")
        ffmpeg.input(tmp_video.name).output(
            audio_path, format="mp3", acodec="libmp3lame"
        ).run(overwrite_output=True, quiet=True)

        # 3️⃣ Transcribe Audio
        logger.info("🧠 Transcribing audio...")
        transcription_text = ""

        if mode == "paid" and client:
            with open(audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            transcription_text = transcript.text
        else:
            # Use Hugging Face API for free transcription
            logger.info("🤖 Using Hugging Face Whisper model for free transcription")
            hf_url = "https://api-inference.huggingface.co/models/openai/whisper-base"
            headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
            with open(audio_path, "rb") as f:
                response = requests.post(hf_url, headers=headers, data=f)
                response.raise_for_status()
                transcription_text = response.json().get("text", "")

        # 4️⃣ Translate (English → Hindi)
        logger.info("🌐 Translating text...")
        try:
            translated_text = GoogleTranslator(source="auto", target="hi").translate(
                transcription_text[:5000]
            )
        except Exception as e:
            translated_text = f"[Translation failed] {str(e)}"

        # 5️⃣ Summarize (only available for OpenAI)
        logger.info("📝 Generating summary...")
        summary_text = ""
        if mode == "paid" and client:
            summary_prompt = (
                "Summarize the following lecture transcript into concise bullet points "
                "and paragraphs focusing on key topics, examples, and definitions:\n\n"
                f"{transcription_text[:5000]}"
            )
            summary_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an educational summarizer."},
                    {"role": "user", "content": summary_prompt},
                ],
                max_tokens=800,
            )
            summary_text = summary_response.choices[0].message.content.strip()
        else:
            summary_text = "[Free API mode] Summary feature available only with OpenAI."

        # 6️⃣ Quiz Generation (only available for OpenAI)
        logger.info("🧩 Generating quiz...")
        quiz_text = ""
        if mode == "paid" and client:
            quiz_prompt = (
                "Create 10 educational quiz questions (both multiple-choice and short-answer) "
                "based on the following lecture transcript. Label difficulty as Easy/Medium/Hard.\n\n"
                f"{transcription_text[:4000]}"
            )
            quiz_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a quiz question generator."},
                    {"role": "user", "content": quiz_prompt},
                ],
                max_tokens=800,
            )
            quiz_text = quiz_response.choices[0].message.content.strip()
        else:
            quiz_text = "[Free API mode] Quiz generation available only with OpenAI."

        # 7️⃣ Save Results
        logger.info("💾 Saving results to database...")
        video.transcription_status = "done"
        video.transcript_text = transcription_text
        video.translation_text = translated_text
        video.summary_text = summary_text
        video.quiz_text = quiz_text
        video.save()

        logger.info(f"✅ Completed processing video_id={video_id}")
        return {"status": "success", "video_id": video_id, "mode": mode}

    except Exception as e:
        logger.error(f"❌ Error processing video {video_id}: {e}", exc_info=True)
        video.transcription_status = "error"
        video.save()
        return {"status": "error", "error": str(e), "mode": mode}

    finally:
        if tmp_video and os.path.exists(tmp_video.name):
            os.remove(tmp_video.name)
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
