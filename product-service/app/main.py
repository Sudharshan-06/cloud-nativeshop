from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Product
from .seed import seed_products


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_products()
    yield


app = FastAPI(
    title="CloudNativeShop Product Service",
    version="1.0.0",
    lifespan=lifespan
)


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
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        return {
            "error": "Product not found"
        }

    return product