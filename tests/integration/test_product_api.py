import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.product_repo import product_repo

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    product_repo.clear()
    yield
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
    assert response.status_code == 422

def test_get_product_not_found():
    response = client.get("/products/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_get_discount():
    client.post("/products/", json={
        "name": "Monitor",
        "price": 200.0,
        "category": "Electronics",
        "stock": 10
    })
    response = client.get("/products/1/discount?pct=20")
    assert response.status_code == 200
    data = response.json()
    assert data["original_price"] == 200.0
    assert data["discount_amount"] == 40.0
    assert data["final_price"] == 160.0

def test_get_all_products_with_filter():
    client.post("/products/", json={"name": "Book", "price": 15.0, "category": "Books", "stock": 10})
    client.post("/products/", json={"name": "Pen", "price": 5.0, "category": "Stationery", "stock": 20})
    
    res = client.get("/products/?category=Books")
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == "Book"

    res_price = client.get("/products/?min_price=10&max_price=20")
    assert res_price.status_code == 200
    assert len(res_price.json()) == 1

def test_update_product():
    client.post("/products/", json={"name": "Desk", "price": 120.0, "category": "Furniture", "stock": 2})
    update_res = client.put("/products/1", json={"price": 150.0})
    assert update_res.status_code == 200
    assert update_res.json()["price"] == 150.0

    not_found_res = client.put("/products/999", json={"price": 100.0})
    assert not_found_res.status_code == 404

def test_delete_product_api():
    client.post("/products/", json={"name": "Chair", "price": 45.0, "category": "Furniture", "stock": 5})
    del_res = client.delete("/products/1")
    assert del_res.status_code == 204

    del_not_found = client.delete("/products/999")
    assert del_not_found.status_code == 404