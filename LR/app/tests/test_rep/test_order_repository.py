import pytest
from LR.app.repositories.order_repository import OrderRepository
from LR.app.repositories.product_repository import ProductRepository
from LR.app.repositories.user_repository import UserRepository
from LR.orm.model import OrderCreate, OrderUpdate, ProductCreate, UserCreate


class TestOrderRepository:

    @pytest.mark.asyncio
    async def test_order_create(
        self,
        order_repository: OrderRepository,
        user_repository: UserRepository,
        product_repository: ProductRepository,
    ):
        """Тест создания заказа"""

        user_data = UserCreate(username="Alex", email="email", description="")
        await user_repository.create(user_data)

        product_data = ProductCreate(product_name="Product1", quantity=1)
        await product_repository.create(product_data)

        order_data = OrderCreate(
            user_id=1, address_id=1, items=[{"product_id": 1, "quantity": 1}]
        )

        order = await order_repository.create(order_data)

        assert order.id is not None
        assert order.user_id == 1
        assert order.address_id == 1
        assert order.items[0].product_id == 1
        assert order.items[0].quantity == 1

    @pytest.mark.asyncio
    async def test_order_get_id(
        self,
        order_repository: OrderRepository,
        user_repository: UserRepository,
        product_repository: ProductRepository,
    ):
        """Тест получение заказа по id"""

        user_data = UserCreate(username="Alex", email="email", description="")
        await user_repository.create(user_data)

        order_data = OrderCreate(user_id=1, address_id=1)

        await order_repository.create(order_data)

        found_order = await order_repository.get_by_id(1)

        assert found_order.id is not None
        assert found_order.user_id == 1
        assert found_order.address_id == 1
        assert found_order.items == []

    @pytest.mark.asyncio
    async def test_order_get_all(
        self,
        order_repository: OrderRepository,
        user_repository: UserRepository,
        product_repository: ProductRepository,
    ):
        """Тест получение списка заказов"""

        user_data = UserCreate(username="Alex", email="email", description="")
        await user_repository.create(user_data)

        user_data = UserCreate(username="Alex1", email="email1", description="")
        await user_repository.create(user_data)

        # создаём продукты
        product_data1 = ProductCreate(product_name="Product1", quantity=10)
        product1 = await product_repository.create(product_data1)

        product_data2 = ProductCreate(product_name="Product2", quantity=5)
        product2 = await product_repository.create(product_data2)

        # создаём заказы с товарами
        order_data1 = OrderCreate(
            user_id=1,
            address_id=1,
            items=[{"product_id": product1.id, "quantity": 2}],
        )
        await order_repository.create(order_data1)

        order_data2 = OrderCreate(
            user_id=2,
            address_id=1,
            items=[{"product_id": product2.id, "quantity": 1}],
        )
        await order_repository.create(order_data2)

        found_orders = await order_repository.get_by_filter()

        assert found_orders is not None

        # проверяем первый заказ
        assert found_orders[0].id is not None
        assert found_orders[0].user_id == 1
        assert found_orders[0].address_id == 1
        assert found_orders[0].items[0].product_id == product1.id
        assert found_orders[0].items[0].quantity == 2

        # проверяем второй заказ
        assert found_orders[1].id is not None
        assert found_orders[1].user_id == 2
        assert found_orders[1].address_id == 1
        assert found_orders[1].items[0].product_id == product2.id
        assert found_orders[1].items[0].quantity == 1

    @pytest.mark.asyncio
    async def test_order_update(
        self,
        order_repository: OrderRepository,
        user_repository: UserRepository,
        product_repository: ProductRepository,
    ):
        """Тест обновления заказа"""

        user_data = UserCreate(username="Alex", email="email", description="")
        await user_repository.create(user_data)

        user_data = UserCreate(username="Alex1", email="email1", description="")
        await user_repository.create(user_data)

        order_data = OrderCreate(user_id=1, address_id=1)

        await order_repository.create(order_data)

        update_order = await order_repository.update(
            1, order_data=OrderUpdate(user_id=2)
        )

        found_order = await order_repository.get_by_id(1)

        assert found_order is not None
        assert update_order is not None
        assert found_order.id == update_order.id
        assert found_order.user_id == update_order.user_id
        assert found_order.address_id == update_order.address_id

    @pytest.mark.asyncio
    async def test_order_delete(
        self,
        order_repository: OrderRepository,
        user_repository: UserRepository,
        product_repository: ProductRepository,
    ):
        """Тест удаления пользователя"""

        user_data = UserCreate(username="Alex1", email="email1", description="")
        await user_repository.create(user_data)

        order_data = OrderCreate(user_id=1, address_id=1)

        await order_repository.create(order_data)
        found_order = await order_repository.get_by_id(1)
        assert found_order is not None

        await order_repository.delete(1)
        found_order = await order_repository.get_by_id(1)
        assert found_order is None
