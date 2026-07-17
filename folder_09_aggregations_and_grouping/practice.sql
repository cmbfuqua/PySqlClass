-- TODO: Count transactions per category
SELECT category, COUNT(*) as count FROM transactions GROUP BY category;
