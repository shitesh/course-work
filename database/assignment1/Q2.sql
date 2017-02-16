-- Database - Postgres
--DROP TABLE IF EXISTS Enrollment;
--
--CREATE TABLE Enrollment(
--SID INTEGER NOT NULL,
--ClassName VARCHAR(40) NOT NULL,
--Grade VARCHAR(1),
--UNIQUE(SID, ClassName)
--);
--
--INSERT INTO Enrollment(SID, ClassName, Grade) VALUES(123, 'ART123', 'A'), (123, 'BUS456', 'B'), (666, 'REL100', 'D'), (666, 'ECO966', 'A'),
--(666, 'BUS456', 'B'), (345, 'BUS456', 'A'), (345, 'ECO966', 'F');

-- Query
SELECT ClassName, COUNT(*) as Total FROM Enrollment GROUP BY ClassName ORDER BY Total;