from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
import alembic
from uuid import UUID, uuid4
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(
        primary_key = True,
        default = uuid4,
    )
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now, nullable=True)

    addresses = relationship("Address")
    orders = relationship("Order")

class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[UUID] = mapped_column(
        primary_key = True,
        default = uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column(nullable=False)
    is_primary: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now, nullable=True)

    user = relationship("User")
    order = relationship("Order")

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(
        primary_key = True,
        default = uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=True)
    address_id: Mapped[UUID] = mapped_column(ForeignKey('addresses.id'), nullable=True)
    product_id: Mapped[UUID] = mapped_column(ForeignKey('products.id'), nullable=True)

    user = relationship("User")
    address = relationship("Address")
    product = relationship("Product")

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[UUID] = mapped_column(
        primary_key = True,
        default = uuid4,
    )
    product_name: Mapped[str] = mapped_column(nullable=True)

    order = relationship("Order")