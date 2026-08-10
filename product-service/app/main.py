from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
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
    lifespan=lifespan,
)


class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int


@app.get("/")
def root():
    return {
        "service": "product-service",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@app.post("/products", status_code=201)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
):
    product = Product(
        name=product_data.name,
        price=product_data.price,
        stock=product_data.stock,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product