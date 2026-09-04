from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text, JSON
from app.db_types import GUID
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid
import enum


class SubmissionStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    returned = "returned"


class SubmissionCategory(str, enum.Enum):
    certification = "certification"
    internship = "internship"
    project = "project"
    competition = "competition"
    research = "research"
    extracurricular = "extracurricular"
    other = "other"


CATEGORY_SKILL_SUGGESTIONS = {
    "certification": [
        "Python", "Java", "SQL", "AWS", "Azure", "GCP", "Machine Learning",
        "Data Science", "Cybersecurity", "Cloud Computing", "DevOps",
        "Docker", "Kubernetes", "React", "Node.js"
    ],
    "internship": [
        "Software Development", "Web Development", "Data Analysis",
        "Business Development", "Marketing", "Finance", "HR",
        "Project Management", "UI/UX Design", "Research"
    ],
    "project": [
        "Python", "JavaScript", "FastAPI", "Django", "Flask", "React",
        "Vue.js", "Machine Learning", "Deep Learning", "IoT", "Blockchain",
        "Android", "iOS", "Flutter", "SQL", "MongoDB", "PostgreSQL"
    ],
    "competition": [
        "Problem Solving", "Algorithm Design", "Competitive Programming",
        "Hackathon", "Design Thinking", "Business Strategy",
        "Public Speaking", "Robotics", "Cybersecurity"
    ],
    "research": [
        "Research Methodology", "Data Analysis", "Literature Review",
        "Machine Learning", "NLP", "Computer Vision", "Bioinformatics",
        "Statistical Analysis", "LaTeX", "Python", "R"
    ],
    "extracurricular": [
        "Leadership", "Team Management", "Event Management",
        "Social Work", "Sports", "Music", "Cultural Activities",
        "Volunteer Work", "Community Service"
    ],
    "other": [],
}


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    student_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(SubmissionCategory), nullable=False)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.pending)
    file_url = Column(String, nullable=True)
    skills = Column(JSON, nullable=True, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("User", back_populates="submissions")
    verification = relationship("Verification", back_populates="submission", uselist=False)