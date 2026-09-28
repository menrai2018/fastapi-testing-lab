import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.product_repo import product_repo

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: เคลียร์ข้อมูลก่อนเริ่มแต่ละ test
    product_repo.clear()
    yield
    # Teardown: เคลียร์ข้อมูลหลังจบแต่ละ test
    product_repo.clear()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}

def test_create_product_success():
    payload = {
        "name": "Mechanical Keyboard",
        "price": 89.99,
        "category": "Accessories",
        "stock": 15
    }
    response = client.post("/products/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Mechanical Keyboard"
    assert data["price"] == 89.99

def test_create_product_invalid_price():
    payload = {
        "name": "Invalid Item",
        "price": -10.0,
        "category": "Test",
        "stock": 5
    }
    response = client.post("/products/", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (Validation Error)

def test_get_product_not_found():
    response = client.get("/products/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_get_discount():
    # สร้างสินค้าก่อน
    client.post("/products/", json={
        "name": "Monitor",
        "price": 200.0,
        "category": "Electronics",
        "stock": 10
    })
    # ทดสอบคำนวณส่วนลด 20%
    response = client.get("/products/1/discount?pct=20")
    assert response.status_code == 200
    data = response.json()
    assert data["original_price"] == 200.0
    assert data["discount_amount"] == 40.0
    assert data["final_price"] == 160.0