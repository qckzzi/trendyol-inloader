import requests

import config
from trendyol.types import (
    TrendyolCategory,
)


class Fetcher:
    """Сборщик данных Trendyol.

    Собирает и хранит в себе атрибуты внешней системы. Возвращает их в таком виде, в каком и получил.
    """

    def __init__(self):
        self._categories: list[TrendyolCategory] = []

        self._fetch_all()

    def _fetch_all(self):
        self._fetch_categories()

    def _fetch_categories(self):
        self._categories = self._get_categories_from_trendyol()

    def _get_categories_from_trendyol(self) -> list[TrendyolCategory]:
        """Возвращает список DTO категорий Trendyol."""

        response = self._send_category_request()
        raw_categories = response.get('categories')

        categories = self._unpack_categories(raw_categories)

        return categories

    def _send_category_request(self) -> dict:
        """Возвращает ответ на запрос получения категорий."""

        try:
            response = requests.get(config.trendyol_categories_url).json()
        except (requests.ConnectionError, requests.ConnectTimeout):
            response = self._send_category_request()

        return response

    def _unpack_categories(self, raw_categories: list[dict]) -> list[TrendyolCategory]:
        """Распаковка дерева категорий и десериализация в DTO."""

        result = []

        for raw_category in raw_categories:
            if raw_category.get('subCategories'):
                sub_categories = self._unpack_categories(raw_category.get('subCategories'))
                result.extend(sub_categories)
            else:
                category = TrendyolCategory(
                    id=raw_category.get('id'),
                    name=raw_category.get('name'),
                )
                result.append(category)

        return result

    def get_categories(self) -> list[TrendyolCategory]:
        if not self._categories:
            self._fetch_categories()

        return self._categories
