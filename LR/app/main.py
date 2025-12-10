import os
from typing import AsyncGenerator

from litestar import Litestar
from litestar.di import Provide
from LR.app.controllers.order_controller import OrderController
from LR.app.controllers.product_controller import ProductController
from LR.app.controllers.user_controller import MainPage, UserController
from LR.app.repositories.order_repository import OrderRepository
from LR.app.repositories.product_repository import ProductRepository
from LR.app.repositories.user_repository import UserRepository
from LR.app.services.order_service import OrderService
from LR.app.services.product_service import ProductService
from LR.app.services.user_service import UserService
from LR.orm.db import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Настройка базы данных
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@postgres_db:5432/my_db"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Провайдер сессии базы данных"""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    """Провайдер репозитория пользователей"""
    return UserRepository(db_session)


async def provide_product_repository(db_session: AsyncSession) -> ProductRepository:
    """Провайдер репозитория продуктов"""
    return ProductRepository(db_session)


async def provide_order_repository(db_session: AsyncSession) -> OrderRepository:
    """Провайдер репозитория заказов"""
    return OrderRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    """Провайдер сервиса пользователей"""
    return UserService(user_repository)


async def provide_product_service(
    product_repository: ProductRepository,
) -> ProductService:
    """Провайдер сервиса продуктов"""
    return ProductService(product_repository)


async def provide_order_service(
    order_repository: OrderRepository,
    user_repository: UserRepository,
    product_repository: ProductRepository,
) -> OrderService:
    """Провайдер сервиса заказов"""
    return OrderService(order_repository, user_repository, product_repository)


app = Litestar(
    route_handlers=[UserController, MainPage, ProductController, OrderController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
        "product_repository": Provide(provide_product_repository),
        "product_service": Provide(provide_product_service),
        "order_repository": Provide(provide_order_repository),
        "order_service": Provide(provide_order_service),
    },
    on_startup=[init_models],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
