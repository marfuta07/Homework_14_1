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
    # Проверяем количество товаров вместо сравнения списков
    assert category.get_product_count() == len(sample_products)
    assert Category.product_count == len(sample_products)


def test_category_initialization_empty_products(empty_product_list: List[Product]) -> None:
    """Проверка инициализации категории с пустым списком продуктов"""
    category = Category(name="Пустая категория", description="Категория без товаров", products=empty_product_list)

    assert category.name == "Пустая категория"
    assert category.description == "Категория без товаров"
    # Проверяем, что в категории нет товаров
    assert category.get_product_count() == 0
    assert Category.product_count == 0


def test_category_initialization_single_product() -> None:
    """Проверка инициализации категории с одним продуктом"""
    single_product: Product = Product("Книга", "Художественная литература", 599.0, 25)
    category = Category("Книги", "Литературные произведения", [single_product])

    assert category.name == "Книги"
    assert category.get_product_count() == 1
    # Используем строковое представление категории (__str__) для проверки общего количества
    total_quantity = single_product.quantity
    assert str(category) == f"Книги, количество продуктов: {total_quantity} шт."
    # Для проверки наличия товара ищем его имя в строковом представлении products (это строка!)
    assert "Книга" in category.products


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
    # Проверяем, что products — это строка (а не список)
    assert isinstance(category.products, str)
    # Чтобы проверить, что товары действительно есть, используем get_product_count
    assert category.get_product_count() == len(sample_products)
    # Если нужно убедиться, что в строке-представлении есть имена товаров, ищем подстроки
    for product in sample_products:
        assert product.name in category.products


# --- ТЕСТЫ ДЛЯ МЕТОДА add_product ---


def test_add_product_to_category(sample_products: List[Product]) -> None:
    """Проверка добавления продукта в категорию"""
    category = Category("Электроника", "Устройства", sample_products[:2])  # Берём 2 продукта из 3
    new_product = Product("Планшет", "10-дюймовый планшет", 29999.00, 8)

    category.add_product(new_product)

    # Проверяем, что продукт добавился — используем get_product_count()
    assert category.get_product_count() == 3
    # Проверяем наличие имени нового продукта в строковом представлении
    assert "Планшет" in category.products
    # Проверяем обновление счётчика
    assert Category.product_count == 3


def test_add_multiple_products_to_category() -> None:
    """Проверка последовательного добавления нескольких продуктов"""
    category = Category("Одежда", "Повседневная одежда", [])
    product1 = Product("Футболка", "Хлопковая футболка", 999.00, 50)
    product2 = Product("Джинсы", "Джинсы прямого кроя", 2999.00, 20)

    category.add_product(product1)
    category.add_product(product2)

    assert category.get_product_count() == 2
    # Проверяем наличие названий товаров в строке products
    assert "Футболка" in category.products
    assert "Джинсы" in category.products
    assert Category.product_count == 2


def test_add_product_invalid_type(sample_products: List[Product]) -> None:
    """Проверка обработки попытки добавления объекта неверного типа"""
    category = Category("Электроника", "Устройства", sample_products)

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
        category.add_product("Не продукт")  # type: ignore

    # Убеждаемся, что количество продуктов не изменилось
    assert category.get_product_count() == 3
    # Счётчик тоже не изменился
    assert Category.product_count == 3


# --- ТЕСТЫ ДЛЯ МЕТОДА get_products_info ---


def test_products_string_contains_product_info(sample_products: List[Product]) -> None:
    """Проверка, что строковое представление продуктов содержит корректную информацию"""
    category = Category("Электроника", "Устройства", sample_products)
    products_str = category.products

    # Проверяем наличие ключевых данных каждого продукта в строке
    assert "Смартфон" in products_str
    assert "49999.5" in products_str  # цена
    assert "10" in products_str  # количество
    assert "Ноутбук" in products_str
    assert "79999.99" in products_str
    assert "5" in products_str
    assert "Наушники" in products_str
    assert "4999.0" in products_str
    assert "20" in products_str


def test_products_string_empty_category() -> None:
    """Проверка строкового представления пустой категории"""
    category = Category("Пустая", "Без товаров", [])
    products_str = category.products
    assert products_str == ""


def test_products_string_single_product() -> None:
    """Проверка строкового представления категории с одним продуктом"""
    product = Product("Книга", "Художественная литература", 599.0, 25)
    category = Category("Книги", "Литературные произведения", [product])
    products_str = category.products

    assert "Книга" in products_str
    assert "599.0" in products_str
    assert "25" in products_str


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
        Product("Смартфон", "Мощный смартфон", 49999.50, 1),
        Product("Ноутбук", "Игровой ноутбук", 79999.99, 1),
    ]
    category = Category("Склад", "Товары на складе", products)
    result = str(category)
    assert result == "Склад, количество продуктов: 2 шт."



# --Тесты наследования--


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
        color="серебристый",
    )

    category.add_product(smartphone)

    assert category.get_product_count() == 1
    assert "iPhone" in category.products
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
        color="зелёный",
    )

    category.add_product(grass)

    assert category.get_product_count() == 1
    assert "Газонная трава" in category.products
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
        color="чёрный",
    )
    grass = LawnGrass(
        name="Спортивная трава",
        description="Износостойкая",
        price=1500.0,
        quantity=7,
        country="Германия",
        germination_period=21,
        color="тёмно-зелёный",
    )

    category = Category("Смешанная", "Электроника и товары для сада", [smartphone, grass])

    assert category.get_product_count() == 2
    assert "Samsung" in category.products
    assert "Спортивная трава" in category.products
    assert Category.product_count == 2


def test_add_invalid_types_raises_type_error() -> None:
    """Проверка, что разные некорректные типы вызывают TypeError"""
    category = Category("Тестовая", "Описание")

    invalid_objects = ["просто строка", 42, 3.14, [], {}, None]

    for obj in invalid_objects:
        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product(obj)  # type: ignore

    # Убеждаемся, что ни один объект не добавился
    assert category.get_product_count() == 0
    assert Category.product_count == 0


def test_init_with_invalid_object_in_products_list() -> None:
    """Проверка, что инициализация с некорректным объектом в списке вызывает TypeError"""
    valid_product = Product("Товар", "Описание", 100.0, 5)

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
        Category("Ошибка", "Описание", [valid_product, "не продукт"])  # type: ignore

#--Тесты по теме исключения--


class TestCategory:
    """Тесты для класса Category"""

    def test_create_category_with_products(self):
        """Тест: создание категории с товарами увеличивает счётчики"""
        product1 = Product("Товар 1", "Описание 1", 100.0, 2)
        product2 = Product("Товар 2", "Описание 2", 200.0, 3)

        category = Category("Тесты", "Категория для тестирования", [product1, product2])

        assert category.name == "Тесты"
        assert category.description == "Категория для тестирования"
        assert len(category.products_list) == 2
        assert Category.category_count >= 1
        assert Category.product_count >= 2


    def test_create_empty_category(self):
        """Тест: создание пустой категории работает корректно"""
        category = Category("Пустая", "Пустая категория", [])
        assert category.get_product_count() == 0
        assert len(category.products_list) == 0


    def test_add_product_to_category(self):
        """Тест: добавление товара в категорию работает корректно"""
        category = Category("Тесты", "Категория для тестирования")
        product = Product("Новый товар", "Описание", 500.0, 4)

        category.add_product(product)

        assert len(category.products_list) == 1
        assert product in category.products_list
        assert Category.product_count >= 1


    def test_add_invalid_object_to_category_raises_type_error(self):
        """Тест: попытка добавить не-продукт вызывает TypeError"""
        category = Category("Тесты", "Категория для тестирования")

        with pytest.raises(TypeError):
            category.add_product("Не товар")

    def test_middle_price_with_products(self):
        """Тест: middle_price корректно вычисляет среднюю цену для категории с товарами"""
        product1 = Product("Товар 1", "Описание 1", 100.0, 2)
        product2 = Product("Товар 2", "Описание 2", 200.0, 3)
        product3 = Product("Товар 3", "Описание 3", 300.0, 1)


        category = Category("Тесты", "Категория с товарами", [product1, product2, product3])
        average_price = category.middle_price()

        expected_average = (100 + 200 + 300) / 3
        assert average_price == round(expected_average, 2)


    def test_middle_price_with_empty_category_returns_zero(self):
        """Тест: middle_price возвращает 0.0 для пустой категории"""
        category = Category("Пустая", "Пустая категория", [])
        average_price = category.middle_price()
        assert average_price == 0.0

    def test_products_property_format(self):
        """Тест: свойство products возвращает корректно отформатированную строку"""
        product1 = Product("Товар 1", "Описание 1", 100.0, 2)
        product2 = Product("Товар 2", "Описание 2", 200.0, 3)


        category = Category("Тесты", "Категория для тестирования", [product1, product2])
        products_str = category.products


        assert "Товар 1, 100.0 руб. Остаток: 2 шт." in products_str
        assert "Товар 2, 200.0 руб. Остаток: 3 шт." in products_str


    def test_get_product_count(self):
        """Тест: get_product_count возвращает корректное количество товаров"""
        product1 = Product("Товар 1", "Описание 1", 100.0, 2)
        product2 = Product("Товар 2", "Описание 2", 200.0, 3)

        category = Category("Тесты", "Категория для тестирования", [product1, product2])
        assert category.get_product_count() == 2
