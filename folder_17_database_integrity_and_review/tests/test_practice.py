import sqlite3
import pytest
from ..practice import safe_update_product_price

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, price REAL)")
    cursor.execute("INSERT INTO products (id, price) VALUES (1, 10.0)")
    conn.commit()
    yield conn
    conn.close()

def test_safe_update_product_price_success(db_connection):
    result = safe_update_product_price(db_connection, 1, 15.0)
    assert result is True
    
    cursor = db_connection.cursor()
    cursor.execute("SELECT price FROM products WHERE id = 1")
    price = cursor.fetchone()[0]
    assert price == 15.0

def test_safe_update_product_price_negative(db_connection):
    result = safe_update_product_price(db_connection, 1, -5.0)
    assert result is False
    
    cursor = db_connection.cursor()
    cursor.execute("SELECT price FROM products WHERE id = 1")
    price = cursor.fetchone()[0]
    assert price == 10.0 # Price should not have changed due to rollback
