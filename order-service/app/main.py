from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="CloudNativeShop Order Service",
    version="1.0.0"
)


class Order(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: str


orders = [
    Order(
        id=1,
        product_id=1,
        quantity=1,
        status="confirmed"
    ),
    Order(
        id=2,
        product_id=2,
        quantity=2,
        status="processing"
    ),
]


@app.get("/")
def root():
    return {
        "service": "order-service",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/orders")
def get_orders():
    return orders


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order.id == order_id:
            return order

    return {
        "error": "Order not found"
    }