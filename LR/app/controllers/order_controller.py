from litestar import Controller, get, post, put, delete, Request
from litestar.di import Provide
from litestar.params import Parameter, Body
from litestar.exceptions import NotFoundException, HTTPException
import logging

from typing import List

from services.order_service import OrderService
from models.model import OrderResponse, OrderCreate, OrderUpdate

class OrderController(Controller):
    path = "/orders"
    signature_namespace = {"OrderService": OrderService, "OrderCreate": OrderCreate, "OrderResponse": OrderResponse}

    @get("/{order_id:int}")
    async def get_order_by_id(self, order_service: OrderService, order_id: int = Parameter(gt=0),
                             ) -> OrderResponse:
        """Получить заказ по ID"""
        order = await order_service.get_by_id(order_id)
        if not order:
            raise NotFoundException(detail=f"Order with ID {order_id} not found")
        return OrderResponse.model_validate(order, from_attributes=True)
    
    @get("/u/{user_id:int}")
    async def get_user_orders(self, order_service: OrderService, user_id: int = Parameter(gt=0),
                            count: int = 10,
                            page: int = 1,
                            ) -> List[OrderResponse]:
        """Получить все заказы пользователя(ID)"""
        try:
            orders = await order_service.get_by_filter(user_id = user_id, count=count, page=page)
            return [OrderResponse.model_validate(order, from_attributes=True) for order in orders]
        except Exception as e:
            import logging
            logging.exception("Error in get_user_orders")
            raise HTTPException(status_code=500, detail=str(e))

    @get()
    async def get_all_orders(self, order_service: OrderService,
                            count: int = 10,
                            page: int = 1,
                            ) -> List[OrderResponse]:
        """Получить все заказы"""
        try:
            orders = await order_service.get_by_filter(count=count, page=page)
            return [OrderResponse.model_validate(order, from_attributes=True) for order in orders]
        except Exception as e:
            import logging
            logging.exception("Error in get_all_orders")
            raise HTTPException(status_code=500, detail=str(e))
    
    @post()
    async def create_order(self, order_service: OrderService, request: Request) -> OrderResponse:
        """Создать продукт"""
        data = await request.json()
        logging.info(f"Received order_data: {data}")
        order_data = OrderCreate(**data)
        try:
            order = await order_service.create(order_data)
            logging.info(f"order.__dict__: {order.__dict__}")
            return OrderResponse.model_validate(order, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logging.exception("Unhandled error in create_order")
            raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

        
    @put("/{order_id:int}")
    async def update_order(self, order_service: OrderService, order_id: int, request: Request,
                          ) -> OrderResponse:
        """Обновить продукт"""
        try:
            data = await request.json()
            logging.info(f"Received update data: {data}")
            order_data = OrderUpdate(**data)
            order = await order_service.update(order_id, order_data)
            if not order:
                raise NotFoundException(detail=f"Order with ID {order_id} not found")
            return OrderResponse.model_validate(order, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating order: {str(e)}")

        
    @delete("/{order_id:int}")
    async def delete_order(self, order_service: OrderService, order_id: int) -> None:
        """Удалить продукт"""
        return await order_service.delete(order_id)
        