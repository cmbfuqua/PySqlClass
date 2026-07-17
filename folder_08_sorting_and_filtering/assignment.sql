SELECT * FROM transactions WHERE merchant IS NOT NULL AND amount > 50 ORDER BY transaction_date ASC;
