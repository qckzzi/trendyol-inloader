from dataclasses import (
    dataclass,
)


@dataclass
class TrendyolCategory:
    """DTO категорий Trendyol."""

    id: int
    name: str
