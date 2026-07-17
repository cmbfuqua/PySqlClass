SELECT t.amount, tg.name FROM transactions t JOIN transaction_tags tt ON t.id = tt.transaction_id JOIN tags tg ON tt.tag_id = tg.id;
