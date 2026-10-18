import json
import httpx
import pytest

from app.models.submission import Submission, SubmissionCategory
from app.models.user import User
from app.schemas.ai import AchievementAnalysis
from app.services import ai_analyzer
from app.services.ai_analyzer import AIAnalysisError, analyze_achievement, extract_json

GOOD = {
    "title": "AWS Cloud Foundations", "category": "Certification",
    "summary": "Foundational knowledge of AWS.",
    "skills": ["AWS", "Cloud Computing", "IAM", "aws"],
    "technologies": ["EC2", "S3"], "career_paths": ["Cloud Engineer"],
    "skill_gaps": ["Docker", "CI/CD"],
    "recommendations": ["Deploy a small app", "Learn CI/CD", "Dockerize it", "Add monitoring", "extra"],
}


def mock_client(*contents, status=200):
    """httpx client whose fake model replies with each content in turn."""
    it = iter(contents)

    def handler(request):
        body = json.loads(request.content)
        assert body["model"] and body["messages"][0]["role"] == "system"
        return httpx.Response(status, json={"choices": [{"message": {"content": next(it)}}]})
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_extract_json_handles_fences_and_prose():
    assert extract_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert extract_json('Sure! {"a": 1} hope it helps') == {"a": 1}
    with pytest.raises(ValueError):
        extract_json("no json here")


def test_analyze_valid_output_is_cleaned():
    a = analyze_achievement("AWS", "EC2, S3", client=mock_client(json.dumps(GOOD)))
    assert a.skills == ["AWS", "Cloud Computing", "IAM"]  # deduped case-insensitively
    assert len(a.recommendations) == 4                      # capped at 4
    assert a.category == "Certification"


def test_unknown_category_falls_back_to_other():
    bad = {**GOOD, "category": "Wizardry"}
    assert analyze_achievement("x", client=mock_client(json.dumps(bad))).category == "Other"


def test_invalid_then_repaired():
    a = analyze_achievement("x", client=mock_client("not json", json.dumps(GOOD)))
    assert a.title == "AWS Cloud Foundations"


def test_always_invalid_raises():
    with pytest.raises(AIAnalysisError):
        analyze_achievement("x", client=mock_client("nope", '{"title": "x"}'))


def test_http_failure_raises():
    with pytest.raises(AIAnalysisError):
        analyze_achievement("x", client=mock_client("{}", status=500))


def test_retries_without_json_mode_when_unsupported():
    calls = []

    def handler(request):
        body = json.loads(request.content)
        calls.append("response_format" in body)
        if "response_format" in body:
            return httpx.Response(400, json={"error": "unsupported"})
        return httpx.Response(200, json={"choices": [{"message": {"content": json.dumps(GOOD)}}]})
    c = httpx.Client(transport=httpx.MockTransport(handler))
    assert analyze_achievement("x", client=c).skills
    assert calls == [True, False]


# ---------- endpoint ----------
def auth(client, payload):
    client.post("/auth/register", json=payload)
    t = client.post("/auth/login", json={"email": payload["email"], "password": payload["password"]})
    return {"Authorization": f"Bearer {t.json()['access_token']}"}


@pytest.fixture
def fake_model(monkeypatch):
    monkeypatch.setattr("app.routers.ai.analyze_achievement",
                        lambda **kw: AchievementAnalysis.model_validate(GOOD))


def test_requires_auth(client):
    assert client.post("/ai/analyze", json={"achievement": "x"}).status_code in (401, 403)


def test_empty_input_rejected(client, student_payload):
    h = auth(client, student_payload)
    assert client.post("/ai/analyze", json={}, headers=h).status_code == 422
    assert client.post("/ai/analyze", json={"achievement": "   "}, headers=h).status_code == 422


def test_free_text(client, student_payload, fake_model):
    h = auth(client, student_payload)
    r = client.post("/ai/analyze", json={"achievement": "AWS Cloud Foundations cert"}, headers=h)
    assert r.status_code == 200 and r.json()["skills"][0] == "AWS" and r.json()["achievement_id"] is None


def test_own_submission_and_isolation(client, db_session, student_payload, fake_model):
    h = auth(client, student_payload)
    me = db_session.query(User).filter(User.email == student_payload["email"]).first()
    mine = Submission(student_id=me.id, title="Pandas project", category=SubmissionCategory.project)
    other_payload = {**student_payload, "email": "other@pragati.com"}
    h2 = auth(client, other_payload)
    other = db_session.query(User).filter(User.email == "other@pragati.com").first()
    theirs = Submission(student_id=other.id, title="Secret", category=SubmissionCategory.project)
    db_session.add_all([mine, theirs]); db_session.commit()

    r = client.post("/ai/analyze", json={"achievement_id": str(mine.id)}, headers=h)
    assert r.status_code == 200 and r.json()["verification_status"] == "pending"
    assert client.post("/ai/analyze", json={"achievement_id": str(theirs.id)}, headers=h).status_code == 404


def test_model_failure_is_generic_502(client, student_payload, monkeypatch):
    def boom(**kw): raise AIAnalysisError("secret internal detail http://10.0.0.5")
    monkeypatch.setattr("app.routers.ai.analyze_achievement", boom)
    h = auth(client, student_payload)
    r = client.post("/ai/analyze", json={"achievement": "x"}, headers=h)
    assert r.status_code == 502
    assert r.json()["detail"] == "AI analysis failed. Please try again."
    assert "secret" not in r.text
