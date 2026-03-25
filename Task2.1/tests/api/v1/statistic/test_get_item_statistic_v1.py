import pytest
from utilities.data_provider import DataProvider

positive_data_provider = DataProvider("api\\v1\\statistic\\","data_get_item_statistic_positive_case.json")
negative_data_provider = DataProvider("api\\v1\\statistic\\","data_get_item_statistic_negative_case.json")

def test_get_item_statistic_positive(api_client,  created_item): # Позитивный тест получения статистики по существующему объявлению

    item_id = created_item["id"]

    response = api_client.get_statistic_by_id_v1(item_id)

    expected_code = positive_data_provider.get_test_case("TC-1_GetExistingItemStatistic")["expected_status_code"]

    # Проверка статус-кода
    assert response.status_code == expected_code

    response_json = response.json()

    # Проверка структуры
    assert isinstance(response_json, list), "Ответ не список"
    assert len(response_json) > 0, "Пустой список статистики"

    statistics_data = response_json[0]
    original_statistics = created_item["payload"]["statistics"]

    # Проверка наличия полей
    for field in ["likes", "viewCount", "contacts"]:
        assert field in statistics_data, f"Нет поля {field}"

    # Проверка значений
    assert statistics_data["likes"] == original_statistics["likes"]
    assert statistics_data["viewCount"] == original_statistics["viewCount"]
    assert statistics_data["contacts"] == original_statistics["contacts"]

@pytest.mark.parametrize(
    "test_data",
    negative_data_provider.get_all_test_cases(),
    ids=negative_data_provider.get_test_case_ids()
)
def test_get_statistic_negative(api_client, test_data): # Негативные тесты для получения статистики по объявлению

    item_id = test_data["item_id"]
    expected_status = test_data["expected_status_code"]

    response = api_client.get_statistic_by_id_v1(item_id)

    # Проверка статус-кода
    assert response.status_code == expected_status

    response_json = response.json()

    # Проверка структуры
    assert "status" in response_json, "Нет поля status"
    assert "result" in response_json, "Нет поля result"

    # Дополнительная проверка result
    result = response_json["result"]

    if isinstance(result, dict):
        assert any(key in result for key in ["message", "messages"]), \
            "Нет message/messages в result"
