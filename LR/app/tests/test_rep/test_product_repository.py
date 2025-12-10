import pytest
from LR.app.repositories.product_repository import ProductRepository
from LR.orm.model import ProductCreate, ProductUpdate


class TestProductRepository:

    @pytest.mark.asyncio
    async def test_product_create(self, product_repository: ProductRepository):
        """Тест создания продукта"""

        product_data = ProductCreate(product_name="Test_Product", quantity=8)

        product = await product_repository.create(product_data)

        assert product.id is not None
        assert product.product_name == "Test_Product"
        assert product.quantity == 8

    @pytest.mark.asyncio
    async def test_product_get_id(self, product_repository: ProductRepository):
        """Тест получение продукта по id"""

        product_data = ProductCreate(product_name="Test_Product", quantity=8)

        await product_repository.create(product_data)

        found_product = await product_repository.get_by_id(1)

        assert found_product is not None
        assert found_product.id == 1
        assert found_product.product_name == "Test_Product"
        assert found_product.quantity == 8

    @pytest.mark.asyncio
    async def test_product_get_all(self, product_repository: ProductRepository):
        """Тест получение списка продуктов"""

        product_data1 = ProductCreate(product_name="Test_Product1", quantity=8)
        await product_repository.create(product_data1)

        product_data2 = ProductCreate(product_name="Test_Product2", quantity=5)
        await product_repository.create(product_data2)

        found_product = await product_repository.get_by_filter()

        assert found_product is not None

        assert found_product[0].id == 1
        assert found_product[0].product_name == "Test_Product1"
        assert found_product[0].quantity == 8

        assert found_product[1].id == 2
        assert found_product[1].product_name == "Test_Product2"
        assert found_product[1].quantity == 5

    @pytest.mark.asyncio
    async def test_product_update(self, product_repository: ProductRepository):
        """Тест обновления продукта"""

        product_data = ProductCreate(product_name="Test_Product", quantity=8)

        await product_repository.create(product_data)

        update_product = await product_repository.update(
            1, product_data=ProductUpdate(product_name="Product", quantity=1)
        )

        found_product = await product_repository.get_by_id(1)

        assert found_product is not None
        assert update_product is not None
        assert found_product.id == update_product.id
        assert found_product.product_name == update_product.product_name
        assert found_product.quantity == update_product.quantity

    @pytest.mark.asyncio
    async def test_product_delete(self, product_repository: ProductRepository):
        """Тест удаления пользователя"""

        product_data = ProductCreate(product_name="Test_Product", quantity=8)

        await product_repository.create(product_data)
        found_product = await product_repository.get_by_id(1)
        assert found_product is not None

        await product_repository.delete(1)
        found_product = await product_repository.get_by_id(1)
        assert found_product is None
