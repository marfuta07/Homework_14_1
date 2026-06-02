import pytest
from src.category import Category
from src.product import Product

@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    """Автоматически сбрасывает счётчики категорий и товаров перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0
