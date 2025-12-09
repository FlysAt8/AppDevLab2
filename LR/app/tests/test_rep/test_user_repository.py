import pytest

from models.model import UserCreate, UserUpdate
from repositories.user_repository import UserRepository


class TestUserRepository:

    @pytest.mark.asyncio
    async def test_user_create(self, user_repository: UserRepository):
        """Тест создания пользователя"""

        user_data = UserCreate(
            username="Test_User", email="test_email@example.com", description=""
        )

        user = await user_repository.create(user_data)

        user_data = UserCreate(
            username="Test2_User", email="test2_email@example.com", description=""
        )

        user = await user_repository.create(user_data)

        assert user.id is not None
        assert user.username == "Test2_User"
        assert user.email == "test2_email@example.com"
        assert user.description == ""

    @pytest.mark.asyncio
    async def test_user_get_id(self, user_repository: UserRepository):
        """Тест получение пользователя по id"""

        user_data = UserCreate(
            username="Test_User", email="test_email@example.com", description=""
        )

        await user_repository.create(user_data)

        found_user = await user_repository.get_by_id(1)

        assert found_user is not None
        assert found_user.id == 1
        assert found_user.username == "Test_User"
        assert found_user.email == "test_email@example.com"
        assert found_user.description == ""

    @pytest.mark.asyncio
    async def test_user_get_all(self, user_repository: UserRepository):
        """Тест получение списка пользователей"""

        user_data1 = UserCreate(
            username="Test_User1", email="test1_email@example.com", description=""
        )
        await user_repository.create(user_data1)

        user_data2 = UserCreate(
            username="Test_User2", email="test2_email@example.com", description=""
        )
        await user_repository.create(user_data2)

        found_user = await user_repository.get_by_filter()

        assert found_user is not None

        assert found_user[0].id == 1
        assert found_user[0].username == "Test_User1"
        assert found_user[0].email == "test1_email@example.com"
        assert found_user[0].description == ""

        assert found_user[1].id == 2
        assert found_user[1].username == "Test_User2"
        assert found_user[1].email == "test2_email@example.com"
        assert found_user[1].description == ""

    @pytest.mark.asyncio
    async def test_user_update(self, user_repository: UserRepository):
        """Тест обновления пользователя"""

        user_data = UserCreate(
            username="Test_User", email="test_email@example.com", description=""
        )

        await user_repository.create(user_data)

        update_user = await user_repository.update(
            1, user_data=UserUpdate(username="Alex", email="alex@example.com")
        )

        found_user = await user_repository.get_by_id(1)

        assert found_user is not None
        assert update_user is not None
        assert found_user.id == update_user.id
        assert found_user.username == update_user.username
        assert found_user.email == update_user.email
        assert found_user.description == update_user.description

    @pytest.mark.asyncio
    async def test_user_delete(self, user_repository: UserRepository):
        """Тест удаления пользователя"""

        user_data = UserCreate(
            username="Test_User", email="test_email@example.com", description=""
        )

        await user_repository.create(user_data)
        found_user = await user_repository.get_by_id(1)
        assert found_user is not None

        await user_repository.delete(1)
        found_user = await user_repository.get_by_id(1)
        assert found_user is None
