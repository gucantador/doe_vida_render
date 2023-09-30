import requests, json
from utils import generate_user


class Saiyanquest():

    def __init__(self, url, username=None, role=None, id=None,
                 access_token=None, user=None, refresh_token=None):
        self.username = username
        self.url = url
        self.access_token = access_token
        self.role = role
        self.user = user
        self.refresh_token = refresh_token
        self.id = id
        
    def post(self, route):
        try:
            json_data = json.dumps(self.user)
            headers = {"Content-Type": "application/json", "Authorization": f'Bearer {self.access_token}'}
            response = requests.post(url=f'{self.url}/{route}', data=json_data, headers=headers)
            return response
        except Exception as e:
            raise e
    
    def get(self, route, by_id=False):
        try:
            json_data = json.dumps(self.user)
            headers = {"Content-Type": "application/json", "Authorization": f'Bearer {self.access_token}'}
            response = requests.get(url=f'{self.url}/{route}', data=json_data, headers=headers)
            if not by_id and response.status_code == 200:
                response_data = response.content.decode('utf-8')
                response_data = json.loads(response_data)
                self.id = response_data["data"]["id"]
            return response
        except Exception as e:
            raise e

    def put(self, route, data):
        try:
            json_data = json.dumps(data)
            headers = {"Content-Type": "application/json", "Authorization": f'Bearer {self.access_token}'}
            response = requests.put(url=f'{self.url}/{route}', data=json_data, headers=headers)
            return response
        except Exception as e:
            raise e
    
    def delete(self, route):
        try:
            json_data = json.dumps(self.user)
            headers = {"Content-Type": "application/json", "Authorization": f'Bearer {self.access_token}'}
            response = requests.delete(url=f'{self.url}/{route}', data=json_data, headers=headers)
            return response
        except Exception as e:
            raise e
    
    def create_user(self):
        user = generate_user()
        self.username = user["username"]
        self.user = user
        return user
        
    def get_access_token(self, user):
        print(user)
        json_data = json.dumps(user)
        headers = {"Content-Type": "application/json"}
        print("Trying to login...")
        response = requests.post(url=f'{self.url}/login', data=json_data, headers=headers)
        print(response.content)
        if response.status_code == 200:
            print("Success")
            response = response.content.decode('utf-8')
            response = json.loads(response)
            print(response)
            self.access_token = response["data"]["access_token"]
            self.refresh_token = response["data"]["refresh_token"]
            return response["data"]["access_token"]
        else:
            print(f"Something went wrong logging in. Response status code: {response.status_code}")
    
    def create_and_login(self):
        user = self.create_user()
        print(user)
        json_data = json.dumps(user)
        headers = {"Content-Type": "application/json"}
        print("Sending http request...")
        response = requests.post(url=f'{self.url}/users', data=json_data, headers=headers)
        print("Got a response")
        print(response.status_code)
        print(response.content)
        if response.status_code == 200:
            self.get_access_token(user)
            return dict(username=self.username, access_token=self.access_token)
