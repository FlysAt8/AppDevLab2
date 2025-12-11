import pika
import json, random

def send_message_order(user_id: int, items: list[dict]):
    # подключение
    credentials = pika.PlainCredentials("admin", "admin")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="rabbitmq",
            port=5672,
            virtual_host="local",
            credentials=credentials
        )
    )
    channel = connection.channel()

    # сообщение
    message = {
        "action": "create",
        "user_id": user_id,
        "address_id": None,
        "items": items
    }

    # отправка
    channel.basic_publish(
        exchange='',
        routing_key="order",
        body=json.dumps(message)
    )
    connection.close()

if __name__ == "__main__":
    order1 = {
        "user_id": 3,
        "items": [
            {"product_id": 3, "quantity": 2},
            {"product_id": 4, "quantity": 3},
            {"product_id": 5, "quantity": 3}
        ]
    }
    send_message_order(user_id=order1["user_id"], items=order1["items"])
