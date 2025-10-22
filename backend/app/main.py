# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.config import settings 
from backend.app.database import Base, engine
from backend.app.routers import video_routes, auth_routes, summary_routes, quiz_routes, dashboard_routes, user_routes, transcript_routes

# Import routers (will add them later)
# from app.routers import auth_routes, video_routes, summary_routes, quiz_routes, dashboard_routes

# Initialize DB
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0",
    description="AI-Powered Lecture Video Analyzer API",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AI Lecture Analyzer Backend Running 🚀"}

# ✅ Mount static folder
app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(video_routes.router, prefix="/api/v1/videos", tags=["Videos"])
app.include_router(summary_routes.router, prefix="/api/v1/summaries", tags=["Summaries"])
app.include_router(quiz_routes.router, prefix="/api/v1/quizzes", tags=["Quizzes"])
app.include_router(dashboard_routes.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(transcript_routes.router, prefix="/api/v1/transcripts", tags=["Transcripts"])

