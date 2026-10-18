"""
Pragati AI — Achievement Intelligence.

AchievementAnalyzer -> OpenAI-compatible chat endpoint -> open-weight model.

The default model is Qwen2.5-7B-Instruct (Apache-2.0). Because the transport is the
standard /chat/completions API, swapping model or host (Ollama, vLLM, Together, Groq,
HF router, ...) is an env-var change: AI_BASE_URL / AI_MODEL / AI_API_KEY.
"""
import json
import logging
import re

import httpx
from pydantic import ValidationError

from app.config import settings
from app.schemas.ai import AchievementAnalysis

logger = logging.getLogger("pragati.ai")


class AIAnalysisError(Exception):
    """Raised when the model is unreachable or never returns valid output.
    The message is internal-only; routers must not expose it to users."""


SYSTEM_PROMPT = """You are Pragati AI, an achievement intelligence engine for college students.

Analyze the supplied student achievement. Use ONLY information reasonably supported by the supplied content.
Do not invent certificates, technologies, tools, experience, employers or achievements.
Do not overstate proficiency (e.g. never call a student an "expert"); describe what the achievement demonstrates.
Keep skill gaps realistic and recommendations practical for a college student (small projects, deployments, courses).

Return ONLY one valid JSON object, with no markdown and no commentary, using exactly these keys:
{
  "title": string,                 // achievement title
  "category": string,              // one of: Certification, Internship, Project, Competition, Research, Extracurricular, Other
  "summary": string,               // 1-2 sentences on what the student actually gained
  "skills": [string],              // 3-8 skills evidenced by the achievement
  "technologies": [string],        // concrete tools/technologies actually mentioned or clearly implied
  "career_paths": [string],        // 2-4 realistic career paths these skills support
  "skill_gaps": [string],          // 2-5 reasonable skills to learn next, not already demonstrated
  "recommendations": [string]      // 2-4 specific, actionable next steps or projects
}"""

CATEGORIES = {"certification", "internship", "project", "competition",
              "research", "extracurricular", "other"}


def build_user_prompt(title: str | None, description: str | None,
                      category: str | None, existing_skills: list[str] | None) -> str:
    lines = ["Student achievement to analyze:"]
    if title:
        lines.append(f"Title: {title}")
    if category:
        lines.append(f"Category (as submitted): {category}")
    if description:
        lines.append(f"Description: {description}")
    if existing_skills:
        lines.append("Skills tagged by the student: " + ", ".join(existing_skills))
    return "\n".join(lines)


def extract_json(text: str) -> dict:
    """Pull a JSON object out of model output, tolerating ``` fences and stray prose."""
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end <= start:
            raise
        return json.loads(text[start:end + 1])


def _call_model(messages: list[dict], client: httpx.Client | None = None) -> str:
    url = settings.AI_BASE_URL.rstrip("/") + "/chat/completions"
    headers = {"Content-Type": "application/json"}
    if settings.AI_API_KEY:
        headers["Authorization"] = f"Bearer {settings.AI_API_KEY}"
    body = {
        "model": settings.AI_MODEL,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 900,
        "response_format": {"type": "json_object"},
    }
    owns_client = client is None
    client = client or httpx.Client(timeout=settings.AI_TIMEOUT_SECONDS)
    try:
        res = client.post(url, json=body, headers=headers)
        if res.status_code in (400, 422):  # provider without JSON mode: retry without it
            body.pop("response_format")
            res = client.post(url, json=body, headers=headers)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except (httpx.HTTPError, KeyError, IndexError, ValueError) as exc:
        raise AIAnalysisError(f"model call failed: {exc.__class__.__name__}") from exc
    finally:
        if owns_client:
            client.close()


def analyze_achievement(title: str | None, description: str | None = None,
                        category: str | None = None,
                        existing_skills: list[str] | None = None,
                        client: httpx.Client | None = None) -> AchievementAnalysis:
    """Run the open-weight model and return a validated analysis (one repair retry)."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(title, description, category, existing_skills)},
    ]
    last_error = "unknown"
    for attempt in range(2):
        raw = _call_model(messages, client)
        try:
            data = extract_json(raw)
            analysis = AchievementAnalysis.model_validate(data)
            if analysis.category.lower() not in CATEGORIES:
                analysis.category = "Other"
            else:
                analysis.category = analysis.category.strip().capitalize()
            return analysis
        except (ValueError, ValidationError) as exc:  # JSONDecodeError is a ValueError
            last_error = exc.__class__.__name__
            logger.warning("Invalid model output (attempt %d): %s", attempt + 1, last_error)
            messages += [
                {"role": "assistant", "content": raw or ""},
                {"role": "user", "content": "That was not valid. Reply again with ONLY the JSON object "
                                            "using exactly the required keys."},
            ]
    raise AIAnalysisError(f"model returned invalid output: {last_error}")
