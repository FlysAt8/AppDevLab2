from unittest.mock import AsyncMock

import pytest
from litestar.di import Provide
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from litestar.testing import create_test_client
from LR.app.controllers.order_controller import OrderController
from LR.app.repositories.order_repository import OrderRepository
from LR.app.repositories.product_repository import ProductRepository
from LR.app.repositories.user_repository import UserRepository
from LR.app.services.order_service import OrderService
from LR.orm.model import (
    OrderCreate,
    OrderItemCreate,
    OrderItemResponse,
    OrderResponse,
    OrderUpdate,
)
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

# class Order(BaseModel):
#     id: int
#     user_id: int
#     address_id: int
#     items: list = []


class OrderFactory(ModelFactory[OrderResponse]):
    model = OrderResponse
    __check_model__ = False


# class OrderCreate(BaseModel):
#     user_id: int
#     address_id: int
#     items: list = []


# class OrderFacCreat(ModelFactory[OrderCreate]):
#     model = OrderCreate
#     __check_model__ = False


class Product(BaseModel):
    id: int
    product_name: str
    quantity: int


class User(BaseModel):
    id: int
    username: str
    email: str
    description: str


@pytest.fixture()
def order():
    return OrderFactory.build()


def test_get_order_by_id(order: OrderResponse):
    """Тест получения определенного заказа"""

    mock_user_repo = AsyncMock(spec=UserRepository)
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_order_repo = AsyncMock(spec=OrderRepository)
    mock_order_repo.get_by_id.return_value = order

    order_service = OrderService(
        order_repository=mock_order_repo,
        user_repository=mock_user_repo,
        product_repository=mock_product_repo,
    )
    mock_service_order = order_service

    with create_test_client(
        route_handlers=[OrderController],
        dependencies={
            "order_service": Provide(lambda: mock_service_order, sync_to_thread=False)
        },
    ) as client:
        response = client.get(f"/orders/{order.id}")
        assert response.status_code == HTTP_200_OK
        assert response.json()["id"] == order.id
        assert response.json()["items"][0]["id"] == order.items[0].id


@pytest.fixture()
def orders():
    return [OrderFactory.build() for i in range(3)]


def test_get_orders_by_filter_user(orders: list[OrderResponse]):
    """Тест получения заказов пользователя"""
    mock_user_repo = AsyncMock(spec=UserRepository)
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_order_repo = AsyncMock(spec=OrderRepository)
    mock_order_repo.get_by_filter.return_value = orders

    order_service = OrderService(
        order_repository=mock_order_repo,
        user_repository=mock_user_repo,
        product_repository=mock_product_repo,
    )
    mock_service_order = order_service

    with create_test_client(
        route_handlers=[OrderController],
        dependencies={
            "order_service": Provide(lambda: mock_service_order, sync_to_thread=False)
        },
    ) as client:
        response = client.get(f"/orders/u/{orders[0].user_id}")
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert data[0]["id"] == orders[0].id
        assert data[1]["id"] == orders[1].id


def test_get_orders_by_filter(orders: list[OrderResponse]):
    """Тест получения всех заказов"""
    mock_user_repo = AsyncMock(spec=UserRepository)
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_order_repo = AsyncMock(spec=OrderRepository)
    mock_order_repo.get_by_filter.return_value = orders

    order_service = OrderService(
        order_repository=mock_order_repo,
        user_repository=mock_user_repo,
        product_repository=mock_product_repo,
    )
    mock_service_order = order_service

    with create_test_client(
        route_handlers=[OrderController],
        dependencies={
            "order_service": Provide(lambda: mock_service_order, sync_to_thread=False)
        },
    ) as client:
        response = client.get(f"/orders")
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert data[0]["id"] == orders[0].id
        assert data[1]["user_id"] == orders[1].user_id


@pytest.fixture()
def order_create():
    return OrderFactory.build()


def test_post_order(order_create: OrderResponse):
    """Тест создания заказа"""
    order = OrderResponse(
        id=1,
        user_id=order_create.user_id,
        address_id=order_create.address_id,
        items=order_create.items,
    )

    mock_user_repo = AsyncMock(spec=UserRepository)
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_order_repo = AsyncMock(spec=OrderRepository)

    order_service = OrderService(
        order_repository=mock_order_repo,
        user_repository=mock_user_repo,
        product_repository=mock_product_repo,
    )

    mock_service_order = AsyncMock(order_service)
    mock_service_order.create.return_value = order

    with create_test_client(
        route_handlers=[OrderController],
        dependencies={
            "order_service": Provide(lambda: mock_service_order, sync_to_thread=False)
        },
    ) as client:
        response = client.post(f"/orders", json=order_create.model_dump())
        assert response.status_code == HTTP_201_CREATED
        assert response.json()["id"] == order.id
        assert response.json()["user_id"] == order.user_id


def test_put_order(order_create: OrderResponse):
    """Тест обновления заказа"""
    order = OrderResponse(
        id=1,
        user_id=order_create.user_id,
        address_id=order_create.address_id,
        items=order_create.items,
    )

    old_order = OrderResponse(id=1, user_id=1, address_id=1, items=[])

    mock_user_repo = AsyncMock(spec=UserRepository)
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_order_repo = AsyncMock(spec=OrderRepository)

    order_service = OrderService(
        order_repository=mock_order_repo,
        user_repository=mock_user_repo,
        product_repository=mock_product_repo,
    )

    mock_service_order = AsyncMock(order_service)
    mock_service_order.get_by_id.re.return_value = old_order
    mock_service_order.update.return_value = order

    with create_test_client(
        route_handlers=[OrderController],
        dependencies={
            "order_service": Provide(lambda: mock_service_order, sync_to_thread=False)
        },
    ) as client:
        response = client.put(f"/orders/{old_order.id}", json=order_create.model_dump())
        assert response.status_code == HTTP_200_OK
        assert response.json()["id"] == order.id
        assert response.json()["user_id"] == order.user_id


def test_delete_order():
    """Тест удаления заказа"""

    old_order = OrderResponse(id=1, user_id=1, address_id=1, items=[])

    mock_user_repo = AsyncMock(spec=UserRepository)
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_order_repo = AsyncMock(spec=OrderRepository)

    order_service = OrderService(
        order_repository=mock_order_repo,
        user_repository=mock_user_repo,
        product_repository=mock_product_repo,
    )

    mock_service_order = AsyncMock(order_service)

    mock_service_order.get_by_id.re.return_value = old_order
    mock_service_order.delete.return_value = None

    with create_test_client(
        route_handlers=[OrderController],
        dependencies={
            "order_service": Provide(lambda: mock_service_order, sync_to_thread=False)
        },
    ) as client:
        response = client.delete(f"/orders/{old_order.id}")
        assert response.status_code == HTTP_204_NO_CONTENT
