import sqlite3
import pytest
import os

def test_practice():
    conn = sqlite3.connect(':memory:')
    # Enable foreign keys in sqlite
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    current_dir = os.path.dirname(os.path.dirname(__file__))
    sql_path = os.path.join(current_dir, 'practice.sql')
    
    with open(sql_path, 'r') as f:
        sql_content = f.read()
        
    try:
        cursor.executescript(sql_content)
    except sqlite3.Error as e:
        pytest.fail(f"SQL Execution Error: {e}")
        
    # Verify 'Items' table schema
    cursor.execute("PRAGMA table_info(Items)")
    columns = cursor.fetchall()
    
    assert len(columns) > 0, "Table 'Items' was not created."
    
    # Verify foreign key
    cursor.execute("PRAGMA foreign_key_list(Items)")
    fks = cursor.fetchall()
    assert len(fks) > 0, "Foreign key missing on Items table."
    assert fks[0][2] == 'Categories', "Foreign key does not reference Categories."
    assert fks[0][3] == 'cat_id', "Foreign key column is not cat_id."
    assert fks[0][4] == 'category_id', "Foreign key does not reference category_id."
    
    # Verify the table is empty (we inserted then deleted it)
    cursor.execute("SELECT COUNT(*) FROM Items")
    count = cursor.fetchone()[0]
    assert count == 0, "Items table should be empty after deleting the item."
    
    # We can test FK constraint by attempting to insert a bad category
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO Items (item_id, name, cat_id) VALUES (99, 'Bad Item', 99)")

    conn.close()
