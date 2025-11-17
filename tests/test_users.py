import pytest
from jose import jwt

from app import schemas
from app.config import settings

# def test_root(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World!"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "hello123@gmail.com", "password": "password123"},
    )
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("test_user@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        ("", "password123", 422),
        ("test_user@gmail.com", "", 422),
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post(
        "/login",
        data={"username": test_user["email"], "password": "wrongpassword"},
    )
    assert response.status_code == 403
    # assert response.json().get("detail") == "Invalid Credentials"
