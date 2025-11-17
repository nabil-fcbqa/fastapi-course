from typing import List

import pytest

from app import schemas


def test_get_posts(authorized_client, test_user, test_posts):
    response = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, response.json())
    posts_list = list(posts_map)
    assert len(posts_list) == len(test_posts)
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)


def test_unauthorized_user_get_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_get_one_post_not_found(authorized_client, test_posts):
    response = authorized_client.get("/posts/9999")
    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert post.Post.id == test_posts[0].id
    assert response.status_code == 200


@pytest.mark.parametrize(
    "title, content",
    [
        ("Awesome new title", "Awesome new content"),
        ("Another title", "Another content"),
        ("FastAPI is great", "I love FastAPI"),
    ],
)
def test_create_post(authorized_client, test_user, title, content):
    response = authorized_client.post(
        "/posts/", json={"title": title, "content": content}
    )
    created_post = schemas.Post(**response.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.owner_id == test_user["id"]
    assert response.status_code == 201


def test_unauthorized_user_create_post(client):
    response = client.post(
        "/posts/", json={"title": "Unauthorized", "content": "Should not work"}
    )
    assert response.status_code == 401


def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_delete_post_not_found(authorized_client, test_user, test_posts):
    response = authorized_client.delete("/posts/9999")
    assert response.status_code == 404


def test_unauthorized_user_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    response = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json={"title": "Updated Title", "content": "Updated Content"},
    )
    updated_post = schemas.Post(**response.json())
    assert updated_post.title == "Updated Title"
    assert updated_post.content == "Updated Content"
    assert response.status_code == 200


def test_update_post_not_found(authorized_client, test_user, test_posts):
    response = authorized_client.put(
        "/posts/9999",
        json={"title": "Updated Title", "content": "Updated Content"},
    )
    assert response.status_code == 404


def test_unauthorized_user_update_post(client, test_posts):
    response = client.put(
        f"/posts/{test_posts[3].id}",
        json={"title": "Hacked Title", "content": "Hacked Content"},
    )
    assert response.status_code == 401


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    response = authorized_client.put(
        f"/posts/{test_posts[3].id}",
        json={"title": "Hacked Title", "content": "Hacked Content"},
    )
    assert response.status_code == 403
