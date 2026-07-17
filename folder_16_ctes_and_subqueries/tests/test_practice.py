import sqlite3
import pytest
import os

def test_practice():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    current_dir = os.path.dirname(os.path.dirname(__file__))
    sql_path = os.path.join(current_dir, 'practice.sql')
    
    with open(sql_path, 'r') as f:
        sql_content = f.read()
        
    try:
        cursor.executescript(sql_content)
        
        statements = sql_content.split(';')
        selects = []
        for stmt in statements:
            lines = [l for l in stmt.split('\n') if not l.strip().startswith('--') and l.strip() != '']
            if not lines: continue
            first_line = lines[0].strip().upper()
            if first_line.startswith('SELECT') or first_line.startswith('WITH'):
                selects.append('\n'.join(lines))
                
        assert len(selects) >= 2, "You need to write at least two queries."
        
        # Query 1
        cursor.execute(selects[0])
        res1 = cursor.fetchall()
        names = set([r[0] for r in res1])
        assert names == {'Alice'}, "The first query should return 'Alice'."
        
        # Query 2
        cursor.execute(selects[1])
        res2 = cursor.fetchall()
        assert len(res2) == 1, "The CTE query should return exactly 1 row."
        assert res2[0][0] == 'Alice'
        assert res2[0][1] == 1200, "The total sales for Alice should be 1200."
        
    except sqlite3.Error as e:
        pytest.fail(f"SQL Execution Error: {e}")
    finally:
        conn.close()
