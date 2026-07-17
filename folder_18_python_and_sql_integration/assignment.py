"""
Python and SQL Integration - Assignment

Problem: Database Seeder
Write a function that takes a list of dictionary data and inserts it into a database table.

Function Signature:
def seed_products(db_path: str, products: list[dict]) -> None:

Requirements:
1. Connect to the SQLite database at `db_path`.
2. The database already contains a `products` table with columns: `name` (TEXT) and `price` (REAL).
3. `products` is a list of dictionaries, e.g., [{'name': 'Laptop', 'price': 999.99}, ...]
4. Iterate through the list and insert each product into the table using parameterized queries.
5. Commit the changes and close the connection.
"""
import sqlite3

def seed_products(db_path: str, products: list[dict]) -> None:
    pass
