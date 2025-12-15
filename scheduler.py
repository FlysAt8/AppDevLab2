import os
from datetime import date

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from taskiq_aio_pika import AioPikaBroker
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from LR.orm.db import Report, OrderItem


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@postgres_db:5432/my_db"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Настройка брокера RabbitMQ
broker = AioPikaBroker(
    "amqp://admin:admin@rabbitmq:5672/local",
    exchange_name="report",
    queue_name="cmd_order"
)

# Планировщик
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

# Задача: формировать отчёты по заказам
@broker.task(
    schedule=[
        {
            "cron": "0 0 * * *",  # каждый день в 00:00
            "schedule_id": "greet_every_minute",
        }
    ]
)

async def my_scheduled_task() -> str:
    """Создание отчета"""
    async with async_session_factory() as session:  # AsyncSession
        today = date.today()

        # Получаем все уникальные order_id
        result = await session.execute(
            select(OrderItem.order_id).distinct()
        )
        order_ids = result.scalars().all()

        for order_id in order_ids:
            # Суммируем количество продукции по заказу
            count_result = await session.execute(
                select(func.sum(OrderItem.quantity)).where(OrderItem.order_id == order_id)
            )
            count_product = count_result.scalar() or 0

            # Создаём отчёт
            report = Report(
                report_at=today,
                order_id=order_id,
                count_product=count_product
            )
            session.add(report)

        await session.commit()

    return f"Reports for {today} created."

