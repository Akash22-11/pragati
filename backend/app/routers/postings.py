"""
Phase 2 -- Internship & Placement Postings Router
Handles:
  - Recruiter: create / update / close / delete own postings
  - Student: browse open postings, apply, view own applications
  - Recruiter: view applicants for a posting, update application status

This file was missing from the original codebase (main.py / routers/__init__.py
already referenced `app.routers.postings.router`, but the module didn't exist),
which crashed the whole app at import time. Models and schemas for Postings /
Applications already existed (app/models/posting.py, app/models/application.py,
app/schemas/posting.py) -- only the router was missing.
"""

import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.posting import Posting, PostingStatus
from app.models.application import Application, ApplicationStatus
from app.schemas.posting import (
    PostingCreate,
    PostingUpdate,
    PostingResponse,
    ApplicationCreate,
    ApplicationStatusUpdate,
    ApplicationResponse,
    ApplicationWithStudent,
    ApplicationWithPosting,
)

router = APIRouter()


# -----------------------------------------------------------------
# RECRUITER -- Create / manage own postings
# -----------------------------------------------------------------

@router.post("/", response_model=PostingResponse, status_code=status.HTTP_201_CREATED)
def create_posting(
    payload: PostingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter)),
):
    posting = Posting(
        recruiter_id=current_user.id,
        **payload.model_dump(),
    )
    db.add(posting)
    db.commit()
    db.refresh(posting)
    return posting


@router.get("/mine", response_model=list[PostingResponse])
def list_my_postings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter)),
):
    return (
        db.query(Posting)
        .filter(Posting.recruiter_id == current_user.id)
        .order_by(Posting.created_at.desc())
        .all()
    )


@router.patch("/{posting_id}", response_model=PostingResponse)
def update_posting(
    posting_id: uuid.UUID,
    payload: PostingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter)),
):
    posting = db.query(Posting).filter(Posting.id == posting_id).first()
    if not posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posting not found")
    if posting.recruiter_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your posting")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(posting, field, value)
    db.commit()
    db.refresh(posting)
    return posting


@router.delete("/{posting_id}", status_code=status.HTTP_200_OK)
def delete_posting(
    posting_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter)),
):
    posting = db.query(Posting).filter(Posting.id == posting_id).first()
    if not posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posting not found")
    if posting.recruiter_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your posting")

    db.delete(posting)
    db.commit()
    return {"message": "Posting deleted"}


# -----------------------------------------------------------------
# STUDENT BROWSE -- List / view open postings
# -----------------------------------------------------------------

@router.get("/", response_model=list[PostingResponse])
def browse_postings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    type: Optional[str] = Query(None, description="Filter by 'internship' or 'job'"),
    location: Optional[str] = Query(None, description="Filter by location"),
    skill: Optional[str] = Query(None, description="Filter by required skill"),
    open_only: bool = Query(True, description="Only show open postings"),
):
    query = db.query(Posting)

    if open_only:
        query = query.filter(Posting.status == PostingStatus.open)
    if type:
        query = query.filter(Posting.type == type)
    if location:
        query = query.filter(Posting.location.ilike(f"%{location}%"))

    postings = query.order_by(Posting.created_at.desc()).all()

    if skill:
        postings = [
            p for p in postings
            if p.skills_required and any(skill.lower() in s.lower() for s in p.skills_required)
        ]

    return postings


@router.get("/{posting_id}", response_model=PostingResponse)
def get_posting(
    posting_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    posting = db.query(Posting).filter(Posting.id == posting_id).first()
    if not posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posting not found")
    return posting


# -----------------------------------------------------------------
# STUDENT -- Apply to a posting / view own applications
# -----------------------------------------------------------------

@router.post(
    "/{posting_id}/apply",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def apply_to_posting(
    posting_id: uuid.UUID,
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.student)),
):
    posting = db.query(Posting).filter(Posting.id == posting_id).first()
    if not posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posting not found")
    if not posting.is_open:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This posting is closed")

    existing = db.query(Application).filter(
        Application.posting_id == posting_id,
        Application.student_id == current_user.id,
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already applied to this posting")

    application = Application(
        posting_id=posting_id,
        student_id=current_user.id,
        cover_note=payload.cover_note,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/applications/mine", response_model=list[ApplicationWithPosting])
def list_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.student)),
):
    return (
        db.query(Application)
        .filter(Application.student_id == current_user.id)
        .order_by(Application.applied_at.desc())
        .all()
    )


# -----------------------------------------------------------------
# RECRUITER -- View applicants for own posting / update status
# -----------------------------------------------------------------

@router.get("/{posting_id}/applications", response_model=list[ApplicationWithStudent])
def list_applicants(
    posting_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter)),
):
    posting = db.query(Posting).filter(Posting.id == posting_id).first()
    if not posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posting not found")
    if posting.recruiter_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your posting")

    return (
        db.query(Application)
        .filter(Application.posting_id == posting_id)
        .order_by(Application.applied_at.desc())
        .all()
    )


@router.patch("/applications/{application_id}", response_model=ApplicationResponse)
def update_application_status(
    application_id: uuid.UUID,
    payload: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter)),
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    posting = db.query(Posting).filter(Posting.id == application.posting_id).first()
    if not posting or posting.recruiter_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your posting")

    if payload.status not in [s.value for s in ApplicationStatus]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")

    application.status = payload.status
    db.commit()
    db.refresh(application)
    return application
