import sqlite3
import pytest
import os
import re

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE employees (first_name TEXT, last_name TEXT, age INTEGER)")
    cursor.execute("INSERT INTO employees VALUES ('John', 'Doe', 30), ('Jane', 'Smith', 25)")
    cursor.execute("CREATE TABLE movies (title TEXT, release_year INTEGER, genre TEXT)")
    cursor.execute("INSERT INTO movies VALUES ('The Matrix', 1999, 'Sci-Fi'), ('Inception', 2010, 'Sci-Fi')")
    conn.commit()
    yield conn
    conn.close()

def test_practice_queries(db_connection):
    sql_file_path = os.path.join(os.path.dirname(__file__), '..', 'practice.sql')
    with open(sql_file_path, 'r') as f:
        sql_script = f.read()
    
    # Remove block comments
    sql_script = re.sub(r'/\*.*?\*/', '', sql_script, flags=re.DOTALL)
    # Remove line comments
    lines = [line for line in sql_script.split('\n') if not line.strip().startswith('--')]
    clean_sql = '\n'.join(lines)
    queries = [q.strip() for q in clean_sql.split(';') if q.strip()]
    
    assert len(queries) >= 3, "Please implement all TODO queries"
    
    cursor = db_connection.cursor()
    
    # Query 1: Example query
    # Query 2: SELECT first_name, last_name FROM employees
    cursor.execute(queries[1])
    cols = [desc[0].lower() for desc in cursor.description]
    assert set(cols) == {'first_name', 'last_name'}, f"Query 2 selected wrong columns: {cols}"
    
    # Query 3: SELECT title, release_year FROM movies
    cursor.execute(queries[2])
    cols = [desc[0].lower() for desc in cursor.description]
    assert set(cols) == {'title', 'release_year'}, f"Query 3 selected wrong columns: {cols}"
