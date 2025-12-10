from unittest.mock import AsyncMock, Mock

import pytest
from LR.app.repositories.user_repository import UserRepository
from LR.app.services.user_service import UserService
from LR.orm.model import UserCreate


class TestUserService:
    @pytest.mark.asyncio
    async def test_create_user_success(self):
        """Тест успешного создания пользователя"""

        # Мокаем репозитории
        mock_user_repo = AsyncMock(spec=UserRepository)

        # Настраиваем моки
        mock_user_repo.get_by_filter.return_value = None
        mock_user_repo.create.return_value = Mock(
            id=1, username="Test_User", email="email@example.com", description=""
        )

        user_service = UserService(user_repository=mock_user_repo)

        user_data = UserCreate(
            username="Test_User", email="email@example.com", description=""
        )

        result = await user_service.create(user_data)

        assert result is not None
        assert result.id == 1
        assert result.username == "Test_User"
        assert result.email == "email@example.com"

    @pytest.mark.asyncio
    async def test_create_user_found_user(self):
        """Тест существования пользователя"""

        # Мокаем репозитории
        mock_user_repo = AsyncMock(spec=UserRepository)

        # Настраиваем моки
        mock_user_repo.get_by_filter.return_value = Mock(
            id=1, username="Test_User", email="email@example.com", description=""
        )
        mock_user_repo.create.return_value = None

        user_service = UserService(user_repository=mock_user_repo)

        user_data = UserCreate(
            username="Test_User", email="email@example.com", description=""
        )

        with pytest.raises(
            ValueError, match="User with this email address already exists"
        ):
            await user_service.create(user_data)
