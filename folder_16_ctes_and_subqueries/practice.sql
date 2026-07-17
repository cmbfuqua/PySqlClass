-- TODO: Use a CTE to find average account balance
WITH AvgBalance AS (SELECT AVG(balance) as avg_bal FROM accounts) SELECT * FROM accounts, AvgBalance WHERE accounts.balance > AvgBalance.avg_bal;
