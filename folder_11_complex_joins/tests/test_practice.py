import sqlite3
import os

def test_practice():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Setup dummy tables
    cursor.executescript("""
        CREATE TABLE colors (id INTEGER, color_name TEXT);
        INSERT INTO colors VALUES (1, 'Red'), (2, 'Blue');
        
        CREATE TABLE sizes (id INTEGER, size_name TEXT);
        INSERT INTO sizes VALUES (1, 'Small'), (2, 'Large');
        
        CREATE TABLE employees (id INTEGER, name TEXT, manager_id INTEGER);
        INSERT INTO employees VALUES (1, 'Alice', NULL), (2, 'Bob', 1), (3, 'Charlie', 1);
    """)
    
    # Read and execute practice.sql
    sql_file = os.path.join(os.path.dirname(__file__), '..', 'practice.sql')
    with open(sql_file, 'r') as f:
        sql_content = f.read()
        
    try:
        cursor.executescript(sql_content)
    except Exception as e:
        assert False, f"SQL Execution Error: {e}"
        
    # Check EXERCISE 1
    try:
        cursor.execute("SELECT color_name, size_name FROM all_combinations ORDER BY color_name, size_name")
        combos = cursor.fetchall()
        expected_combos = [('Blue', 'Large'), ('Blue', 'Small'), ('Red', 'Large'), ('Red', 'Small')]
        assert combos == expected_combos, f"Expected {expected_combos}, got {combos}"
    except sqlite3.OperationalError:
        assert False, "View all_combinations not created or invalid"
    
    # Check EXERCISE 2
    try:
        cursor.execute("SELECT employee_name, manager_name FROM employee_managers ORDER BY employee_name")
        managers = cursor.fetchall()
        expected_managers = [('Alice', None), ('Bob', 'Alice'), ('Charlie', 'Alice')]
        assert managers == expected_managers, f"Expected {expected_managers}, got {managers}"
    except sqlite3.OperationalError:
        assert False, "View employee_managers not created or invalid"
        
    conn.close()
