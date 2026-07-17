import sqlite3
import os

def test_practice_sql():
    # Set up in-memory database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create dummy tables
    cursor.execute('''
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department_id INTEGER
        )
    ''')

    # Insert dummy data
    cursor.execute("INSERT INTO departments (id, name) VALUES (1, 'Engineering'), (2, 'Sales')")
    cursor.execute("INSERT INTO employees (id, name, department_id) VALUES (1, 'Alice', 1), (2, 'Bob', 2), (3, 'Charlie', NULL)")

    # Read and execute practice.sql
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'practice.sql')
    with open(sql_path, 'r') as f:
        sql_script = f.read()
    
    # We may need to execute statements one by one or ignore failures if student code is incomplete.
    # Let's execute the script, catching potential syntax errors if incomplete, but the test should assert on the final data.
    try:
        cursor.executescript(sql_script)
    except sqlite3.OperationalError:
        pass # Ignore errors in case the script is incomplete, but assert will fail below

    # Check Exercise 1 (practice_inner_join)
    try:
        cursor.execute("SELECT * FROM practice_inner_join ORDER BY name")
        inner_results = cursor.fetchall()
        assert len(inner_results) == 2, "INNER JOIN should return 2 rows"
        assert inner_results[0] == ('Alice', 'Engineering')
        assert inner_results[1] == ('Bob', 'Sales')
    except sqlite3.OperationalError as e:
        assert False, f"Failed to query practice_inner_join view: {e}"

    # Check Exercise 2 (practice_left_join)
    try:
        cursor.execute("SELECT * FROM practice_left_join ORDER BY name")
        left_results = cursor.fetchall()
        assert len(left_results) == 3, "LEFT JOIN should return 3 rows"
        assert left_results[0] == ('Alice', 'Engineering')
        assert left_results[1] == ('Bob', 'Sales')
        assert left_results[2] == ('Charlie', None)
    except sqlite3.OperationalError as e:
        assert False, f"Failed to query practice_left_join view: {e}"

    conn.close()
