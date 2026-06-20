import json


class MetricsRepository:
    """ "
    Класс для работы с метриками запросов,
    связанных с анализом тональности комментариев.
    """

    def __init__(self):
        self.file_path = "app/metrics.json"

    def get_metrics(self):
        """Загружает и возвращает текущие метрики из файла JSON."""
        with open(
            self.file_path,
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def collect_metrics(self, sentiment: str):
        """ "Обновляет метрики"""
        data = self.get_metrics()

        data["total_requests"] += 1
        data[sentiment] += 1

        with open(
            self.file_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
            )
