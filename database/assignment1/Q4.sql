-- Database - Postgres

--DROP TABLE IF EXISTS JunkMail;
----
--CREATE TABLE JunkMail
--(
--Name VARCHAR(20),
--Address VARCHAR(10),
--ID INTEGER UNIQUE,
--SameFam INTEGER
--);
--
--INSERT INTO JunkMail(Name, Address, ID) VALUES('Alice', 'A', 10), ('Bob', 'B', 15), ('Carmen', 'C', 22);
--INSERT INTO JunkMail(Name, Address, ID, SameFam) VALUES('Diego', 'A', 9, 10), ('Ella', 'B', 3, 15);
--INSERT INTO JunkMail(Name, Address, ID) VALUES('Farkhad', 'D', 11);
-- SELECT * FROM JunkMail;


-- Query
DELETE FROM JunkMail WHERE SameFam IS NULL AND ID IN(SELECT SameFam FROM JunkMail WHERE SameFam IS NOT NULL);

-- SELECT * FROM JunkMail;