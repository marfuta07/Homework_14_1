from src.product import Product
import pytest
from typing import List, Generator, Any

# Фикстура на уровне функции — создаёт один продукт для теста
@pytest.fixture
def sample_product() -> Product:
    return Product(
        name="Смартфон",
        description="Новый смартфон 2024",
        price=49999.50,
        quantity=10
    )

# Фикстура с параметрами — позволяет создавать разные продукты
@pytest.fixture(params=[
    ("Книга", "Художественная литература", 599.0, 25),
    ("Кофе", "Арабика свежеобжаренная", 1299.90, 15),
    ("Ручка", "Шариковая синяя", 49.99, 100)
])
def product_with_params(request: Any) -> Product:
    name, description, price, quantity = request.param
    return Product(name, description, price, quantity)

# Фикстура для набора продуктов
@pytest.fixture
def product_list() -> List[Product]:
    return [
        Product("Книга", "Художественная литература", 599.0, 25),
        Product("Кофе", "Арабика свежеобжаренная", 1299.90, 15),
        Product("Ручка", "Шариковая синяя", 49.99, 100)
    ]

# Фикстура с областью видимости "session" — создаётся один раз за сессию
@pytest.fixture(scope="session")
def expensive_product_setup() -> Generator[List[Product], None, None]:
    """Фикстура для ресурсоёмкой инициализации"""
    print("\nИнициализация сложных тестовых данных...")
    products: List[Product] = []
    for i in range(100):
        products.append(Product(f"Товар_{i}", f"Описание товара {i}", i * 100.5, i))
    yield products
    print("Очистка сложных тестовых данных...")

# Фикстура с очисткой (использует yield)
@pytest.fixture
def temporary_product() -> Generator[Product, None, None]:
    product = Product("Временный товар", "Для временного теста", 999.0, 1)
    yield product
    # Код после yield выполняется после завершения теста
    print(f"Продукт '{product.name}' удалён после теста")

# --- ТЕСТЫ С ИСПОЛЬЗОВАНИЕМ ФИКСТУР ---
def test_product_creation_with_fixture(sample_product: Product) -> None:
    """Тест с использованием простой фикстуры"""
    assert sample_product.name == "Смартфон"
    assert sample_product.description == "Новый смартфон 2024"
    assert sample_product.price == 49999.50
    assert sample_product.quantity == 10

def test_multiple_products_with_parametrized_fixture(product_with_params: Product) -> None:
    """Тест с параметризованной фикстурой — будет запущен 3 раза"""
    # Проверяем, что все атрибуты присутствуют
    assert hasattr(product_with_params, 'name')
    assert hasattr(product_with_params, 'description')
    assert hasattr(product_with_params, 'price')
    assert hasattr(product_with_params, 'quantity')
    # Базовый тест типов
    assert isinstance(product_with_params.name, str)
    assert isinstance(product_with_params.price, float)
    assert isinstance(product_with_params.quantity, int)

def test_product_list_operations(product_list: List[Product]) -> None:
    """Тест операций с набором продуктов"""
    assert len(product_list) == 3

    # Проверка общего количества товаров
    total_quantity = sum(product.quantity for product in product_list)
    assert total_quantity == 140  # 25 + 15 + 100

    # Проверка средней цены
    average_price = sum(product.price for product in product_list) / len(product_list)
    assert round(average_price, 2) == 649.63

def test_expensive_setup(expensive_product_setup: List[Product]) -> None:
    """Тест с использованием ресурсоёмкой фикстуры"""
    assert len(expensive_product_setup) == 100
    # Проверяем первый и последний элементы
    assert expensive_product_setup[0].name == "Товар_0"
    assert expensive_product_setup[-1].name == "Товар_99"

def test_temporary_product_operations(temporary_product: Product) -> None:
    """Тест с фикстурой, имеющей очистку"""
    assert temporary_product.name == "Временный товар"
    assert temporary_product.price == 999.0

    # Изменяем количество для проверки
    temporary_product.quantity = 5
    assert temporary_product.quantity == 5

# Комбинированный тест — использует несколько фикстур одновременно
def test_combined_fixtures(sample_product: Product, product_list: List[Product]) -> None:
    """Тест, использующий несколько фикстур"""
    # Сравниваем цену образца с ценами из списка
    sample_price = sample_product.price
    list_prices = [p.price for p in product_list]

    assert sample_price > max(list_prices)  # Смартфон дороже всех товаров в списке

# Тест с зависимостью от фикстуры (использует фикстуру внутри теста)
def test_dynamic_product_creation() -> None:
    """Тест с динамическим созданием фикстуры внутри теста"""
    def create_test_product(name: str, price: float) -> Product:
        return Product(name, "Автоматически созданный продукт", price, 1)

    cheap_product: Product = create_test_product("Дешёвый товар", 10.0)
    expensive_product: Product = create_test_product("Дорогой товар", 10000.0)


    assert cheap_product.price == 10.0
    assert expensive_product.price == 10000.0
