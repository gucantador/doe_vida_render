import requests, json, pytest
from . import utils

@pytest.fixture(scope="session")
def user():
    return utils.generate_user()

def test_create_user(user):

    try:
        json_data = json.dumps(user)
        headers = {"Content-Type": "application/json"}
        response = requests.post(url='http://localhost:5000/users', data=json_data, headers=headers)
    except:
        raise Exception
    
    assert response.status_code == 200 and user["username"].encode('utf-8') in response.content 

def test_check_created_user_by_username(user):
    try:
        response = requests.get(url=f'http://localhost:5000/users/{user["username"]}')
    except:
        raise Exception
    
    assert response.status_code == 200 and user["username"].encode('utf-8') in response.content

def test_update_user(user):
    try:
        username = user["username"]
        data = utils.complete_generate_user()
        json_data = json.dumps(data)
        headers = {"Content-Type": "application/json"}
        response = requests.put(url=f'http://localhost:5000/users/{username}', data=json_data, headers=headers)
    except:
        raise Exception
    
    assert response.status_code == 200 and data["first_name"].encode('utf-8') in response.content

def test_delete_user(user):
    try:
        response = requests.delete(url=f'http://localhost:5000/users/{user["username"]}')
    except:
        raise Exception
    
    assert response.status_code == 200 