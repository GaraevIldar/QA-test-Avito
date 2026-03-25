import pytest
from utilities.data_provider import DataProvider

@pytest.fixture(scope="module")
def created_item(api_client):

    data_provider = DataProvider("api\\v1\\item\\","data_post_positive_test_case.json")
    test_case_data = data_provider.get_test_case("TC-1_ValidData")
    payload = test_case_data["payload"]

    response = api_client.create_item_v1(payload)
    assert response.status_code == 200, "Предусловие не выполнено: не удалось создать объявление"

    response_json = response.json()

    yield {"id": response_json.get("id"), "payload": payload}
