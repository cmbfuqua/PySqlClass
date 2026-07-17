import sqlite3
import os

def test_assignment_sql():
    # Set up in-memory database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create dummy tables
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            total_amount REAL
        )
    ''')

    # Insert dummy data
    cursor.execute("INSERT INTO customers (customer_id, customer_name) VALUES (1, 'Customer A'), (2, 'Customer B'), (3, 'Customer C')")
    cursor.execute("INSERT INTO orders (order_id, customer_id, order_date, total_amount) VALUES (101, 1, '2023-10-01', 150.0), (102, 2, '2023-10-02', 200.0)")

    # Read and execute assignment.sql
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'assignment.sql')
    with open(sql_path, 'r') as f:
        sql_script = f.read()
    
    try:
        cursor.executescript(sql_script)
    except sqlite3.OperationalError:
        pass # Ignore errors if incomplete, assertions will catch failure

    # Check Task 1 (assignment_result_1)
    try:
        cursor.execute("SELECT * FROM assignment_result_1 ORDER BY customer_name")
        res1 = cursor.fetchall()
        assert len(res1) == 2, "Task 1 (INNER JOIN) should return 2 rows"
        assert res1[0] == ('Customer A', 150.0)
        assert res1[1] == ('Customer B', 200.0)
    except sqlite3.OperationalError as e:
        assert False, f"Failed to query assignment_result_1 table: {e}"

    # Check Task 2 (assignment_result_2)
    try:
        cursor.execute("SELECT * FROM assignment_result_2 ORDER BY customer_name")
        res2 = cursor.fetchall()
        assert len(res2) == 3, "Task 2 (LEFT JOIN) should return 3 rows"
        assert res2[0] == ('Customer A', 101)
        assert res2[1] == ('Customer B', 102)
        assert res2[2] == ('Customer C', None)
    except sqlite3.OperationalError as e:
        assert False, f"Failed to query assignment_result_2 table: {e}"

    conn.close()
