-- Database - Postgres
-- This uses the same table structure as present in Q5.sql. This query is based on relational division.
--Query
SELECT DISTINCT A.Chef
FROM ChefDishMapping AS A
WHERE NOT EXISTS (
    SELECT *
    FROM Dish AS B
    WHERE NOT EXISTS (
        SELECT *
        FROM ChefDishMapping AS C
        WHERE (C.Chef=A.Chef) AND (C.Dish=B.DishName)
   )
);
