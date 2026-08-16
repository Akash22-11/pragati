from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routers import auth_router, submissions_router, profile_router
import app.models

app = FastAPI(
    title="Pragati API",
    description="Centralised Student Activity Record Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(submissions_router)
app.include_router(profile_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "project": "Pragati"}