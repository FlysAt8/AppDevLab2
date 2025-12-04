import pytest
from unittest.mock import Mock, AsyncMock

from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository

from services.order_service import OrderService

from models.model import OrderCreate

class TestOrderService:
    @pytest.mark.asyncio
    async def test_create_order_success(self):
        """Тест успешного создания заказа"""

        # Мокаем репозитории
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)

        # Настраиваем моки
        mock_user_repo.get_by_id.return_value = Mock(id=1, username="Test_User", email="email@example.com", description="")
        mock_product_repo.get_by_id.return_value = Mock(id=1, product_name="Product1", quantity=1)
        mock_order_repo.get_by_filter.return_value = None
        mock_order_repo.create.return_value = Mock(id=1, user_id=1, address_id=None, product_id=1, quantity=1)

        order_service = OrderService(
            order_repository=mock_order_repo,
            user_repository=mock_user_repo,
            product_repository=mock_product_repo
        )

        order_data = OrderCreate(
            user_id=1,
            address_id=None,
            product_id=1,
            quantity = 1
        )

        result = await order_service.create(order_data)

        assert result is not None
        assert result.id == 1
        mock_order_repo.get_by_filter.assert_called_once_with(user_id=1, product_id=1)
        mock_order_repo.create.assert_called_once_with(order_data)


    @pytest.mark.asyncio
    async def test_create_order_not_user(self):
        """Тест отсутствия пользователя"""

        # Мокаем репозитории
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)

        # Настраиваем моки
        mock_user_repo.get_by_id.return_value = None
        mock_product_repo.get_by_id.return_value = Mock(id=1, product_name="Product1", quantity=1)
        mock_order_repo.get_by_filter.return_value = None
        mock_order_repo.create.return_value = Mock(id=1, user_id=1, address_id=None, product_id=1, quantity=1)

        order_service = OrderService(
            order_repository=mock_order_repo,
            user_repository=mock_user_repo,
            product_repository=mock_product_repo
        )

        order_data = OrderCreate(
            user_id=1,
            address_id=None,
            product_id=1,
            quantity = 1
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
        mock_user_repo.get_by_id.return_value = Mock(id=1, username="Test_User", email="email@example.com", description="")
        mock_product_repo.get_by_id.return_value = None
        mock_order_repo.get_by_filter.return_value = None
        mock_order_repo.create.return_value = Mock(id=1, user_id=1, address_id=None, product_id=1, quantity=1)

        order_service = OrderService(
            order_repository=mock_order_repo,
            user_repository=mock_user_repo,
            product_repository=mock_product_repo
        )

        order_data = OrderCreate(
            user_id=1,
            address_id=None,
            product_id=1,
            quantity = 1
        )

        with pytest.raises(ValueError, match="Product not found"):
            await order_service.create(order_data)


    @pytest.mark.asyncio
    async def test_create_order_found_order(self):
        """Тест существования заказа"""

        # Мокаем репозитории
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)

        # Настраиваем моки
        mock_user_repo.get_by_id.return_value = Mock(id=1, username="Test_User", email="email@example.com", description="")
        mock_product_repo.get_by_id.return_value = Mock(id=1, product_name="Product1", quantity=1)
        mock_order_repo.get_by_filter.return_value = Mock(id=1, user_id=1, address_id=None, product_id=1, quantity = 1)
        mock_order_repo.create.return_value = None

        order_service = OrderService(
            order_repository=mock_order_repo,
            user_repository=mock_user_repo,
            product_repository=mock_product_repo
        )

        order_data = OrderCreate(
            user_id=1,
            address_id=None,
            product_id=1,
            quantity = 1
        )

        with pytest.raises(ValueError, match="With this order already exists"):
            await order_service.create(order_data)


    @pytest.mark.asyncio
    async def test_create_order_not_quantity(self):
        """Тест нехватки продукта"""

        # Мокаем репозитории
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)

        # Настраиваем моки
        mock_user_repo.get_by_id.return_value = Mock(id=1, username="Test_User", email="email@example.com", description="")
        mock_product_repo.get_by_id.return_value = Mock(id=1, product_name="Product1", quantity=1)
        mock_order_repo.get_by_filter.return_value = None
        mock_order_repo.create.return_value = Mock(id=1, user_id=1, address_id=None, product_id=1, quantity=2)

        order_service = OrderService(
            order_repository=mock_order_repo,
            user_repository=mock_user_repo,
            product_repository=mock_product_repo
        )

        order_data = OrderCreate(
            user_id=1,
            address_id=None,
            product_id=1,
            quantity = 2
        )

        with pytest.raises(ValueError, match="There is not enough product in stock"):
            await order_service.create(order_data)
