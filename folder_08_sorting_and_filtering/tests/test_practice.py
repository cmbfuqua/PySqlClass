import sqlite3
import pytest
import os
import re

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE employees (first_name TEXT, last_name TEXT, age INTEGER, department TEXT, salary REAL)")
    cursor.execute("INSERT INTO employees VALUES ('John', 'Doe', 35, 'Sales', 60000.0), ('Jane', 'Smith', 28, 'HR', 55000.0), ('Alice', 'Johnson', 40, 'Sales', 80000.0)")
    conn.commit()
    yield conn
    conn.close()

def test_practice_queries(db_connection):
    sql_file_path = os.path.join(os.path.dirname(__file__), '..', 'practice.sql')
    with open(sql_file_path, 'r') as f:
        sql_script = f.read()
    
    sql_script = re.sub(r'/\*.*?\*/', '', sql_script, flags=re.DOTALL)
    lines = [line for line in sql_script.split('\n') if not line.strip().startswith('--')]
    clean_sql = '\n'.join(lines)
    queries = [q.strip() for q in clean_sql.split(';') if q.strip()]
    
    assert len(queries) >= 3, "Please implement all TODO queries"
    
    cursor = db_connection.cursor()
    
    # Query 1: Example query
    
    # Query 2: SELECT * FROM employees WHERE department = 'Sales'
    cursor.execute(queries[1])
    results2 = cursor.fetchall()
    assert len(results2) == 2, "Query 2 should return 2 rows for Sales department"
    for row in results2:
        assert row[3] == 'Sales', "All returned rows should be from Sales department"
        
    # Query 3: SELECT first_name, salary FROM employees ORDER BY salary DESC
    cursor.execute(queries[2])
    results3 = cursor.fetchall()
    cols3 = [desc[0].lower() for desc in cursor.description]
    assert set(cols3) == {'first_name', 'salary'}, f"Query 3 selected wrong columns: {cols3}"
    assert results3[0][1] == 80000.0, "The first row should have the highest salary (80000.0)"
    assert results3[1][1] == 60000.0
    assert results3[2][1] == 55000.0
