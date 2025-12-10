from LR.orm.db import Order, OrderItem
from LR.orm.model import OrderCreate, OrderUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: int) -> Order | None:
        query = (
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
            .where(Order.id == order_id)
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_by_filter(
        self, count: int | None = None, page: int | None = None, **kwargs
    ) -> list[Order]:
        query = select(Order).options(
            selectinload(Order.items).selectinload(OrderItem.product)
        )
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
        # сам заказ
        order = Order(
            user_id=order_data.user_id,
            address_id=order_data.address_id,
        )
        self.session.add(order)
        await self.session.flush()  # получаем id заказа

        # позиции заказа
        for item in order_data.items:
            order_item = OrderItem(
                order_id=order.id, product_id=item.product_id, quantity=item.quantity
            )
            self.session.add(order_item)

        await self.session.commit()  # фиксируем изменения
        query = (
            select(Order).options(selectinload(Order.items)).where(Order.id == order.id)
        )
        result = await self.session.execute(query)
        return result.scalars().one()

    async def update(self, order_id: int, order_data: OrderUpdate) -> Order:
        order = await self.get_by_id(order_id)
        if not order:
            return None

        update_data = order_data.model_dump(exclude_unset=True)

        for k, v in update_data.items():
            if k not in "items":
                setattr(order, k, v)

        # если пришёл список items — обновляем их
        if "items" in update_data:
            for item_update in update_data["items"]:
                if item_update.id:  # обновляем существующую позицию
                    item = await self.session.get(OrderItem, item_update.id)
                    if item and item.order_id == order.id:
                        upd = item_update.model_dump(exclude_unset=True)
                        for k, v in upd.items():
                            setattr(item, k, v)
                else:  # добавляем новую позицию
                    new_item = OrderItem(
                        order_id=order.id,
                        product_id=item_update.product_id,
                        quantity=item_update.quantity,
                    )
                    self.session.add(new_item)

        await self.session.commit()
        query = (
            select(Order).options(selectinload(Order.items)).where(Order.id == order.id)
        )
        result = await self.session.execute(query)
        return result.scalars().one()

    async def delete(self, order_id: int) -> None:
        order = await self.get_by_id(order_id)
        if order:
            await self.session.delete(order)
            await self.session.commit()
