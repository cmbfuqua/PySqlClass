import sqlite3
import pytest
import os

def test_assignment():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    current_dir = os.path.dirname(os.path.dirname(__file__))
    sql_path = os.path.join(current_dir, 'assignment.sql')
    
    with open(sql_path, 'r') as f:
        sql_content = f.read()
        
    try:
        cursor.executescript(sql_content)
    except sqlite3.Error as e:
        pytest.fail(f"SQL Execution Error: {e}")
        
    cursor.execute("PRAGMA table_info(LibraryMembers)")
    columns = cursor.fetchall()
    
    assert len(columns) > 0, "Table 'LibraryMembers' was not created."
    
    col_dict = {col[1]: col for col in columns}
    
    # 1. member_id
    assert 'member_id' in col_dict
    assert col_dict['member_id'][2].upper() == 'INTEGER'
    assert col_dict['member_id'][5] == 1 # pk
    
    # 2. phone_number UNIQUE
    assert 'phone_number' in col_dict
    
    cursor.execute("INSERT INTO LibraryMembers (member_id, phone_number, full_name, books_borrowed) VALUES (1, '123', 'John Doe', 1)")
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO LibraryMembers (member_id, phone_number, full_name, books_borrowed) VALUES (2, '123', 'Jane Doe', 1)")
        
    # 3. full_name NOT NULL
    assert 'full_name' in col_dict
    assert col_dict['full_name'][3] == 1 # not null
    
    # 4. join_date DEFAULT
    cursor.execute("INSERT INTO LibraryMembers (member_id, phone_number, full_name, books_borrowed) VALUES (3, '456', 'Alice', 1)")
    cursor.execute("SELECT join_date FROM LibraryMembers WHERE member_id = 3")
    assert cursor.fetchone()[0] == '2020-01-01'
    
    # 5. books_borrowed CHECK
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO LibraryMembers (member_id, phone_number, full_name, books_borrowed) VALUES (4, '789', 'Bob', -1)")
        
    conn.close()
