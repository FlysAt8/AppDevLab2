import requests

# user - 0, product - 1, order
x = 1
match x:
    case 0:
        url = "http://localhost:8000/users"
        data = {
            "username": "Alex3",
            "email": "alex3@example.com",
            "description": "aaa2"
        }
    case 1:
        url = "http://localhost:8000/products"
        data = {
            "product_name": "Product13",
            "quantity": 1
        }
    case 2:
        url = "http://localhost:8000/orders"
        data = {
            "user_id": 1,
            "product_id": 2,
            "quantity": 2
        }


response = requests.post(url, json=data)
print(response.status_code, response.text)