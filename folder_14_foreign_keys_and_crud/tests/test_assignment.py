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
        
    # Verify 'Classes' table
    cursor.execute("PRAGMA table_info(Classes)")
    columns = cursor.fetchall()
    
    assert len(columns) > 0, "Table 'Classes' was not created."
    
    # Verify foreign key
    cursor.execute("PRAGMA foreign_key_list(Classes)")
    fks = cursor.fetchall()
    assert len(fks) > 0, "Foreign key missing on Classes table."
    assert fks[0][2] == 'Teachers', "Foreign key does not reference Teachers."
    assert fks[0][3] == 't_id', "Foreign key column is not t_id."
    assert fks[0][4] == 'teacher_id', "Foreign key does not reference teacher_id."
    # Check ON DELETE CASCADE - sqlite pragma returns cascade as index 5 (on_update), index 6 (on_delete)
    assert fks[0][6] == 'CASCADE', "ON DELETE CASCADE is missing."
    
    # We expect one class left (the one by Mr. Smith) since we deleted the one by Ms. Johnson.
    cursor.execute("SELECT t_id FROM Classes")
    rows = cursor.fetchall()
    assert len(rows) == 1, "There should be exactly one class left."
    assert rows[0][0] == 1, "The remaining class should belong to Mr. Smith (teacher_id 1)."
    
    # Test ON DELETE CASCADE
    cursor.execute("DELETE FROM Teachers WHERE teacher_id = 1")
    cursor.execute("SELECT * FROM Classes")
    assert len(cursor.fetchall()) == 0, "Classes were not deleted when the teacher was deleted (CASCADE failed)."
    
    conn.close()
