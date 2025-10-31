# backend/Dockerfile
FROM python:3.10-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsm6 libxext6 libgl1-mesa-glx gcc g++ git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]

