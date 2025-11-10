import requests

data = {
    "username": "Alex",
    "email": "alex@example.com",
    "description": "aaa"
}

response = requests.post("http://localhost:8000/users", json=data)
print(response.status_code, response.text)