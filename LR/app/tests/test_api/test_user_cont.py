from typing import Protocol
from unittest.mock import AsyncMock, Mock

import pytest
from litestar.di import Provide
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from litestar.testing import create_test_client
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from controllers.user_controller import UserController
from repositories.user_repository import UserRepository
from services.user_service import UserService


class User(BaseModel):
    id: int
    username: str
    email: str
    description: str


class UserFactory(ModelFactory[User]):
    model = User
    __check_model__ = False


class UserCreate(BaseModel):
    username: str
    email: str
    description: str


class UserFacCreat(ModelFactory[UserCreate]):
    model = UserCreate
    __check_model__ = False


@pytest.fixture()
def user():
    return UserFactory.build()


def test_get_user_by_id(user: User):
    """Тест получения определенного пользователя"""
    mock_user_repo = AsyncMock(spec=UserRepository)
    mock_user_repo.get_by_id.return_value = user

    mock_service = UserService(mock_user_repo)

    with create_test_client(
        route_handlers=[UserController],
        dependencies={
            "user_service": Provide(lambda: mock_service, sync_to_thread=False)
        },
    ) as client:
        response = client.get(f"/users/{user.id}")
        assert response.status_code == HTTP_200_OK
        assert response.json()["id"] == user.id
        assert response.json()["username"] == user.username


@pytest.fixture()
def users():
    return [UserFactory.build() for i in range(3)]


def test_get_users_by_filter(users: list[User]):
    """Тест получения пользователей"""
    mock_user_repo = AsyncMock(spec=UserRepository)
    mock_user_repo.get_by_filter.return_value = users

    mock_service = UserService(mock_user_repo)

    with create_test_client(
        route_handlers=[UserController],
        dependencies={
            "user_service": Provide(lambda: mock_service, sync_to_thread=False)
        },
    ) as client:
        response = client.get(f"/users")
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert isinstance(data, list)
        assert len(data) == len(users)
        assert data[0]["id"] == users[0].id
        assert data[1]["username"] == users[1].username
        assert data[2]["email"] == users[2].email


@pytest.fixture()
def user_create():
    return UserFacCreat.build()


def test_post_user(user_create: UserCreate):
    """Тест создания пользователя"""
    user = User(
        id=1,
        username=user_create.username,
        email=user_create.email,
        description=user_create.description,
    )

    mock_service = AsyncMock(spec=UserService)
    mock_service.create.return_value = user

    with create_test_client(
        route_handlers=[UserController],
        dependencies={
            "user_service": Provide(lambda: mock_service, sync_to_thread=False)
        },
    ) as client:
        response = client.post(f"/users", json=user_create.model_dump())
        assert response.status_code == HTTP_201_CREATED
        assert response.json()["id"] == user.id
        assert response.json()["username"] == user.username


def test_put_user(user_create: UserCreate):
    """Тест обновления пользователя"""
    user = User(
        id=1,
        username=user_create.username,
        email=user_create.email,
        description=user_create.description,
    )

    old_user = User(id=1, username="test", email="test", description="t")

    mock_service = AsyncMock(spec=UserService)
    mock_service.get_by_id.re.return_value = old_user
    mock_service.update.return_value = user

    with create_test_client(
        route_handlers=[UserController],
        dependencies={
            "user_service": Provide(lambda: mock_service, sync_to_thread=False)
        },
    ) as client:
        response = client.put(f"/users/{old_user.id}", json=user_create.model_dump())
        assert response.status_code == HTTP_200_OK
        assert response.json()["id"] == user.id
        assert response.json()["username"] == user.username


def test_delete_user():
    """Тест удаления пользователя"""

    old_user = User(id=1, username="test", email="test", description="t")

    mock_service = AsyncMock(spec=UserService)
    mock_service.get_by_id.re.return_value = old_user
    mock_service.delete.return_value = None

    with create_test_client(
        route_handlers=[UserController],
        dependencies={
            "user_service": Provide(lambda: mock_service, sync_to_thread=False)
        },
    ) as client:
        response = client.delete(f"/users/{old_user.id}")
        assert response.status_code == HTTP_204_NO_CONTENT
