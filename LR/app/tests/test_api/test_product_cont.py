from unittest.mock import AsyncMock, Mock

import pytest
from litestar.di import Provide
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from litestar.testing import create_test_client
from LR.app.controllers.product_controller import ProductController
from LR.app.repositories.product_repository import ProductRepository
from LR.app.services.product_service import ProductService
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    product_name: str
    quantity: int


class ProductFactory(ModelFactory[Product]):
    model = Product
    __check_model__ = False


class ProductCreate(BaseModel):
    product_name: str
    quantity: int


class ProductFacCreat(ModelFactory[ProductCreate]):
    model = ProductCreate
    __check_model__ = False


@pytest.fixture()
def product():
    return ProductFactory.build()


def test_get_product_by_id(product: Product):
    """Тест получения определенного продукта"""
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_product_repo.get_by_id.return_value = product

    mock_redis = Mock()  # простой мок для Redis
    mock_redis.setex = Mock()
    mock_redis.delete = Mock()
    mock_redis.get = Mock(return_value=None)

    mock_service = ProductService(
        product_repository=mock_product_repo, redis_client=mock_redis
    )

    with create_test_client(
        route_handlers=[ProductController],
        dependencies={
            "product_service": Provide(lambda: mock_service, sync_to_thread=False)
        },
    ) as client:
        response = client.get(f"/products/{product.id}")
        assert response.status_code == HTTP_200_OK
        assert response.json()["id"] == product.id
        assert response.json()["product_name"] == product.product_name
        assert response.json()["quantity"] == product.quantity


@pytest.fixture()
def products():
    return [ProductFactory.build() for i in range(3)]


def test_get_products_by_filter(products: list[Product]):
    """Тест получения продуктов"""
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_product_repo.get_by_filter.return_value = products

    mock_redis = Mock()  # простой мок для Redis
    mock_redis.setex = Mock()
    mock_redis.delete = Mock()
    mock_redis.get = Mock(return_value=None)

    mock_service = ProductService(
        product_repository=mock_product_repo, redis_client=mock_redis
    )

    with create_test_client(
        route_handlers=[ProductController],
        dependencies={
            "product_service": Provide(lambda: mock_service, sync_to_thread=False)
        },
    ) as client:
        response = client.get(f"/products")
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert isinstance(data, list)
        assert len(data) == len(products)
        assert data[0]["id"] == products[0].id
        assert data[1]["product_name"] == products[1].product_name
        assert data[2]["quantity"] == products[2].quantity


@pytest.fixture()
def product_create():
    return ProductFacCreat.build()


def test_post_product(product_create: ProductCreate):
    """Тест создания продукта"""
    product = Product(
        id=1, product_name=product_create.product_name, quantity=product_create.quantity
    )

    mock_service = AsyncMock(spec=ProductService)
    mock_service.create.return_value = product

    with create_test_client(
        route_handlers=[ProductController],
        dependencies={
            "product_service": Provide(lambda: mock_service, sync_to_thread=False)
        },
    ) as client:
        response = client.post(f"/products", json=product_create.model_dump())
        assert response.status_code == HTTP_201_CREATED
        assert response.json()["id"] == product.id
        assert response.json()["product_name"] == product.product_name


def test_put_product(product_create: ProductCreate):
    """Тест обновления продукта"""
    product = Product(
        id=1, product_name=product_create.product_name, quantity=product_create.quantity
    )

    old_product = Product(id=1, product_name="test", quantity=1)

    mock_service = AsyncMock(spec=ProductService)
    mock_service.get_by_id.re.return_value = old_product
    mock_service.update.return_value = product

    with create_test_client(
        route_handlers=[ProductController],
        dependencies={
            "product_service": Provide(lambda: mock_service, sync_to_thread=False)
        },
    ) as client:
        response = client.put(
            f"/products/{old_product.id}", json=product_create.model_dump()
        )
        assert response.status_code == HTTP_200_OK
        assert response.json()["id"] == product.id
        assert response.json()["product_name"] == product.product_name


def test_delete_product():
    """Тест удаления продукта"""

    old_product = Product(id=1, product_name="test", quantity=1)

    mock_service = AsyncMock(spec=ProductService)
    mock_service.get_by_id.re.return_value = old_product
    mock_service.delete.return_value = None

    with create_test_client(
        route_handlers=[ProductController],
        dependencies={
            "product_service": Provide(lambda: mock_service, sync_to_thread=False)
        },
    ) as client:
        response = client.delete(f"/products/{old_product.id}")
        assert response.status_code == HTTP_204_NO_CONTENT


@pytest.fixture()
def products10():
    return [ProductFactory.build() for i in range(10)]


def test_get_products_by_filter_page(products10: list[Product]):
    """Тест получения продуктов по страницам"""
    mock_product_repo = AsyncMock(spec=ProductRepository)

    async def fake_get_by_filter(count: int, page: int):
        if count == 5 and page == 1:
            return products10[0:5]
        if count == 5 and page == 2:
            return products10[5:10]
        return []

    mock_product_repo.get_by_filter.side_effect = fake_get_by_filter

    mock_redis = Mock()  # простой мок для Redis
    mock_redis.setex = Mock()
    mock_redis.delete = Mock()
    mock_redis.get = Mock(return_value=None)

    mock_service = ProductService(
        product_repository=mock_product_repo, redis_client=mock_redis
    )

    with create_test_client(
        route_handlers=[ProductController],
        dependencies={
            "product_service": Provide(lambda: mock_service, sync_to_thread=False)
        },
    ) as client:
        # Первые продукты
        response = client.get(f"/products/?count=5&page=1")
        assert response.status_code == HTTP_200_OK
        data = response.json()
        assert len(data) == 5
        # Следующие продукты
        response2 = client.get(f"/products/?count=5&page=2")
        assert response2.status_code == HTTP_200_OK
        data2 = response2.json()
        assert len(data2) == 5
        # Проверка, что товары не пересекаются
        ids_page1 = {d["id"] for d in data}
        ids_page2 = {d["id"] for d in data2}
        assert ids_page1.isdisjoint(ids_page2)
