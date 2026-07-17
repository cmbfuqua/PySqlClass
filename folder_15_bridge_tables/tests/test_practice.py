import sqlite3
import pytest
import os

def test_practice():
    conn = sqlite3.connect(':memory:')
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
        
    # Verify 'ActorMovies' schema
    cursor.execute("PRAGMA table_info(ActorMovies)")
    columns = cursor.fetchall()
    assert len(columns) > 0, "Table 'ActorMovies' was not created."
    
    # Check composite primary key
    pk_cols = [col[1] for col in columns if col[5] > 0]
    assert 'a_id' in pk_cols and 'm_id' in pk_cols, "Composite primary key (a_id, m_id) is missing."
    
    # Check foreign keys
    cursor.execute("PRAGMA foreign_key_list(ActorMovies)")
    fks = cursor.fetchall()
    assert len(fks) == 2, "There should be exactly 2 foreign keys in ActorMovies."
    
    fk_tables = [fk[2] for fk in fks]
    assert 'Actors' in fk_tables and 'Movies' in fk_tables
    
    # Check data
    cursor.execute("SELECT * FROM ActorMovies ORDER BY a_id, m_id")
    rows = cursor.fetchall()
    assert len(rows) == 3, "There should be exactly 3 records in ActorMovies."
    
    expected_rows = [(1, 10), (1, 11), (2, 10)]
    for i in range(3):
        assert rows[i][0] == expected_rows[i][0] and rows[i][1] == expected_rows[i][1]
        
    conn.close()
