import requests

from config import (
    config,
)


def process_attributes():
    """Main функция обработки атрибутов."""

    trendyol_attributes = get_trendyol_attributes()
    processed_attributes, processed_attribute_values = unpack_attributes(trendyol_attributes)
    send_attributes(processed_attributes)
    send_attribute_values(processed_attribute_values)


def get_trendyol_attributes() -> list[dict]:
    """Возвращает атрибуты из Trendyol."""

    print('Getting attributes from trendyol...')
    category_attributes_url = config.get('trendyol', 'category_attributes_url').format('1058')
    category_attributes_json = requests.get(category_attributes_url).json()
    category_attributes = category_attributes_json.get('categoryAttributes')
    print('Attributes received!\n')

    return category_attributes


def format_attributes(attributes: list[dict]) -> tuple[list[dict], list[dict]]:
    """Форматирует атрибуты и их значений из внешней системы для создания в нашей."""

    print('Unpacking attributes and values...')
    unpacked_attributes, unpacked_attribute_values = unpack_attributes(attributes)
    print('Attributes and values are unpacked!')

    return unpacked_attributes, unpacked_attribute_values


def unpack_attributes(attributes: list[dict]) -> tuple[list[dict], list[dict]]:
    """Распаковывает записи атрибутов и их значений."""

    processed_attributes = []
    processed_attribute_values = []

    for attribute_info in attributes:
        raw_attribute = attribute_info.get('attribute')
        attribute = dict(
            external_id=raw_attribute.get('id'),
            name=raw_attribute.get('name'),
            is_required=raw_attribute.get('required'),
            provider_category=attribute_info.get('categoryId'),
        )
        processed_attributes.append(attribute)

        raw_attribute_values = attribute_info.get('attributeValues')

        attribute_values = []

        for raw_value in raw_attribute_values:
            attribute_values.append(
                dict(
                    value=raw_value.get('name'),
                    external_id=raw_value.get('id'),
                    provider_characteristic=raw_attribute.get('id'),
                )
            )

        processed_attribute_values.extend(attribute_values)

    return processed_attributes, processed_attribute_values


def send_attributes(attributes: list[dict]):
    """Отправляет записи атрибутов на сервер для их сохранения, либо обновления."""

    print('Loading attributes to the server...')

    characteristics_url = config.get('markets_bridge', 'provider_characteristics_url')

    for attribute in attributes:
        response = requests.post(characteristics_url, json=attribute)

        if response.status_code == 201:
            decoded_response = response.json()
            print(f'Attribute "{decoded_response.get("name")}" is created')

    print('Attributes loading finished!\n')


def send_attribute_values(attribute_values: list[dict]):
    """Отправляет записи значений атрибутов на сервер для их сохранения, либо обновления."""

    print('Loading attribute values to the server...')

    characteristic_values_url = config.get('markets_bridge', 'provider_characteristic_values_url')

    for value in attribute_values:
        response = requests.post(characteristic_values_url, json=value)

        if response.status_code == 201:
            decoded_response = response.json()
            print(f'Attribute value "{decoded_response.get("value")}" is created')

    print('Attribute values loading finished!\n')
