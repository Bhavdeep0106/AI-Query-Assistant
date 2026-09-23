import sqlite3
from datetime import date, timedelta
import random
import os


DB_NAME = "database.db"


def create_database():

    if os.path.exists(DB_NAME):
        print("Database already exists. Skipping creation.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        country TEXT NOT NULL
    );

    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    );

    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );

    CREATE TABLE order_items (
        id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    """)

    customers = [
        (1, "Rahul Sharma", "rahul@example.com", "India"),
        (2, "Aarav Mehta", "aarav@example.com", "India"),
        (3, "Emma Smith", "emma@example.com", "USA"),
        (4, "John Wilson", "john@example.com", "UK"),
        (5, "Sophia Brown", "sophia@example.com", "USA"),
        (6, "Liam Jones", "liam@example.com", "UK"),
        (7, "Priya Singh", "priya@example.com", "India"),
        (8, "Daniel Lee", "daniel@example.com", "Singapore"),
    ]

    products = [
        (1, "Laptop Pro", "Electronics", 1200),
        (2, "Wireless Mouse", "Electronics", 40),
        (3, "Mechanical Keyboard", "Electronics", 100),
        (4, "Running Shoes", "Sports", 90),
        (5, "Yoga Mat", "Sports", 30),
        (6, "Coffee Maker", "Home", 150),
        (7, "Desk Lamp", "Home", 60),
        (8, "Backpack", "Accessories", 70),
        (9, "Water Bottle", "Accessories", 25),
        (10, "Headphones", "Electronics", 200),
    ]

    cursor.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?)",
        customers
    )

    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        products
    )

    start_date = date(2025, 1, 1)

    orders = []
    order_items = []

    order_id = 1
    item_id = 1

    random.seed(42)

    for _ in range(100):
        customer_id = random.randint(1, len(customers))
        order_date = start_date + timedelta(days=random.randint(0, 364))
        status = random.choice(
            ["completed", "completed", "completed", "cancelled"]
        )

        orders.append(
            (order_id, customer_id, order_date.isoformat(), status)
        )

        number_of_items = random.randint(1, 3)

        for _ in range(number_of_items):
            product_id = random.randint(1, len(products))
            quantity = random.randint(1, 4)

            order_items.append(
                (item_id, order_id, product_id, quantity)
            )

            item_id += 1

        order_id += 1

    cursor.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?)",
        orders
    )

    cursor.executemany(
        "INSERT INTO order_items VALUES (?, ?, ?, ?)",
        order_items
    )

    conn.commit()
    conn.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()