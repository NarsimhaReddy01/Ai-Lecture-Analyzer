# Ai-Lecture-Analyzer# AI Lecture Analyzer

A web-based educational platform that converts lecture videos into **bilingual transcripts**, **summaries**, and **adaptive quizzes**.

---

## 🛠 Project Overview

Students can:

- Upload lecture videos (MP4, AVI, MKV)
- Receive timestamped transcripts in **English & Hindi**
- Read multi-paragraph summaries
- Take automatically generated quizzes
- Track progress via dashboard

Admins/teachers can:

- Download transcripts, summaries, quiz sets
- Monitor platform activity

---

## ⚡ Tech Stack

- **Backend:** Django 5.0.1, Django REST Framework
- **Frontend:** React (SPA)
- **Transcription:** OpenAI Whisper / WhisperX
- **Summarization & Quiz:** OpenAI GPT or Hugging Face Transformers
- **Database:** PostgreSQL (SQLite for dev)
- **Storage:** AWS S3
- **Background Jobs:** Celery + Redis
- **Authentication:** JWT / Django Allauth
- **Containerization:** Docker & docker-compose

---

## 🔧 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/NarsimhaReddy01/Ai-Lecture-Analyzer.git
cd Ai-Lecture-Analyzer
