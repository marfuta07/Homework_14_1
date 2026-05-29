import pytest
from typing import List
from src.product import Product
from src.category import Category
from src.product import Smartphone, LawnGrass


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


def test_add_smartphone_to_category() -> None:
    """Проверка добавления смартфона (наследника Product) в категорию"""
    category = Category("Электроника", "Смартфоны и гаджеты")
    smartphone = Smartphone(
        name="iPhone",
        description="Флагманский смартфон",
        price=89999.0,
        quantity=5,
        efficiency="высокая",
        model="14 Pro",
        memory=256,
        color="серебристый"
    )

    category.add_product(smartphone)

    assert len(category.products) == 1
    assert category.products[0].name == "iPhone"
    assert Category.product_count == 1


def test_add_lawn_grass_to_category() -> None:
    """Проверка добавления газонной травы (наследника Product) в категорию"""
    category = Category("Сад и огород", "Товары для дачи")
    grass = LawnGrass(
        name="Газонная трава",
        description="Универсальная смесь",
        price=1200.0,
        quantity=10,
        country="Россия",
        germination_period=14,
        color="зелёный"
    )

    category.add_product(grass)

    assert len(category.products) == 1
    assert category.products[0].name == "Газонная трава"
    assert Category.product_count == 1


def test_init_with_smartphones_and_grass() -> None:
    """Проверка инициализации категории со смешанным списком наследников Product"""
    smartphone = Smartphone(
        name="Samsung",
        description="Android-смартфон",
        price=45000.0,
        quantity=8,
        efficiency="средняя",
        model="S23",
        memory=128,
        color="чёрный"
    )
    grass = LawnGrass(
        name="Спортивная трава",
        description="Износостойкая",
        price=1500.0,
        quantity=7,
        country="Германия",
        germination_period=21,
        color="тёмно-зелёный"
    )

    category = Category("Смешанная", "Электроника и товары для сада", [smartphone, grass])

    assert len(category.products) == 2
    assert isinstance(category.products[0], Smartphone)
    assert isinstance(category.products[1], LawnGrass)
    assert Category.product_count == 2


def test_add_invalid_types_raises_type_error() -> None:
    """Проверка, что разные некорректные типы вызывают TypeError"""
    category = Category("Тестовая", "Описание")

    invalid_objects = [
        "просто строка",
        42,
        3.14,
        [],
        {},
        None
    ]

    for obj in invalid_objects:
        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product(obj)  # type: ignore

    # Убеждаемся, что ни один объект не добавился
    assert len(category.products) == 0
    assert Category.product_count == 0


def test_init_with_invalid_object_in_products_list() -> None:
    """Проверка, что инициализация с некорректным объектом в списке вызывает TypeError"""
    valid_product = Product("Товар", "Описание", 100.0, 5)

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
        Category("Ошибка", "Описание", [valid_product, "не продукт"])  # type: ignore


def test_get_products_info_with_smartphone() -> None:
    """Проверка вывода информации для смартфона через get_products_info"""
    smartphone = Smartphone(
        name="Xiaomi",
        description="Бюджетный смартфон",
        price=19999.0,
        quantity=15,
        efficiency="средняя",
        model="Redmi 12",
        memory=64,
        color="синий"
    )
    category = Category("Смартфоны", "Мобильные устройства", [smartphone])
    products_info = category.get_products_info()

    expected = ["Xiaomi Redmi 12, синий, 64 ГБ, 19999.0 руб. Остаток: 15 шт."]
    assert products_info == expected


def test_get_products_info_with_lawn_grass() -> None:
    """Проверка вывода информации для газонной травы через get_products_info"""
    grass = LawnGrass(
        name="Партерная трава",
        description="Для декоративных газонов",
        price=1800.0,
        quantity=8,
        country="Франция",
        germination_period=18,
        color="изумрудно-зелёный"
    )
    category = Category("Газоны", "Семена трав", [grass])
    products_info = category.get_products_info()

    expected = ["Партерная трава, изумрудно-зелёный, произв. Франция, прорастание 18 дн., 1800.0 руб. Остаток: 8 шт."]
    assert products_info == expected


def test_category_str_with_smartphones_and_grass() -> None:
    """Проверка строкового представления категории со смешанными наследниками"""
    smartphone = Smartphone(
        name="Google Pixel",
        description="Чистый Android",
        price=65000.0,
        quantity=3,
        efficiency="высокая",
        model="7",
        memory=128,
        color="белый"
    )
    grass = LawnGrass(
        name="Теневыносливая трава",
        description="Для затенённых участков",
        price=2000.0,
        quantity=12,
        country="Канада",
        germination_period=25,
        color="светло-зелёный"
    )

    category = Category("Микс", "Разные товары", [smartphone, grass])
    result = str(category)

    # Общее количество: 3 + 12 = 15 шт.
    assert result == "Микс, количество продуктов: 15 шт."
