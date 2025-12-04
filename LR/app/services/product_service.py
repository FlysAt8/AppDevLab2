from repositories.product_repository import ProductRepository
from models.test_db import Product
from models.model import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_by_id(self, product_id: int) -> Product | None:
        return await self.product_repository.get_by_id(product_id)

    async def get_by_filter(self, count: int = 10, page: int = 1, **kwargs) -> list[Product]:
        return await self.product_repository.get_by_filter(count, page, **kwargs)

    async def create(self, product_data: ProductCreate) -> Product:
        filt = await self.product_repository.get_by_filter(product_name = product_data.product_name)
        if filt:
            raise ValueError("With this product name already exists")
        
        if product_data.quantity < 0:
            raise ValueError("The product cannot be a negative number")

        return await self.product_repository.create(product_data)

    async def update(self, product_id: int, product_data: ProductUpdate) -> Product:
        filt = await self.product_repository.get_by_filter(product_name = product_data.product_name)
        if filt:
            raise ValueError("With this product name already exists")
        if product_data.quantity < 0:
            raise ValueError("The product cannot be a negative number")
        return await self.product_repository.update(product_id, product_data)

    async def delete(self, product_id: int) -> None:
        return await self.product_repository.delete(product_id)
