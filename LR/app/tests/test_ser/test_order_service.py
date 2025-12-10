from unittest.mock import AsyncMock, Mock

import pytest
from LR.app.repositories.order_repository import OrderRepository
from LR.app.repositories.product_repository import ProductRepository
from LR.app.repositories.user_repository import UserRepository
from LR.app.services.order_service import OrderService
from LR.orm.model import OrderCreate, OrderItemCreate


class TestOrderService:
    @pytest.mark.asyncio
    async def test_create_order_success(self):
        """Тест успешного создания заказа"""

        # Мокаем репозитории
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)

        # Настраиваем моки
        mock_user_repo.get_by_id.return_value = Mock(
            id=1, username="Test_User", email="email@example.com", description=""
        )
        mock_product_repo.get_by_id.return_value = Mock(
            id=1, product_name="Product1", quantity=1
        )
        mock_order_repo.create.return_value = Mock(
            id=1, user_id=1, address_id=None, items=[Mock(product_id=1, quantity=1)]
        )

        order_service = OrderService(
            order_repository=mock_order_repo,
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
        )

        order_data = OrderCreate(
            user_id=1,
            address_id=None,
            items=[OrderItemCreate(product_id=1, quantity=1)],
        )

        result = await order_service.create(order_data)

        assert result is not None
        assert result.id == 1
        assert result.items[0].product_id == 1
        assert result.items[0].quantity == 1

        mock_order_repo.create.assert_called_once_with(order_data)

    @pytest.mark.asyncio
    async def test_create_order_not_user(self):
        """Тест отсутствия пользователя"""

        # Мокаем репозитории
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)

        # Настраиваем моки
        mock_user_repo.get_by_id = AsyncMock(return_value=None)
        mock_product_repo.get_by_id.return_value = Mock(
            id=1, product_name="Product1", quantity=1
        )
        mock_order_repo.create.return_value = Mock(
            id=1, user_id=1, address_id=None, items=[Mock(product_id=1, quantity=1)]
        )

        order_service = OrderService(
            order_repository=mock_order_repo,
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
        )

        order_data = OrderCreate(
            user_id=1,
            address_id=None,
            items=[OrderItemCreate(product_id=1, quantity=1)],
        )

        with pytest.raises(ValueError, match="User not found"):
            await order_service.create(order_data)

    @pytest.mark.asyncio
    async def test_create_order_not_product(self):
        """Тест отсутствия продукта"""

        # Мокаем репозитории
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)

        # Настраиваем моки
        mock_user_repo.get_by_id.return_value = Mock(
            id=1, username="Test_User", email="email@example.com", description=""
        )
        mock_product_repo.get_by_id = AsyncMock(return_value=None)
        mock_order_repo.create.return_value = Mock(
            id=1, user_id=1, address_id=None, items=[Mock(product_id=1, quantity=1)]
        )

        order_service = OrderService(
            order_repository=mock_order_repo,
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
        )

        order_data = OrderCreate(
            user_id=1,
            address_id=None,
            items=[OrderItemCreate(product_id=1, quantity=1)],
        )

        with pytest.raises(ValueError, match="Product 1 not found"):
            await order_service.create(order_data)

    @pytest.mark.asyncio
    async def test_create_order_not_quantity(self):
        """Тест нехватки продукта"""

        # Мокаем репозитории
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)

        # Настраиваем моки
        mock_user_repo.get_by_id.return_value = Mock(
            id=1, username="Test_User", email="email@example.com", description=""
        )
        mock_product_repo.get_by_id.return_value = Mock(
            id=1, product_name="Product1", quantity=1
        )
        mock_order_repo.create.return_value = Mock(
            id=1, user_id=1, address_id=None, items=[Mock(product_id=1, quantity=2)]
        )

        order_service = OrderService(
            order_repository=mock_order_repo,
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
        )

        order_data = OrderCreate(
            user_id=1,
            address_id=None,
            items=[OrderItemCreate(product_id=1, quantity=2)],
        )

        with pytest.raises(
            ValueError, match="Not enough stock for product 1 \(Product1\)"
        ):
            await order_service.create(order_data)
