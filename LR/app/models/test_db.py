from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key = True,
    )
    username: Mapped[str] = mapped_column(nullable=False, unique=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    address = relationship("Address", back_populates="user")
    order = relationship("Order", back_populates="user")

class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(
        primary_key = True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)

    user = relationship("User", back_populates="address")
    order = relationship("Order", back_populates="address")

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(
        primary_key = True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey('addresses.id'), nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    user = relationship("User", back_populates="order")
    address = relationship("Address", back_populates="order")
    product = relationship("Product", back_populates="order")

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        primary_key = True,
    )
    product_name: Mapped[str] = mapped_column(nullable=True, unique=True)
    quantity: Mapped[int] = mapped_column(nullable=True)

    order = relationship("Order", back_populates="product")