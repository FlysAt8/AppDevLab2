from LR.app.repositories.order_repository import OrderRepository
from LR.app.repositories.product_repository import ProductRepository
from LR.app.repositories.user_repository import UserRepository
from LR.orm.db import Order
from LR.orm.model import OrderCreate, OrderUpdate


class OrderService:

    def __init__(
        self,
        order_repository: OrderRepository,
        user_repository: UserRepository,
        product_repository: ProductRepository,
    ):
        self.order_repository = order_repository
        self.user_repository = user_repository
        self.product_repository = product_repository

    async def get_by_id(self, order_id: int) -> Order | None:
        return await self.order_repository.get_by_id(order_id)

    async def get_by_filter(
        self, count: int = 10, page: int = 1, **kwargs
    ) -> list[Order]:
        return await self.order_repository.get_by_filter(count, page, **kwargs)

    async def create(self, order_data: OrderCreate) -> Order:

        user = await self.user_repository.get_by_id(order_data.user_id)
        if not user:
            raise ValueError("User not found")

        # проверяем все товары
        for item in order_data.items:
            product = await self.product_repository.get_by_id(item.product_id)
            if not product:
                raise ValueError(f"Product {item.product_id} not found")
            if product.quantity < item.quantity:
                raise ValueError(
                    f"Not enough stock for product {product.id} ({product.product_name})"
                )

        return await self.order_repository.create(order_data)

    async def update(self, order_id: int, order_data: OrderUpdate) -> Order:
        # проверяем пользователя, если он указан
        if order_data.user_id is not None:
            user = await self.user_repository.get_by_id(order_data.user_id)
            if not user:
                raise ValueError("User not found")

        # проверяем товары, если они указаны
        if order_data.items is not None:
            for item in order_data.items:
                product = await self.product_repository.get_by_id(item.product_id)
                if not product:
                    raise ValueError(f"Product {item.product_id} not found")
                if product.quantity < item.quantity:
                    raise ValueError(
                        f"Not enough stock for product {product.id} ({product.product_name})"
                    )

        return await self.order_repository.update(order_id, order_data)

    async def delete(self, order_id: int) -> None:
        return await self.order_repository.delete(order_id)
