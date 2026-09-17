from app.services.skill_gap import get_student_skills
from app.services.matching import explain_shortlist

@router.get("/{posting_id}/applications")
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

    applications = (
        db.query(Application)
        .filter(Application.posting_id == posting_id)
        .order_by(Application.applied_at.desc())
        .all()
    )

    results = []
    for app in applications:
        student_skills = get_student_skills(db, app.student_id)
        explanation = explain_shortlist(student_skills, posting)
        results.append({
            "id": str(app.id),
            "student_id": str(app.student_id),
            "student_name": app.student_name,
            "student_email": app.student_email,
            "status": app.status,
            "cover_note": app.cover_note,
            "applied_at": str(app.applied_at) if app.applied_at else None,
            "match_explanation": explanation,
        })
    return results