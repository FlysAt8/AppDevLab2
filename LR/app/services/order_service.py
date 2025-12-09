from LR.app.models.model import OrderCreate, OrderUpdate
from LR.app.models.test_db import Order
from LR.app.repositories.order_repository import OrderRepository
from LR.app.repositories.product_repository import ProductRepository
from LR.app.repositories.user_repository import UserRepository


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

        filt = await self.order_repository.get_by_filter(
            user_id=order_data.user_id, product_id=order_data.product_id
        )
        if filt:
            raise ValueError("With this order already exists")

        user = await self.user_repository.get_by_id(order_data.user_id)
        if not user:
            raise ValueError("User not found")

        product = await self.product_repository.get_by_id(order_data.product_id)
        if not product:
            raise ValueError("Product not found")

        if product.quantity < order_data.quantity:
            raise ValueError("There is not enough product in stock")

        return await self.order_repository.create(order_data)

    async def update(self, order_id: int, order_data: OrderUpdate) -> Order:
        filt = await self.order_repository.get_by_filter(
            user_id=order_data.user_id, product_id=order_data.product_id
        )
        if filt:
            raise ValueError("With this order already exists")

        user = await self.user_repository.get_by_id(order_data.user_id)
        if not user:
            raise ValueError("User not found")

        product = await self.product_repository.get_by_id(order_data.product_id)
        if not product:
            raise ValueError("Product not found")

        if product.quantity < order_data.quantity:
            raise ValueError("There is not enough product in stock")
        return await self.order_repository.update(order_id, order_data)

    async def delete(self, order_id: int) -> None:
        return await self.order_repository.delete(order_id)
