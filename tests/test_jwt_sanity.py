import requests, json, pytest

from . import utils

URL = 'http://localhost:5000'

@pytest.fixture(scope="session")
def url():
    return URL

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

@pytest.fixture(scope="session")
def hospital():
    return utils.create_hospital()

def test_jwt_get_by_username(username, token, user, url):

    try:
        json_data = json.dumps(user)
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {token}'}
        response = requests.get(url=f'{url}/users/{username}', data=json_data, headers=headers)
    except:
        raise Exception
    
    assert response.status_code == 200 and user["username"].encode('utf-8') in response.content 

def test_jwt_update_user(username, token, url):
    try:
        data = utils.complete_generate_user()
        json_data = json.dumps(data)
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {token}'}
        response = requests.put(url=f'{url}/users/{username}', data=json_data, headers=headers)
    except Exception as e:
        print(f"Ocorreu uma exceção: {e}")
    assert response.status_code == 200 and data["first_name"].encode('utf-8') in response.content


def test_post_hospital(hospital, token, url):
    try:
        json_data = json.dumps(hospital)
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {token}'}
        response = requests.post(url=f'{url}/hospitals', data=json_data, headers=headers)
    except Exception as e:
        print(f"Ocorreu uma exceção: {e}")
    assert response.status_code == 200 and hospital["hospital_name"].encode('utf-8') in response.content    

def test_delete_hospital(hospital, token, url):
    try:
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {token}'}
        response = requests.delete(url=f'{url}/hospitals/{hospital["hospital_name"]}', headers=headers)
    except:
        raise Exception
    
    assert response.status_code == 200 

def test_post_donation_order_creating_hospital(token, url):
    data = {
          "patient_name": "John Doe",
          "blood_type": 2,
          "description": "Patient is in need of blood.",
          "qty_bags": 2,
          "hospital": "John Hopkins Hospital",
          "requester": 1,
          "city_name": "Baltimore",
          "state": 1
          }
    
    try:
        json_data = json.dumps(data)
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {token}'}
        response = requests.post(url=f'{url}/donations_orders', data=json_data, headers=headers)
    except Exception as e:
        print(f"Ocorreu uma exceção: {e}")
    print(response.content)
    assert response.status_code == 200 and "John Doe".encode('utf-8') in response.content


def test_delete_user(username, token, url):
    try:
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {token}'}
        response = requests.delete(url=f'{url}/users/{username}', headers=headers)
    except:
        raise Exception
    
    assert response.status_code == 200 