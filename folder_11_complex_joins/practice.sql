-- TODO: Join users, accounts, and transactions
SELECT u.name, t.amount FROM users u JOIN accounts a ON u.id = a.user_id JOIN transactions t ON a.id = t.account_id;
