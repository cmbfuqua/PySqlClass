import sqlite3
def get_high_value_accounts(db_path, threshold):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    rows = cursor.execute('SELECT user_id, balance FROM accounts WHERE balance > ?', (threshold,)).fetchall()
    conn.close()
    return [{'user_id': r['user_id'], 'balance': r['balance']} for r in rows]
