from src.product import Product
from typing import List, Optional


class Category:
    """Класс для представления категорий"""

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        """Метод для инициализации экземпляра класса."""
        self.name = name
        self.description = description
        self.__products: List[Product] = products if products is not None else []
        Category.category_count += 1
        Category.product_count += len(self.__products)

    @property
    def products(self) -> List[Product]:
        """
        Геттер для доступа к списку товаров.
        Возвращает копию списка, чтобы предотвратить прямое изменение приватного атрибута.
        """
        return self.__products.copy()

    def add_product(self, product: Product) -> None:
        """
        Метод для добавления товара в категорию.

        Args:
            product: объект класса Product, который нужно добавить в категорию
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(product)
        Category.product_count += 1

    def get_products_info(self) -> List[str]:
        """
        Геттер для получения информации о товарах в виде форматированных строк.

        Формат каждой строки:
        "Название продукта, 80 руб. Остаток: 15 шт."

        Returns:
            Список строк с информацией о товарах категории
        """
        products_info = []
        for product in self.__products:
            info = f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            products_info.append(info)
        return products_info

    def get_product_count(self) -> int:
        """
        Метод для получения количества товаров в данной категории.

        Returns:
            Количество товаров в категории
        """
        return len(self.__products)
