import pytest
from unittest.mock import Mock, AsyncMock

from repositories.product_repository import ProductRepository

from services.product_service import ProductService

from models.model import ProductCreate

class TestProductService:
    @pytest.mark.asyncio
    async def test_create_product_success(self):
        """Тест успешного создания продукта"""

        # Мокаем репозитории
        mock_product_repo = AsyncMock(spec=ProductRepository)

        # Настраиваем моки
        mock_product_repo.get_by_filter.return_value = None
        mock_product_repo.create.return_value = Mock(id=1, product_name="Product1", quantity=1)

        product_service = ProductService(product_repository=mock_product_repo)

        product_data = ProductCreate(
            product_name="Product1",
            quantity = 1
        )

        result = await product_service.create(product_data)

        assert result is not None
        assert result.id == 1
        assert result.product_name == "Product1"
        assert result.quantity == 1


    @pytest.mark.asyncio
    async def test_create_product_found_product(self):
        """Тест существования продукта"""

        # Мокаем репозитории
        mock_product_repo = AsyncMock(spec=ProductRepository)

        # Настраиваем моки
        mock_product_repo.get_by_filter.return_value = Mock(id=1, product_name="Product1", quantity=1)
        mock_product_repo.create.return_value = None

        product_service = ProductService(product_repository=mock_product_repo)

        product_data = ProductCreate(
            product_name="Product1",
            quantity = 1
        )

        with pytest.raises(ValueError, match="With this product name already exists"):
            await product_service.create(product_data)


    @pytest.mark.asyncio
    async def test_create_product_negative(self):
        """Тест отрицательных заказов"""

        # Мокаем репозитории
        mock_product_repo = AsyncMock(spec=ProductRepository)

        # Настраиваем моки
        mock_product_repo.get_by_filter.return_value = None
        mock_product_repo.create.return_value = None

        product_service = ProductService(product_repository=mock_product_repo)

        product_data = ProductCreate(
            product_name="Product1",
            quantity = -1
        )

        with pytest.raises(ValueError, match="The product cannot be a negative number"):
            await product_service.create(product_data)

