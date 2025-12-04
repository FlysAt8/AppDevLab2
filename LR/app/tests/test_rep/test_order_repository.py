import pytest
from models.model import OrderCreate, OrderUpdate, UserCreate, ProductCreate
from repositories.order_repository import OrderRepository
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository

class TestOrderRepository:
    
    @pytest.mark.asyncio
    async def test_order_create(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository):
        """Тест создания заказа"""

        user_data = UserCreate(
            username="Alex",
            email="email",
            description=""
        )
        await user_repository.create(user_data)

        product_data = ProductCreate(
            product_name="prod",
            quantity=1
        )
        await product_repository.create(product_data)

        order_data = OrderCreate(
            user_id = 1,
            product_id = 1,
            quantity = 1
        )

        order = await order_repository.create(order_data)

        assert order.id is not None
        assert order.user_id == 1
        assert order.product_id == 1
        assert order.quantity == 1


    @pytest.mark.asyncio
    async def test_order_get_id(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository):
        """Тест получение заказа по id"""

        user_data = UserCreate(
            username="Alex",
            email="email",
            description=""
        )
        await user_repository.create(user_data)

        product_data = ProductCreate(
            product_name="prod",
            quantity=1
        )
        await product_repository.create(product_data)

        order_data = OrderCreate(
            user_id = 1,
            product_id = 1,
            quantity = 1
        )

        await order_repository.create(order_data)

        found_order = await order_repository.get_by_id(1)

        assert found_order.id is not None
        assert found_order.user_id == 1
        assert found_order.product_id == 1
        assert found_order.quantity == 1


    @pytest.mark.asyncio
    async def test_order_get_all(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository):
        """Тест получение списка заказов"""

        user_data = UserCreate(
            username="Alex",
            email="email",
            description=""
        )
        await user_repository.create(user_data)

        user_data = UserCreate(
            username="Alex1",
            email="email1",
            description=""
        )
        await user_repository.create(user_data)

        product_data = ProductCreate(
            product_name="prod",
            quantity=2
        )
        await product_repository.create(product_data)

        order_data1 = OrderCreate(
            user_id = 1,
            product_id = 1,
            quantity = 1
        )
        await order_repository.create(order_data1)

        order_data2 = OrderCreate(
            user_id = 2,
            product_id = 1,
            quantity = 1
        )
        await order_repository.create(order_data2)

        found_order = await order_repository.get_by_filter()

        assert found_order is not None

        assert found_order[0].id == 1
        assert found_order[0].user_id == 1
        assert found_order[0].product_id == 1
        assert found_order[0].quantity == 1

        assert found_order[1].id == 2
        assert found_order[1].user_id == 2
        assert found_order[1].product_id == 1
        assert found_order[1].quantity == 1


    @pytest.mark.asyncio
    async def test_order_update(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository):
        """Тест обновления заказа"""

        user_data = UserCreate(
            username="Alex",
            email="email",
            description=""
        )
        await user_repository.create(user_data)

        user_data = UserCreate(
            username="Alex1",
            email="email1",
            description=""
        )
        await user_repository.create(user_data)

        product_data = ProductCreate(
            product_name="prod",
            quantity=1
        )
        await product_repository.create(product_data)

        order_data = OrderCreate(
            user_id = 1,
            product_id = 1,
            quantity = 1
        )

        await order_repository.create(order_data)

        update_order = await order_repository.update(
            1,
            order_data=OrderUpdate(
                user_id = 2
            )
        )

        found_order = await order_repository.get_by_id(1)

        assert found_order is not None
        assert update_order is not None
        assert found_order.id == update_order.id
        assert found_order.user_id == update_order.user_id
        assert found_order.product_id == update_order.product_id
        assert found_order.quantity == update_order.quantity


    @pytest.mark.asyncio
    async def test_order_delete(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository):
        """Тест удаления пользователя"""

        user_data = UserCreate(
            username="Alex1",
            email="email1",
            description=""
        )
        await user_repository.create(user_data)

        product_data = ProductCreate(
            product_name="prod",
            quantity=1
        )
        await product_repository.create(product_data)

        order_data = OrderCreate(
            user_id = 1,
            product_id = 1,
            quantity = 1
        )

        await order_repository.create(order_data)
        found_order = await order_repository.get_by_id(1)
        assert found_order is not None

        await order_repository.delete(1)
        found_order = await order_repository.get_by_id(1)
        assert found_order is None