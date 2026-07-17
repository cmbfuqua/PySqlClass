import sqlite3
import os

def setup():
    # Use an absolute or correct relative path to the root finance.db
    db_path = os.path.join(os.path.dirname(__file__), '..', 'finance.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create baseline tables
    cursor.executescript('''
    DROP TABLE IF EXISTS transactions;
    DROP TABLE IF EXISTS accounts;
    DROP TABLE IF EXISTS users;
    
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        join_date TEXT
    );
    
    CREATE TABLE accounts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        account_type TEXT,
        balance REAL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY,
        account_id INTEGER,
        category TEXT,
        amount REAL,
        transaction_date TEXT,
        merchant TEXT,
        status TEXT,
        FOREIGN KEY(account_id) REFERENCES accounts(id)
    );
    ''')
    
    # Seed Data
    cursor.executescript('''
    INSERT INTO users (id, name, email, join_date) VALUES 
        (1, 'Alice Smith', 'alice@example.com', '2023-01-15'),
        (2, 'Bob Jones', 'bob@example.com', '2023-03-22');
        
    INSERT INTO accounts (id, user_id, account_type, balance) VALUES 
        (1, 1, 'Checking', 2500.00),
        (2, 2, 'Savings', 10500.50);
        
    INSERT INTO transactions (id, account_id, category, amount, transaction_date, merchant, status) VALUES 
        (1, 1, 'Groceries', 150.25, '2024-01-02', 'SuperMart', 'completed'),
        (2, 1, 'Entertainment', 45.00, '2024-01-05', 'Cinema', 'completed'),
        (3, 2, 'Salary', 3000.00, '2024-01-01', 'Corp Inc', 'completed');
    ''')
    
    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == '__main__':
    setup()
