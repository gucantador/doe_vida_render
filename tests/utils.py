from faker import Factory


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
