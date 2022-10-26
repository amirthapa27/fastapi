
import pytest
from app import schemas


def test_get_all_posts(authorized_client, tests_post):
    response = authorized_client.get('/posts/')

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, response.json())
    print(list(posts_map))

    assert len(response.json()) == len(tests_post)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, tests_post):
    response = client.get('/posts/')
    assert response.status_code == 401


def test_unauthorized_user_get_one_post(client, tests_post):
    response = client.get(f'/posts/{tests_post[0].id}')
    assert response.status_code == 401


def test_get_one_post_not_exist(authorized_client, tests_post):
    response = authorized_client.get(f'/posts/8888')
    assert response.status_code == 404


def test_get_one_post(authorized_client, tests_post):
    response = authorized_client.get(f'/posts/{tests_post[0].id}')
    posts = schemas.PostOut(**response.json())
    assert posts.Post.id == tests_post[0].id


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, tests_post, test_user, title, content, published):
    response = authorized_client.post(
        '/posts/', json={'title': title, 'content': content, 'published': published})
    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201


def test_unauthorized_user_get_all_post(client, tests_post):
    response = client.get('/posts/')
    assert response.status_code == 401


def test_unauthorized_delete_post(client, tests_post):
    response = client.delete(f'/posts/{tests_post[0].id}')
    assert response.status_code == 401


def test_authorized_delete(authorized_client, tests_post):
    response = authorized_client.delete(f'/posts/{tests_post[0].id}')
    assert response.status_code == 204


def test_delete_posts_non_exist(authorized_client, tests_post):
    response = authorized_client.delete('/posts/888')
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, tests_post):
    response = authorized_client.delete(f'/posts/{tests_post[3].id}')
    assert response.status_code == 403


def test_update_post(authorized_client, tests_post):
    data = {
        'title': "updated title",
        'content': "updated content",
        'id': tests_post[0].id
    }
    response = authorized_client.put(f'/posts/{tests_post[0].id}', json=data)
    updated_post = schemas.PostResponse(**response.json())
    assert response.status_code == 200


def test_update_other_user_post(authorized_client, tests_post):
    data = {
        'title': "updated title",
        'content': "updated content",
        'id': tests_post[3].id
    }
    response = authorized_client.put(f'/posts/{tests_post[3].id}', json=data)
    assert response.status_code == 403


def test_unauthorized_update_post(client, tests_post):
    response = client.put(f'/posts/{tests_post[0].id}')
    assert response.status_code == 401


def test_update_posts_non_exist(authorized_client, tests_post):
    data = {
        'title': "updated title",
        'content': "updated content",
        'id': tests_post[0].id
    }
    response = authorized_client.put('/posts/888', json=data)
    assert response.status_code == 404
