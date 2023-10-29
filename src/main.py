#!/usr/bin/env python
from markets_bridge.services import (
    Formatter,
    Sender,
)
from trendyol.services import (
    Fetcher,
)


def main():
    fetcher = Fetcher()

    categories = fetcher.get_categories()
    formatted_categories = Formatter.format_categories(categories)
    Sender.send_categories(formatted_categories)


if __name__ == '__main__':
    main()
