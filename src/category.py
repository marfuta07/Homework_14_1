from src.product import Product
from typing import List, Optional


class Category:
    """Класс для представления категорий"""

    name: str
    description: str
    products: List[Product]
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        """Метод для инициализации экземпляра класса.
        Задаем значения атрибутам экземпляра."""
        self.name = name
        self.description = description
        self.products = products if products is not None else []
        Category.category_count += 1
        Category.product_count += len(self.products)
