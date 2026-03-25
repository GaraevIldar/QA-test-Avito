import pytest
from utilities.api_client import ApiClient

# Создаются на всю сессию тестов
@pytest.fixture(scope="session")
def base_url(): # Фикстура, которая возвращает базовый URL
    return "https://qa-internship.avito.com"

@pytest.fixture(scope="session")
def api_client(base_url):# Фикстура для создания клиента API
    return ApiClient(base_url)
