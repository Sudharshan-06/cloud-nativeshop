from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import Product


def seed_products():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        existing_products = db.query(Product).count()

        if existing_products > 0:
            return

        products = [
            Product(
                name="Laptop",
                price=75000,
                stock=10
            ),
            Product(
                name="Keyboard",
                price=2500,
                stock=25
            ),
            Product(
                name="Mouse",
                price=1200,
                stock=40
            ),
        ]

        db.add_all(products)
        db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    seed_products()