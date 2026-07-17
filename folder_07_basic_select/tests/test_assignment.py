import sqlite3
import pytest
import os
import re

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE products (product_id INTEGER, product_name TEXT, price REAL)")
    cursor.execute("CREATE TABLE customers (customer_id INTEGER, first_name TEXT, last_name TEXT, email TEXT)")
    conn.commit()
    yield conn
    conn.close()

def test_assignment_queries(db_connection):
    sql_file_path = os.path.join(os.path.dirname(__file__), '..', 'assignment.sql')
    with open(sql_file_path, 'r') as f:
        sql_script = f.read()
    
    # Remove block comments
    sql_script = re.sub(r'/\*.*?\*/', '', sql_script, flags=re.DOTALL)
    # Remove line comments
    lines = [line for line in sql_script.split('\n') if not line.strip().startswith('--')]
    clean_sql = '\n'.join(lines)
    queries = [q.strip() for q in clean_sql.split(';') if q.strip()]
    
    assert len(queries) >= 3, "Please implement all 3 assignment queries."
    
    cursor = db_connection.cursor()
    
    # 1. SELECT * FROM products
    cursor.execute(queries[0])
    cols1 = [desc[0].lower() for desc in cursor.description]
    assert set(cols1) == {'product_id', 'product_name', 'price'}
    
    # 2. SELECT product_name, price FROM products
    cursor.execute(queries[1])
    cols2 = [desc[0].lower() for desc in cursor.description]
    assert set(cols2) == {'product_name', 'price'}
    
    # 3. SELECT customer_id, first_name, email FROM customers
    cursor.execute(queries[2])
    cols3 = [desc[0].lower() for desc in cursor.description]
    assert set(cols3) == {'customer_id', 'first_name', 'email'}
