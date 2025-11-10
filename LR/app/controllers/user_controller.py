from litestar import Controller, get, post, put, delete, Request
from litestar.di import Provide
from litestar.params import Parameter, Body
from litestar.exceptions import NotFoundException, HTTPException
import logging

from typing import List

from services.user_service import UserService
from models.model import UserResponse, UserCreate, UserUpdate

class UserController(Controller):
    path = "/users"
    signature_namespace = {"UserService": UserService, "UserCreate": UserCreate, "UserResponse": UserResponse}

    @get("/{user_id:int}")
    async def get_user_by_id(self, user_service: UserService, user_id: int = Parameter(gt=0),
                             ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(self, user_service: UserService,
                            ) -> List[UserResponse]:
        """Получить всех пользователей"""
        users = await user_service.get_by_filter()
        return [UserResponse.model_validate(user) for user in users]
    
    @post()
    async def create_user(self, user_service: UserService, request: Request) -> UserResponse:
        data = await request.json()
        logging.info(f"Received user_data: {data}")
        user_data = UserCreate(**data)
        try:
            user = await user_service.create(user_data)
            logging.info(f"user.__dict__: {user.__dict__}")
            return UserResponse.model_validate(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logging.exception("Unhandled error in create_user")
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

        
    @put("/{user_id:int}")
    async def update_user(self, user_service: UserService, user_id: int, request: Request,
                          ) -> UserResponse:
        """Обновить пользователя"""
        try:
            data = await request.json()
            logging.info(f"Received update data: {data}")
            user_data = UserUpdate(**data)
            user = await user_service.update(user_id, user_data)
            if not user:
                raise NotFoundException(detail=f"User with ID {user_id} not found")
            return UserResponse.model_validate(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

        
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
"""