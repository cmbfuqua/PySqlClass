import sqlite3
import os

def test_assignment():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Setup dummy tables
    cursor.executescript("""
        CREATE TABLE teams (id INTEGER, team_name TEXT);
        INSERT INTO teams VALUES (1, 'Lions'), (2, 'Tigers'), (3, 'Bears');
        
        CREATE TABLE matches (id INTEGER, home_team_id INTEGER, away_team_id INTEGER, home_score INTEGER, away_score INTEGER);
        INSERT INTO matches VALUES (1, 1, 2, 2, 1);
    """)
    
    # Read and execute assignment.sql
    sql_file = os.path.join(os.path.dirname(__file__), '..', 'assignment.sql')
    with open(sql_file, 'r') as f:
        sql_content = f.read()
        
    try:
        cursor.executescript(sql_content)
    except Exception as e:
        assert False, f"SQL Execution Error: {e}"
        
    # Check Task 1
    try:
        cursor.execute("SELECT team1_name, team2_name FROM tournament_matchups ORDER BY team1_name, team2_name")
        matchups = cursor.fetchall()
        expected_matchups = [('Bears', 'Lions'), ('Bears', 'Tigers'), ('Lions', 'Bears'), ('Lions', 'Tigers'), ('Tigers', 'Bears'), ('Tigers', 'Lions')]
        assert matchups == expected_matchups, f"Expected {expected_matchups}, got {matchups}"
    except sqlite3.OperationalError:
        assert False, "View tournament_matchups not created or invalid"

    # Check Task 2
    try:
        cursor.execute("SELECT team_name, home_score FROM team_home_matches ORDER BY team_name")
        scores = cursor.fetchall()
        expected_scores = [('Bears', None), ('Lions', 2), ('Tigers', None)]
        assert scores == expected_scores, f"Expected {expected_scores}, got {scores}"
    except sqlite3.OperationalError:
        assert False, "View team_home_matches not created or invalid"
        
    conn.close()
