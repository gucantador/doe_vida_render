from saiyan import Saiyanquest
URL = 'https://doevida.onrender.com/'
URL_LOCAL = 'http://localhost:5000'

test = Saiyanquest(url=URL)

print(test.create_and_login())
