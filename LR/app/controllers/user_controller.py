import logging
from typing import List

from litestar import Controller, Request, delete, get, post, put
from litestar.exceptions import HTTPException, NotFoundException
from litestar.params import Parameter
from LR.app.services.user_service import UserService
from LR.orm.model import UserCreate, UserResponse, UserUpdate


class UserController(Controller):
    path = "/users"
    signature_namespace = {
        "UserService": UserService,
        "UserCreate": UserCreate,
        "UserResponse": UserResponse,
    }

    @get("/{user_id:int}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: int = Parameter(gt=0),
    ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user, from_attributes=True)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = 10,
        page: int = 1,
    ) -> List[UserResponse]:
        """Получить всех пользователей"""
        try:
            users = await user_service.get_by_filter(count=count, page=page)
            return [
                UserResponse.model_validate(user, from_attributes=True)
                for user in users
            ]
        except Exception as e:
            logging.exception("Error in get_all_users")
            raise HTTPException(status_code=500, detail=str(e)) from e

    @post()
    async def create_user(
        self, user_service: UserService, request: Request
    ) -> UserResponse:
        """Создать пользователя"""
        data = await request.json()
        logging.info("Received user_data: %s", data)
        user_data = UserCreate(**data)
        try:
            user = await user_service.create(user_data)
            logging.info("user.__dict__: %s", user.__dict__)
            return UserResponse.model_validate(user, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            logging.exception("Unhandled error in create_user")
            raise HTTPException(
                status_code=500, detail=f"Error creating user: {str(e)}"
            ) from e

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: int,
        request: Request,
    ) -> UserResponse:
        """Обновить пользователя"""
        try:
            data = await request.json()
            logging.info("Received update data: %s", data)
            user_data = UserUpdate(**data)
            user = await user_service.update(user_id, user_data)
            if not user:
                raise NotFoundException(detail=f"User with ID {user_id} not found")
            return UserResponse.model_validate(user, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error updating user: {str(e)}"
            ) from e

    @delete("/{user_id:int}")
    async def delete_user(self, user_service: UserService, user_id: int) -> None:
        """Удалить пользователя"""
        return await user_service.delete(user_id)


class MainPage(Controller):
    path = "/"

    @get()
    async def main(self) -> str:
        return """          Welcome to my web application!
Используйте:
    /users - для просмотра всех пользователей
    /users/[id пользователя] - для просмотра конкретного пользователя

    /products - просмотреть продукты
    /products/[id продукта] - для просмотра конкретного продукта

    /orders - все заказы
    /orders/[id заказа] - конкретный заказ
    /orders/u/[id пользователя] - заказы конкретного пользователя

    /report?date=[год]-[месяц]-[день] - отчет по заказам
"""
