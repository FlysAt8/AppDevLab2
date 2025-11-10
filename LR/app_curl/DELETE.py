import requests

url ="http://127.0.0.1:8000/users/"

id_user = "2" # id пользователя для удаления

full_url = url + id_user

response = requests.delete(full_url)

print(response.status_code)
print(response.text)