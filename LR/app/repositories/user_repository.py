from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.test_db import User
from models.model import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()


    async def get_by_filter(self, count: int | None = None, page: int | None = None, **kwargs) -> list[User]:
        query = select(User)
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(User, key) and value is not None:
                    query = query.where(getattr(User, key) == value)

        if count is not None and page is not None:
            offset = (page - 1) * count
            query = query.offset(offset).limit(count)

        result = await self.session.execute(query)
        return list(result.scalars().all())


    async def create(self, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            description=user_data.description or ""
        )
        self.session.add(user)
        await self.session.commit()       # фиксируем изменения
        await self.session.refresh(user)  # обновляем объект с id
        return user


    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)

        for k, v in update_data.items():
            setattr(user, k, v)

        await self.session.commit()
        await self.session.refresh(user)
        return user


    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()

