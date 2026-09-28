import pytest
from app.repositories.product_repo import ProductRepository
from app.services.product_service import ProductService
from app.schemas import ProductCreate, ProductUpdate

@pytest.fixture
def repo():
    r = ProductRepository()
    yield r
    r.clear()

@pytest.fixture
def service(repo):
    return ProductService(repo=repo)

def test_calculate_discount_valid(service):
    prod = service.create_product(ProductCreate(name="Laptop", price=1000.0, category="Electronics", stock=5))
    res = service.calculate_discount(prod.id, 10.0)
    assert res is not None
    assert res["discount_amount"] == 100.0
    assert res["final_price"] == 900.0

def test_calculate_discount_not_found(service):
    res = service.calculate_discount(999, 10.0)
    assert res is None

def test_create_and_get_product(service):
    created = service.create_product(ProductCreate(name="Mouse", price=25.0, category="Accessories", stock=50))
    assert created.id == 1
    assert created.name == "Mouse"
    fetched = service.get_product(1)
    assert fetched is not None
    assert fetched.name == "Mouse"

def test_delete_product(service):
    created = service.create_product(ProductCreate(name="Keyboard", price=50.0, category="Accessories", stock=20))
    assert service.delete_product(created.id) is True
    assert service.get_product(created.id) is None
    assert service.delete_product(created.id) is False