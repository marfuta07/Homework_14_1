class Product:
    """Класс для представления продуктов"""

    name: str
    description: str
    _quantity: int  # Приватный атрибут количества
    _price: float  # Приватный атрибут цены

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра."""
        # Инициализируем приватные атрибуты ДО вызова сеттеров
        self._price = 0.0
        self._quantity = 0

        # Используем сеттеры для валидации
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        """Создаёт новый объект Product из словаря с данными."""
        required_keys = ["name", "description", "price", "quantity"]
        missing_keys = [key for key in required_keys if key not in product_data]
        if missing_keys:
            raise KeyError(f"Отсутствуют обязательные ключи в словаре: {missing_keys}")

        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    @property
    def price(self) -> float:
        """Геттер для получения цены продукта."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Сеттер для установки цены с валидацией."""
        if value < 0:
            print("Предупреждение: цена не может быть отрицательной. Значение не изменено.")
            return
        self._price = value

    @property
    def quantity(self) -> int:
        """Геттер для получения количества продукта."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Сеттер для установки количества с валидацией."""
        if value < 0:
            raise ValueError("Количество не может быть отрицательным")
        self._quantity = value

    @property
    def total_cost(self) -> float:
        """Свойство, возвращающее общую стоимость товара (цена × количество)."""
        return self._price * self._quantity

    def apply_discount(self, discount_percent: float) -> None:
        """
        Применяет скидку к цене продукта.

        Args:
            discount_percent: процент скидки (0–100)

        Raises:
            ValueError: если процент скидки вне диапазона 0–100%
        """
        if not (0 <= discount_percent <= 100):
            raise ValueError("Скидка должна быть в диапазоне 0–100%")

        discount_factor = 1 - (discount_percent / 100)
        self._price *= discount_factor
