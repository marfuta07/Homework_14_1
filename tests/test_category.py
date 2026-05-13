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
