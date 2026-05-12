from src.product import Product
class Category:
    """Класс для представления категорий"""
    name:str
    description:str
    products: list[Product]
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        """Метод для инициализации экземпляра класса.
        Задаем значения атрибутам экземпляра."""
        self.name = name
        self.description = description
        self.products = products
        Category.category_count += 1
        Category.product_count = len(products) if products else 0


