import pytest
from app import models


@pytest.fixture()
def test_vote(tests_post, session, test_user):
    new_vote = models.Vote(post_id=tests_post[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, tests_post, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": tests_post[1].id, "dir": 1})
    assert res.status_code == 201


def test_vote_twice_on_post(authorized_client, tests_post, test_vote):
    response = authorized_client.post(
        '/vote/', json={'post_id': tests_post[3].id, 'dir': 1})
    assert response.status_code == 409


def test_delete_vote(authorized_client, tests_post, test_vote):
    response = authorized_client.post(
        '/vote/', json={'post_id': tests_post[3].id, 'dir': 0})
    assert response.status_code == 201


def test_delete_vote_on_post_not_exist(authorized_client, tests_post):
    res = authorized_client.post(
        "/vote/", json={"post_id": tests_post[3].id, "dir": 0})
    assert res.status_code == 404


def test_vote_on_post_not_exist(authorized_client, tests_post):
    res = authorized_client.post(
        "/vote/", json={"post_id": 8000, "dir": 1})
    assert res.status_code == 404


def test_vote_on_post_not_authorized(client, tests_post):
    res = client.post(
        "/vote/", json={"post_id": tests_post[3].id, "dir": 1})
    assert res.status_code == 401
