import sqlite3
import pytest
import os
import re

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE products (product_id INTEGER, product_name TEXT, price REAL, stock_quantity INTEGER)")
    cursor.execute("INSERT INTO products VALUES (1, 'Laptop', 999.99, 10), (2, 'Mouse', 25.50, 50), (3, 'Keyboard', 45.00, 15)")
    cursor.execute("CREATE TABLE customers (customer_id INTEGER, first_name TEXT, last_name TEXT, city TEXT)")
    cursor.execute("INSERT INTO customers VALUES (101, 'Alice', 'Wonderland', 'New York'), (102, 'Bob', 'Builder', 'Chicago'), (103, 'Charlie', 'Brown', 'Los Angeles')")
    conn.commit()
    yield conn
    conn.close()

def test_assignment_queries(db_connection):
    sql_file_path = os.path.join(os.path.dirname(__file__), '..', 'assignment.sql')
    with open(sql_file_path, 'r') as f:
        sql_script = f.read()
    
    sql_script = re.sub(r'/\*.*?\*/', '', sql_script, flags=re.DOTALL)
    lines = [line for line in sql_script.split('\n') if not line.strip().startswith('--')]
    clean_sql = '\n'.join(lines)
    queries = [q.strip() for q in clean_sql.split(';') if q.strip()]
    
    assert len(queries) >= 3, "Please implement all 3 assignment queries."
    
    cursor = db_connection.cursor()
    
    # 1. SELECT * FROM products WHERE price > 50
    cursor.execute(queries[0])
    results1 = cursor.fetchall()
    assert len(results1) == 1, "Query 1 should return exactly 1 row (price > 50)"
    assert results1[0][1] == 'Laptop', "Query 1 should return the Laptop"
    
    # 2. SELECT product_name, stock_quantity FROM products WHERE stock_quantity < 20 ORDER BY stock_quantity ASC
    cursor.execute(queries[1])
    results2 = cursor.fetchall()
    cols2 = [desc[0].lower() for desc in cursor.description]
    assert set(cols2) == {'product_name', 'stock_quantity'}, "Query 2 should select product_name and stock_quantity"
    assert len(results2) == 2, "Query 2 should return 2 rows (stock < 20)"
    assert results2[0][1] == 10, "Query 2 should order by stock_quantity ASC (10 first)"
    assert results2[1][1] == 15, "Query 2 should order by stock_quantity ASC (15 second)"
    
    # 3. SELECT first_name, last_name, city FROM customers WHERE city = 'New York' OR city = 'Chicago' ORDER BY last_name ASC
    cursor.execute(queries[2])
    results3 = cursor.fetchall()
    cols3 = [desc[0].lower() for desc in cursor.description]
    assert set(cols3) == {'first_name', 'last_name', 'city'}, "Query 3 should select first_name, last_name, and city"
    assert len(results3) == 2, "Query 3 should return 2 rows (New York or Chicago)"
    assert results3[0][1] == 'Builder', "Query 3 should order by last_name ASC (Builder first)"
    assert results3[1][1] == 'Wonderland', "Query 3 should order by last_name ASC (Wonderland second)"
