from dataclasses import (
    dataclass,
)


@dataclass
class MBCategory:
    external_id: int
    name: str
    marketplace_id: int
