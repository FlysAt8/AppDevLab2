import asyncio
import logging
import os

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from LR.app.repositories.order_repository import OrderRepository
from LR.app.repositories.product_repository import ProductRepository
from LR.app.repositories.user_repository import UserRepository
from LR.app.services.order_service import OrderService
from LR.app.services.product_service import ProductService
from LR.orm.model import OrderCreate, OrderUpdate, ProductUpdate, ProductCreate

# Настройка базы данных
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@postgres_db:5432/my_db"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

broker = RabbitBroker("amqp://admin:admin@rabbitmq:5672/local")
app = FastStream(broker)


async def get_services() -> tuple[OrderService, ProductService, AsyncSession]:
    """Создаём сервисы с репозиториями внутри новой сессии"""
    session: AsyncSession = async_session_factory()
    order_repo = OrderRepository(session)
    product_repo = ProductRepository(session)
    user_repo = UserRepository(session)

    order_service = OrderService(order_repo, user_repo, product_repo)
    product_service = ProductService(product_repo)
    return order_service, product_service, session


@broker.subscriber("order")
async def subscribe_order(order: dict):
    logging.info(f"Received order message: {order}")
    order_service, _, session = await get_services()

    try:
        action = order.get("action", "create")

        if action == "create":
            order_data = OrderCreate(**order)
            created_order = await order_service.create(order_data)
            logging.info(f"Order created: {created_order.id}")

        elif action == "update":
            order_id = order["id"]
            order_data = OrderUpdate(**order)
            updated_order = await order_service.update(order_id, order_data)
            logging.info(f"Order updated: {updated_order.id}")

        else:
            logging.warning(f"Unknown action: {action}")

    except ValueError as e:
        logging.warning(f"Order rejected: {e}")
    except Exception as e:
        logging.exception(f"Error processing order: {e}")
    finally:
        await session.close()


@broker.subscriber("product")
async def subscribe_product(product: dict):
    logging.info(f"Received product message: {product}")
    _, product_service, session = await get_services()

    try:
        action = product.get("action", "create")

        if action == "create":
            product_data = ProductCreate(**product)
            created_product = await product_service.create(product_data)
            logging.info(f"Product created: {created_product.id}")

        elif action == "update":
            product_id = product["id"]
            product_data = ProductUpdate(**product)
            updated_product = await product_service.update(product_id, product_data)
            logging.info(f"Product updated: {updated_product.id}")

        elif action == "out_of_stock":
            product_id = product["id"]
            # отмечаем как закончившийся
            product_data = ProductUpdate(id=product_id, quantity=0)
            updated_product = await product_service.update(product_id, product_data)
            logging.info(f"Product {updated_product.id} marked as out of stock")

        else:
            logging.warning(f"Unknown action: {action}")

    except ValueError as e:
        logging.warning(f"Product rejected: {e}")
    except Exception as e:
        logging.exception(f"Error processing product: {e}")
    finally:
        await session.close()
    

async def main():
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
