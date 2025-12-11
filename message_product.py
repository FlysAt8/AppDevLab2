import pika
import json, random

def send_message_product(product_name: str, quantity: int):
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
        "product_name": product_name,
        "quantity": quantity
    }

    # отправка
    channel.basic_publish(
        exchange='',
        routing_key="product",
        body=json.dumps(message)
    )
    connection.close()

if __name__ == "__main__":
    for i in range(5):
        str0 = f"Product{i+1}"
        q = random.randint(1, 8) 
        send_message_product(str0, q)
