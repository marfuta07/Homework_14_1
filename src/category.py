from src.product import Product
from typing import List, Optional


class Category:
    """Класс для представления категорий"""

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        """Метод для инициализации экземпляра класса.

        При создании категории увеличивает счётчики категорий и товаров.
        """
        self.name = name
        self.description = description
        self.__products: List[Product] = []
        Category.category_count += 1

        # Добавляем продукты через add_product, чтобы соблюсти валидацию и корректный подсчёт
        if products is not None:
            for product in products:
                self.add_product(product)

    @property
    def products_list(self) -> List[Product]:
        """
        Геттер для доступа к списку товаров.
        Возвращает копию списка, чтобы предотвратить прямое изменение приватного атрибута.
        """
        return self.__products.copy()

    def add_product(self, product: Product) -> None:
        """
        Метод для добавления товара в категорию.

        Args:
            product: объект класса Product или его наследника, который нужно добавить в категорию

        Raises:
            TypeError: если переданный объект не является экземпляром Product или его наследником
        """
        if not isinstance(product, Product):
            raise TypeError(
                f"Можно добавлять только объекты класса Product и его наследников, "
                f"получен {type(product).__name__}"
            )
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """
        Геттер для получения информации о товарах в виде форматированных строк.

        Returns:
            Список строк с информацией о товарах категории
        """
        product_str = ""
        for product in self.__products:
            product_str += f"{str(product)}\n"
        return product_str

    def get_product_count(self) -> int:
        """
        Метод для получения количества товаров в данной категории.

        Returns:
            Количество товаров в категории
        """
        return len(self.__products)

    def middle_price(self) -> float:
        """
        Вычисляет среднюю цену товаров в категории.

        Returns:
            Средняя цена всех товаров в категории. Если товаров нет, возвращает 0.0.
        """
        try:
            total_price = sum(product.get_price() for product in self.__products)
            average_price = total_price / len(self.__products)
            return round(average_price, 2)
        except ZeroDivisionError:
            return 0.0

    def __str__(self) -> str:
        """Строковое представление категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."