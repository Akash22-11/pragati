"""
Phase 1 — Recruiter Router
Handles:
  - Recruiter company profile update
  - Admin verifying a company
  - Student browse + filter
  - Shortlist add / remove / view
"""

import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.submission import Submission, SubmissionStatus
from app.models.recruiter_shortlist import RecruiterShortlist
from app.schemas.recruiter import (
    RecruiterProfileUpdate,
    RecruiterProfileResponse,
    StudentListItem,
    StudentDetailResponse,
    ShortlistCreate,
    ShortlistResponse,
)

router = APIRouter()


# ─────────────────────────────────────────────────────────────
# RECRUITER — Update own company profile
# ─────────────────────────────────────────────────────────────

@router.get("/profile", response_model=RecruiterProfileResponse)
def get_recruiter_profile(
    current_user: User = Depends(require_role("recruiter")),
):
    """Get own company profile."""
    return current_user


@router.patch("/profile", response_model=RecruiterProfileResponse)
def update_recruiter_profile(
    payload: RecruiterProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("recruiter")),
):
    """Recruiter updates their company details."""
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


# ─────────────────────────────────────────────────────────────
# ADMIN — Verify / unverify a recruiter company
# ─────────────────────────────────────────────────────────────

@router.patch("/{recruiter_id}/verify", response_model=RecruiterProfileResponse)
def verify_company(
    recruiter_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """Admin marks a recruiter's company as verified."""
    recruiter = db.query(User).filter(
        User.id == recruiter_id,
        User.role == UserRole.recruiter
    ).first()

    if not recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter not found"
        )

    recruiter.is_verified_company = True
    db.commit()
    db.refresh(recruiter)
    return recruiter


@router.patch("/{recruiter_id}/unverify", response_model=RecruiterProfileResponse)
def unverify_company(
    recruiter_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """Admin revokes verification from a recruiter."""
    recruiter = db.query(User).filter(
        User.id == recruiter_id,
        User.role == UserRole.recruiter
    ).first()

    if not recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter not found"
        )

    recruiter.is_verified_company = False
    db.commit()
    db.refresh(recruiter)
    return recruiter


@router.get("/all", response_model=list[RecruiterProfileResponse])
def list_all_recruiters(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
    verified_only: bool = Query(False),
):
    """Admin sees all registered recruiters."""
    query = db.query(User).filter(User.role == UserRole.recruiter)
    if verified_only:
        query = query.filter(User.is_verified_company == True)
    return query.all()


# ─────────────────────────────────────────────────────────────
# STUDENT BROWSE — Recruiter searches students
# ─────────────────────────────────────────────────────────────

@router.get("/students", response_model=list[StudentListItem])
def browse_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("recruiter")),
    department: Optional[str] = Query(None, description="Filter by department e.g. CSE"),
    year: Optional[int] = Query(None, description="Filter by year of study e.g. 3"),
    skill: Optional[str] = Query(None, description="Filter by skill tag e.g. Python"),
    search: Optional[str] = Query(None, description="Search by name"),
    min_cgpa: Optional[float] = Query(None, description="Minimum CGPA e.g. 7.5"),
):
    """
    Recruiter browses verified students with optional filters.
    Only returns active students.
    """
    query = db.query(User).filter(
        User.role == UserRole.student,
        User.is_active == True
    )

    if department:
        query = query.filter(User.department.ilike(f"%{department}%"))

    if year:
        query = query.filter(User.year == year)

    if min_cgpa:
        query = query.filter(User.cgpa >= min_cgpa)

    if search:
        query = query.filter(User.full_name.ilike(f"%{search}%"))

    students = query.all()

    # Filter by skill — done in Python since skills are in submissions JSON
    if skill:
        filtered = []
        for student in students:
            # Get all approved submissions for this student
            approved = db.query(Submission).filter(
                Submission.student_id == student.id,
                Submission.status == SubmissionStatus.approved
            ).all()
            # Check if any submission has the skill tag
            student_skills = []
            for sub in approved:
                if sub.skills:
                    student_skills.extend(sub.skills)
            if any(skill.lower() in s.lower() for s in student_skills):
                filtered.append(student)
        students = filtered

    # Attach verified achievement count to each student
    result = []
    for student in students:
        verified_count = db.query(Submission).filter(
            Submission.student_id == student.id,
            Submission.status == SubmissionStatus.approved
        ).count()

        # Gather all skills from approved submissions
        approved_subs = db.query(Submission).filter(
            Submission.student_id == student.id,
            Submission.status == SubmissionStatus.approved
        ).all()
        all_skills = []
        for sub in approved_subs:
            if sub.skills:
                all_skills.extend(sub.skills)
        unique_skills = list(set(all_skills))

        result.append(StudentListItem(
            id=student.id,
            full_name=student.full_name,
            email=student.email,
            department=student.department,
            year=student.year,
            cgpa=student.cgpa,
            institution=student.institution,
            verified_achievements=verified_count,
            skills=unique_skills,
        ))

    return result


@router.get("/students/{student_id}", response_model=StudentDetailResponse)
def get_student_detail(
    student_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("recruiter")),
):
    """
    Recruiter views a student's full verified profile.
    Only shows approved (verified) submissions.
    """
    student = db.query(User).filter(
        User.id == student_id,
        User.role == UserRole.student,
        User.is_active == True
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Only show verified submissions to recruiters
    verified_submissions = db.query(Submission).filter(
        Submission.student_id == student_id,
        Submission.status == SubmissionStatus.approved
    ).order_by(Submission.created_at.desc()).all()

    # Aggregate skills
    all_skills = []
    for sub in verified_submissions:
        if sub.skills:
            all_skills.extend(sub.skills)
    unique_skills = list(set(all_skills))

    # Check if this recruiter has shortlisted the student
    is_shortlisted = db.query(RecruiterShortlist).filter(
        RecruiterShortlist.recruiter_id == current_user.id,
        RecruiterShortlist.student_id == student_id
    ).first() is not None

    return StudentDetailResponse(
        id=student.id,
        full_name=student.full_name,
        email=student.email,
        department=student.department,
        year=student.year,
        cgpa=student.cgpa,
        institution=student.institution,
        skills=unique_skills,
        verified_submissions=verified_submissions,
        is_shortlisted=is_shortlisted,
    )


# ─────────────────────────────────────────────────────────────
# SHORTLIST — Recruiter saves students
# ─────────────────────────────────────────────────────────────

@router.post("/shortlist", response_model=ShortlistResponse, status_code=status.HTTP_201_CREATED)
def shortlist_student(
    payload: ShortlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("recruiter")),
):
    """Recruiter adds a student to their shortlist."""
    # Check student exists
    student = db.query(User).filter(
        User.id == payload.student_id,
        User.role == UserRole.student
    ).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Check not already shortlisted
    existing = db.query(RecruiterShortlist).filter(
        RecruiterShortlist.recruiter_id == current_user.id,
        RecruiterShortlist.student_id == payload.student_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student already shortlisted"
        )

    shortlist = RecruiterShortlist(
        recruiter_id=current_user.id,
        student_id=payload.student_id,
        note=payload.note,
    )
    db.add(shortlist)
    db.commit()
    db.refresh(shortlist)
    return shortlist


@router.delete("/shortlist/{student_id}", status_code=status.HTTP_200_OK)
def remove_from_shortlist(
    student_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("recruiter")),
):
    """Recruiter removes a student from their shortlist."""
    entry = db.query(RecruiterShortlist).filter(
        RecruiterShortlist.recruiter_id == current_user.id,
        RecruiterShortlist.student_id == student_id
    ).first()

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not in shortlist"
        )

    db.delete(entry)
    db.commit()
    return {"message": "Removed from shortlist"}


@router.get("/shortlist", response_model=list[StudentListItem])
def get_my_shortlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("recruiter")),
):
    """Recruiter views all their shortlisted students."""
    entries = db.query(RecruiterShortlist).filter(
        RecruiterShortlist.recruiter_id == current_user.id
    ).all()

    result = []
    for entry in entries:
        student = db.query(User).filter(User.id == entry.student_id).first()
        if not student:
            continue

        verified_count = db.query(Submission).filter(
            Submission.student_id == student.id,
            Submission.status == SubmissionStatus.approved
        ).count()

        approved_subs = db.query(Submission).filter(
            Submission.student_id == student.id,
            Submission.status == SubmissionStatus.approved
        ).all()
        all_skills = []
        for sub in approved_subs:
            if sub.skills:
                all_skills.extend(sub.skills)

        result.append(StudentListItem(
            id=student.id,
            full_name=student.full_name,
            email=student.email,
            department=student.department,
            year=student.year,
            cgpa=student.cgpa,
            institution=student.institution,
            verified_achievements=verified_count,
            skills=list(set(all_skills)),
        ))

    return result
