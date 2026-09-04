from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import (
    auth_router,
    submissions_router,
    profile_router,
    notifications_router,
    uploads_router,
    pdf_router,
    analytics_router,
    qr_router,
    bulk_upload_router,
    reports_router,
    recruiter_router,
    skills_router,
    postings_router,
)
from app.socket import sio
import socketio
import app.models  # noqa: F401


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
fastapi_app.include_router(pdf_router)
fastapi_app.include_router(analytics_router)
fastapi_app.include_router(qr_router)
fastapi_app.include_router(bulk_upload_router)
fastapi_app.include_router(reports_router)
fastapi_app.include_router(recruiter_router, prefix="/recruiters", tags=["Recruiters"])
fastapi_app.include_router(skills_router, prefix="/skills", tags=["Skills"])
fastapi_app.include_router(postings_router, prefix="/postings", tags=["Internships & Placements"])


@fastapi_app.get("/health")
def health_check():
    return {"status": "ok", "project": "Pragati"}


app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)  # noqa: F811