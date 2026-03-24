import json
from pathlib import Path

class DataProvider: #Класс для работы с json файлами

    def __init__(self, div: str, filename: str): # Загрузка данных из JSON файла.
        base_path = Path(__file__).parent.parent
        file_path = base_path / "test_data" / div / filename
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def get_test_case(self, case_name: str): # Функция для получения данных для конкретного тест-кейса
        return self.data.get(case_name)

    def get_all_test_cases(self): # Функция для получения данных всех тест-кейсов
        return list(self.data.values())

    def get_test_case_ids(self): # Функция для получения списка ключей всех тест-кейсов
        return list(self.data.keys())