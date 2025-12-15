from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(nullable=False, unique=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    address = relationship("Address", back_populates="user")
    orders = relationship("Order", back_populates="user")


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)

    user = relationship("User", back_populates="address")
    orders = relationship("Order", back_populates="address")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=True)

    user = relationship("User", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    product_name: Mapped[str] = mapped_column(nullable=True, unique=True)
    quantity: Mapped[int] = mapped_column(nullable=True)

    order_items = relationship("OrderItem", back_populates="product")
    

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    report_at: Mapped[date] = mapped_column(nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    count_product: Mapped[int] = mapped_column(nullable=False)

    order = relationship("Order")

