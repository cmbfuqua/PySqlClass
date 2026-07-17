SELECT * FROM users WHERE id IN (SELECT user_id FROM accounts WHERE balance > 10000);
