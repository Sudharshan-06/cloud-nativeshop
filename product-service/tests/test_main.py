import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


# SQLite database used only for tests.
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["service"] == "product-service"
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_products_empty():
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == []

def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "Monitor",
            "price": 15000,
            "stock": 15,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Monitor"
    assert data["price"] == 15000
    assert data["stock"] == 15
    assert "id" in data

def test_get_product():
    create_response = client.post(
        "/products",
        json={
            "name": "Headphones",
            "price": 5000,
            "stock": 20,
        },
    )

    product_id = create_response.json()["id"]

    response = client.get(
        f"/products/{product_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Headphones"

def test_get_missing_product():
    response = client.get("/products/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"