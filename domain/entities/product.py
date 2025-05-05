from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float

    def __post_init__(self):
        if not self.name:
            raise ValueError("Name cannot be empty")
        if not self.price:
            raise ValueError("Price cannot be empty")
