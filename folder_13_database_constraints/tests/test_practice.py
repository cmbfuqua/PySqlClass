import sqlite3
import pytest
import os

def test_practice():
    # Connect to in-memory database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Read the practice.sql file
    current_dir = os.path.dirname(os.path.dirname(__file__))
    sql_path = os.path.join(current_dir, 'practice.sql')
    
    with open(sql_path, 'r') as f:
        sql_content = f.read()
        
    # Execute the student's code
    try:
        cursor.executescript(sql_content)
    except sqlite3.Error as e:
        pytest.fail(f"SQL Execution Error: {e}")
        
    # Verify table schema
    cursor.execute("PRAGMA table_info(Employees)")
    columns = cursor.fetchall()
    
    assert len(columns) > 0, "Table 'Employees' was not created."
    
    # Extract column details
    col_dict = {col[1]: col for col in columns}
    
    # Check emp_id
    assert 'emp_id' in col_dict
    assert col_dict['emp_id'][2].upper() == 'INTEGER'
    assert col_dict['emp_id'][5] == 1 # pk
    
    # Check email
    assert 'email' in col_dict
    assert col_dict['email'][3] == 1 # not null
    
    # Verify unique constraint by attempting to insert duplicate
    try:
        cursor.execute("INSERT INTO Employees (emp_id, email, salary, department) VALUES (1, 'a@b.com', 40000, 'HR')")
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO Employees (emp_id, email, salary, department) VALUES (2, 'a@b.com', 40000, 'HR')")
    except Exception as e:
        if not isinstance(e, pytest.raises.Exception):
            pass # Ignore other errors if not uniqueness related
            
    # Check salary check constraint
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO Employees (emp_id, email, salary, department) VALUES (3, 'c@b.com', 20000, 'HR')")
        
    # Check default department
    cursor.execute("INSERT INTO Employees (emp_id, email, salary) VALUES (4, 'd@b.com', 50000)")
    cursor.execute("SELECT department FROM Employees WHERE emp_id = 4")
    assert cursor.fetchone()[0] == 'Engineering'
    
    conn.close()
