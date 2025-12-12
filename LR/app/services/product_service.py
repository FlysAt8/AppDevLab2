import json

from LR.app.repositories.product_repository import ProductRepository
from LR.orm.db import Product
from LR.orm.model import ProductCreate, ProductResponse, ProductUpdate
from redis import Redis


class ProductService:
    def __init__(self, product_repository: ProductRepository, redis_client: Redis):
        self.product_repository = product_repository
        self.redis = redis_client

    async def get_by_id(self, product_id: int) -> Product | None:
        key = f"product:{product_id}"
        cached = self.redis.get(key)
        if cached:
            data = json.loads(cached)
            return Product(**data)

        product = await self.product_repository.get_by_id(product_id)
        if product:
            product_data = ProductResponse.model_validate(product, from_attributes=True)
            self.redis.setex(key, 600, product_data.model_dump_json())
        return product

    async def get_by_filter(
        self, count: int = 10, page: int = 1, **kwargs
    ) -> list[Product]:
        return await self.product_repository.get_by_filter(count, page, **kwargs)

    async def create(self, product_data: ProductCreate) -> Product:
        filt = await self.product_repository.get_by_filter(
            product_name=product_data.product_name
        )
        if filt:
            raise ValueError("With this product name already exists")

        if product_data.quantity < 0:
            raise ValueError("The product cannot be a negative number")

        product = await self.product_repository.create(product_data)
        product_data = ProductResponse.model_validate(product, from_attributes=True)
        self.redis.setex(f"product:{product.id}", 600, product_data.model_dump_json())
        return product

    async def update(self, product_id: int, product_data: ProductUpdate) -> Product:
        filt = await self.product_repository.get_by_filter(
            product_name=product_data.product_name
        )
        if filt:
            raise ValueError("With this product name already exists")
        if product_data.quantity < 0:
            raise ValueError("The product cannot be a negative number")

        updated = await self.product_repository.update(product_id, product_data)
        self.redis.delete(f"product:{product_id}")
        return updated

    async def delete(self, product_id: int) -> None:
        delet = await self.product_repository.delete(product_id)
        self.redis.delete(f"product:{product_id}")
        return delet
