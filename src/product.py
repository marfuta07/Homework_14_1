class Product:
    """Класс для представления продуктов"""


    name: str
    description: str
    quantity: int
    _price: float  # Приватный атрибут цены

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Метод для инициализации экземпляра класса.
        Задаем значения атрибутам экземпляра."""
        self.name = name
        self.description = description
        # Используем сеттер для валидации при инициализации
        self.price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict) -> 'Product':
        """
        Создаёт новый объект Product из словаря с данными.

        Args:
            product_data: Словарь с ключами 'name', 'description', 'price', 'quantity'

        Returns:
            Новый экземпляр класса Product
        """
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    @property
    def price(self) -> float:
        """Геттер для получения цены продукта."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """
        Сеттер для установки цены с валидацией.

        Args:
            value: Новое значение цены

        Если цена равна или ниже нуля, выводится сообщение об ошибке
        и цена не изменяется.
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self._price = value
