import json

from LR.app.repositories.user_repository import UserRepository
from LR.orm.db import User
from LR.orm.model import UserCreate, UserResponse, UserUpdate
from redis import Redis


class UserService:
    def __init__(self, user_repository: UserRepository, redis_client: Redis):
        self.user_repository = user_repository
        self.redis = redis_client

    async def get_by_id(self, user_id: int) -> User | None:
        key = f"user:{user_id}"
        cached = self.redis.get(key)
        if cached:
            data = json.loads(cached)
            return User(**data)

        user = await self.user_repository.get_by_id(user_id)
        if user:
            user_data = UserResponse.model_validate(user, from_attributes=True)
            self.redis.setex(key, 3600, user_data.model_dump_json())
        return user

    async def get_by_filter(
        self, count: int = 10, page: int = 1, **kwargs
    ) -> list[User]:
        return await self.user_repository.get_by_filter(count, page, **kwargs)

    async def create(self, user_data: UserCreate) -> User:
        filt = await self.user_repository.get_by_filter(email=user_data.email)
        if filt:
            raise ValueError("User with this email address already exists")

        user = await self.user_repository.create(user_data)
        user_data = UserResponse.model_validate(user, from_attributes=True)
        self.redis.setex(f"user:{user.id}", 3600, user_data.model_dump_json())
        return user

    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        updated = await self.user_repository.update(user_id, user_data)
        self.redis.delete(f"user:{user_id}")
        return updated

    async def delete(self, user_id: int) -> None:
        delet = await self.user_repository.delete(user_id)
        self.redis.delete(f"user:{user_id}")
        return delet
