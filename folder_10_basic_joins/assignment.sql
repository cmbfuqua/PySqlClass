SELECT u.name, a.account_type, a.balance FROM users u LEFT JOIN accounts a ON u.id = a.user_id;
