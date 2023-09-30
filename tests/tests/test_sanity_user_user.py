from saiyan import Saiyanquest
import pytest
from utils import complete_generate_user
import json

URL = 'https://doevida.onrender.com/'


def route(route, sub_route=None):
    return f'{route}/{sub_route}'


@pytest.fixture(scope='session')
def quest():
    quest = Saiyanquest(URL)
    return quest


def test_create_user(quest):
    response = quest.create_and_login()
    assert response["username"]


def test_get_user_by_username(quest):
    try:
        response = quest.get(route('users', quest.username))
        assert response.status_code == 200
    except Exception as e:
        print(e)
        raise e


def test_get_user_by_id(quest):
    try:
        response = quest.get(route('users', quest.id), by_id=True)
        assert response.status_code == 200
    except Exception as e:
        print(e)
        raise e


def test_update_user(quest):
    try:
        response = quest.put(route('users', quest.username), data=complete_generate_user())
        assert response.status_code == 200 and json.loads(response.content.decode('utf-8'))["data"]["blood_type"] == "A+"
    except Exception as e:
        print(e)
        raise e


def test_delete_user(quest):
    try:
        response = quest.delete(route('users', quest.username))
        assert response.status_code == 200
        response = quest.get(route('users', quest.username))
        assert response.status_code == 404
    except Exception as e:
        print(e)
        raise e
