import pytest
from src.product import Product
from src.category import Category

# Фикстуры для тестирования
@pytest.fixture
def sample_products():
    """Фикстура с набором тестовых продуктов"""
    return [
        Product("Смартфон", "Мощный смартфон", 49999.50, 10),
        Product("Ноутбук", "Игровой ноутбук", 79999.99, 5),
        Product("Наушники", "Беспроводные наушники", 4999.00, 20)
    ]

@pytest.fixture
def empty_product_list():
    """Фикстура с пустым списком продуктов"""
    return []

@pytest.fixture(autouse=True)
def reset_counters():
    """Автоматически сбрасывает счётчики перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0

# --- ТЕСТЫ ДЛЯ КЛАССА CATEGORY ---

def test_category_initialization_with_products(sample_products):
    """Проверка корректной инициализации категории с продуктами"""
    category = Category(
        name="Электроника",
        description="Электронные устройства",
        products=sample_products
    )

    assert category.name == "Электроника"
    assert category.description == "Электронные устройства"
    assert category.products == sample_products
    assert len(category.products) == 3

def test_category_initialization_empty_products(empty_product_list):
    """Проверка инициализации категории с пустым списком продуктов"""
    category = Category(
        name="Пустая категория",
        description="Категория без товаров",
        products=empty_product_list
    )

    assert category.name == "Пустая категория"
    assert category.description == "Категория без товаров"
    assert category.products == []
    assert len(category.products) == 0

def test_category_initialization_single_product():
    """Проверка инициализации категории с одним продуктом"""
    single_product = Product("Книга", "Художественная литература", 599.0, 25)
    category = Category("Книги", "Литературные произведения", [single_product])

    assert category.name == "Книги"
    assert len(category.products) == 1
    assert category.products[0].name == "Книга"

# --- ТЕСТЫ ДЛЯ ПОДСЧЁТА КОЛИЧЕСТВА КАТЕГОРИЙ ---

def test_category_count_increases_with_each_instance(sample_products):
    """Проверка увеличения счётчика категорий при создании новых экземпляров"""
    # Создаём первую категорию
    category1 = Category("Электроника", "Устройства", sample_products)
    assert Category.category_count == 1

    # Создаём вторую категорию
    category2 = Category("Книги", "Литература", [])
    assert Category.category_count == 2

    # Создаём третью категорию
    category3 = Category("Одежда", "Одежда и аксессуары", [])
    assert Category.category_count == 3

def test_multiple_categories_creation():
    """Проверка последовательного создания нескольких категорий"""
    products1 = [Product("Товар1", "Описание1", 100.0, 5)]
    products2 = [Product("Товар2", "Описание2", 200.0, 3)]

    category1 = Category("Категория1", "Описание1", products1)
    category2 = Category("Категория2", "Описание2", products2)

    assert Category.category_count == 2

# --- ТЕСТЫ ДЛЯ ПОДСЧЁТА КОЛИЧЕСТВА ПРОДУКТОВ ---

def test_product_count_correct_with_multiple_products(sample_products):
    """Проверка корректного подсчёта количества продуктов (несколько продуктов)"""
    category = Category("Электроника", "Устройства", sample_products)

    # Счётчик продуктов должен быть равен количеству переданных продуктов
    assert Category.product_count == len(sample_products)  # 3

def test_product_count_zero_with_empty_list(empty_product_list):
    """Проверка нулевого подсчёта продуктов для пустой категории"""
    category = Category("Пустая", "Без товаров", empty_product_list)

    assert Category.product_count == 0

def test_product_count_single_product():
    """Проверка подсчёта одного продукта"""
    product = Product("Товар", "Описание", 150.0, 7)
    category = Category("Одиночный", "Один товар", [product])

    assert Category.product_count == 1

def test_product_count_updates_with_last_category(sample_products):
    """Проверка того, что product_count отражает количество продуктов последней созданной категории"""
    # Первая категория с 3 продуктами
    category1 = Category("Первая", "Первая категория", sample_products)
    assert Category.product_count == 3  # Должно быть 3

    # Вторая категория с 1 продуктом
    single_product = Product("Один", "Один товар", 100.0, 1)
    category2 = Category("Вторая", "Вторая категория", [single_product])
    assert Category.product_count == 1  # Теперь должно быть 1 (перезаписалось)

    # Третья категория с 2 продуктами
    products_for_third = [
        Product("Товар1", "Описание1", 50.0, 2),
        Product("Товар2", "Описание2", 75.0, 3)
    ]
    category3 = Category("Третья", "Третья категория", products_for_third)
    assert Category.product_count == 2  # Теперь должно быть 2 (перезаписалось)

# --- КОМБИНИРОВАННЫЕ ТЕСТЫ ---

def test_category_counters_with_different_scenarios(sample_products, empty_product_list):
    """Комбинированный тест для разных сценариев использования"""
    # Сценарий 1: пустая категория
    category1 = Category("Пустая", "Без товаров", empty_product_list)
    assert Category.category_count == 1
    assert Category.product_count == 0

    # Сценарий 2: категория с несколькими продуктами
    category2 = Category("Электроника", "Устройства", sample_products)
    assert Category.category_count == 2
    assert Category.product_count == 3

    # Сценарий 3: категория с одним продуктом
    single_product = Product("Книга", "Литература", 599.0, 25)
    category3 = Category("Книги", "Литературные произведения", [single_product])
    assert Category.category_count == 3
    assert Category.product_count == 1

# --- ТЕСТЫ КРАЙНИХ СЛУЧАЕВ ---

def test_category_attribute_types(sample_products):
    """Проверка типов атрибутов категории после инициализации"""
    category = Category("Тест", "Тестовая категория", sample_products)

    assert isinstance(category.name, str)
    assert isinstance(category.description, str)
    assert isinstance(category.products, list)
    for product in category.products:
        assert isinstance(product, Product)
