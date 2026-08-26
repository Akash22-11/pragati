def test_register_student(client, student_payload):
    response = client.post("/auth/register", json=student_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == student_payload["email"]
    assert data["role"] == "student"


def test_register_duplicate_email(client, student_payload):
    client.post("/auth/register", json=student_payload)
    response = client.post("/auth/register", json=student_payload)
    assert response.status_code == 400


def test_login_success(client, student_payload):
    client.post("/auth/register", json=student_payload)
    response = client.post("/auth/login", json={
        "email": student_payload["email"],
        "password": student_payload["password"],
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, student_payload):
    client.post("/auth/register", json=student_payload)
    response = client.post("/auth/login", json={
        "email": student_payload["email"],
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_get_me_requires_auth(client):
    response = client.get("/auth/me")
    assert response.status_code in (401, 403)


def test_get_me_with_valid_token(client, student_payload):
    client.post("/auth/register", json=student_payload)
    login_response = client.post("/auth/login", json={
        "email": student_payload["email"],
        "password": student_payload["password"],
    })
    token = login_response.json()["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == student_payload["email"]