from faker import Factory
import requests
import json

def generate_user():
     fake = Factory.create()
     data = {
          
          "username": fake.email(),
          "password": "secreta"
     }
     fake = None
     return data
     

def complete_generate_user():
     fake = Factory.create()
     data = {
        "first_name": fake.name().split()[0],
        "last_name": fake.name().split()[1],
        "birthdate": "10/01/1987",
        "blood_type": "A+",
        "city": "Campinas",
        "password": "changed_password",
        "phone": "19914598",
        }
     
     return data

def create_user_and_login():

     user = generate_user()
     json_data = json.dumps(user)
     headers = {"Content-Type": "application/json"}
     print("Sending http request...")
     response = requests.post(url='http://localhost:5000/users', data=json_data, headers=headers)
     print("Got a response")

     if response.status_code == 200:
          print("Response status: 200")
          print("Trying to login...")
          response = requests.post(url='http://localhost:5000/login', data=json_data, headers=headers)
          if response.status_code == 200:
               print("Success")
               response = response.content.decode('utf-8')
               response = json.loads(response)
               return {"username": user["username"],"token": response["token"], "user":user}
          else:
               print(f"Something went wrong logging in. Response status code: {response.status}")
     else:
          print(f"Something went wrong creating the user. Response status code: {response.status}")
     

