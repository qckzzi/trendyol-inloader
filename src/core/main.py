#!/usr/bin/env python
import requests

from core import (
    config,
)


def main():

    categories_url = config.get('trendyol', 'categories_url')
    categories = requests.get(categories_url).json().get('categories')
    processed_categories = unpack_categories(categories)
    send_categories(processed_categories)

    category_attributes_url = config.get('trendyol', 'category_attributes_url').format('5349')
    category_attributes_json = requests.get(category_attributes_url).json()
    category_attributes = category_attributes_json.get('categoryAttributes')
    processed_attributes, processed_attribute_values = unpack_attributes(category_attributes)
    send_attributes(processed_attributes)
    send_attribute_values(processed_attribute_values)


def unpack_categories(categories):
    result = []

    for category_data in categories:

        if category_data["subCategories"]:
            sub_categories = unpack_categories(category_data["subCategories"])
            result.extend(sub_categories)
        else:
            category = dict(
                external_id=category_data["id"],
                name=category_data["name"],
                provider_marketplace=config.get('markets_bridge', 'marketplace_id'),
            )
            result.append(category)

    return result


def send_categories(categories):
    categories_url = config.get('markets_bridge', 'provider_categories_url')
    only_external_id_records = requests.get(categories_url, params={'only_need_external_id': True}).json()
    existed_external_ids = set(record.get('external_id') for record in only_external_id_records)
    new_categories = list(filter(lambda category: category.get('external_id') not in existed_external_ids, categories))
    existed_categories = list(filter(lambda category: category.get('external_id') in existed_external_ids, categories))

    response_messages = {
        200: 'Запрос успешен',
        201: '{action} {len} записей',
        204: 'Сервер ничего не вернул',
    }

    post_response = requests.post(categories_url, json=new_categories)
    post_message = (
        response_messages.get(
            post_response.status_code,
            'Ошибка загрузки категорий',
        ).format(
            action='Создано',
            len=len(post_response.json()),
        )
    )
    print(post_message)

    # patch_response = requests.patch(categories_url, json=existed_categories)
    # patch_message = (
    #     response_messages.get(
    #         patch_response.status_code,
    #         'Ошибка обновления категорий',
    #     ).format(
    #         action='Обновлено',
    #         len=len(patch_response.json()),
    #     )
    # )
    # print(patch_message)


def unpack_attributes(attribute_datas: list[dict]) -> tuple[list[dict], list[dict]]:
    processed_attributes = []
    processed_attribute_values = []

    for attribute_data in attribute_datas:
        attribute = attribute_data.get('attribute')
        processed_attributes.append(
            dict(name=attribute.get('name'), external_id=attribute.get('id'), provider_category=['5349'])
        )

        attribute_values = attribute_data.get('attributeValues')
        attribute_values = [
            dict(value=value.get('name'), external_id=value.get('id'), provider_characteristic=attribute.get('id'))
            for value in attribute_values
        ]
        processed_attribute_values.extend(attribute_values)

    return processed_attributes, processed_attribute_values


def send_attributes(attributes: list[dict]):
    characteristics_url = config.get('markets_bridge', 'provider_characteristics_url')
    response = requests.post(characteristics_url, json=attributes)

    print(f'{"Загрузка характеристик в систему успешна" if response.status_code == 201 else "Ошибка загрузки характеристик"}')


def send_attribute_values(attribute_values: list[dict]):
    characteristic_values_url = config.get('markets_bridge', 'provider_characteristic_values_url')
    response = requests.post(characteristic_values_url, json=attribute_values)

    print(f'{"Загрузка значений характеристик в систему успешна" if response.status_code == 201 else "Ошибка загрузки значений характеристик"}')


if __name__ == '__main__':
    main()
