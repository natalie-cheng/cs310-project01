
-- select now();

-- CREATE DATABASE photoapp;

--
-- assume this was already done: CREATE DATABASE photoapp;
-- --

-- USE photoapp;

-- DROP TABLE IF EXISTS assets;
-- DROP TABLE IF EXISTS users;

-- CREATE TABLE users
-- (
--     userid       int not null AUTO_INCREMENT,
--     email        varchar(128) not null,
--     lastname     varchar(64) not null,
--     firstname    varchar(64) not null,
--     bucketfolder varchar(48) not null,  -- random, unique name (UUID)
--     PRIMARY KEY (userid),
--     UNIQUE      (email),
--     UNIQUE      (bucketfolder)
-- );

-- ALTER TABLE users AUTO_INCREMENT = 80001;  -- starting value

-- CREATE TABLE assets
-- (
--     assetid      int not null AUTO_INCREMENT,
--     userid       int not null,
--     assetname    varchar(128) not null,  -- original name from user
--     bucketkey    varchar(128) not null,  -- random, unique name in bucket
--     PRIMARY KEY (assetid),
--     FOREIGN KEY (userid) REFERENCES users(userid),
--     UNIQUE      (bucketkey)
-- );

-- ALTER TABLE assets AUTO_INCREMENT = 1001;  -- starting value

--
-- DONE
--

--
-- inserts one user and one asset into respective tables:
--
-- NOTE: userid in users table is automatically generated, so we
-- don't provide a userid. Likewise for assetid in assets table.
--

-- USE photoapp;

-- INSERT INTO 
--   users(email, lastname, firstname, bucketfolder)
--   values('pooja.sarkar@company.com', 'sarkar', 'pooja', 
--          '41c45ac8-34a8-459e-98a9-74a19408c287');

-- INSERT INTO 
--   users(email, lastname, firstname, bucketfolder)
--   values('e_ricci@email.com', 'ricci', 'emanuele', 
--          '4b499861-f31e-4307-8d09-d3be98776f03');

-- INSERT INTO 
--   users(email, lastname, firstname, bucketfolder)
--   values('li_chen@domain.com', 'chen', 'li', 
--          '86c4958e-b446-4985-9be0-9a1706b6ab83');

-- INSERT INTO 
--   assets(userid, assetname, bucketkey)
--   values(80001,
--          'sushiwalk.jpg',
--          '41c45ac8-34a8-459e-98a9-74a19408c287/6bbd19cd-ca23-4ac8-b7f2-2221024fb65d.jpg');

-- INSERT INTO 
--   assets(userid, assetname, bucketkey)
--   values(80001,
--          'sushihat.jpg',
--          '41c45ac8-34a8-459e-98a9-74a19408c287/8e453b7a-02c9-453c-b17c-978445cabea7.jpg');

-- INSERT INTO 
--   assets(userid, assetname, bucketkey)
--   values(80002,
--          'sushibeach.jpg',
--          '4b499861-f31e-4307-8d09-d3be98776f03/518c4d0f-dad6-4ed9-8b33-570259a79a63.jpg');

-- INSERT INTO 
--   assets(userid, assetname, bucketkey)
--   values(80002,
--          'sushisweater.jpg',
--          '4b499861-f31e-4307-8d09-d3be98776f03/75ec05a7-d7e1-41f7-b9dc-1bc8417eff38.jpg<');

-- INSERT INTO 
--   assets(userid, assetname, bucketkey)
--   values(80003,
--          'sushihike.jpg',
--          '86c4958e-b446-4985-9be0-9a1706b6ab83/850c008f-4d6a-4c70-8a3e-244265e95474.jpg');

-- INSERT INTO 
--   assets(userid, assetname, bucketkey)
--   values(80003,
--          'sushisleep.jpg',
--          '86c4958e-b446-4985-9be0-9a1706b6ab83/dfba0566-9180-476b-801e-f7907c69ab35.jpg');

USE photoapp;

SELECT * FROM assets;

--
-- adds two users to the database, one for read-only access and
-- another for read-write access:
--
-- NOTE: do NOT change the user names, and do NOT change the pwds.
-- These need to remain as is for grading purposes.
--
-- ref: https://dev.mysql.com/doc/refman/8.0/en/create-user.html
--

-- USE photoapp;

-- DROP USER IF EXISTS 'photoapp-read-only';
-- DROP USER IF EXISTS 'photoapp-read-write';

-- CREATE USER 'photoapp-read-only' IDENTIFIED BY 'abc123!!';
-- CREATE USER 'photoapp-read-write' IDENTIFIED BY 'def456!!';

-- GRANT SELECT, SHOW VIEW ON photoapp.* 
--       TO 'photoapp-read-only';
-- GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE ON photoapp.* 
--       TO 'photoapp-read-write';
      
-- FLUSH PRIVILEGES;