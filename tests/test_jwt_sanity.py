import requests, json, pytest

from . import utils

@pytest.fixture(scope="session")
def get_username_and_token():
    return utils.create_user_and_login()

@pytest.fixture(scope="session")
def username(get_username_and_token):
    return get_username_and_token["username"]

@pytest.fixture(scope="session")
def token(get_username_and_token):
    return get_username_and_token["token"]

@pytest.fixture(scope="session")
def user(get_username_and_token):
    return get_username_and_token["user"]

def test_jwt(username, token, user):

    try:
        json_data = json.dumps(user)
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {token}'}
        response = requests.get(url=f'http://localhost:5000/users/{username}', data=json_data, headers=headers)
    except:
        raise Exception
    
    assert response.status_code == 200 and user["username"].encode('utf-8') in response.content 