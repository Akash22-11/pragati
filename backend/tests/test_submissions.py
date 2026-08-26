def get_auth_token(client, payload):
    client.post("/auth/register", json=payload)
    response = client.post("/auth/login", json={
        "email": payload["email"],
        "password": payload["password"],
    })
    return response.json()["access_token"]


def test_list_submissions_requires_auth(client):
    response = client.get("/submissions/")
    assert response.status_code in (401, 403)


def test_list_submissions_empty(client, student_payload):
    token = get_auth_token(client, student_payload)
    response = client.get("/submissions/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == []


def test_verify_requires_faculty_role(client, student_payload):
    token = get_auth_token(client, student_payload)
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.patch(
        f"/submissions/{fake_id}/verify",
        json={"action": "approved", "note": "test"},
        headers={"Authorization": f"Bearer {token}"},
    )
    # Student role should be forbidden from verifying
    assert response.status_code == 403


def test_verify_nonexistent_submission_as_faculty(client, faculty_payload):
    token = get_auth_token(client, faculty_payload)
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.patch(
        f"/submissions/{fake_id}/verify",
        json={"action": "approved", "note": "test"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404