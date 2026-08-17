from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routers import auth_router, submissions_router, profile_router, notifications_router, uploads_router
from app.socket import sio
import socketio
import app.models


fastapi_app = FastAPI(
    title="Pragati API",
    description="Centralised Student Activity Record Platform",
    version="1.0.0",
)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_app.include_router(auth_router)
fastapi_app.include_router(submissions_router)
fastapi_app.include_router(profile_router)
fastapi_app.include_router(notifications_router)
fastapi_app.include_router(uploads_router)


@fastapi_app.get("/health")
def health_check():
    return {"status": "ok", "project": "Pragati"}


app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)