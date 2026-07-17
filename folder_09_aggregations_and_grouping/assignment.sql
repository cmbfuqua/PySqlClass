SELECT category, SUM(amount) as total_spent FROM transactions GROUP BY category HAVING SUM(amount) > 500;
