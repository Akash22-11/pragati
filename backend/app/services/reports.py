from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.submission import Submission, SubmissionStatus, SubmissionCategory
from app.models.user import User, UserRole
import io


def get_naac_data(db, start_date=None, end_date=None):
    query = db.query(Submission).filter(Submission.status == SubmissionStatus.approved)
    if start_date:
        query = query.filter(Submission.created_at >= start_date)
    if end_date:
        query = query.filter(Submission.created_at <= end_date)

    submissions = query.all()
    total_verified = len(submissions)
    total_students_participated = len(set(s.student_id for s in submissions))
    total_students = db.query(User).filter(User.role == UserRole.student).count()

    category_breakdown = {}
    for cat in SubmissionCategory:
        category_breakdown[cat.value] = len([s for s in submissions if s.category == cat.value])

    rate = 0
    if total_students > 0:
        rate = round((total_students_participated / total_students * 100), 1)

    return {
        "total_verified_activities": total_verified,
        "total_students_participated": total_students_participated,
        "total_students": total_students,
        "participation_rate": rate,
        "category_breakdown": category_breakdown,
        "submissions": submissions,
    }


def get_nirf_data(db, start_date=None, end_date=None):
    query = db.query(Submission).filter(Submission.status == SubmissionStatus.approved)
    if start_date:
        query = query.filter(Submission.created_at >= start_date)
    if end_date:
        query = query.filter(Submission.created_at <= end_date)

    submissions = query.all()

    dept_data = {}
    for s in submissions:
        student = db.query(User).filter(User.id == s.student_id).first()
        dept = student.department if student else "Unknown"
        if dept not in dept_data:
            dept_data[dept] = 0
        dept_data[dept] += 1

    return {
        "total_verified_activities": len(submissions),
        "department_breakdown": dept_data,
        "submissions": submissions,
    }


def generate_naac_pdf(data, institution_name="Pragati Institution"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=0.75 * inch, leftMargin=0.75 * inch,
                             topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=20,
                                  textColor=colors.HexColor("#1a1a2e"), alignment=TA_CENTER, spaceAfter=6)
    subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=11,
                                     textColor=colors.HexColor("#4a4a6a"), alignment=TA_CENTER, spaceAfter=4)
    section_style = ParagraphStyle("Section", parent=styles["Heading2"], fontSize=13,
                                    textColor=colors.HexColor("#1a1a2e"), spaceBefore=14, spaceAfter=6)

    elements.append(Paragraph(institution_name, title_style))
    elements.append(Paragraph("NAAC Student Activity Report", subtitle_style))
    elements.append(Paragraph("Generated on " + datetime.utcnow().strftime("%d %B %Y"), subtitle_style))
    elements.append(Spacer(1, 0.15 * inch))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a1a2e")))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Summary", section_style))
    summary_data = [
        ["Total Verified Activities", str(data["total_verified_activities"])],
        ["Students Participated", str(data["total_students_participated"])],
        ["Total Students", str(data["total_students"])],
        ["Participation Rate", str(data["participation_rate"]) + "%"],
    ]
    summary_table = Table(summary_data, colWidths=[3 * inch, 3 * inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f3f4f6")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Category-wise Breakdown", section_style))
    cat_data = [["Category", "Verified Count"]]
    for cat, count in data["category_breakdown"].items():
        cat_data.append([cat.capitalize(), str(count)])
    cat_table = Table(cat_data, colWidths=[3 * inch, 3 * inch])
    cat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
    ]))
    elements.append(cat_table)

    doc.build(elements)
    return buffer.getvalue()


def generate_nirf_pdf(data, institution_name="Pragati Institution"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=0.75 * inch, leftMargin=0.75 * inch,
                             topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=20,
                                  textColor=colors.HexColor("#1a1a2e"), alignment=TA_CENTER, spaceAfter=6)
    subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=11,
                                     textColor=colors.HexColor("#4a4a6a"), alignment=TA_CENTER, spaceAfter=4)
    section_style = ParagraphStyle("Section", parent=styles["Heading2"], fontSize=13,
                                    textColor=colors.HexColor("#1a1a2e"), spaceBefore=14, spaceAfter=6)

    elements.append(Paragraph(institution_name, title_style))
    elements.append(Paragraph("NIRF Department-wise Activity Report", subtitle_style))
    elements.append(Paragraph("Generated on " + datetime.utcnow().strftime("%d %B %Y"), subtitle_style))
    elements.append(Spacer(1, 0.15 * inch))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a1a2e")))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Summary", section_style))
    elements.append(Paragraph("Total Verified Activities: " + str(data["total_verified_activities"]), styles["Normal"]))
    elements.append(Spacer(1, 0.15 * inch))

    elements.append(Paragraph("Department-wise Breakdown", section_style))
    dept_data = [["Department", "Verified Activities"]]
    for dept, count in data["department_breakdown"].items():
        dept_data.append([dept, str(count)])
    dept_table = Table(dept_data, colWidths=[3 * inch, 3 * inch])
    dept_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
    ]))
    elements.append(dept_table)

    doc.build(elements)
    return buffer.getvalue()
