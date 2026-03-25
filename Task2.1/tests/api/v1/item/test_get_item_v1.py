import pytest
from utilities.data_provider import DataProvider

positive_data_provider = DataProvider("api\\v1\\item\\","data_get_positive_test_case.json")
negative_data_provider = DataProvider("api\\v1\\item\\","data_get_negative_test_case.json")

def test_get_item_positive(api_client, created_item): # Позитивный тест для получения объявления по id

    created_id = created_item["id"]

    response = api_client.get_item_by_id_v1(created_id)

    assert response.status_code == positive_data_provider.get_test_case("TС-1_GetExistingItem")["expected_status_code"]

    item = response.json()[0]

@pytest.mark.parametrize(
    "case",
    negative_data_provider.get_all_test_cases(),
    ids=negative_data_provider.get_test_case_ids()
)
def test_get_item_with_invalid_data(api_client, case): # Негативные тесты для получения объявления по id

    item_id = case["item_id"]
    expected_status = case["expected_status_code"]

    response = api_client.get_item_by_id_v1(item_id)

    # проверка статус-кода
    assert response.status_code == expected_status

    # проверка тела ответа
    if "application/json" in response.headers.get("Content-Type", ""):
        body = response.json()

        assert isinstance(body, dict), "Ответ не является JSON-объектом"

        assert any(key in body for key in ["status", "result", "message"]) , "Ответ не содержит ожидаемых полей"


