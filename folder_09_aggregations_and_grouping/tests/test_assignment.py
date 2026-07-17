import sqlite3
import os
import pytest

def test_assignment():
    # Setup in-memory DB
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create tables and insert dummy data
    cursor.execute("""
        CREATE TABLE student_grades (
            student_id INTEGER,
            course_name TEXT,
            grade INTEGER,
            semester TEXT
        )
    """)
    cursor.executemany("""
        INSERT INTO student_grades (student_id, course_name, grade, semester) VALUES (?, ?, ?, ?)
    """, [
        (1, 'Math', 90, 'Fall'),
        (1, 'Science', 80, 'Fall'),
        (2, 'Math', 95, 'Fall'),
        (2, 'Science', 85, 'Fall'),
        (1, 'History', 88, 'Spring')
    ])
    
    # Read the assignment file
    assignment_file = os.path.join(os.path.dirname(__file__), '..', 'assignment.sql')
    with open(assignment_file, 'r') as f:
        sql_script = f.read()
        
    try:
        cursor.executescript(sql_script)
    except sqlite3.OperationalError as e:
        pytest.fail(f"SQL script failed to execute: {e}")
        
    # Check student_averages view
    try:
        cursor.execute("SELECT student_id, average_grade FROM student_averages ORDER BY student_id")
        results = cursor.fetchall()
        assert results == [(1, 86.0), (2, 90.0)], "student_averages results are incorrect."
    except sqlite3.OperationalError:
        pytest.fail("View student_averages does not exist or has incorrect columns.")

    # Check course_stats view
    try:
        cursor.execute("SELECT course_name, min_grade, max_grade, avg_grade FROM course_stats ORDER BY course_name")
        results = cursor.fetchall()
        expected = [
            ('History', 88, 88, 88.0),
            ('Math', 90, 95, 92.5),
            ('Science', 80, 85, 82.5)
        ]
        assert results == expected, "course_stats results are incorrect."
    except sqlite3.OperationalError:
        pytest.fail("View course_stats does not exist or has incorrect columns.")
