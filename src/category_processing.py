import requests

from config import (
    config,
)


def process_categories():
    """Main функция обработки категорий."""

    trendyol_categories = get_trendyol_categories()
    processed_categories = format_categories(trendyol_categories)
    send_categories(processed_categories)


def get_trendyol_categories() -> list[dict]:
    """Возвращает категории, полученные от Trendyol."""

    print('Getting categories from trendyol...')
    categories_url = config.get('trendyol', 'categories_url')
    categories = requests.get(categories_url).json().get('categories')
    print('Categories received!\n')

    return categories


def format_categories(categories):
    """Форматирует категории из внешней системы для создания в нашей."""

    print('Unpacking categories...')
    unpacked_categories = unpack_categories(categories)
    print('Categories are unpacked!\n')

    return unpacked_categories


def unpack_categories(categories: list[dict]) -> list[dict]:
    """Распаковывает древовидную структуру категорий."""

    result = []

    for category_data in categories:
        if category_data.get('subCategories'):
            sub_categories = unpack_categories(category_data.get('subCategories'))
            result.extend(sub_categories)
        else:
            category = dict(
                external_id=category_data.get('id'),
                name=category_data.get('name'),
                marketplace=config.get('markets_bridge', 'marketplace_id'),
            )
            result.append(category)

    return result


def send_categories(categories: list[dict]):
    """Отправляет записи категорий на сервер для их сохранения, либо обновления."""

    print('Loading categories to the server...')

    categories_url = config.get('markets_bridge', 'provider_categories_url')

    for category in categories:
        response = requests.post(categories_url, json=category)

        if response.status_code == 201:
            decoded_response = response.json()
            print(f'Category "{decoded_response.get("name")}" is created')

    print('Categories loading finished!\n')
