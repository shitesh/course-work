-- Database - Postgres

--DROP TABLE IF EXISTS ProjectStatus;
--
--CREATE TABLE ProjectStatus(
--ProjectID VARCHAR(10) NOT NULL,
--Step INTEGER,
--Status VARCHAR(1),
--UNIQUE (projectID, Step)
--);
--
--
--INSERT into ProjectStatus(ProjectID, Step, Status) VALUES('P100',0,'C'), ('P100',1,'W'),('P100',2,'W'),('P201',0,'C'),('P201',1,'C'), ('P333',0, 'W'), ('P333',1,'W'), ('P333',2,'W'), ('P333',3,'W');

-- Query
SELECT ProjectID FROM ProjectStatus WHERE Step=0 AND Status='C' AND ProjectID NOT IN(SELECT ProjectID FROM ProjectStatus WHERE Step>0 and Status='C');
