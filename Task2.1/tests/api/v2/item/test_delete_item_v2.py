import pytest
from utilities.data_provider import DataProvider

negative_data_provider = DataProvider("api\\v2\\item\\", "data_delete_item_negative_test_case.json")
positive_data_provider = DataProvider("api\\v2\\item\\", "data_delete_item_positive_test_case.json")

def test_delete_item_positive(api_client,created_item): # Позитивный тест удаления объявления

    delete_id = created_item["id"]
    expected_status = positive_data_provider.get_test_case("TC-1_DeleteItemSuccessfully")["expected_status_code"]

    delete_response = api_client.get_item_by_id_v1(delete_id)

    # Проверка статус-кода
    assert delete_response.status_code == expected_status

    # Проверка тела ответа
    assert delete_response.text == "", "Тело ответа должно быть пустым после успешного удаления"

    # Проверка удаления объявления
    get_response = api_client.get_item_by_id_v1(created_item["id"])
    assert get_response.status_code == 404, "Объявление не было удалено"

@pytest.mark.parametrize(
    "test_data",
    negative_data_provider.get_all_test_cases(),
    ids=negative_data_provider.get_test_case_ids()
)
def test_delete_item_v2_negative(api_client, test_data): # Негативные тесты удаления объявления

    delete_id = test_data["item_id"]
    expected_status = test_data["expected_status_code"]

    response = api_client.delete_item_by_id_v2(delete_id)

    # Проверка статус-кода
    assert response.status_code == expected_status

    response_json = response.json()

    # Проверка структуры
    assert "status" in response_json, "Нет поля status"
    assert "result" in response_json, "Нет поля result"

    result = response_json["result"]
    if isinstance(result, dict):
        assert any(key in result for key in ["message", "messages"]), \
            "Нет message/messages в result"