import os

from dotenv import (
    load_dotenv,
)


load_dotenv()


# Markets-Bridge
mb_domain = os.getenv('MB_DOMAIN')

if not mb_domain:
    raise ValueError('Не задан домен Markets-Bridge.')

mb_categories_url = f'{mb_domain}api/v1/provider/categories/'
marketplace_id = int(os.getenv('TRENDYOL_ID', default=0))

if not marketplace_id:
    raise ValueError('Не задан ID записи маркетплейса "Trendyol", находящейся в БД Markets-Bridge.')


# Trendyol
trendyol_domain = 'https://api.trendyol.com/'
trendyol_categories_url = f'{trendyol_domain}sapigw-product/product-categories'

