-- TODO: Join accounts and users
SELECT users.name, accounts.balance FROM users INNER JOIN accounts ON users.id = accounts.user_id;
