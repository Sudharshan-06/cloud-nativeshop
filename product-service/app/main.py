from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="CloudNativeShop Product Service",
    version="1.0.0"
)


class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int


products = [
    Product(id=1, name="Laptop", price=75000, stock=10),
    Product(id=2, name="Keyboard", price=2500, stock=25),
    Product(id=3, name="Mouse", price=1200, stock=40),
]


@app.get("/")
def root():
    return {
        "service": "product-service",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/products")
def get_products():
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product

    return {
        "error": "Product not found"
    }