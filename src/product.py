from src.base_product import BaseProduct
from typing import Dict
from src.miksin import LoggingMixin


class Product(LoggingMixin, BaseProduct):
    """Класс для представления продуктов"""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализирует экземпляр класса Product."""
        self.name = name
        self.description = description
        self._price = 0.0
        self._quantity = 0

        # Используем сеттеры для валидации
        self.price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: Dict[str, any]) -> "Product":
        """Создаёт новый объект Product из словаря с данными."""
        required_keys = ["name", "description", "price", "quantity"]
        missing_keys = [key for key in required_keys if key not in product_data]
        if missing_keys:
            raise KeyError(f"Отсутствуют обязательные ключи: {missing_keys}. " f"Ожидаемые ключи: {required_keys}")
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    # Реализуем абстрактные методы
    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self._price

    def get_quantity(self) -> int:
        return self._quantity

    @property
    def price(self) -> float:
        """Возвращает цену продукта."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Устанавливает цену продукта."""
        if value <= 0:
            raise ValueError("Цена должна быть положительной")
        self._price = value  # Записываем в приватный атрибут

    @property
    def quantity(self) -> int:
        """Возвращает количество продукта на складе."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Устанавливает количество продукта."""
        if value < 0:
            raise ValueError("Количество не может быть отрицательным")
        self._quantity = value  # Записываем в приватный атрибут

    @property
    def total_cost(self) -> float:
        """Вычисляет общую стоимость товара (цена × количество)."""
        return self._price * self._quantity

    def apply_discount(self, discount_percent: float) -> None:
        """Применяет скидку к цене продукта."""
        if not (0 <= discount_percent <= 100):
            raise ValueError("Скидка должна быть в диапазоне 0–100%")

        discount_factor = 1 - (discount_percent / 100)
        self._price = round(self._price * discount_factor, 2)

    def __str__(self) -> str:
        """Возвращает строковое представление продукта."""
        return f"{self.name}, {self._price} руб. Остаток: {self._quantity} шт."

    def __add__(self, other: "BaseProduct") -> float:
        """Складывает общую стоимость двух продуктов."""
        if not isinstance(other, BaseProduct):
            return NotImplemented
        return self.total_cost + other.total_cost

    class Smartphone(LoggingMixin, Product):
        """Класс для представления смартфонов, наследник Product."""

        def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            efficiency: str,
            model: str,
            memory: int,
            color: str,
        ) -> None:
            super().__init__(name, description, price, quantity)
            if memory <= 0:
                raise ValueError("Объём памяти должен быть положительным")
            self.efficiency = efficiency
            self.model = model
            self.memory = memory
            self.color = color

    def __str__(self) -> str:
        """Строковое представление смартфона."""
        return (
            f"{self.name} {self.model}, {self.memory} ГБ, "
            f"{self.color}, {self._price} руб. Остаток: {self._quantity} шт."
        )

    class LawnGrass(LoggingMixin, Product):
        """Класс для представления газонной травы, наследник Product."""

        def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            country: str,
            germination_period: int,
            color: str,
        ) -> None:
            super().__init__(name, description, price, quantity)
            if germination_period <= 0:
                raise ValueError("Срок прорастания должен быть положительным")
            self.country = country
            self.germination_period = germination_period
            self.color = color

    def __str__(self) -> str:
        """Строковое представление газонной травы."""
        return (
            f"{self.name}, {self.color}, из {self.country}, "
            f"прорастание {self.germination_period} дн., "
            f"{self._price} руб. Остаток: {self._quantity} шт."
        )
