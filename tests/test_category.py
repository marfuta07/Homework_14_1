import pytest
from typing import List
from src.product import Product
from src.category import Category


# Фикстуры для тестирования
@pytest.fixture
def sample_products() -> List[Product]:
    """Фикстура с набором тестовых продуктов"""
    return [
        Product("Смартфон", "Мощный смартфон", 49999.50, 10),
        Product("Ноутбук", "Игровой ноутбук", 79999.99, 5),
        Product("Наушники", "Беспроводные наушники", 4999.00, 20),
    ]


@pytest.fixture
def empty_product_list() -> List[Product]:
    """Фикстура с пустым списком продуктов"""
    return []


@pytest.fixture(autouse=True)
def reset_counters() -> None:
    """Автоматически сбрасывает счётчики перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0


# --- ТЕСТЫ ДЛЯ КЛАССА CATEGORY ---


def test_category_initialization_with_products(sample_products: List[Product]) -> None:
    """Проверка корректной инициализации категории с продуктами"""
    category = Category(name="Электроника", description="Электронные устройства", products=sample_products)

    assert category.name == "Электроника"
    assert category.description == "Электронные устройства"
    assert category.products == sample_products
    assert len(category.products) == 3


def test_category_initialization_empty_products(empty_product_list: List[Product]) -> None:
    """Проверка инициализации категории с пустым списком продуктов"""
    category = Category(name="Пустая категория", description="Категория без товаров", products=empty_product_list)

    assert category.name == "Пустая категория"
    assert category.description == "Категория без товаров"
    assert category.products == []
    assert len(category.products) == 0


def test_category_initialization_single_product() -> None:
    """Проверка инициализации категории с одним продуктом"""
    single_product: Product = Product("Книга", "Художественная литература", 599.0, 25)
    category = Category("Книги", "Литературные произведения", [single_product])

    assert category.name == "Книги"
    assert len(category.products) == 1
    assert category.products[0].name == "Книга"


# --- ТЕСТЫ ДЛЯ ПОДСЧЁТА КОЛИЧЕСТВА КАТЕГОРИЙ ---


def test_category_count_increases_with_each_instance(sample_products: List[Product]) -> None:
    Category("Электроника", "Устройства", sample_products)
    assert Category.category_count == 1

    Category("Книги", "Литература", [])
    assert Category.category_count == 2

    Category("Одежда", "Одежда и аксессуары", [])
    assert Category.category_count == 3


def test_multiple_categories_creation() -> None:
    products1: List[Product] = [Product("Товар1", "Описание1", 100.0, 5)]
    products2: List[Product] = [Product("Товар2", "Описание2", 200.0, 3)]

    Category("Категория1", "Описание1", products1)
    Category("Категория2", "Описание2", products2)
    assert Category.category_count == 2


# --- ТЕСТЫ ДЛЯ ПОДСЧЁТА КОЛИЧЕСТВА ПРОДУКТОВ ---


def test_product_count_zero_with_empty_list(empty_product_list: List[Product]) -> None:
    """Проверка нулевого подсчёта продуктов для пустой категории"""
    Category("Пустая", "Без товаров", empty_product_list)
    assert Category.product_count == 0


def test_product_count_single_product() -> None:
    """Проверка подсчёта одного продукта"""
    product: Product = Product("Товар", "Описание", 150.0, 7)
    Category("Одиночный", "Один товар", [product])
    assert Category.product_count == 1


# --- ТЕСТЫ КРАЙНИХ СЛУЧАЕВ ---
def test_category_attribute_types(sample_products: List[Product]) -> None:
    """Проверка типов атрибутов категории после инициализации"""
    category = Category("Тест", "Тестовая категория", sample_products)

    assert isinstance(category.name, str)
    assert isinstance(category.description, str)
    assert isinstance(category.products, list)
    for product in category.products:
        assert isinstance(product, Product)


# --- ТЕСТЫ ДЛЯ МЕТОДА add_product ---


def test_add_product_to_category(sample_products: List[Product]) -> None:
    """Проверка добавления продукта в категорию"""
    category = Category("Электроника", "Устройства", sample_products[:2])  # Берём 2 продукта из 3
    new_product = Product("Планшет", "10-дюймовый планшет", 29999.00, 8)

    category.add_product(new_product)

    # Проверяем, что продукт добавился
    assert len(category.products) == 3
    assert category.products[-1].name == "Планшет"
    # Проверяем обновление счётчика
    assert Category.product_count == 3


def test_add_multiple_products_to_category() -> None:
    """Проверка последовательного добавления нескольких продуктов"""
    category = Category("Одежда", "Повседневная одежда", [])
    product1 = Product("Футболка", "Хлопковая футболка", 999.00, 50)
    product2 = Product("Джинсы", "Джинсы прямого кроя", 2999.00, 20)

    category.add_product(product1)
    category.add_product(product2)

    assert len(category.products) == 2
    assert category.products[0].name == "Футболка"
    assert category.products[1].name == "Джинсы"
    assert Category.product_count == 2


def test_add_product_invalid_type(sample_products: List[Product]) -> None:
    """Проверка обработки попытки добавления объекта неверного типа"""
    category = Category("Электроника", "Устройства", sample_products)

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
        category.add_product("Не продукт")  # type: ignore

    # Убеждаемся, что список продуктов не изменился
    assert len(category.products) == 3
    # Счётчик тоже не изменился
    assert Category.product_count == 3


# --- ТЕСТЫ ДЛЯ МЕТОДА get_products_info ---


def test_get_products_info_format(sample_products: List[Product]) -> None:
    """Проверка формата вывода информации о продуктах"""
    category = Category("Электроника", "Устройства", sample_products)
    products_info = category.get_products_info()

    expected_format = [
        "Смартфон, 49999.5 руб. Остаток: 10 шт.",
        "Ноутбук, 79999.99 руб. Остаток: 5 шт.",
        "Наушники, 4999.0 руб. Остаток: 20 шт.",
    ]

    assert products_info == expected_format


def test_get_products_info_empty_category() -> None:
    """Проверка вывода информации для пустой категории"""
    category = Category("Пустая", "Без товаров", [])
    products_info = category.get_products_info()

    assert products_info == []


def test_get_products_info_single_product() -> None:
    """Проверка вывода информации для категории с одним продуктом"""
    product = Product("Книга", "Художественная литература", 599.0, 25)
    category = Category("Книги", "Литературные произведения", [product])
    products_info = category.get_products_info()

    expected = ["Книга, 599.0 руб. Остаток: 25 шт."]
    assert products_info == expected


# --- ТЕСТЫ ДЛЯ СТРОКОВОГО ПРЕДСТАВЛЕНИЯ CATEGORY (__str__) ---


def test_category_str_representation(sample_products: List[Product]) -> None:
    """Проверка строкового представления категории с несколькими продуктами"""
    category = Category("Электроника", "Электронные устройства", sample_products)
    result = str(category)
    # Общее количество товаров: 10 + 5 + 20 = 35
    assert result == "Электроника, количество продуктов: 35 шт."


def test_category_str_empty_products() -> None:
    """Проверка строкового представления пустой категории"""
    category = Category("Пустая", "Без товаров", [])
    result = str(category)
    assert result == "Пустая, количество продуктов: 0 шт."


def test_category_str_single_product() -> None:
    """Проверка строкового представления категории с одним продуктом"""
    product = Product("Книга", "Художественная литература", 599.0, 25)
    category = Category("Книги", "Литературные произведения", [product])
    result = str(category)
    assert result == "Книги, количество продуктов: 25 шт."


def test_category_str_after_adding_product(sample_products: List[Product]) -> None:
    """Проверка, что строковое представление корректно обновляется после добавления товара"""
    # Берём только два продукта из трёх
    category = Category("Электроника", "Устройства", sample_products[:2])
    # Изначально: 10 + 5 = 15 шт.
    assert str(category) == "Электроника, количество продуктов: 15 шт."

    # Добавляем третий продукт с количеством 20
    category.add_product(sample_products[2])
    # Теперь общее количество: 10 + 5 + 20 = 35 шт.
    assert str(category) == "Электроника, количество продуктов: 35 шт."


def test_category_str_with_zero_quantity_products() -> None:
    """Проверка строкового представления, когда у товаров нулевое количество"""
    products = [
        Product("Смартфон", "Мощный смартфон", 49999.50, 0),
        Product("Ноутбук", "Игровой ноутбук", 79999.99, 0),
    ]
    category = Category("Склад", "Товары на складе", products)
    result = str(category)
    assert result == "Склад, количество продуктов: 0 шт."
