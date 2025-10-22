# backend/app/utils/cleanup.py
import os, time

def cleanup_temp(folder="./backend/app/static/temp", max_age_hours=12):
    now = time.time()
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path) and now - os.path.getmtime(path) > max_age_hours * 3600:
            os.remove(path)
