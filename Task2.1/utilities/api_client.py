import requests

class ApiClient: # Класс клиент для работы с api
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def get_item_by_id_v1(self, id:str): # Функция для получения объявления по идентификатору(GET)
        url = f'{self.base_url}/api/1/item/{id}'
        return requests.get(url, headers=self.headers)

    def create_item_v1(self, item: dict):
        url = f'{self.base_url}/api/1/item'
        return requests.post(url, json=item, headers=self.headers)

    def get_statistic_by_id_v1(self, id:str): # Функция для получения статистики объявления по идентификатору(GET,v1)
        url = f'{self.base_url}/api/1/statistic/{id}'
        return requests.get(url, headers=self.headers)

    def get_all_items_by_seller_id_v1(self, seller_id:int): # Функция для получения всех объявлений по идентификатору продавца(GET)
        url = f'{self.base_url}/api/1/{seller_id}/item'
        return requests.get(url, headers=self.headers)

    def delete_item_by_id_v2(self, id:str): # Функция удаления объявления по идентификатору(DELETE)
        url = f'{self.base_url}/api/2/item/{id}'
        return requests.delete(url, headers=self.headers)

    def get_statistic_by_id_v2(self, item_id: str): # Функция для получения статистики объявления по идентификатору(GET,v2)
        url = f"{self.base_url}/api/2/statistic/{item_id}"
        return requests.get(url, headers=self.headers)






