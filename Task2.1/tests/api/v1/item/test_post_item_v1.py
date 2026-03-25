import pytest
from utilities.data_provider import DataProvider

positive_data_provider = DataProvider("api\\v1\\item\\","data_post_positive_test_case.json")
negative_data_provider = DataProvider("api\\v1\\item\\","data_post_negative_test_case.json")
boundary_data_provider = DataProvider("api\\v1\\item\\","data_post_boundary_test_case.json")

@pytest.mark.parametrize(
    "test_data",
    positive_data_provider.get_all_test_cases(),
    ids=positive_data_provider.get_test_case_ids()
)
def test_create_item_positive(api_client, test_data): # Позитивные тесты для создания объявления

    payload = test_data["payload"]
    expected_status = test_data["expected_status_code"]

    response = api_client.create_item_v1(payload)

    # Проверка статус-кода
    assert response.status_code == expected_status

    response_json = response.json()

    # Проверка базовой структуры ответа
    assert "id" in response_json, "В ответе отсутствует id"
    assert "createdAt" in response_json, "В ответе отсутствует createdAt"

    # Проверка соответствия данных
    for key, value in payload.items():

        if key == "sellerID":
            assert response_json["sellerId"] == value
            continue

        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                assert response_json[key][inner_key] == inner_value
            continue

        assert response_json[key] == value

@pytest.mark.parametrize(
    "test_data",
    negative_data_provider.get_all_test_cases(),
    ids=negative_data_provider.get_test_case_ids()
)
def test_create_item_negative(api_client, test_data): # Негативные тесты для создания объявления

    payload = test_data["payload"]
    expected_status = test_data["expected_status_code"]

    response = api_client.create_item_v1(payload)

    # Проверка статус-кода
    assert response.status_code == expected_status

    response_json = response.json()

    # Проверка структуры ответа
    assert "status" in response_json, "Нет поля status"
    assert "result" in response_json, "Нет поля result"

    # Проверка содержимого result
    result = response_json["result"]

    if isinstance(result, dict):
        assert any(key in result for key in ["message", "messages"]), \
            "Нет message/messages в result"

@pytest.mark.parametrize(
    "test_data",
    boundary_data_provider.get_all_test_cases(),
    ids=boundary_data_provider.get_test_case_ids()
)
def test_create_item_boundary(api_client, test_data): # Граничные тесты для создания объявления

    payload = test_data["payload"]
    expected_status = test_data["expected_status_code"]

    response = api_client.create_item_v1(payload)

    # Проверка статус-кода
    assert response.status_code == expected_status

    response_json = response.json()

    if response.status_code == 200:
        # Проверка успешного ответа
        assert "id" in response_json, "Нет id в ответе"
        assert response_json["sellerId"] == payload["sellerID"]

    else:
        # Проверка ошибки
        assert "status" in response_json, "Нет поля status"
        assert "result" in response_json, "Нет поля result"

        result = response_json["result"]

        if isinstance(result, dict):
            assert any(key in result for key in ["message", "messages"]), \
                "Нет message/messages в result"