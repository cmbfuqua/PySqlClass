SELECT u.email, a.account_type, t.merchant, t.amount FROM users u JOIN accounts a ON u.id = a.user_id JOIN transactions t ON a.id = t.account_id WHERE t.status = 'completed';
