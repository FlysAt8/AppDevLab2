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


class OrderBase(BaseModel):
    user_id: int
    address_id: Optional[int] = None
    product_id: int
    quantity: int

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    address_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True


class OrderResponse(OrderBase):
    id: int

    class ConfigDict:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True
