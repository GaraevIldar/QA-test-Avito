import pytest
from utilities.data_provider import DataProvider

negative_data_provider = DataProvider("api\\v2\\statistic\\", "data_get_item_statistic_negative_case_v2.json")
positive_data_provider = DataProvider("api\\v2\\statistic\\", "data_get_item_statistic_positive_case_v2.json")

def test_get_item_statistic_positive(api_client, created_item): # Позитивный тест на получение статистики

    item_id = created_item["id"]
    expected_status = positive_data_provider.get_test_case("TC-1_GetExistingItemStatisticV2")["expected_status_code"]

    response = api_client.get_statistic_by_id_v2(item_id)

    # Проверка статус-кода
    assert response.status_code == expected_status

    # Проверка тела ответа
    response_json = response.json()
    assert isinstance(response_json, list), "Ответ не список"
    assert len(response_json) > 0, "Пустой список статистики"

    statistics_data = response_json[0]
    original_statistics = created_item["payload"]["statistics"]

    # Проверка наличия полей
    for field in ["likes", "viewCount", "contacts"]:
        assert field in statistics_data, f"Нет поля {field}"

    # Проверка значений
    for key in ["likes", "viewCount", "contacts"]:
        assert statistics_data[key] == original_statistics[key]

def test_get_item_statistic_negative(api_client, created_item): # Негативный тест на получение статистики

    item_id = created_item["id"]
    expected_status = positive_data_provider.get_test_case("TC-2_NonExistentUUID_V2")["expected_status_code"]

    response = api_client.get_statistic_by_id_v2(item_id)

    # Проверка статус-кода
    assert response.status_code == expected_status

    # Парсинг ответа
    response_json = response.json()

    # Проверка структуры ошибки
    assert "status" in response_json
    assert "result" in response_json