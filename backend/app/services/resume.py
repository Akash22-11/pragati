from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER
from sqlalchemy.orm import Session
from app.models.submission import Submission, SubmissionStatus
from app.models.user import User
import io


def draft_resume_data(db: Session, student_id) -> dict:
   
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        return None

    verified = db.query(Submission).filter(
        Submission.student_id == student_id,
        Submission.status == SubmissionStatus.approved,
    ).order_by(Submission.created_at.desc()).all()

    all_skills = []
    for s in verified:
        if s.skills:
            for skill in s.skills:
                if skill not in all_skills:
                    all_skills.append(skill)

    return {
        "full_name": student.full_name,
        "email": student.email,
        "institution": student.institution,
        "department": student.department,
        "skills": all_skills,
        "activities": [
            {
                "title": s.title,
                "category": str(s.category),
                "description": s.description,
                "date": str(s.created_at)[:10],
            }
            for s in verified
        ],
    }


def generate_resume_pdf(data: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=0.75 * inch, leftMargin=0.75 * inch,
                             topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    elements = []

    name_style = ParagraphStyle("Name", parent=styles["Heading1"], fontSize=22,
                                 textColor=colors.HexColor("#1a1a2e"), alignment=TA_CENTER, spaceAfter=4)
    contact_style = ParagraphStyle("Contact", parent=styles["Normal"], fontSize=10,
                                    textColor=colors.HexColor("#4a4a6a"), alignment=TA_CENTER, spaceAfter=10)
    section_style = ParagraphStyle("Section", parent=styles["Heading2"], fontSize=13,
                                    textColor=colors.HexColor("#1a1a2e"), spaceBefore=14, spaceAfter=6)
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10,
                                 textColor=colors.HexColor("#374151"), spaceAfter=4)

    elements.append(Paragraph(data["full_name"], name_style))
    contact_line = data["email"]
    if data.get("institution"):
        contact_line += " | " + data["institution"]
    if data.get("department"):
        contact_line += " | " + data["department"]
    elements.append(Paragraph(contact_line, contact_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1a1a2e")))

    if data["skills"]:
        elements.append(Paragraph("Skills", section_style))
        elements.append(Paragraph(", ".join(data["skills"]), body_style))

    if data["activities"]:
        elements.append(Paragraph("Verified Activities", section_style))
        for act in data["activities"]:
            elements.append(Paragraph("<b>" + act["title"] + "</b> — " + act["category"] + " (" + act["date"] + ")", body_style))
            if act["description"]:
                elements.append(Paragraph(act["description"], body_style))
            elements.append(Spacer(1, 0.08 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(
        "Draft generated from Pragati verified records. Review and edit before submitting.",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8,
                       textColor=colors.HexColor("#9ca3af"), alignment=TA_CENTER)
    ))

    doc.build(elements)
    return buffer.getvalue()
