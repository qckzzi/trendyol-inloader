import requests

import config
from markets_bridge.types import (
    MBCategory,
)
from trendyol.types import (
    TrendyolCategory,
)


class Formatter:
    """Преобразователь данных для сервиса Markets-Bridge."""

    @classmethod
    def format_categories(cls, raw_categories: list[TrendyolCategory]) -> list[MBCategory]:
        """Форматирует категории Trendyol под шаблон MB категорий."""

        result = []

        for raw_category in raw_categories:
            category = cls._format_category(raw_category)
            result.append(category)

        return result

    @classmethod
    def _format_category(cls, category: TrendyolCategory) -> MBCategory:
        formatted_category = MBCategory(
            external_id=category.id,
            name=category.name,
            marketplace_id=config.marketplace_id,
        )

        return formatted_category


class Sender:
    """Отправитель данных в сервис Markets-Bridge."""

    @classmethod
    def send_categories(cls, categories: list[MBCategory]):
        cls._send_objects(
            categories,
            url=config.mb_categories_url,
            name='category',
            display_field='name',
        )

    @classmethod
    def _send_objects(cls, objects, **kwargs):
        for obj in objects:
            cls._send_object(obj, **kwargs)

    @staticmethod
    def _send_object(obj, url, name, display_field):
        response = requests.post(url, json=vars(obj))
        display_value = getattr(obj, display_field)

        if response.status_code == 201:
            print(f'The "{display_value}" {name} has been created.')
        elif response.status_code == 200:
            print(f'The "{display_value}" {name} already exists.')
        else:
            print(f'When creating the "{display_value}" {name}, the server returned an error.')
