import sqlite3
import os
import pytest

def test_practice_sql():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(current_dir, '..', 'practice.sql')
    
    with open(sql_file, 'r') as f:
        sql_script = f.read()
        
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    statements = sql_script.split(';')
    
    table_students_existed = False
    added_grade_column = False
    
    try:
        for stmt in statements:
            stmt = stmt.strip()
            if not stmt:
                continue
            cursor.execute(stmt)
            
            # Check intermediate states
            if 'CREATE TABLE students' in stmt.upper() or 'CREATE TABLE "students"' in stmt.upper():
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
                if cursor.fetchone():
                    table_students_existed = True
            
            if 'ALTER TABLE students' in stmt.upper() and 'grade' in stmt.lower():
                cursor.execute("PRAGMA table_info(students)")
                columns = [info[1] for info in cursor.fetchall()]
                if 'grade' in columns:
                    added_grade_column = True

        assert table_students_existed, "Table 'students' was not created."
        assert added_grade_column, "Column 'grade' was not added to 'students'."
        
        # Check if dropped
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
        assert cursor.fetchone() is None, "Table 'students' should have been dropped."
            
    except sqlite3.Error as e:
        pytest.fail(f"SQL execution failed: {e}")
    finally:
        conn.close()
