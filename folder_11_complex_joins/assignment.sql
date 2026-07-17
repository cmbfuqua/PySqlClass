-- ASSIGNMENT: Complex Joins
-- 
-- In this assignment, you will work with a database of a tournament.
-- You have a table `teams` (id, team_name).
-- 
-- Task 1:
-- Write a query to generate all possible unique matchups between teams.
-- A team should not play against itself. 
-- For teams A and B, (A, B) is considered a matchup. You don't need to worry about (B, A) being a duplicate for this exercise, just ensure no team plays itself.
-- Create a view named `tournament_matchups` with columns `team1_name` and `team2_name`.
--
-- Task 2:
-- You have another table `matches` (id, home_team_id, away_team_id, home_score, away_score).
-- Write a query to list all team names and their home match scores.
-- If a team has not played any home matches, they should still appear in the list with NULL scores (Use a LEFT or RIGHT JOIN).
-- Create a view named `team_home_matches` with columns `team_name` and `home_score`.

CREATE VIEW tournament_matchups AS
-- Write your query here
;

CREATE VIEW team_home_matches AS
-- Write your query here
;
