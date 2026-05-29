class Product:
    """Класс для представления продуктов"""

    name: str
    description: str
    _quantity: int  # Приватный атрибут количества
    _price: float  # Приватный атрибут цены

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализирует экземпляр класса Product.

        Args:
            name: название продукта
            description: описание продукта
            price: цена продукта (должна быть положительной)
            quantity: количество продукта на складе (не может быть отрицательным)
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        """Создаёт новый объект Product из словаря с данными.

        Args:
            product_data: словарь с ключами 'name', 'description', 'price', 'quantity'

        Returns:
            Новый экземпляр Product

        Raises:
            KeyError: если в словаре отсутствуют обязательные ключи
        """
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
        """Возвращает цену продукта."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Устанавливает цену продукта.

        Args:
            value: новая цена

        Raises:
            ValueError: если цена не положительная
        """
        if value <= 0:
            raise ValueError("Цена должна быть положительной")
        self._price = value

    @property
    def quantity(self) -> int:
        """Возвращает количество продукта на складе."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Устанавливает количество продукта.

        Args:
            value: новое количество

        Raises:
            ValueError: если количество отрицательное
        """
        if value < 0:
            raise ValueError("Количество не может быть отрицательным")
        self._quantity = value

    @property
    def total_cost(self) -> float:
        """Вычисляет общую стоимость товара (цена × количество)."""
        return self._price * self._quantity

    def apply_discount(self, discount_percent: float) -> None:
        """Применяет скидку к цене продукта.

        Args:
            discount_percent: процент скидки (должен быть в диапазоне от 0 до 100)

        Raises:
            ValueError: если процент скидки вне допустимого диапазона
        """
        if not (0 <= discount_percent <= 100):
            raise ValueError("Скидка должна быть в диапазоне 0–100%")

        discount_factor = 1 - (discount_percent / 100)
        self._price *= discount_factor

    def __str__(self) -> str:
        """Возвращает строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Складывает общую стоимость двух продуктов одного класса.
        Args:
            other: другой объект Product
        Returns:
            Сумма общей стоимости текущего и другого продукта
        Raises:
            TypeError: если другой объект не относится к тому же классу, что и текущий
        """
        if not isinstance(other, Product):
            return NotImplemented
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return self.total_cost + other.total_cost


class Smartphone(Product):
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
        """
        Инициализирует экземпляр класса Smartphone.

        Args:
            name: название продукта
            description: описание продукта
            price: цена продукта
            quantity: количество на складе
            efficiency: производительность (например, "высокая", "средняя")
            model: модель смартфона
            memory: объем встроенной памяти в ГБ
            color: цвет смартфона
        """
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        """Строковое представление смартфона."""
        return (
            f"{self.name} {self.model}, {self.color}, "
            f"{self.memory} ГБ, {self.price} руб. Остаток: {self.quantity} шт."
        )


class LawnGrass(Product):
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
        """
        Инициализирует экземпляр класса LawnGrass.

        Args:
            name: название продукта
            description: описание продукта
            price: цена продукта
            quantity: количество на складе
            country: страна-производитель
            germination_period: срок прорастания в днях
            color: цвет травы
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        """Строковое представление газонной травы."""
        return (
            f"{self.name}, {self.color}, произв. {self.country}, "
            f"прорастание {self.germination_period} дн., "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )
