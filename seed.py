"""
seed.py — resets and populates the KulBalam database with known test data.

Run from the project root:  python seed.py
Safe to run multiple times — drops all data and starts fresh each time.
"""

from faker import Faker
from passlib.hash import bcrypt_sha256
from db.database import engine, SessionLocal
from db.models import (
    Base, DbUser, DbProduct, DbOrder, DbOrderLine,
    DbProductReview, DbFriendship,
)
from enums import OrderStatus

fake = Faker()
Faker.seed(42)


def _hash(plain: str) -> str:
    return bcrypt_sha256.hash(plain)


FIXED_USERS = [
    dict(username="admin",  email="admin@kulbalam.local",  password="Admin123!"),
    dict(username="alice",  email="alice@kulbalam.local",  password="Alice123!"),
    dict(username="bob",    email="bob@kulbalam.local",    password="Bob456@#"),
    dict(username="carlos", email="carlos@kulbalam.local", password="Carlos78!"),
    dict(username="diana",  email="diana@kulbalam.local",  password="Diana99$!"),
]

FIXED_PRODUCTS = [
    dict(product_name="Artisan Keyboard",
         description="Mechanical keyboard, tactile switches, tenkeyless layout",
         price=149.99, quantity=5, published=True, seller="alice"),
    dict(product_name="Wireless Mouse",
         description="Ergonomic wireless mouse, 3000 DPI, USB receiver",
         price=39.99, quantity=20, published=True, seller="alice"),
    dict(product_name="USB-C Hub",
         description="7-port USB-C hub with HDMI and SD card reader",
         price=59.99, quantity=12, published=True, seller="diana"),
    dict(product_name="Monitor Stand",
         description="Adjustable aluminium monitor stand, 360-degree rotation",
         price=79.99, quantity=8, published=True, seller="diana"),
    dict(product_name="Laptop Sleeve",
         description="Neoprene sleeve, fits up to 15-inch laptops",
         price=24.99, quantity=30, published=True, seller="diana"),
]


def seed():
    print("Resetting database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        for u in FIXED_USERS:
            db.add(DbUser(username=u["username"], email=u["email"],
                          password=_hash(u["password"])))
        db.commit()

        users = {u.username: u for u in db.query(DbUser).all()}

        seen_names = set(users)
        for _ in range(10):
            uname = fake.user_name()
            while uname in seen_names:
                uname = fake.user_name()
            seen_names.add(uname)
            db.add(DbUser(username=uname, email=fake.email(),
                          password=_hash("Password1!")))
        db.commit()

        all_users = db.query(DbUser).all()

        for p in FIXED_PRODUCTS:
            db.add(DbProduct(
                product_name=p["product_name"],
                description=p["description"],
                price=p["price"],
                quantity=p["quantity"],
                published=p["published"],
                seller_id=users[p["seller"]].id,
            ))
        db.commit()

        products = {p.product_name: p for p in db.query(DbProduct).all()}

        for _ in range(25):
            db.add(DbProduct(
                product_name=fake.catch_phrase(),
                description=fake.sentence(nb_words=8),
                price=round(fake.pyfloat(min_value=5, max_value=500, right_digits=2), 2),
                quantity=fake.random_int(min=1, max=50),
                published=True,
                seller_id=fake.random_element(all_users).id,
            ))
        db.commit()

        carlos = users["carlos"]
        order = DbOrder(order_status=OrderStatus.COMPLETED, user_id=carlos.id, total=0.0)
        db.add(order)
        db.commit()
        db.refresh(order)

        for product_name, qty in [("Wireless Mouse", 1), ("USB-C Hub", 2)]:
            prod = products[product_name]
            line_total = prod.price * qty
            db.add(DbOrderLine(order_id=order.id, product_id=prod.id,
                               quantity=qty, total=line_total))
            order.total += line_total
        db.commit()

        db.add(DbProductReview(
            product_id=products["Wireless Mouse"].id,
            score=4,
            comment="Works well, solid range.",
            creator_id=carlos.id,
        ))
        db.commit()

        alice = users["alice"]
        bob = users["bob"]
        diana = users["diana"]

        db.add(DbFriendship(user_id=alice.id, friend_id=carlos.id,
                            sender_username=alice.username, accepted=True))
        db.add(DbFriendship(user_id=carlos.id, friend_id=alice.id,
                            sender_username=alice.username, accepted=True))
        db.add(DbFriendship(user_id=bob.id, friend_id=diana.id,
                            sender_username=bob.username, accepted=False))
        db.commit()

        print("Done. Fixed users:")
        for u in FIXED_USERS:
            print(f"  {u['username']:10s}  {u['email']:32s}  password: {u['password']}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
