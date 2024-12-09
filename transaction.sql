{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 DELIMITER //\
\
CREATE PROCEDURE DeleteUser(IN input_user_id INT)\
BEGIN\
    -- Start a transaction\
    DECLARE EXIT HANDLER FOR SQLEXCEPTION\
    BEGIN\
        -- Rollback the transaction in case of an error\
        ROLLBACK;\
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error occurred during deletion';\
    END;\
\
    START TRANSACTION;\
\
    -- Check if the user exists\
    IF NOT EXISTS (SELECT 1 FROM User WHERE UserID = input_user_id) THEN\
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User not found';\
    END IF;\
\
    -- Delete references to the user's podcasts\
    DELETE FROM BookReference\
    WHERE PodcastID IN (SELECT PodcastID FROM Podcast WHERE UserID = input_user_id);\
\
    DELETE FROM PeopleReference\
    WHERE PodcastID IN (SELECT PodcastID FROM Podcast WHERE UserID = input_user_id);\
\
    DELETE FROM CompanyReference\
    WHERE PodcastID IN (SELECT PodcastID FROM Podcast WHERE UserID = input_user_id);\
\
    -- Delete user's podcasts\
    DELETE FROM Podcast\
    WHERE UserID = input_user_id;\
\
    -- Delete the user\
    DELETE FROM User\
    WHERE UserID = input_user_id;\
\
    -- Commit the transaction\
    COMMIT;\
END $$\
\
DELIMITER ;\
}