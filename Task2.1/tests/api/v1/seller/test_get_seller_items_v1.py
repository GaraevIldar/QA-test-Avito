import pytest
from utilities.data_provider import DataProvider

positive_data_provider = DataProvider("api\\v1\\seller\\","data_get_seller_items_positive_test_case.json")
negative_data_provider = DataProvider("api\\v1\\seller\\","data_get_seller_items_negative_test_case.json")
boundary_data_provider = DataProvider("api\\v1\\seller\\","data_get_seller_items_boundary_test_case.json")

def test_get_seller_items_positive(api_client, created_item): # Позитивный сценарий для получения списка объявлений для существующего пользователя

    seller_id = created_item["payload"]["sellerID"]

    response = api_client.get_all_items_by_seller_id_v1(seller_id)

    expected_code = positive_data_provider.get_test_case("TC-1_GetItemsExistingSeller")["expected_status_code"]

    # Проверка статус-кода
    assert response.status_code == expected_code

    response_json = response.json()

    # Проверка структуры
    assert isinstance(response_json, list), "Ответ не является списком"
    assert len(response_json) > 0, "Список объявлений пуст"

    # Поиск созданного объявления
    found_item = next(
        (item for item in response_json if item["id"] == created_item["id"]),
        None
    )
    assert found_item is not None, "Созданное объявление не найдено"

    # Проверка данных
    assert found_item["name"] == created_item["payload"]["name"]
    assert found_item["sellerId"] == seller_id

    # Проверка, что все объявления принадлежат seller
    assert all(item["sellerId"] == seller_id for item in response_json), "Не все объявления принадлежат указанному seller"

@pytest.mark.parametrize(
    "test_data",
    negative_data_provider.get_all_test_cases(),
    ids=negative_data_provider.get_test_case_ids()
)
def test_get_seller_items_negative(api_client, test_data): #Негативные тесты получения объявлений по sellerID

    seller_id = test_data["sellerID"]
    expected_status = test_data["expected_status_code"]

    response = api_client.get_all_items_by_seller_id_v1(seller_id)

    # Проверка статус-кода
    assert response.status_code == expected_status

    response_json = response.json()

    # Проверка структуры
    assert "status" in response_json, "Нет поля status"
    assert "result" in response_json, "Нет поля result"

    # Проверка result
    result = response_json["result"]

    if isinstance(result, dict):
        assert any(key in result for key in ["message", "messages"]), \
            "Нет message/messages в result"

@pytest.mark.parametrize(
    "test_data",
    boundary_data_provider.get_all_test_cases(),
    ids=boundary_data_provider.get_test_case_ids()
)
def test_get_seller_items_boundary(api_client, test_data): #Граничные тесты получения объявлений по sellerID

    seller_id = test_data["sellerID"]
    expected_status = test_data["expected_status_code"]

    response = api_client.get_all_items_by_seller_id_v1(seller_id)

    # Проверка статус-кода (поддержка диапазонов)
    assert response.status_code == expected_status

    response_json = response.json()

    if response.status_code == 200:
        # Проверка структуры
        assert isinstance(response_json, list), "Ответ не список"

        for item in response_json:
            assert "id" in item
            assert "sellerId" in item

    else:
        # Проверка ошибки
        assert "status" in response_json
        assert "result" in response_json

        result = response_json["result"]

        if isinstance(result, dict):
            assert any(key in result for key in ["message", "messages"]), \
                "Нет message/messages в result"