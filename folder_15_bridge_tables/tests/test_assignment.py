import sqlite3
import pytest
import os

def test_assignment():
    conn = sqlite3.connect(':memory:')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    current_dir = os.path.dirname(os.path.dirname(__file__))
    sql_path = os.path.join(current_dir, 'assignment.sql')
    
    with open(sql_path, 'r') as f:
        sql_content = f.read()
        
    try:
        cursor.executescript(sql_content)
    except sqlite3.Error as e:
        pytest.fail(f"SQL Execution Error: {e}")
        
    # Verify 'Appointments' schema
    cursor.execute("PRAGMA table_info(Appointments)")
    columns = cursor.fetchall()
    assert len(columns) > 0, "Table 'Appointments' was not created."
    
    # Check composite primary key
    pk_cols = [col[1] for col in columns if col[5] > 0]
    assert 'doc_id' in pk_cols and 'pat_id' in pk_cols and 'appointment_date' in pk_cols, "Composite PK should include doc_id, pat_id, and appointment_date."
    
    # Check foreign keys
    cursor.execute("PRAGMA foreign_key_list(Appointments)")
    fks = cursor.fetchall()
    assert len(fks) == 2, "There should be exactly 2 foreign keys in Appointments."
    
    # Check data
    cursor.execute("SELECT doc_id, pat_id, appointment_date FROM Appointments ORDER BY doc_id, pat_id")
    rows = cursor.fetchall()
    assert len(rows) == 3, "There should be exactly 3 appointments."
    
    expected_rows = [
        (1, 100, '2023-10-01'),
        (1, 101, '2023-10-01'),
        (2, 100, '2023-10-02')
    ]
    assert rows == expected_rows, "Inserted data does not match the assignment requirements."
    
    conn.close()
