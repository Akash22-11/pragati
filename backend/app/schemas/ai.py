from uuid import UUID
from pydantic import BaseModel, Field, field_validator, model_validator

MAX_ITEMS = 8


def _clean_list(values, limit: int = MAX_ITEMS) -> list[str]:
    """Trim, de-duplicate (case-insensitive) and cap a list of strings."""
    seen, out = set(), []
    for v in values or []:
        if not isinstance(v, str):
            continue
        v = v.strip()
        if v and v.lower() not in seen:
            seen.add(v.lower())
            out.append(v)
    return out[:limit]


class AnalyzeRequest(BaseModel):
    """Analyze an existing Pragati submission (preferred) or free text."""
    achievement_id: UUID | None = None
    achievement: str | None = Field(default=None, max_length=3000)

    @model_validator(mode="after")
    def _one_source(self):
        if self.achievement is not None:
            self.achievement = self.achievement.strip() or None
        if not self.achievement_id and not self.achievement:
            raise ValueError("Provide achievement_id or achievement text.")
        return self


class AchievementAnalysis(BaseModel):
    """Validated structure the model must return."""
    title: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=60)
    summary: str = Field(min_length=1, max_length=600)
    skills: list[str]
    technologies: list[str]
    career_paths: list[str]
    skill_gaps: list[str]
    recommendations: list[str]

    @field_validator("title", "category", "summary", mode="before")
    @classmethod
    def _strip(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("skills", "technologies", "career_paths", "skill_gaps", mode="before")
    @classmethod
    def _clean(cls, v):
        return _clean_list(v)

    @field_validator("recommendations", mode="before")
    @classmethod
    def _clean_recs(cls, v):
        return _clean_list(v, limit=4)

    @model_validator(mode="after")
    def _not_empty(self):
        if not self.skills:
            raise ValueError("No skills returned")
        if not self.recommendations:
            raise ValueError("No recommendations returned")
        return self


class AnalyzeResponse(AchievementAnalysis):
    """Analysis plus provenance, so the UI can show verified vs. unverified input."""
    model: str
    achievement_id: UUID | None = None
    verification_status: str | None = None
