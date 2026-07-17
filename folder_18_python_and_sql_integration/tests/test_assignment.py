import sqlite3
import pytest
import tempfile
import os
from ..assignment import seed_products

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp()
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    conn.commit()
    conn.close()
    
    yield path
    
    os.close(fd)
    os.remove(path)

def test_seed_products(temp_db):
    data = [
        {'name': 'Laptop', 'price': 999.99},
        {'name': 'Mouse', 'price': 25.50},
        {'name': 'Keyboard', 'price': 45.00}
    ]
    
    seed_products(temp_db, data)
    
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    
    assert len(rows) == 3
    assert rows[0] == ('Laptop', 999.99)
    assert rows[1] == ('Mouse', 25.50)
    assert rows[2] == ('Keyboard', 45.00)
