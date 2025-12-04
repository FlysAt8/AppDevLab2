from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.test_db import Product
from models.model import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_id(self, product_id: int) -> Product | None:
        query = select(Product).where(Product.id == product_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()


    async def get_by_filter(self, count: int | None = None, page: int | None = None, **kwargs) -> list[Product]:
        query = select(Product)
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(Product, key) and value is not None:
                    query = query.where(getattr(Product, key) == value)

        if count is not None and page is not None:
            offset = (page - 1) * count
            query = query.offset(offset).limit(count)

        result = await self.session.execute(query)
        return list(result.scalars().all())


    async def create(self, product_data: ProductCreate) -> Product:
        product = Product(
            product_name=product_data.product_name,
            quantity=product_data.quantity
        )
        self.session.add(product)
        await self.session.commit()       # фиксируем изменения
        await self.session.refresh(product)  # обновляем объект с id
        return product


    async def update(self, product_id: int, product_data: ProductUpdate) -> Product:
        product = await self.get_by_id(product_id)
        if not product:
            return None
        
        update_data = product_data.model_dump(exclude_unset=True)

        for k, v in update_data.items():
            setattr(product, k, v)

        await self.session.commit()
        await self.session.refresh(product)
        return product


    async def delete(self, product_id: int) -> None:
        product = await self.get_by_id(product_id)
        if product:
            await self.session.delete(product)
            await self.session.commit()

