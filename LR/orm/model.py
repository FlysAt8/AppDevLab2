from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    description: Optional[str]

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class UserResponse(UserBase):
    id: int

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class ProductBase(BaseModel):
    product_name: str
    quantity: int

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    quantity: Optional[int] = None

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class ProductResponse(ProductBase):
    id: int

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class OrderItemResponse(OrderItemBase):
    id: int

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class OrderBase(BaseModel):
    user_id: int
    address_id: Optional[int] = None

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class OrderCreate(OrderBase):
    # при создании заказа можно сразу передать список позиций
    items: Optional[list[OrderItemCreate]] = []


class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    address_id: Optional[int] = None
    items: Optional[list[OrderItemUpdate]] = None

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class OrderResponse(OrderBase):
    id: int
    items: list[OrderItemResponse]

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True
