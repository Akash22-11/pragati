"""
Phase 1 -- Recruiter Router
Handles:
  - Recruiter company profile update
  - Admin verifying a company
  - Student browse + filter
  - Shortlist add / remove / view

NOTE: The live `users` table has no `year` or `roll_number` columns.
Filtering/display by year has been removed to match the actual schema.
"""

import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

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


# -----------------------------------------------------------------
# RECRUITER -- Update own company profile
# -----------------------------------------------------------------

@router.get("/profile", response_model=RecruiterProfileResponse)
def get_recruiter_profile(
    current_user: User = Depends(require_role("recruiter")),
):
    return current_user


@router.patch("/profile", response_model=RecruiterProfileResponse)
def update_recruiter_profile(
    payload: RecruiterProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("recruiter")),
):
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


# -----------------------------------------------------------------
# ADMIN -- Verify / unverify a recruiter company
# -----------------------------------------------------------------

@router.patch("/{recruiter_id}/verify", response_model=RecruiterProfileResponse)
def verify_company(
    recruiter_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    recruiter = db.query(User).filter(
        User.id == recruiter_id,
        User.role == UserRole.recruiter
    ).first()

    if not recruiter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recruiter not found")

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
    recruiter = db.query(User).filter(
        User.id == recruiter_id,
        User.role == UserRole.recruiter
    ).first()

    if not recruiter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recruiter not found")

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
    query = db.query(User).filter(User.role == UserRole.recruiter)
    if verified_only:
        query = query.filter(User.is_verified_company == True)
    return query.all()


# -----------------------------------------------------------------
# STUDENT BROWSE -- Recruiter searches students
# -----------------------------------------------------------------

@router.get("/students", response_model=list[StudentListItem])
def browse_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("recruiter")),
    department: Optional[str] = Query(None, description="Filter by department e.g. CSE"),
    skill: Optional[str] = Query(None, description="Filter by skill tag e.g. Python"),
    search: Optional[str] = Query(None, description="Search by name"),
    min_cgpa: Optional[float] = Query(None, description="Minimum CGPA e.g. 7.5"),
):
    query = db.query(User).filter(
        User.role == UserRole.student,
        User.is_active == True
    )

    if department:
        query = query.filter(User.department.ilike(f"%{department}%"))

    if min_cgpa:
        query = query.filter(User.cgpa >= min_cgpa)

    if search:
        query = query.filter(User.full_name.ilike(f"%{search}%"))

    students = query.all()

    if skill:
        filtered = []
        for student in students:
            approved = db.query(Submission).filter(
                Submission.student_id == student.id,
                Submission.status == SubmissionStatus.approved
            ).all()
            student_skills = []
            for sub in approved:
                if sub.skills:
                    student_skills.extend(sub.skills)
            if any(skill.lower() in s.lower() for s in student_skills):
                filtered.append(student)
        students = filtered

    result = []
    for student in students:
        approved_subs = db.query(Submission).filter(
            Submission.student_id == student.id,
            Submission.status == SubmissionStatus.approved
        ).all()

        verified_count = len(approved_subs)
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
    student = db.query(User).filter(
        User.id == student_id,
        User.role == UserRole.student,
        User.is_active == True
    ).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    verified_submissions = db.query(Submission).filter(
        Submission.student_id == student_id,
        Submission.status == SubmissionStatus.approved
    ).order_by(Submission.created_at.desc()).all()

    all_skills = []
    for sub in verified_submissions:
        if sub.skills:
            all_skills.extend(sub.skills)
    unique_skills = list(set(all_skills))

    is_shortlisted = db.query(RecruiterShortlist).filter(
        RecruiterShortlist.recruiter_id == current_user.id,
        RecruiterShortlist.student_id == student_id
    ).first() is not None

    return StudentDetailResponse(
        id=student.id,
        full_name=student.full_name,
        email=student.email,
        department=student.department,
        cgpa=student.cgpa,
        institution=student.institution,
        skills=unique_skills,
        verified_submissions=verified_submissions,
        is_shortlisted=is_shortlisted,
    )


# -----------------------------------------------------------------
# SHORTLIST -- Recruiter saves students
# -----------------------------------------------------------------

@router.post("/shortlist", response_model=ShortlistResponse, status_code=status.HTTP_201_CREATED)
def shortlist_student(
    payload: ShortlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("recruiter")),
):
    student = db.query(User).filter(
        User.id == payload.student_id,
        User.role == UserRole.student
    ).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    existing = db.query(RecruiterShortlist).filter(
        RecruiterShortlist.recruiter_id == current_user.id,
        RecruiterShortlist.student_id == payload.student_id
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student already shortlisted")

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
    entry = db.query(RecruiterShortlist).filter(
        RecruiterShortlist.recruiter_id == current_user.id,
        RecruiterShortlist.student_id == student_id
    ).first()

    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not in shortlist")

    db.delete(entry)
    db.commit()
    return {"message": "Removed from shortlist"}


@router.get("/shortlist", response_model=list[StudentListItem])
def get_my_shortlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("recruiter")),
):
    entries = db.query(RecruiterShortlist).filter(
        RecruiterShortlist.recruiter_id == current_user.id
    ).all()

    result = []
    for entry in entries:
        student = db.query(User).filter(User.id == entry.student_id).first()
        if not student:
            continue

        approved_subs = db.query(Submission).filter(
            Submission.student_id == student.id,
            Submission.status == SubmissionStatus.approved
        ).all()
        verified_count = len(approved_subs)
        all_skills = []
        for sub in approved_subs:
            if sub.skills:
                all_skills.extend(sub.skills)

        result.append(StudentListItem(
            id=student.id,
            full_name=student.full_name,
            email=student.email,
            department=student.department,
            cgpa=student.cgpa,
            institution=student.institution,
            verified_achievements=verified_count,
            skills=list(set(all_skills)),
        ))

    return result
