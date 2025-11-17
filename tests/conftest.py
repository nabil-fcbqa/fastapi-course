import pytest
from fastapi.testclient import TestClient

from app import models, schemas
from app.config import settings
from app.database import Base, create_engine, declarative_base, get_db, sessionmaker
from app.main import app
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    response = client.post(
        "/users/",
        json={"email": "test_user@gmail.com", "password": "password123"},
    )
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = "password123"
    return new_user


@pytest.fixture
def test_user2(client):
    response = client.post(
        "/users/",
        json={"email": "test_user2@gmail.com", "password": "password123"},
    )
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = "password123"
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "First Post",
            "content": "Content of first post",
            "owner_id": test_user["id"],
        },
        {
            "title": "Second Post",
            "content": "Content of second post",
            "owner_id": test_user["id"],
        },
        {
            "title": "Third Post",
            "content": "Content of third post",
            "owner_id": test_user["id"],
        },
        {
            "title": "Fourth Post",
            "content": "Content of fourth post",
            "owner_id": test_user2["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_models = list(map(create_post_model, posts_data))
    session.add_all(post_models)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
