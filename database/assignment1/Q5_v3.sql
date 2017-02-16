-- Database - Postgres
-- This uses the same table structure as present in Q5.sql. This query is based on array operations.
--Query
SELECT Chef FROm ChefDishMapping GROUP BY Chef HAVING array_agg(Dish) @> (SELECT array_agg(DishName) FROM Dish);
