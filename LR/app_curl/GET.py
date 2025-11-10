import requests

url ="http://127.0.0.1:8000/users/"

id_user = "2" # пусто для всех, /{id} для конкретного

full_url = url + id_user

response = requests.get(full_url)

print(response.json())