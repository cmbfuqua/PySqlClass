-- TODO: Create a transaction_tags bridge table
CREATE TABLE transaction_tags (transaction_id INTEGER, tag_id INTEGER, PRIMARY KEY(transaction_id, tag_id));
