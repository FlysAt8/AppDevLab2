from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.test_db import Order
from models.model import OrderCreate, OrderUpdate
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_id(self, order_id: int) -> Order | None:
        query = select(Order).where(Order.id == order_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()


    async def get_by_filter(self, count: int | None = None, page: int | None = None, **kwargs) -> list[Order]:
        query = select(Order)
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(Order, key) and value is not None:
                    query = query.where(getattr(Order, key) == value)

        if count is not None and page is not None:
            offset = (page - 1) * count
            query = query.offset(offset).limit(count)

        result = await self.session.execute(query)
        return list(result.scalars().all())


    async def create(self, order_data: OrderCreate) -> Order:
        order = Order(
            user_id=order_data.user_id,
            address_id=order_data.address_id,
            product_id=order_data.product_id,
            quantity=order_data.quantity
        )

        self.session.add(order)
        await self.session.commit()       # фиксируем изменения
        await self.session.refresh(order)  # обновляем объект с id
        return order


    async def update(self, order_id: int, order_data: OrderUpdate) -> Order:
        order = await self.get_by_id(order_id)
        if not order:
            return None
        
        update_data = order_data.model_dump(exclude_unset=True)

        for k, v in update_data.items():
            setattr(order, k, v)

        await self.session.commit()
        await self.session.refresh(order)
        return order


    async def delete(self, order_id: int) -> None:
        order = await self.get_by_id(order_id)
        if order:
            await self.session.delete(order)
            await self.session.commit()

