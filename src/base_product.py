from abc import ABC, abstractmethod

class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.
    Определяет общую функциональность, которая должна быть у каждого продукта.
    """

    @abstractmethod
    def get_name(self) -> str:
        """Возвращает название продукта."""
        pass

    @abstractmethod
    def get_price(self) -> float:
        """Возвращает цену продукта."""
        pass

    @abstractmethod
    def get_quantity(self) -> int:
        """Возвращает количество продукта на складе."""
        pass

    @abstractmethod
    def apply_discount(self, discount_percent: float) -> None:
        """
        Применяет скидку к цене продукта.

        Args:
            discount_percent: процент скидки (должен быть в диапазоне от 0 до 100)
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Возвращает строковое представление продукта."""
        pass

    @abstractmethod
    def __add__(self, other: 'BaseProduct') -> float:
        """
        Складывает общую стоимость двух продуктов.

        Args:
            other: другой объект BaseProduct

        Returns:
            Сумма общей стоимости текущего и другого продукта
        """
        pass
