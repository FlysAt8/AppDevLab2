import requests

data = {
    "username": "Ben",
    "email": "ben@example.com",
    "description": "ts"
}

id_user = "5" # Меняем для нужного пользователя

url = "http://localhost:8000/users/"
full_url = url + id_user

response = requests.put(full_url, json=data)
print(response.status_code, response.text)