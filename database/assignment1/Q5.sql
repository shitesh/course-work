-- Database - Postgres

--DROP TABLE IF EXISTS ChefDishMapping;
--DROP TABLE IF EXISTS Dish;
----
--CREATE TABLE ChefDishMapping(
--Chef VARCHAR(20),
--Dish VARCHAR(40),
--UNIQUE(Chef, Dish)
--);
--
--INSERT INTO ChefDishMapping(Chef, Dish) VALUES('A','Mint chocolate brownie'), ('B','Upside down pineapple cake'), ('B','Creme brulee'),
--('B','Mint chocolate brownie'),('C','Upside down pineapple cake'),('C','Creme brulee'),('D','Apple pie'),
--('D','Upside down pineapple cake'),('D','Creme brulee'),('E','Apple pie'),('E','Upside down pineapple cake'),
--('E','Creme brulee'),('E','Bananas Foster');
--
--CREATE TABLE Dish(
--DishName VARCHAR(40),
--UNIQUE(DishName)
--);
--
--INSERT INTO Dish(DishName) VALUES('Apple pie'),('Upside down pineapple cake'),('Creme brulee');

--Query
SELECT Chef FROM ChefDishMapping where Dish IN(select DishName from Dish) GROUP BY Chef HAVING COUNT(*) = (SELECT COUNT(*) FROM Dish);